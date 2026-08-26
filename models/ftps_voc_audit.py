#!/usr/bin/env python3
"""Preregistered calculation helpers for the R2 FTPS + Voc-intensity mechanism audit.

This module does not contain experimental results. The built-in self-test uses synthetic
inputs and is intended to verify units, signs, and independent calculation paths.

Primary relations
-----------------
Urbach tail: ln(EQE) = a + E / E_U  => E_U = 1 / slope.
Light-intensity ideality diagnostic: dVoc/dln(I) = n k_B T / q.
With energy expressed in eV, k_B/q numerically equals k_B[eV/K] in V/K.
Nonradiative loss: DeltaV_nr = -(k_B T/q) ln(EQE_EL).
"""
from __future__ import annotations

import argparse
import math
import platform
from dataclasses import dataclass

import numpy as np

KB_EV_PER_K = 8.617333262e-5
DEFAULT_SEED = 20260826


@dataclass(frozen=True)
class LinearFit:
    slope: float
    intercept: float


def ols(x: np.ndarray, y: np.ndarray) -> LinearFit:
    """Closed-form OLS with intercept; independent of np.polyfit."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    xm = x.mean()
    ym = y.mean()
    denom = np.sum((x - xm) ** 2)
    if denom <= 0:
        raise ValueError("x must have nonzero variance")
    slope = np.sum((x - xm) * (y - ym)) / denom
    return LinearFit(float(slope), float(ym - slope * xm))


def urbach_energy_ev(energy_ev: np.ndarray, eqe: np.ndarray) -> float:
    """Return empirical Urbach energy E_U [eV] from ln(EQE) vs E.

    Validity: only use within a preregistered exponential-tail window with positive,
    background-resolved EQE. This is an empirical descriptor, not by itself proof of
    a unique microscopic disorder mechanism.
    """
    energy_ev = np.asarray(energy_ev, dtype=float)
    eqe = np.asarray(eqe, dtype=float)
    if np.any(eqe <= 0):
        raise ValueError("EQE must be positive")
    fit = ols(energy_ev, np.log(eqe))
    if fit.slope <= 0:
        raise ValueError("Expected positive ln(EQE)-vs-energy slope in Urbach tail")
    return 1.0 / fit.slope


def urbach_endpoint_crosscheck_ev(energy_ev: np.ndarray, eqe: np.ndarray) -> float:
    """Independent two-endpoint cross-check; diagnostic only, not final estimator."""
    energy_ev = np.asarray(energy_ev, dtype=float)
    eqe = np.asarray(eqe, dtype=float)
    dl = math.log(float(eqe[-1])) - math.log(float(eqe[0]))
    if dl <= 0:
        raise ValueError("Tail must rise with energy")
    return float((energy_ev[-1] - energy_ev[0]) / dl)


def ideality_from_ln_intensity(intensity_ratio: np.ndarray, voc_v: np.ndarray, temperature_k: float) -> float:
    """Empirical ideality n from Voc vs ln(relative intensity)."""
    if temperature_k <= 0:
        raise ValueError("temperature must be positive")
    x = np.log(np.asarray(intensity_ratio, dtype=float))
    fit = ols(x, np.asarray(voc_v, dtype=float))
    return fit.slope / (KB_EV_PER_K * temperature_k)


def ideality_from_log10_intensity(intensity_ratio: np.ndarray, voc_v: np.ndarray, temperature_k: float) -> float:
    """Independent log10 derivation: slope_dec = n kBT ln(10)/q."""
    x = np.log10(np.asarray(intensity_ratio, dtype=float))
    fit = ols(x, np.asarray(voc_v, dtype=float))
    return fit.slope / (KB_EV_PER_K * temperature_k * math.log(10.0))


def delta_vnr_v(eqe_el: float, temperature_k: float) -> float:
    """Nonradiative voltage loss [V] from absolute external EL quantum efficiency."""
    if not 0 < eqe_el <= 1:
        raise ValueError("EQE_EL must be in (0, 1]")
    if temperature_k <= 0:
        raise ValueError("temperature must be positive")
    return -KB_EV_PER_K * temperature_k * math.log(eqe_el)


def self_test(seed: int = DEFAULT_SEED) -> None:
    rng = np.random.default_rng(seed)

    # Limiting/sign checks for DeltaV_nr.
    assert abs(delta_vnr_v(1.0, 300.0)) < 1e-15
    assert delta_vnr_v(1e-6, 300.0) > delta_vnr_v(1e-4, 300.0) > 0

    # Synthetic Urbach tail: E_U = 25 meV, 2% log-domain noise.
    energy = np.linspace(1.10, 1.30, 101)
    eu_true = 0.025
    ln_eqe = -55.0 + energy / eu_true
    eqe = np.exp(ln_eqe + rng.normal(0.0, 0.02, energy.size))
    eu_fit = urbach_energy_ev(energy, eqe)
    eu_endpoint_noise_free = urbach_endpoint_crosscheck_ev(energy, np.exp(ln_eqe))
    assert abs(eu_fit - eu_true) < 0.0005  # 0.5 meV preregistered code self-test tolerance
    assert abs(eu_endpoint_noise_free - eu_true) < 1e-12

    # Synthetic Voc-intensity: n = 1.30 at 300 K, 0.5 mV Gaussian read noise.
    T = 300.0
    n_true = 1.30
    intensity = np.logspace(-1.0, math.log10(1.2), 9)
    voc = 0.85 + n_true * KB_EV_PER_K * T * np.log(intensity)
    voc_noisy = voc + rng.normal(0.0, 0.0005, intensity.size)
    n_ln = ideality_from_ln_intensity(intensity, voc_noisy, T)
    n_log10 = ideality_from_log10_intensity(intensity, voc_noisy, T)
    assert abs(n_ln - n_log10) < 1e-12
    assert abs(n_ln - n_true) < 0.05

    expected_slope_v_per_dec = n_true * KB_EV_PER_K * T * math.log(10.0)
    print(f"seed={seed}")
    print(f"python={platform.python_version()} numpy={np.__version__}")
    print(f"kBT/q @300K={KB_EV_PER_K*T:.12f} V")
    print(f"synthetic EU true={eu_true*1e3:.6f} meV fit={eu_fit*1e3:.6f} meV")
    print(f"synthetic ideality true={n_true:.6f} ln-fit={n_ln:.6f} log10-fit={n_log10:.6f}")
    print(f"expected Voc slope for n=1.30 @300K={expected_slope_v_per_dec*1e3:.6f} mV/dec")
    print("SELF_TEST_PASS")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="run deterministic synthetic checks")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()
    if args.self_test:
        self_test(args.seed)
    else:
        parser.print_help()
