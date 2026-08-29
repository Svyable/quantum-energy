#!/usr/bin/env python3
"""Prospective D18/PY-IT/eC9 >=1 cm^2 scale-transfer protocol validator.

Standard-library only. Synthetic fixtures exercise logic; they are not material predictions.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "research" / "protocols" / "d18-pyit-ec9-scale-transfer-v3.68.json"
TOL = 1e-12


def relative_gain(candidate: float, baseline: float) -> float:
    if candidate <= 0 or baseline <= 0:
        raise ValueError("Pmax density must be positive")
    return candidate / baseline - 1.0


def exact_relative_gain(candidate_tenths: int, baseline_tenths: int) -> Fraction:
    if candidate_tenths <= 0 or baseline_tenths <= 0:
        raise ValueError("Pmax density must be positive")
    return Fraction(candidate_tenths, baseline_tenths) - 1


def evaluate_large_area_useful_work(candidate: list[float], baseline: list[float], threshold: float = 0.05) -> dict:
    if len(candidate) != len(baseline):
        raise ValueError("candidate/baseline lot counts differ")
    if len(candidate) < 3:
        return {"status": "INCOMPLETE", "reason": "fewer than 3 independent fabrication lots"}
    gains = [relative_gain(c, b) for c, b in zip(candidate, baseline)]
    mean_gain = sum(gains) / len(gains)
    same_sign = all(g > 0 for g in gains)
    passed = same_sign and mean_gain >= threshold
    return {
        "status": "PASS" if passed else "FAIL",
        "gains": gains,
        "mean_gain": mean_gain,
        "same_sign": same_sign,
    }


def scale_retention(large: float, small: float) -> float:
    if large <= 0 or small <= 0:
        raise ValueError("Pmax density must be positive")
    return large / small


def self_test() -> None:
    data = json.loads(CONTRACT.read_text())
    fx = data["synthetic_fixture"]
    threshold = data["decision_metrics"]["stabilized_useful_work_gain"]["existing_project_threshold_relative"]

    # Primary float path.
    passed = evaluate_large_area_useful_work(
        fx["candidate_large_pmax_density_pass"], fx["b0_large_pmax_density"], threshold
    )
    failed = evaluate_large_area_useful_work(
        fx["candidate_large_pmax_density_fail"], fx["b0_large_pmax_density"], threshold
    )

    assert passed["status"] == "PASS"
    assert failed["status"] == "FAIL"
    assert math.isclose(passed["mean_gain"], fx["expected_pass_mean_gain"], abs_tol=TOL)

    # Independent exact-rational arithmetic for the nominal 10.6/10.0 lot gain.
    exact = exact_relative_gain(106, 100)
    assert abs(float(exact) - passed["gains"][0]) <= TOL
    assert exact == Fraction(3, 50)

    # Limiting case: equal stabilized power density -> zero gain.
    assert relative_gain(10.0, 10.0) == 0.0
    assert scale_retention(10.0, 10.0) == 1.0

    # Negative/control case: one reversed lot defeats same-sign rule even if others are favorable.
    assert failed["gains"][-1] < 0
    assert failed["same_sign"] is False

    # Experimental hierarchy rule: two lots cannot support the existing project useful-work gate.
    incomplete = evaluate_large_area_useful_work([10.6, 10.6], [10.0, 10.0], threshold)
    assert incomplete["status"] == "INCOMPLETE"

    # Area applicability: protocol's large-area class starts at 1 cm^2.
    assert data["scope"]["large_area_minimum_cm2"] == 1.0

    # No synthetic physical margins are allowed to appear.
    assert data["decision_metrics"]["scale_retention"]["physical_acceptance_threshold"] is None
    assert data["decision_metrics"]["field_generation_noninferiority"]["physical_acceptance_margin"] is None
    assert data["decision_metrics"]["transport_collection_noninferiority"]["physical_acceptance_margin"] is None
    assert data["decision_metrics"]["yield"]["physical_acceptance_threshold"] is None

    print(f"pass_mean_gain={passed['mean_gain']:.12f}")
    print(f"pass_gains={[round(x, 12) for x in passed['gains']]}")
    print(f"fail_gains={[round(x, 12) for x in failed['gains']]}")
    print("checks=PASS")


if __name__ == "__main__":
    self_test()
