#!/usr/bin/env python3
"""R2 low-temperature feasibility calculations for v3.5.

All default numerical values are SYNTHETIC/PLANNING assumptions unless explicitly
identified as physical constants. This script does not represent measured R2 data.
"""

from __future__ import annotations
import math
import csv
from pathlib import Path

KB_MEV_PER_K = 0.08617333262  # CODATA-equivalent k_B in meV/K


def coth(x: float) -> float:
    return math.cosh(x) / math.sinh(x)


def dynamic_variance_mev2(T_K: float, lambda_mev: float, mode_mev: float) -> float:
    """Keil/one-mode planning variance: lambda*hbarOmega*coth(hbarOmega/(2 kBT))."""
    x = mode_mev / (2.0 * KB_MEV_PER_K * T_K)
    return lambda_mev * mode_mev * coth(x)


def dynamic_sigma_mev(T_K: float, lambda_mev: float, mode_mev: float) -> float:
    return math.sqrt(dynamic_variance_mev2(T_K, lambda_mev, mode_mev))


def dsigma_dT_mev_per_K(T_K: float, lambda_mev: float, mode_mev: float) -> float:
    """Analytic temperature derivative of sigma(T), used for temperature-error budget."""
    x = mode_mev / (2.0 * KB_MEV_PER_K * T_K)
    sigma = dynamic_sigma_mev(T_K, lambda_mev, mode_mev)
    csch2 = 1.0 / (math.sinh(x) ** 2)
    dvar_dT = (
        lambda_mev
        * mode_mev
        * csch2
        * mode_mev
        / (2.0 * KB_MEV_PER_K * T_K**2)
    )
    return dvar_dT / (2.0 * sigma)


def high_T_marcus_variance_mev2(T_K: float, lambda_mev: float) -> float:
    return 2.0 * lambda_mev * KB_MEV_PER_K * T_K


def relative_keil_excess(T_K: float, lambda_mev: float, mode_mev: float) -> float:
    exact = dynamic_variance_mev2(T_K, lambda_mev, mode_mev)
    marcus = high_T_marcus_variance_mev2(T_K, lambda_mev)
    return exact / marcus - 1.0


def main() -> None:
    # Frozen synthetic planning priors inherited from v3.4, not R2 measurements.
    lambda_mev = 150.0
    mode_mev = 15.0
    temperature_error_K = 1.0
    temperatures = [120.0, 150.0, 240.0, 270.0, 300.0, 330.0]

    rows = []
    for T in temperatures:
        sigma = dynamic_sigma_mev(T, lambda_mev, mode_mev)
        slope = dsigma_dT_mev_per_K(T, lambda_mev, mode_mev)
        rows.append(
            {
                "temperature_K": T,
                "synthetic_dynamic_sigma_meV": sigma,
                "dsigma_dT_meV_per_K": slope,
                "linewidth_bias_for_1K_meV": abs(slope) * temperature_error_K,
                "keil_vs_marcus_variance_excess_pct": 100.0
                * relative_keil_excess(T, lambda_mev, mode_mev),
            }
        )

    out = Path(__file__).with_name("r2_low_temperature_feasibility_v3_5.csv")
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    # Independent limiting-case check: exact one-mode result approaches Marcus at high T.
    T_test = 10000.0
    rel = abs(relative_keil_excess(T_test, lambda_mev, mode_mev))
    assert rel < 1e-4, rel

    # Sign/monotonicity check: dynamic linewidth rises with T for these positive parameters.
    sigmas = [dynamic_sigma_mev(T, lambda_mev, mode_mev) for T in temperatures]
    assert all(b > a for a, b in zip(sigmas, sigmas[1:])), sigmas

    print(f"wrote {out}")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
