#!/usr/bin/env python3
"""Reproduce the v3.62 charge-generation/collection counterexample.

Standard-library only. Source values are literature-derived experimental summaries
from Wang et al. (Advanced Materials, 2026), Table 1; they are not D18 data.
"""

from fractions import Fraction
import json
import math

TOL = 1e-12


def collection(iqe: float, eta_exc: float, eta_diss: float) -> float:
    for name, value in (("IQE", iqe), ("eta_exc", eta_exc), ("eta_diss", eta_diss)):
        if not (0.0 < value <= 1.0):
            raise ValueError(f"{name} must be in (0,1]")
    result = iqe / (eta_exc * eta_diss)
    if not (0.0 < result <= 1.0 + TOL):
        raise ValueError("derived eta_col is outside the physical fixture domain")
    return result


def exact_collection(iqe_num: int, exc_num: int, diss_num: int, den: int = 100) -> Fraction:
    return Fraction(iqe_num, den) / (Fraction(exc_num, den) * Fraction(diss_num, den))


def resolution_bounds(iqe: float, exc: float, diss: float, half_digit: float = 0.005):
    lo_iqe, hi_iqe = iqe - half_digit, iqe + half_digit
    lo_exc, hi_exc = exc - half_digit, exc + half_digit
    lo_diss, hi_diss = diss - half_digit, diss + half_digit
    lo = lo_iqe / (hi_exc * hi_diss)
    hi = hi_iqe / (lo_exc * lo_diss)
    return lo, hi


def main() -> None:
    low = {"iqe": 0.18, "exc": 0.38, "diss": 0.96}
    high = {"iqe": 0.85, "exc": 0.96, "diss": 0.95}

    low_col = collection(low["iqe"], low["exc"], low["diss"])
    high_col = collection(high["iqe"], high["exc"], high["diss"])

    low_exact = exact_collection(18, 38, 96)
    high_exact = exact_collection(85, 96, 95)
    assert math.isclose(low_col, float(low_exact), rel_tol=0.0, abs_tol=TOL)
    assert math.isclose(high_col, float(high_exact), rel_tol=0.0, abs_tol=TOL)

    # Limiting case: no collection loss.
    assert math.isclose(collection(0.48, 0.60, 0.80), 1.0, rel_tol=0.0, abs_tol=TOL)

    # Negative/control: nearly equal dissociation does not imply nearly equal collection.
    diss_abs_diff = abs(high["diss"] - low["diss"])
    col_ratio = high_col / low_col
    assert diss_abs_diff <= 0.01 + TOL
    assert col_ratio > 1.5

    # Reporting-resolution sensitivity only, not a confidence interval.
    low_bounds = resolution_bounds(low["iqe"], low["exc"], low["diss"])
    high_bounds = resolution_bounds(high["iqe"], high["exc"], high["diss"])
    worst_case_collection_ratio = high_bounds[0] / low_bounds[1]
    assert worst_case_collection_ratio > 1.5

    # Fail closed on invalid input.
    try:
        collection(0.2, 0.0, 0.9)
    except ValueError:
        invalid_input_rejected = True
    else:
        invalid_input_rejected = False
    assert invalid_input_rejected

    result = {
        "claim_class": "external experimental benchmark plus independently recomputed arithmetic",
        "low_pm6_2pct": {
            "eta_diss": low["diss"],
            "iqe": low["iqe"],
            "eta_col": low_col,
            "eta_col_exact": str(low_exact),
            "eta_col_reporting_resolution_bounds": low_bounds,
        },
        "high_pm6_45pct": {
            "eta_diss": high["diss"],
            "iqe": high["iqe"],
            "eta_col": high_col,
            "eta_col_exact": str(high_exact),
            "eta_col_reporting_resolution_bounds": high_bounds,
        },
        "dissociation_absolute_difference": diss_abs_diff,
        "iqe_ratio_45pct_over_2pct": high["iqe"] / low["iqe"],
        "collection_ratio_45pct_over_2pct": col_ratio,
        "worst_case_collection_ratio_under_reporting_resolution": worst_case_collection_ratio,
        "decision": "GOOD_DISSOCIATION_NOT_SUFFICIENT_FOR_GOOD_COLLECTION_OR_USEFUL_WORK",
        "physical_D18_result": "NONE_CROSS_MATERIAL_BENCHMARK_ONLY",
        "checks": "PASS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
