#!/usr/bin/env python3
"""Reproduce v3.65 eC9 blade-coated module scale benchmark arithmetic.

Standard-library only. Source values are literature-derived experimental summaries
from Journal of Materials Chemistry C (2025), DOI 10.1039/D5TC01245G.
They are not D18/PY-IT/eC9 measurements or acceptance thresholds.
"""
from fractions import Fraction
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "research/benchmarks/ec9-blade-module-scale-bound-v3.65.json"
TOL = 1e-12


def retention(cell_pce: float, module_pce: float) -> tuple[float, float]:
    if cell_pce <= 0 or module_pce <= 0:
        raise ValueError("PCE inputs must be positive")
    r = module_pce / cell_pce
    return r, 1.0 - r


def main() -> None:
    d = json.loads(INPUT.read_text(encoding="utf-8"))
    x = d["inputs"]
    cell = float(x["blade_coated_cell_pce_percent"]["value"])
    module = float(x["module_pce_percent"]["value"])
    area = float(x["module_effective_area_cm2"]["value"])
    if area <= 0:
        raise ValueError("module area must be positive")

    r, drop = retention(cell, module)

    # Independent exact arithmetic from the printed decimal source summaries.
    exact_r = Fraction("15.7") / Fraction("18.1")
    exact_drop = 1 - exact_r
    assert math.isclose(r, float(exact_r), rel_tol=0.0, abs_tol=TOL)
    assert math.isclose(drop, float(exact_drop), rel_tol=0.0, abs_tol=TOL)

    # Limiting case: no cell-to-module PCE change.
    r0, d0 = retention(10.0, 10.0)
    assert r0 == 1.0 and d0 == 0.0

    # Negative/control: a higher module PCE remains a negative 'drop'.
    rn, dn = retention(10.0, 11.0)
    assert rn == 1.1 and math.isclose(dn, -0.1, rel_tol=0.0, abs_tol=TOL)

    # Invalid domain fails closed.
    try:
        retention(0.0, 10.0)
    except ValueError:
        invalid_rejected = True
    else:
        invalid_rejected = False
    assert invalid_rejected

    # Printed-value resolution sensitivity only, not measurement uncertainty.
    # One-decimal PCE values imply half-unit of 0.05 percentage point.
    r_lo = (module - 0.05) / (cell + 0.05)
    r_hi = (module + 0.05) / (cell - 0.05)
    assert r_lo < r < r_hi
    assert r_lo > 0.85

    print(json.dumps({
        "claim_class": d["claim_class"],
        "module_effective_area_cm2": area,
        "pce_retention_fraction": r,
        "relative_pce_drop_fraction": drop,
        "pce_retention_reporting_resolution_bounds": [r_lo, r_hi],
        "decision": "EC9_NOT_INTRINSICALLY_EXCLUDED_FROM_SCALABLE_BLADE_MODULES_PROCESS_TRANSFER_REMAINS_THE_FALSIFIER",
        "physical_D18_PYIT_EC9_result": "NONE_CROSS_MATERIAL_BENCHMARK_ONLY",
        "checks": "PASS"
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
