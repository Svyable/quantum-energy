#!/usr/bin/env python3
"""Synthetic R2 mechanism-recovery study with a low-temperature CT-linewidth discriminator.

PLANNING/SYNTHETIC ONLY. No values in this file are R2 measurements.

Adds a temperature-dependent CT linewidth proxy to the v3.3 H1-H4 classifier.
The physical planning model is

    sigma_D^2(T) = lambda * hbar_omega * coth(hbar_omega / (2 k_B T))
    sigma_T^2(T) = sigma_S^2 + sigma_D^2(T)

where sigma_S is a static-disorder contribution and the dynamic term approaches
2*lambda*k_B*T at high temperature.

Synthetic assumptions for the nominal H1 generator:
- hbar_omega = 15 meV (literature-motivated planning prior, not an R2 fit)
- lambda = 150 meV (planning value)
- T = 120, 150, 240, 270, 300, 330 K
- sigma_S^2 = max(100, 1600 + 600*z) meV^2, z~N(0,1)
- linewidth measurement noise = 2 meV (1 sigma)
- DeltaVnr effect SD = 10 mV; DeltaVnr random noise SD = 4 mV

H2/H3/H4 use dynamic-only linewidths (sigma_S=0) in the nominal generator.
A per-substrate static-variance proxy is estimated by ordinary least squares in
variance space with hbar_omega fixed and lambda refit. This proxy competes with
E_U as an H1 predictor under leave-one-substrate-out validation.

The classifier remains deliberately low-dimensional. H5/EPC is NOT an output.
"""
from __future__ import annotations

import argparse
import math
import platform
from dataclasses import dataclass
from typing import Dict

import numpy as np

K_B_MEV_K = 0.08617333262
DEFAULT_SEED = 20260826
LABELS = ("H1", "H2", "H3", "H4")
TEMPS_K = np.array([120.0, 150.0, 240.0, 270.0, 300.0, 330.0])
HBAR_OMEGA_MEV = 15.0
LAMBDA_MEV = 150.0


@dataclass(frozen=True)
class Scenario:
    n_substrates: int = 7
    effect_sd_mv: float = 10.0
    dvnr_noise_mv: float = 4.0
    linewidth_noise_mev: float = 2.0
    eu_noise_mev: float = 1.0
    ideality_noise: float = 0.03
    null_el_shift_noise_mev: float = 1.2
    null_direct_recip_noise_mv: float = 4.0
    h4_el_shift_mean_mev: float = 7.0
    h4_el_shift_noise_mev: float = 1.5
    h4_direct_recip_mean_mv: float = 25.0
    h4_direct_recip_noise_mv: float = 6.0


def coth(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / np.tanh(x)


def keil_variance_mev2(T_K: np.ndarray, lam_mev: float = LAMBDA_MEV,
                       hbar_omega_mev: float = HBAR_OMEGA_MEV) -> np.ndarray:
    x = hbar_omega_mev / (2.0 * K_B_MEV_K * np.asarray(T_K, dtype=float))
    return lam_mev * hbar_omega_mev * coth(x)


def marcus_variance_mev2(T_K: np.ndarray, lam_mev: float = LAMBDA_MEV) -> np.ndarray:
    return 2.0 * lam_mev * K_B_MEV_K * np.asarray(T_K, dtype=float)


def estimate_static_variance(sigmas_mev: np.ndarray) -> float:
    """Fit sigma^2 = a + lambda*f(T), fixing hbar_omega to the external prior."""
    y = np.asarray(sigmas_mev, dtype=float) ** 2
    f = keil_variance_mev2(TEMPS_K, lam_mev=1.0)
    X = np.column_stack([np.ones(len(TEMPS_K)), f])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return float(beta[0])


def _fit_predict_holdout(x: np.ndarray, y: np.ndarray, holdout: int) -> float:
    mask = np.arange(len(y)) != holdout
    xm = x[mask].mean()
    ym = y[mask].mean()
    denom = np.sum((x[mask] - xm) ** 2)
    slope = 0.0 if denom <= 0 else np.sum((x[mask] - xm) * (y[mask] - ym)) / denom
    return float(ym + slope * (x[holdout] - xm))


def loso_mae(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.mean([abs(_fit_predict_holdout(x, y, i) - y[i]) for i in range(len(y))]))


def intercept_loso_mae(y: np.ndarray) -> float:
    total = float(np.sum(y))
    n = len(y)
    return float(np.mean([abs(y[i] - (total - y[i]) / (n - 1)) for i in range(n)]))


def classify(obs: Dict[str, np.ndarray]) -> str:
    if np.any(np.abs(obs["el_shift_mev"]) >= 5.0) or np.any(np.abs(obs["direct_minus_recip_mv"]) > 20.0):
        return "H4"

    y = obs["dvnr_recip_mv"]
    base = intercept_loso_mae(y)
    maes = {
        "H1_EU": loso_mae(obs["eu_mev"], y),
        "H1_T": loso_mae(obs["static_var_proxy_mev2"], y),
        "H3": loso_mae(obs["ideality"], y),
    }
    best = min(maes, key=maes.get)
    improve = (base - maes[best]) / base if base > 0 else 0.0
    if improve < 0.20:
        return "H2"
    return "H3" if best == "H3" else "H1"


def simulate_observations(true_h: str, scenario: Scenario, rng: np.random.Generator) -> Dict[str, np.ndarray]:
    n = scenario.n_substrates
    z = rng.normal(size=n)
    eu = 24.0 + rng.normal(0.0, 1.5, n)
    ideality = 1.25 + rng.normal(0.0, 0.05, n)
    dvnr = 300.0 + rng.normal(0.0, scenario.dvnr_noise_mv, n)
    direct_minus_recip = rng.normal(0.0, scenario.null_direct_recip_noise_mv, n)
    el_shift = rng.normal(0.0, scenario.null_el_shift_noise_mev, n)

    dynamic_var = keil_variance_mev2(TEMPS_K)
    static_proxy = np.empty(n)
    for i in range(n):
        static_var_true = max(100.0, 1600.0 + 600.0 * z[i]) if true_h == "H1" else 0.0
        sigma_true = np.sqrt(static_var_true + dynamic_var)
        sigma_obs = sigma_true + rng.normal(0.0, scenario.linewidth_noise_mev, len(TEMPS_K))
        static_proxy[i] = estimate_static_variance(sigma_obs)

    if true_h == "H1":
        eu = 24.0 + 3.0 * z + rng.normal(0.0, scenario.eu_noise_mev, n)
        dvnr = 300.0 + scenario.effect_sd_mv * z + rng.normal(0.0, scenario.dvnr_noise_mv, n)
    elif true_h == "H3":
        ideality = 1.25 + 0.15 * z + rng.normal(0.0, scenario.ideality_noise, n)
        dvnr = 300.0 + scenario.effect_sd_mv * z + rng.normal(0.0, scenario.dvnr_noise_mv, n)
    elif true_h == "H4":
        direct_minus_recip = scenario.h4_direct_recip_mean_mv + rng.normal(0.0, scenario.h4_direct_recip_noise_mv, n)
        el_shift = scenario.h4_el_shift_mean_mev + rng.normal(0.0, scenario.h4_el_shift_noise_mev, n)
    elif true_h != "H2":
        raise ValueError(true_h)

    return {
        "eu_mev": eu,
        "ideality": ideality,
        "dvnr_recip_mv": dvnr,
        "direct_minus_recip_mv": direct_minus_recip,
        "el_shift_mev": el_shift,
        "static_var_proxy_mev2": static_proxy,
    }


def confusion_matrix(nsim: int, scenario: Scenario, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    m = np.zeros((4, 4), dtype=int)
    for i, truth in enumerate(LABELS):
        for _ in range(nsim):
            pred = classify(simulate_observations(truth, scenario, rng))
            m[i, LABELS.index(pred)] += 1
    return m


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--nsim", type=int, default=5000)
    ap.add_argument("--n-substrates", type=int, default=7)
    ap.add_argument("--linewidth-noise-mev", type=float, default=2.0)
    args = ap.parse_args()
    sc = Scenario(n_substrates=args.n_substrates, linewidth_noise_mev=args.linewidth_noise_mev)
    m = confusion_matrix(args.nsim, sc, args.seed)
    print(f"python={platform.python_version()} numpy={np.__version__} seed={args.seed}")
    print(f"scenario={sc}")
    for T in (120, 150, 180, 240, 270, 300, 330):
        keil = float(keil_variance_mev2(np.array([T]))[0])
        marcus = float(marcus_variance_mev2(np.array([T]))[0])
        print(f"T={T}K keil/marcus={keil/marcus:.9f}")
    print("rows=true columns=predicted: " + ",".join(LABELS))
    for i, h in enumerate(LABELS):
        vals = ",".join(str(int(v)) for v in m[i])
        print(f"{h},{vals},recovery={m[i,i]/args.nsim:.6f}")


if __name__ == "__main__":
    main()
