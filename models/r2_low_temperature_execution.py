#!/usr/bin/env python3
"""R2 low-temperature execution/recovery tool.

OPEN-SCIENCE STATUS: analysis infrastructure only. Default values are synthetic
planning assumptions, never R2 measurements.

Input CSV columns:
temperature_K, usable, linewidth_sd_meV, dut_temp_accuracy_K,
dut_temp_stability_K, max_self_heating_K, spectral_snr

The script:
1) selects temperatures that pass frozen low-T qualification gates;
2) uses the worst accepted empirical linewidth SD as the recovery noise input;
3) reruns the v3.4 H1-H4 synthetic recovery generator on the usable grid;
4) reports whether every class crosses the preregistered >=0.80 recovery gate.

H5/EPC is not a classifier output.
"""
from __future__ import annotations
import argparse, csv, platform
from dataclasses import dataclass
import numpy as np

K_B_MEV_K = 0.08617333262
LABELS = ("H1", "H2", "H3", "H4")
DEFAULT_SEED = 20260826
HBAR_OMEGA_MEV = 15.0
LAMBDA_MEV = 150.0

def coth(x): return 1.0 / np.tanh(x)
def keil_variance(T, lam=LAMBDA_MEV, hwo=HBAR_OMEGA_MEV):
    T = np.asarray(T, dtype=float)
    return lam * hwo * coth(hwo / (2 * K_B_MEV_K * T))

def static_intercept(sigmas, temps):
    y = np.asarray(sigmas, dtype=float) ** 2
    f = keil_variance(np.asarray(temps, dtype=float), lam=1.0)
    fm, ym = float(f.mean()), float(y.mean())
    den = float(np.sum((f - fm) ** 2))
    slope = 0.0 if den <= 0 else float(np.sum((f - fm) * (y - ym)) / den)
    return ym - slope * fm

def holdout_predict(x, y, h):
    keep = np.arange(len(y)) != h
    xm, ym = float(x[keep].mean()), float(y[keep].mean())
    den = float(np.sum((x[keep] - xm) ** 2))
    slope = 0.0 if den <= 0 else float(np.sum((x[keep] - xm) * (y[keep] - ym)) / den)
    return ym + slope * (float(x[h]) - xm)

def loso_mae(x, y):
    return float(np.mean([abs(holdout_predict(x, y, i) - y[i]) for i in range(len(y))]))

def intercept_mae(y):
    n, total = len(y), float(np.sum(y))
    return float(np.mean([abs(float(y[i]) - (total - float(y[i])) / (n - 1)) for i in range(n)]))

def classify(obs):
    if np.any(np.abs(obs["el_shift"]) >= 5.0) or np.any(np.abs(obs["direct_recip"]) > 20.0):
        return "H4"
    y = obs["dvnr"]
    baseline = intercept_mae(y)
    maes = {
        "H1_EU": loso_mae(obs["eu"], y),
        "H1_T": loso_mae(obs["static_proxy"], y),
        "H3": loso_mae(obs["ideality"], y),
    }
    best = min(maes, key=maes.get)
    improvement = (baseline - maes[best]) / baseline if baseline > 0 else 0.0
    if improvement < 0.20:
        return "H2"
    return "H3" if best == "H3" else "H1"

@dataclass(frozen=True)
class Scenario:
    n_substrates: int = 7
    effect_sd_mv: float = 10.0
    dvnr_noise_mv: float = 4.0
    eu_noise_mev: float = 1.0
    ideality_noise: float = 0.03
    h4_el_shift_mean_mev: float = 7.0
    h4_el_shift_noise_mev: float = 1.5
    h4_direct_recip_mean_mv: float = 25.0
    h4_direct_recip_noise_mv: float = 6.0

def simulate(truth, sc, temps, linewidth_noise, rng):
    n = sc.n_substrates
    z = rng.normal(size=n)
    eu = 24 + rng.normal(0, 1.5, n)
    ideality = 1.25 + rng.normal(0, 0.05, n)
    dvnr = 300 + rng.normal(0, sc.dvnr_noise_mv, n)
    direct_recip = rng.normal(0, 4.0, n)
    el_shift = rng.normal(0, 1.2, n)
    dyn = keil_variance(temps)
    static_proxy = np.empty(n)
    for i in range(n):
        static = max(100.0, 1600.0 + 600.0 * z[i]) if truth == "H1" else 0.0
        measured = np.sqrt(static + dyn) + rng.normal(0, linewidth_noise, len(temps))
        static_proxy[i] = static_intercept(measured, temps)
    if truth == "H1":
        eu = 24 + 3 * z + rng.normal(0, sc.eu_noise_mev, n)
        dvnr = 300 + sc.effect_sd_mv * z + rng.normal(0, sc.dvnr_noise_mv, n)
    elif truth == "H3":
        ideality = 1.25 + 0.15 * z + rng.normal(0, sc.ideality_noise, n)
        dvnr = 300 + sc.effect_sd_mv * z + rng.normal(0, sc.dvnr_noise_mv, n)
    elif truth == "H4":
        direct_recip = sc.h4_direct_recip_mean_mv + rng.normal(0, sc.h4_direct_recip_noise_mv, n)
        el_shift = sc.h4_el_shift_mean_mev + rng.normal(0, sc.h4_el_shift_noise_mev, n)
    return {"eu": eu, "ideality": ideality, "dvnr": dvnr,
            "direct_recip": direct_recip, "el_shift": el_shift,
            "static_proxy": static_proxy}

def recovery(temps, linewidth_noise, n_substrates, nsim, seed):
    rng = np.random.default_rng(seed)
    sc = Scenario(n_substrates=n_substrates)
    out = {}
    for truth in LABELS:
        hits = 0
        for _ in range(nsim):
            hits += classify(simulate(truth, sc, temps, linewidth_noise, rng)) == truth
        out[truth] = hits / nsim
    return out

def read_qc(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    usable = []
    for r in rows:
        ok = str(r["usable"]).strip().lower() in ("1", "true", "yes", "pass")
        ok &= float(r["dut_temp_accuracy_K"]) <= 1.0
        ok &= float(r["dut_temp_stability_K"]) <= 0.25
        ok &= float(r["max_self_heating_K"]) <= 0.5
        ok &= float(r["spectral_snr"]) >= 20.0
        if ok:
            usable.append(r)
    if len(usable) < 3:
        raise SystemExit("FAIL: fewer than 3 qualified temperature points")
    temps = np.array([float(r["temperature_K"]) for r in usable])
    noise = max(float(r["linewidth_sd_meV"]) for r in usable)
    return temps, noise

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qc_csv")
    ap.add_argument("--n-substrates", type=int, default=7)
    ap.add_argument("--nsim", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = ap.parse_args()
    temps, noise = read_qc(args.qc_csv)
    rec = recovery(temps, noise, args.n_substrates, args.nsim, args.seed)
    print(f"python={platform.python_version()} numpy={np.__version__} seed={args.seed}")
    print("qualified_temperatures_K=" + ",".join(f"{x:g}" for x in temps))
    print(f"empirical_linewidth_noise_meV={noise:.6g}")
    for h in LABELS:
        print(f"{h}_recovery={rec[h]:.6f}")
    passed = all(rec[h] >= 0.80 for h in LABELS)
    print("MECHANISM_SAMPLE_GATE=" + ("PASS" if passed else "FAIL"))
    print("NOTE=synthetic recovery conditional on committed generator assumptions; not physical performance")

if __name__ == "__main__":
    main()
