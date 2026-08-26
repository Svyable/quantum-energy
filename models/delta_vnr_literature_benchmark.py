#!/usr/bin/env python3
"""Independent literature regression test for the program's ΔVnr calculation.

Public source values are from:
Li et al., Nature Communications 13, 3113 (2022),
https://www.nature.com/articles/s41467-022-30225-7

The paper reports measured EQE_EL and corresponding non-radiative voltage
losses for five PM6:NFA devices. This script checks the canonical relation

    ΔV_nr = -(k_B T / q) ln(EQE_EL)

using EQE_EL as a dimensionless fraction. Because k_B is expressed here in
eV/K, k_B T numerically equals k_B T / q in volts.

The published numbers are experimental/literature values. This script does
not reproduce their experiment; it independently recomputes the tabulated
voltage-loss relation from the published rounded values.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

K_B_EV_PER_K = 8.617333262145e-5
T_BENCHMARK_K = 300.0
MAX_ABS_ERROR_MV = 1.0
IMPLIED_T_MIN_K = 298.0
IMPLIED_T_MAX_K = 302.0


@dataclass(frozen=True)
class BenchmarkPoint:
    device: str
    eqe_el_fraction: float
    reported_delta_vnr_v: float


POINTS = (
    BenchmarkPoint("PM6:Y6", 6.2e-5, 0.250),
    BenchmarkPoint("PM6:BO-4F", 1.3e-4, 0.231),
    BenchmarkPoint("PM6:BO-4Cl", 1.4e-4, 0.229),
    BenchmarkPoint("PM6:BO-5Cl", 1.02e-3, 0.178),
    BenchmarkPoint("PM6:BO-6Cl", 7.2e-4, 0.187),
)


def delta_vnr_from_eqe(eqe_el_fraction: float, temperature_k: float) -> float:
    if not 0.0 < eqe_el_fraction <= 1.0:
        raise ValueError("EQE_EL must be a dimensionless fraction in (0, 1].")
    if temperature_k <= 0.0:
        raise ValueError("temperature_k must be positive.")
    return -K_B_EV_PER_K * temperature_k * math.log(eqe_el_fraction)


def implied_temperature_k(eqe_el_fraction: float, delta_vnr_v: float) -> float:
    if not 0.0 < eqe_el_fraction < 1.0:
        raise ValueError("EQE_EL must be a dimensionless fraction in (0, 1).")
    return delta_vnr_v / (-K_B_EV_PER_K * math.log(eqe_el_fraction))


def run_benchmark() -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for p in POINTS:
        calculated_v = delta_vnr_from_eqe(p.eqe_el_fraction, T_BENCHMARK_K)
        error_mv = 1e3 * (calculated_v - p.reported_delta_vnr_v)
        implied_t = implied_temperature_k(p.eqe_el_fraction, p.reported_delta_vnr_v)

        # Deliberately wrong unit interpretation: treating an already fractional
        # EQE_EL as though it must be multiplied by 100. This provides a regression
        # test for the common percent-vs-fraction mistake.
        wrong_percent_v = delta_vnr_from_eqe(p.eqe_el_fraction * 100.0, T_BENCHMARK_K)
        percent_bug_error_mv = 1e3 * (wrong_percent_v - p.reported_delta_vnr_v)

        rows.append(
            {
                "device": p.device,
                "eqe_el_fraction": p.eqe_el_fraction,
                "reported_delta_vnr_v": p.reported_delta_vnr_v,
                "calculated_delta_vnr_300k_v": calculated_v,
                "error_mv": error_mv,
                "implied_temperature_k": implied_t,
                "percent_bug_error_mv": percent_bug_error_mv,
            }
        )
    return rows


def validate(rows: list[dict[str, float | str]]) -> None:
    max_abs_error = max(abs(float(r["error_mv"])) for r in rows)
    if max_abs_error > MAX_ABS_ERROR_MV:
        raise AssertionError(f"Published benchmark mismatch {max_abs_error:.3f} mV > {MAX_ABS_ERROR_MV:.3f} mV")

    for r in rows:
        t = float(r["implied_temperature_k"])
        if not IMPLIED_T_MIN_K <= t <= IMPLIED_T_MAX_K:
            raise AssertionError(f"Implied temperature {t:.3f} K outside expected room-temperature window")

    # Limiting cases and sign/unit sanity.
    if delta_vnr_from_eqe(1.0, 300.0) != 0.0:
        raise AssertionError("EQE_EL=1 must imply zero non-radiative loss")
    if not delta_vnr_from_eqe(1e-6, 300.0) > delta_vnr_from_eqe(1e-3, 300.0):
        raise AssertionError("Lower EQE_EL must imply larger ΔVnr")

    # The deliberate percent/fraction bug must be obviously detectable.
    min_bug = min(abs(float(r["percent_bug_error_mv"])) for r in rows)
    if min_bug < 100.0:
        raise AssertionError("Percent/fraction regression control unexpectedly weak")


def write_csv(rows: list[dict[str, float | str]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = run_benchmark()
    validate(rows)
    out = Path(__file__).with_name("delta_vnr_literature_benchmark_v3_8.csv")
    write_csv(rows, out)
    print(f"PASS: {len(rows)} published device points; output={out.name}")
    print(f"max |error| = {max(abs(float(r['error_mv'])) for r in rows):.6f} mV")
    print(
        "implied T range = "
        f"{min(float(r['implied_temperature_k']) for r in rows):.6f}–"
        f"{max(float(r['implied_temperature_k']) for r in rows):.6f} K"
    )
    print(
        "percent/fraction bug error range = "
        f"{min(abs(float(r['percent_bug_error_mv'])) for r in rows):.3f}–"
        f"{max(abs(float(r['percent_bug_error_mv'])) for r in rows):.3f} mV"
    )


if __name__ == "__main__":
    main()
