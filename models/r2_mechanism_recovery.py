#!/usr/bin/env python3
"""Synthetic recovery study for R2 H1-H4 mechanism discrimination.

This is a planning/synthetic model, not experimental evidence. It tests whether the
preregistered low-dimensional mechanism-audit logic can recover known generating
mechanisms under explicit noise/effect assumptions while preserving substrate-level
independence.

H1: bulk energetic/CT disorder -> E_U predicts DeltaVnr.
H2: thickness/optical-density confound -> no mechanism predictor improves DeltaVnr.
H3: interface/contact recombination -> empirical ideality predicts DeltaVnr.
H4: injection/state-filling artifact -> EL spectral-shift or direct-vs-reciprocity alert.

The classifier mirrors v3.2 decision logic at planning level:
- H4 has priority if any substrate crosses either frozen alert threshold;
- otherwise compare leave-one-substrate-out (LOSO) MAE for intercept-only, E_U, and
  ideality models;
- H1/H3 requires >=20% LOSO-MAE improvement over intercept-only and must beat the
  competing one-predictor model; otherwise classify H2.

All effect sizes/noise values below are synthetic engineering assumptions.
"""
from __future__ import annotations

import argparse
import math
import platform
from dataclasses import dataclass
from typing import Dict

import numpy as np

DEFAULT_SEED = 20260826
LABELS = ("H1", "H2", "H3", "H4")


@dataclass(frozen=True)
class Scenario:
    n_substrates: int = 5
    effect_sd_mv: float = 10.0
    dvnr_noise_mv: float = 4.0
    eu_noise_mev: float = 1.0
    ideality_noise: float = 0.03
    null_el_shift_noise_mev: float = 1.2
    null_direct_recip_noise_mv: float = 4.0
    h4_el_shift_mean_mev: float = 7.0
    h4_el_shift_noise_mev: float = 1.5
    h4_direct_recip_mean_mv: float = 25.0
    h4_direct_recip_noise_mv: float = 6.0


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
    # Frozen v3.2 H4 alert thresholds.
    if np.any(np.abs(obs["el_shift_mev"]) >= 5.0) or np.any(np.abs(obs["direct_minus_recip_mv"]) > 20.0):
        return "H4"

    y = obs["dvnr_recip_mv"]
    base = intercept_loso_mae(y)
    eu_mae = loso_mae(obs["eu_mev"], y)
    n_mae = loso_mae(obs["ideality"], y)
    improve_eu = (base - eu_mae) / base if base > 0 else 0.0
    improve_n = (base - n_mae) / base if base > 0 else 0.0

    if improve_eu >= 0.20 and eu_mae < n_mae:
        return "H1"
    if improve_n >= 0.20 and n_mae < eu_mae:
        return "H3"
    return "H2"


def simulate_observations(true_h: str, scenario: Scenario, rng: np.random.Generator) -> Dict[str, np.ndarray]:
    n = scenario.n_substrates
    z = rng.normal(size=n)

    eu = 24.0 + rng.normal(0.0, 1.5, n)
    ideality = 1.25 + rng.normal(0.0, 0.05, n)
    dvnr = 300.0 + rng.normal(0.0, scenario.dvnr_noise_mv, n)
    direct_minus_recip = rng.normal(0.0, scenario.null_direct_recip_noise_mv, n)
    el_shift = rng.normal(0.0, scenario.null_el_shift_noise_mev, n)

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
        raise ValueError(f"unknown mechanism {true_h}")

    return {
        "eu_mev": eu,
        "ideality": ideality,
        "dvnr_recip_mv": dvnr,
        "direct_minus_recip_mv": direct_minus_recip,
        "el_shift_mev": el_shift,
    }


def confusion_matrix(nsim_per_class: int, scenario: Scenario, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    matrix = np.zeros((4, 4), dtype=int)
    for i, truth in enumerate(LABELS):
        for _ in range(nsim_per_class):
            pred = classify(simulate_observations(truth, scenario, rng))
            matrix[i, LABELS.index(pred)] += 1
    return matrix


def wilson_interval(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    p = k / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return center - half, center + half


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--nsim", type=int, default=2000)
    ap.add_argument("--n-substrates", type=int, default=5)
    ap.add_argument("--effect-sd-mv", type=float, default=10.0)
    ap.add_argument("--dvnr-noise-mv", type=float, default=4.0)
    args = ap.parse_args()

    scenario = Scenario(
        n_substrates=args.n_substrates,
        effect_sd_mv=args.effect_sd_mv,
        dvnr_noise_mv=args.dvnr_noise_mv,
    )
    matrix = confusion_matrix(args.nsim, scenario, args.seed)
    print(f"python={platform.python_version()} numpy={np.__version__} seed={args.seed}")
    print(f"scenario={scenario}")
    print("rows=true, columns=predicted: " + ",".join(LABELS))
    for i, h in enumerate(LABELS):
        lo, hi = wilson_interval(int(matrix[i, i]), args.nsim)
        vals = ",".join(str(int(v)) for v in matrix[i])
        print(f"{h},{vals},recovery={matrix[i,i]/args.nsim:.6f},wilson95=[{lo:.6f},{hi:.6f}]")


if __name__ == "__main__":
    main()
