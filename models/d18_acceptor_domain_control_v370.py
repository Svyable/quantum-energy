#!/usr/bin/env python3
"""Validate the v3.70 donor-free acceptor-domain control and exercise inference logic.

This script does not analyze physical D18/PY-IT/eC9 data. Synthetic fixtures test
only the prospective decision logic. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

DEFAULT_CONTRACT = Path(__file__).resolve().parents[1] / "research" / "protocols" / "d18-pyit-ec9-acceptor-domain-control-v3.70.json"
TOL = 1e-12


def validate_contract(contract: dict) -> None:
    if contract.get("schema_version") != "quantum-energy-d18-pyit-ec9-acceptor-domain-control-v3.70":
        raise ValueError("unexpected schema_version")

    groups = {g["id"] for g in contract.get("experimental_groups", [])}
    required = {"A0", "A1", "A2", "B0", "B1", "B2"}
    if groups != required:
        raise ValueError(f"experimental groups mismatch: {groups}")

    thresholds = contract.get("physical_thresholds", {})
    for key in ("A0_vs_A1_A2_effect_margin", "B0_vs_B1_B2_interface_effect_margin", "F50_noninferiority_margin"):
        if thresholds.get(key) is not None:
            raise ValueError(f"v3.70 must not freeze a physical threshold before baseline data: {key}")

    if thresholds.get("status") != "DEFERRED_PENDING_REAL_BASELINE_AND_METHOD_CAPABILITY":
        raise ValueError("physical threshold status must remain deferred")

    hierarchy = contract.get("statistical_hierarchy", "")
    if "fabrication lot" not in hierarchy or "field point" not in hierarchy:
        raise ValueError("statistical hierarchy missing required levels")

    if "falsifier" not in contract or not contract["falsifier"].strip():
        raise ValueError("explicit falsifier required")


def verify_literature_method_precedent(contract: dict) -> dict[str, float]:
    """Cross-check the arithmetic on the Hart et al. Y5 method-precedent values."""
    p = contract["method_precedent_numbers"]
    iqe0 = float(p["iqe_short_circuit_fraction"])
    iqe1 = float(p["iqe_at_0p15_V_per_nm_fraction"])
    if not (0 < iqe0 <= 1 and 0 < iqe1 <= 1):
        raise ValueError("IQE fractions must be in (0,1]")

    ratio_float = iqe1 / iqe0
    ratio_exact = float(Fraction(93, 100) / Fraction(5, 1000))
    if abs(ratio_float - ratio_exact) > TOL:
        raise AssertionError((ratio_float, ratio_exact))
    if abs(ratio_float - float(p["descriptive_iqe_ratio"])) > TOL:
        raise AssertionError("stored descriptive IQE ratio changed")

    if not (float(p["trpl_lifetime_ns_final_upper_bound"]) < float(p["trpl_lifetime_ns_initial"])):
        raise AssertionError("TRPL limiting-order check failed")

    return {"iqe_ratio": ratio_float, "iqe_ratio_exact": ratio_exact}


def classify(
    donor_free_effect: float | None,
    donor_effect: float | None,
    donor_free_margin: float | None,
    donor_margin: float | None,
    donor_free_independent_lots: int,
    donor_independent_lots: int,
    min_independent_lots: int,
    field_calibration_pass: bool,
    optical_control_pass: bool,
) -> str:
    """Prospective semantics only; all magnitudes are caller-supplied."""
    if donor_free_margin is None or donor_margin is None:
        return "INCOMPLETE"
    if donor_free_effect is None or donor_effect is None:
        return "INCOMPLETE"
    if donor_free_margin < 0 or donor_margin < 0:
        raise ValueError("margins must be non-negative")
    if min_independent_lots < 1:
        raise ValueError("min_independent_lots must be >=1")
    if donor_free_independent_lots < min_independent_lots or donor_independent_lots < min_independent_lots:
        return "INCOMPLETE"
    if not field_calibration_pass or not optical_control_pass:
        return "INCOMPLETE"

    a = abs(donor_free_effect) > donor_free_margin
    b = abs(donor_effect) > donor_margin
    if a and b:
        return "MIXED_BULK_INTERFACE_EFFECT"
    if (not a) and b:
        return "INTERFACE_SPECIFICITY_STRENGTHENED"
    if a and (not b):
        return "DONOR_FREE_EFFECT_PRESENT"
    return "NO_RESOLVED_EFFECT"


def synthetic_checks() -> dict[str, str]:
    """Arbitrary software-only fixtures; not physical thresholds or expected effects."""
    common = dict(
        donor_free_margin=0.05,
        donor_margin=0.05,
        donor_free_independent_lots=3,
        donor_independent_lots=3,
        min_independent_lots=3,
        field_calibration_pass=True,
        optical_control_pass=True,
    )
    out = {
        "missing_margins": classify(0.1, 0.1, None, None, 3, 3, 3, True, True),
        "mixed": classify(0.08, 0.09, **common),
        "interface_specificity": classify(0.02, 0.09, **common),
        "donor_free_only": classify(0.08, 0.02, **common),
        "none": classify(0.02, 0.02, **common),
        "too_few_lots": classify(0.08, 0.09, 0.05, 0.05, 2, 3, 3, True, True),
        "bad_field_calibration": classify(0.02, 0.09, 0.05, 0.05, 3, 3, 3, False, True),
        "bad_optical_control": classify(0.02, 0.09, 0.05, 0.05, 3, 3, 3, True, False),
    }
    expected = {
        "missing_margins": "INCOMPLETE",
        "mixed": "MIXED_BULK_INTERFACE_EFFECT",
        "interface_specificity": "INTERFACE_SPECIFICITY_STRENGTHENED",
        "donor_free_only": "DONOR_FREE_EFFECT_PRESENT",
        "none": "NO_RESOLVED_EFFECT",
        "too_few_lots": "INCOMPLETE",
        "bad_field_calibration": "INCOMPLETE",
        "bad_optical_control": "INCOMPLETE",
    }
    if out != expected:
        raise AssertionError((out, expected))

    # Exact-boundary check: equal to the frozen margin is NOT called resolved.
    boundary = classify(0.05, 0.05, **common)
    if boundary != "NO_RESOLVED_EFFECT":
        raise AssertionError("strict > margin decision rule changed")

    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    args = p.parse_args()

    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    validate_contract(contract)
    precedent = verify_literature_method_precedent(contract)
    checks = synthetic_checks()

    print("d18 acceptor-domain control v3.70: PASS")
    print(f"hart_y5_descriptive_iqe_ratio={precedent['iqe_ratio']:.12f}")
    print("physical_thresholds=DEFERRED_PENDING_REAL_BASELINE_AND_METHOD_CAPABILITY")
    for k in sorted(checks):
        print(f"fixture_{k}={checks[k]}")
    print("physical_result=NONE_PROSPECTIVE_PROTOCOL_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
