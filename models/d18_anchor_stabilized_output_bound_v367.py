#!/usr/bin/env python3
"""Validate the v3.67 target-anchor stabilized-output evidence boundary.

Standard-library only. This script classifies evidence type; it does not estimate
D18/PY-IT/eC9 stabilized power or invent a physical device threshold.
"""
from fractions import Fraction
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "research/benchmarks/d18-anchor-stabilized-output-bound-v3.67.json"
TOL = 1e-12


def classify_output_evidence(scan_present: bool, stabilized_trace_present: bool, independent_lots: int, min_lots: int = 3) -> str:
    if independent_lots < 0:
        raise ValueError("independent_lots must be non-negative")
    if stabilized_trace_present and independent_lots >= min_lots:
        return "STABILIZED_OUTPUT_EVIDENCE_PRESENT"
    if scan_present:
        return "SCANNED_JV_ONLY_NOT_STABILIZED_PMAX_GATE"
    return "NO_OUTPUT_EVIDENCE"


def main() -> None:
    d = json.loads(CONTRACT.read_text(encoding="utf-8"))
    x = d["literature_inputs"]
    g = d["project_gate"]

    delay_ms = float(x["JV_point_delay_ms_approx"])
    if delay_ms <= 0:
        raise ValueError("reported delay must be positive")
    delay_s = delay_ms / 1000.0

    # Independent representation of the reported nominal 5 ms conversion.
    exact_delay_s = Fraction(5, 1000)
    assert math.isclose(delay_s, float(exact_delay_s), rel_tol=0.0, abs_tol=TOL)
    assert math.isclose(delay_s, d["unit_conversion"]["expected_delay_s_approx"], rel_tol=0.0, abs_tol=TOL)

    decision = classify_output_evidence(
        scan_present=True,
        stabilized_trace_present=bool(x["stabilized_mpp_trace_in_inspected_main_article"]),
        independent_lots=int(x["independent_material_lot_count_established_for_optimized_output"]),
        min_lots=int(g["independent_lots_min"]),
    )
    assert decision == d["decision"]

    # Limiting case: an evidence record with stabilized trace + required lot count.
    assert classify_output_evidence(True, True, 3, 3) == "STABILIZED_OUTPUT_EVIDENCE_PRESENT"

    # Negative/control: nominally favorable scan data cannot substitute for stabilization.
    assert classify_output_evidence(True, False, 99, 3) == "SCANNED_JV_ONLY_NOT_STABILIZED_PMAX_GATE"

    # Fail closed if neither form of output evidence exists.
    assert classify_output_evidence(False, False, 0, 3) == "NO_OUTPUT_EVIDENCE"

    # Invalid hierarchy count must fail visibly.
    try:
        classify_output_evidence(True, False, -1, 3)
    except ValueError:
        invalid_rejected = True
    else:
        invalid_rejected = False
    assert invalid_rejected

    print(json.dumps({
        "claim_class": d["claim_class"],
        "reported_JV_point_delay_s_approx": delay_s,
        "project_stabilized_pmax_relative_gate": g["stabilized_pmax_relative_improvement_min"],
        "project_independent_lots_min": g["independent_lots_min"],
        "decision": decision,
        "physical_project_result": "NONE_EXTERNAL_EVIDENCE_BOUNDARY_ONLY",
        "checks": "PASS"
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
