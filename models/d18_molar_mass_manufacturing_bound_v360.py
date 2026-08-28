#!/usr/bin/env python3
"""v3.60 D18 molar-mass manufacturing confound audit.

Standard-library only. Reads the committed evidence contract, recomputes the
conservative PCE bound, checks exact arithmetic independently with Fraction,
and exercises prospective causal-control fixtures.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "research/data/d18-molar-mass-manufacturing-bound-v360.json"
TOL = 1e-12


def load_contract() -> dict:
    with INPUT.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def causal_attribution_eligible(*, lot_id: bool, mw_recorded: bool, same_lot_randomized: bool) -> bool:
    """Fail closed unless the three predeclared D18 provenance controls pass."""
    return lot_id and mw_recorded and same_lot_randomized


def main() -> None:
    contract = load_contract()
    inp = contract["inputs"]

    high_min = float(inp["high_mw_pce_percent"]["min"])
    low_ceiling = float(inp["low_mw_pce_percent"]["upper_bound_exclusive"])
    commercial = float(inp["commercial_reference_pce_percent"]["value"])
    high_max = float(inp["high_mw_pce_percent"]["max"])

    # Primary calculation. Because the low-Mw source statement is PCE <2%, the
    # ratio is strictly greater than this conservative ceiling calculation.
    multiplier_ceiling_ratio = high_min / low_ceiling
    high_fraction_commercial = (high_min / commercial, high_max / commercial)

    # Independent arithmetic path: exact rational values derived from decimal
    # source summaries. This is not a second physical dataset.
    exact_multiplier = Fraction("7.8") / Fraction("2.0")
    exact_fraction_min = Fraction("7.8") / Fraction("8.9")
    exact_fraction_max = Fraction("8.0") / Fraction("8.9")

    assert math.isclose(multiplier_ceiling_ratio, float(exact_multiplier), rel_tol=0.0, abs_tol=TOL)
    assert math.isclose(high_fraction_commercial[0], float(exact_fraction_min), rel_tol=0.0, abs_tol=TOL)
    assert math.isclose(high_fraction_commercial[1], float(exact_fraction_max), rel_tol=0.0, abs_tol=TOL)

    expected = contract["derived_quantities"]
    assert expected["conservative_high_to_low_pce_multiplier"]["relation"] == ">"
    assert math.isclose(expected["conservative_high_to_low_pce_multiplier"]["value"], multiplier_ceiling_ratio, rel_tol=0.0, abs_tol=TOL)
    assert math.isclose(expected["high_mw_fraction_of_commercial_reference"]["min"], high_fraction_commercial[0], rel_tol=0.0, abs_tol=TOL)
    assert math.isclose(expected["high_mw_fraction_of_commercial_reference"]["max"], high_fraction_commercial[1], rel_tol=0.0, abs_tol=TOL)

    # Dimensional and domain checks: PCE/PCE is dimensionless and all PCEs are
    # positive percentages. The active-area quantity is positive but is not
    # used to infer a scale penalty.
    assert high_min > 0 and high_max > 0 and low_ceiling > 0 and commercial > 0
    assert float(inp["active_area_cm2"]["value"]) > 0
    assert high_fraction_commercial[0] < high_fraction_commercial[1] < 1.0

    # Limiting/control tests for the causal-provenance rule.
    assert causal_attribution_eligible(lot_id=True, mw_recorded=True, same_lot_randomized=True)
    assert not causal_attribution_eligible(lot_id=True, mw_recorded=False, same_lot_randomized=True)
    assert not causal_attribution_eligible(lot_id=True, mw_recorded=True, same_lot_randomized=False)
    assert not causal_attribution_eligible(lot_id=False, mw_recorded=True, same_lot_randomized=True)

    print("v3.60 D18 molar-mass manufacturing bound: PASS")
    print(f"conservative high/low PCE multiplier: > {multiplier_ceiling_ratio:.6f}x")
    print(
        "high-Mw source PCE as fraction of commercial D18 reference: "
        f"{high_fraction_commercial[0]:.6f} to {high_fraction_commercial[1]:.6f}"
    )
    print("B0/B1/B2 causal attribution gate: record lot ID + Mw provenance + same-lot randomized arms")
    print("No D18/PY-IT/eC9 Mw acceptance threshold is created by this audit.")


if __name__ == "__main__":
    main()
