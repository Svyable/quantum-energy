#!/usr/bin/env python3
"""Reproduce v3.67 target-anchor stabilized-output evidence boundary.

Standard-library only. Synthetic fixtures test classification logic; they are not
physical predictions or target thresholds.
"""
from fractions import Fraction
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "research/data/d18-pyit-ec9-stabilized-output-bound-v3.67.json"
TOL = 1e-12


def classify(has_stabilized_pmax: bool, independent_lots: int) -> str:
    if has_stabilized_pmax and independent_lots >= 3:
        return "eligible_for_useful_work_gate_evaluation"
    return "scan_or_incomplete_output_evidence_only"


def main() -> None:
    d = json.loads(DATA.read_text())
    ms = float(d["observations"]["jv_delay_ms"])
    seconds = ms / 1000.0
    exact = float(Fraction(str(ms)) / 1000)
    expected = float(d["observations"]["jv_delay_s"])
    assert abs(seconds - exact) <= TOL
    assert abs(seconds - expected) <= TOL
    assert seconds > 0.0

    # Limiting case: actual stabilized output across >=3 independent lots can be evaluated.
    assert classify(True, 3) == "eligible_for_useful_work_gate_evaluation"
    # Negative/control: excellent scan performance alone cannot pass the output-evidence gate.
    assert classify(False, 99) == "scan_or_incomplete_output_evidence_only"
    # Independence control: stabilized trace on fewer than three lots is still incomplete for the project gate.
    assert classify(True, 2) == "scan_or_incomplete_output_evidence_only"

    print(f"5 ms = {seconds:.6f} s; exact cross-check passed at {TOL:g}")
    print("anchor classification:", classify(False, 0))
    print("decision: require prospective stabilized Pmax before useful-work promotion")


if __name__ == "__main__":
    main()
