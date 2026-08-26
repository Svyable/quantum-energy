#!/usr/bin/env python3
"""R2 raw-spectrum synthetic test harness v3.7.

OPEN-SCIENCE STATUS
-------------------
This program generates SYNTHETIC raw optical spectra and tests the complete
raw-counts -> background subtraction -> radiometric correction -> wavelength-
to-energy density conversion -> linewidth extraction path. It is not an R2
measurement and must never be cited as physical device performance.

Reference configuration is intentionally modular:
- Linkam-class gas-tight temperature stage (selected in program v2.0/v3.6)
- fixed integrating-sphere/free-space collection
- cooled Si/InGaAs spectrometer chain

All detector throughput, noise, signal amplitude, and drift values in the
default config are synthetic planning assumptions until replaced by an actual
facility configuration and calibration files.
"""
from __future__ import annotations

import argparse, csv, json, math, platform
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

HC_EV_NM = 1239.8419843320026
K_B_MEV_K = 0.08617333262
DEFAULT_SEED = 20260826
DEFAULT_TEMPS_K = (150.0, 240.0, 300.0, 330.0)
LAMBDA_MEV = 150.0
HBAR_OMEGA_MEV = 15.0


def coth(x):
    return 1.0 / np.tanh(x)


def keil_sigma_mev(T_K, lam_mev=LAMBDA_MEV, hwo_mev=HBAR_OMEGA_MEV):
    """Synthetic planning linewidth sigma from the committed one-mode model."""
    variance = lam_mev * hwo_mev * coth(hwo_mev / (2.0 * K_B_MEV_K * T_K))
    return float(np.sqrt(variance))


@dataclass(frozen=True)
class Config:
    wavelength_min_nm: float = 800.0
    wavelength_max_nm: float = 1500.0
    wavelength_step_nm: float = 1.0
    ct_center_eV: float = 1.15
    photon_density_peak_scale: float = 4.0e5
    integration_s: float = 30.0
    dark_rate_cps: float = 3.0
    stray_rate_cps: float = 1.5
    read_noise_counts_rms: float = 2.0
    residual_calibration_slope_fraction: float = 0.003
    background_scale: float = 1.0
    fit_energy_min_eV: float = 0.84
    fit_energy_max_eV: float = 1.48
    nominal_system_throughput: float = 0.13
    throughput_bump: float = 0.06
    throughput_center_nm: float = 1080.0
    throughput_width_nm: float = 280.0


def wavelength_grid(cfg):
    return np.arange(
        cfg.wavelength_min_nm,
        cfg.wavelength_max_nm + 0.5 * cfg.wavelength_step_nm,
        cfg.wavelength_step_nm,
        dtype=float,
    )


def gaussian_energy_density(E_eV, amplitude, mu_eV, sigma_eV):
    return amplitude * np.exp(-0.5 * ((E_eV - mu_eV) / sigma_eV) ** 2)


def energy_to_wavelength_density(wavelength_nm, photon_density_per_eV):
    """Conserve photons: N_E dE = N_lambda d(lambda)."""
    jac = HC_EV_NM / wavelength_nm**2
    return photon_density_per_eV * jac


def wavelength_to_energy_density(wavelength_nm, photon_density_per_nm):
    """Inverse Jacobian of energy_to_wavelength_density."""
    jac = HC_EV_NM / wavelength_nm**2
    return photon_density_per_nm / jac


def system_throughput(wavelength_nm, cfg):
    return (
        cfg.nominal_system_throughput
        + cfg.throughput_bump
        * np.exp(-0.5 * ((wavelength_nm - cfg.throughput_center_nm) / cfg.throughput_width_nm) ** 2)
    )


def dark_and_stray_rates(wavelength_nm, cfg):
    dark = cfg.dark_rate_cps + 1.0 * np.exp(-0.5 * ((wavelength_nm - 1350.0) / 150.0) ** 2)
    stray = cfg.stray_rate_cps + 0.003 * (wavelength_nm - cfg.wavelength_min_nm)
    return dark, stray


def generate_raw(T_K, cfg, rng):
    wl = wavelength_grid(cfg)
    true_sigma_mev = keil_sigma_mev(T_K)
    E = HC_EV_NM / wl
    N_E = gaussian_energy_density(
        E, cfg.photon_density_peak_scale, cfg.ct_center_eV, true_sigma_mev / 1000.0
    )
    N_lambda = energy_to_wavelength_density(wl, N_E)

    throughput_true = system_throughput(wl, cfg)
    dark_rate, stray_rate = dark_and_stray_rates(wl, cfg)

    sample_expectation = (N_lambda * throughput_true + dark_rate + stray_rate) * cfg.integration_s
    background_expectation = (dark_rate + stray_rate) * cfg.integration_s
    dark_expectation = dark_rate * cfg.integration_s

    sample = rng.poisson(sample_expectation).astype(float)
    background = rng.poisson(background_expectation).astype(float)
    dark = rng.poisson(dark_expectation).astype(float)

    if cfg.read_noise_counts_rms > 0:
        sample += rng.normal(0.0, cfg.read_noise_counts_rms, len(wl))
        background += rng.normal(0.0, cfg.read_noise_counts_rms, len(wl))
        dark += rng.normal(0.0, cfg.read_noise_counts_rms, len(wl))

    x = (wl - wl.mean()) / (wl.max() - wl.min())
    throughput_est = throughput_true * (1.0 + cfg.residual_calibration_slope_fraction * x)

    return {
        "temperature_K": T_K,
        "true_sigma_meV": true_sigma_mev,
        "wavelength_nm": wl,
        "sample_counts": sample,
        "background_counts": background,
        "dark_counts": dark,
        "throughput_true": throughput_true,
        "throughput_est": throughput_est,
        "true_photon_density_per_nm": N_lambda,
    }


def calibrate(raw, cfg):
    wl = raw["wavelength_nm"]
    net_counts = raw["sample_counts"] - cfg.background_scale * raw["background_counts"]
    photons_per_nm_s = (net_counts / cfg.integration_s) / raw["throughput_est"]
    E = HC_EV_NM / wl
    photons_per_eV_s = wavelength_to_energy_density(wl, photons_per_nm_s)
    order = np.argsort(E)
    return E[order], photons_per_eV_s[order]


def gaussian_with_offset(E, amplitude, mu, sigma, offset):
    return amplitude * np.exp(-0.5 * ((E - mu) / sigma) ** 2) + offset


def fit_sigma_curve(E, y, cfg):
    mask = (
        np.isfinite(E) & np.isfinite(y)
        & (E >= cfg.fit_energy_min_eV)
        & (E <= cfg.fit_energy_max_eV)
    )
    x = E[mask]
    z = y[mask]
    if len(x) < 20:
        raise RuntimeError("too few valid points for linewidth fit")

    p0 = [max(float(np.max(z) - np.median(z)), 1.0), cfg.ct_center_eV, 0.08, float(np.median(z))]
    bounds = ([0.0, 0.95, 0.02, -np.inf], [np.inf, 1.30, 0.18, np.inf])
    popt, _ = curve_fit(gaussian_with_offset, x, z, p0=p0, bounds=bounds, maxfev=20000)
    return {
        "sigma_meV": float(popt[2] * 1000.0),
        "center_eV": float(popt[1]),
        "offset": float(popt[3]),
    }


def sigma_from_fwhm(E, y):
    """Independent, interpolation-based linewidth check for noiseless spectra."""
    order = np.argsort(E)
    x = np.asarray(E)[order]
    z = np.asarray(y)[order]
    i = int(np.argmax(z))
    half = z[i] / 2.0
    left = np.where(z[:i] <= half)[0]
    right = np.where(z[i:] <= half)[0]
    if not len(left) or not len(right):
        raise RuntimeError("FWHM crossing not found")

    def crossing(j1, j2):
        x1, x2 = x[j1], x[j2]
        y1, y2 = z[j1], z[j2]
        return x1 + (half - y1) * (x2 - x1) / (y2 - y1)

    li = int(left[-1])
    ri = int(i + right[0])
    xl = crossing(li, li + 1)
    xr = crossing(ri - 1, ri)
    fwhm_eV = xr - xl
    sigma_eV = fwhm_eV / (2.0 * math.sqrt(2.0 * math.log(2.0)))
    return float(sigma_eV * 1000.0)


def numerical_integral(x, y):
    return float(np.trapezoid(y, x))


def self_tests(cfg):
    wl = wavelength_grid(cfg)
    E = HC_EV_NM / wl
    true_sigma_mev = 80.0
    N_E = gaussian_energy_density(E, 1.0e6, cfg.ct_center_eV, true_sigma_mev / 1000.0)
    N_lambda = energy_to_wavelength_density(wl, N_E)
    roundtrip = wavelength_to_energy_density(wl, N_lambda)

    order_E = np.argsort(E)
    int_E = numerical_integral(E[order_E], N_E[order_E])
    int_lambda = numerical_integral(wl, N_lambda)
    integral_rel_error = abs(int_E - int_lambda) / abs(int_E)

    fit_correct = fit_sigma_curve(E[order_E], roundtrip[order_E], cfg)["sigma_meV"]
    fwhm_correct = sigma_from_fwhm(E[order_E], roundtrip[order_E])

    wrong_fit = fit_sigma_curve(E[order_E], N_lambda[order_E], cfg)
    wrong_center_shift_meV = (wrong_fit["center_eV"] - cfg.ct_center_eV) * 1000.0

    def integral_error_at_step(step_nm):
        test_cfg = Config(**{**asdict(cfg), "wavelength_step_nm": step_nm})
        twl = wavelength_grid(test_cfg)
        tE = HC_EV_NM / twl
        tNE = gaussian_energy_density(tE, 1.0e6, cfg.ct_center_eV, true_sigma_mev / 1000.0)
        tNl = energy_to_wavelength_density(twl, tNE)
        order = np.argsort(tE)
        a = numerical_integral(tE[order], tNE[order])
        b = numerical_integral(twl, tNl)
        return abs(a - b) / abs(a)

    err_2nm = integral_error_at_step(2.0)
    err_1nm = integral_error_at_step(1.0)
    err_0p5nm = integral_error_at_step(0.5)
    ratio_2_to_1 = err_2nm / err_1nm
    ratio_1_to_0p5 = err_1nm / err_0p5nm

    checks = {
        "photon_integral_relative_error": integral_rel_error,
        "integral_error_2nm": err_2nm,
        "integral_error_1nm": err_1nm,
        "integral_error_0p5nm": err_0p5nm,
        "integral_convergence_ratio_2nm_to_1nm": ratio_2_to_1,
        "integral_convergence_ratio_1nm_to_0p5nm": ratio_1_to_0p5,
        "noiseless_curvefit_sigma_error_meV": fit_correct - true_sigma_mev,
        "noiseless_fwhm_sigma_error_meV": fwhm_correct - true_sigma_mev,
        "wrong_no_jacobian_center_shift_meV": wrong_center_shift_meV,
    }
    passed = (
        integral_rel_error < 2e-6
        and 3.5 < ratio_2_to_1 < 4.5
        and 3.5 < ratio_1_to_0p5 < 4.5
        and abs(checks["noiseless_curvefit_sigma_error_meV"]) < 1e-6
        and abs(checks["noiseless_fwhm_sigma_error_meV"]) < 0.01
        and abs(wrong_center_shift_meV) > 5.0
    )
    return passed, checks


def monte_carlo_summary(cfg, temperatures, nsim, seed):
    scenarios = {
        "nominal": cfg,
        "cal_slope_2pct": Config(**{**asdict(cfg), "residual_calibration_slope_fraction": 0.02}),
        "background_minus10pct": Config(**{**asdict(cfg), "background_scale": 0.90}),
        "background_plus10pct": Config(**{**asdict(cfg), "background_scale": 1.10}),
    }
    rows = []
    for scenario_name, scfg in scenarios.items():
        for ti, T in enumerate(temperatures):
            truth = keil_sigma_mev(T)
            estimates = []
            failures = 0
            for i in range(nsim):
                rng = np.random.default_rng(seed + 100000 * ti + i)
                raw = generate_raw(T, scfg, rng)
                E, y = calibrate(raw, scfg)
                try:
                    estimates.append(fit_sigma_curve(E, y, scfg)["sigma_meV"])
                except Exception:
                    failures += 1
            estimates = np.asarray(estimates, dtype=float)
            bias = float(np.mean(estimates) - truth) if len(estimates) else float("nan")
            rmse = float(np.sqrt(np.mean((estimates - truth) ** 2))) if len(estimates) else float("nan")
            rows.append({
                "scenario": scenario_name,
                "temperature_K": T,
                "true_sigma_meV": truth,
                "mean_estimated_sigma_meV": float(np.mean(estimates)) if len(estimates) else float("nan"),
                "bias_meV": bias,
                "rmse_meV": rmse,
                "fit_failure_fraction": failures / nsim,
            })
    return rows


def write_example_raw(path, raw):
    fields = [
        "wavelength_nm", "sample_counts", "background_counts", "dark_counts",
        "throughput_true", "throughput_est", "true_photon_density_per_nm",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i in range(len(raw["wavelength_nm"])):
            w.writerow({k: float(raw[k][i]) for k in fields})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="r2_raw_spectrum_harness_out")
    ap.add_argument("--nsim", type=int, default=200)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = ap.parse_args()

    cfg = Config()
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)

    passed, checks = self_tests(cfg)
    if not passed:
        raise SystemExit("SELF_TEST_FAIL " + json.dumps(checks, sort_keys=True))

    rows = monte_carlo_summary(cfg, DEFAULT_TEMPS_K, args.nsim, args.seed)
    with open(out / "linewidth_recovery_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    example = generate_raw(150.0, cfg, np.random.default_rng(args.seed))
    write_example_raw(out / "synthetic_raw_150K.csv", example)

    metadata = {
        "open_science_status": "synthetic planning/verification only; not experimental R2 data",
        "runtime": {"python": platform.python_version(), "numpy": np.__version__},
        "seed": args.seed,
        "nsim_per_temperature_scenario": args.nsim,
        "config": asdict(cfg),
        "self_tests": checks,
        "acceptance": {
            "nominal_abs_bias_meV": "<= 1.0 at each temperature",
            "nominal_rmse_meV": "<= 2.0 at each temperature",
            "fit_failure_fraction": "<= 0.01",
            "integral_conservation_relative_error": "< 2e-6 at 1 nm grid; convergence must improve ~4x per halved step",
        },
    }
    with open(out / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, sort_keys=True)

    nominal = [r for r in rows if r["scenario"] == "nominal"]
    decision = all(
        abs(r["bias_meV"]) <= 1.0 and r["rmse_meV"] <= 2.0 and r["fit_failure_fraction"] <= 0.01
        for r in nominal
    )
    print(f"python={platform.python_version()} numpy={np.__version__} seed={args.seed}")
    for k, v in checks.items():
        print(f"{k}={v:.12g}")
    for r in nominal:
        print(
            f"nominal T={r['temperature_K']:.0f}K truth={r['true_sigma_meV']:.6f} "
            f"bias={r['bias_meV']:.6f} rmse={r['rmse_meV']:.6f} "
            f"failure={r['fit_failure_fraction']:.6f}"
        )
    print("RAW_SPECTRUM_PIPELINE_GATE=" + ("PASS" if decision else "FAIL"))
    print("NOTE=synthetic verification only; replace config with measured facility calibration/noise before physical inference")


if __name__ == "__main__":
    main()
