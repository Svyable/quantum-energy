#!/usr/bin/env python3
"""Reproduce v3.64 thick-film transport/manufacturing benchmark arithmetic.

Standard-library only. Source values are literature-derived experimental summaries
from Nature Communications (2025), DOI 10.1038/s41467-025-64808-x.
They are not D18/PY-IT/eC9 measurements or acceptance thresholds.
"""
from fractions import Fraction
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "research/benchmarks/thick-film-transport-scale-bound-v3.64.json"
TOL = 1e-12


def positive_ratio(control: float, modified: float) -> tuple[float, float]:
    if control <= 0 or modified <= 0:
        raise ValueError("ratio inputs must be positive")
    return control / modified, 1.0 - modified / control


def main() -> None:
    d = json.loads(INPUT.read_text(encoding="utf-8"))
    x = d["inputs"]
    tc = float(x["tpc_extraction_time_us_control"]["value"])
    tm = float(x["tpc_extraction_time_us_btp_ec9"]["value"])
    nc = float(x["defect_density_cm3_control"]["value"])
    nm = float(x["defect_density_cm3_btp_ec9"]["value"])
    ec = float(x["urbach_meV_control"]["value"])
    em = float(x["urbach_meV_btp_ec9"]["value"])

    speedup, time_reduction = positive_ratio(tc, tm)
    _, defect_reduction = positive_ratio(nc, nm)
    _, urbach_reduction = positive_ratio(ec, em)

    # Independent exact arithmetic from the printed decimal source summaries.
    exact_speedup = Fraction("0.93") / Fraction("0.43")
    exact_time_reduction = 1 - Fraction("0.43") / Fraction("0.93")
    exact_defect_reduction = 1 - Fraction(494, 617)
    exact_urbach_reduction = 1 - Fraction("20.8") / Fraction("23.0")
    for a, b in ((speedup, exact_speedup), (time_reduction, exact_time_reduction),
                 (defect_reduction, exact_defect_reduction), (urbach_reduction, exact_urbach_reduction)):
        assert math.isclose(a, float(b), rel_tol=0.0, abs_tol=TOL)

    # Limiting case.
    r, red = positive_ratio(1.0, 1.0)
    assert r == 1.0 and red == 0.0

    # Negative/control: a slower modified device remains visibly negative.
    slow_ratio, slow_reduction = positive_ratio(1.0, 2.0)
    assert slow_ratio == 0.5 and slow_reduction == -1.0

    # Invalid domain fails closed.
    try:
        positive_ratio(1.0, 0.0)
    except ValueError:
        invalid_rejected = True
    else:
        invalid_rejected = False
    assert invalid_rejected

    # Reporting-resolution sensitivity only, not statistical uncertainty.
    speedup_lo = (tc - 0.005) / (tm + 0.005)
    speedup_hi = (tc + 0.005) / (tm - 0.005)
    assert speedup_lo > 2.0

    print(json.dumps({
        "claim_class": d["claim_class"],
        "tpc_extraction_speedup": speedup,
        "tpc_extraction_time_reduction_fraction": time_reduction,
        "defect_density_reduction_fraction": defect_reduction,
        "urbach_energy_reduction_fraction": urbach_reduction,
        "jsc_alpha_change": float(x["jsc_light_intensity_alpha_btp_ec9"]["value"]) - float(x["jsc_light_intensity_alpha_control"]["value"]),
        "ideality_factor_change": float(x["ideality_factor_btp_ec9"]["value"]) - float(x["ideality_factor_control"]["value"]),
        "tpc_speedup_reporting_resolution_bounds": [speedup_lo, speedup_hi],
        "decision": "ZERO_FIELD_MOBILITY_ALONE_NOT_ADEQUATE_FOR_THICK_FILM_SCALE_TRANSFER",
        "physical_D18_PYIT_EC9_result": "NONE_CROSS_MATERIAL_BENCHMARK_ONLY",
        "checks": "PASS"
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
