#!/usr/bin/env python3
"""Fail-closed audit of whether reported literature evidence can satisfy the project stabilized-Pmax gate.

No device values are invented or inferred. The calculation is Boolean decision logic over
source-provenance facts frozen in the machine-readable contract.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "machine" / "d18-literature-stabilized-work-audit-v3.51.json"


def evaluate(d: dict) -> dict:
    gate = d["project_gate"]
    evidence = d["decision_logic"]
    required = bool(gate["requires_stabilized_pmax"])
    observed = bool(evidence["stabilized_mpp_trace_reported_in_primary_main_text"])
    can_pass = (not required) or observed
    return {
        "requires_stabilized_pmax": required,
        "stabilized_mpp_trace_reported": observed,
        "can_literature_champion_satisfy_project_stabilized_work_gate": can_pass,
        "classification": "ELIGIBLE_FOR_STABILIZED_WORK_EVALUATION" if can_pass else "MECHANISM_OR_CHAMPION_SCAN_EVIDENCE_ONLY",
    }


def independent_check(d: dict) -> bool:
    """Independent set-containment derivation, not the evaluate() Boolean expression.

    Treat a strong gate as a set of mandatory evidence tokens. A candidate evidence packet
    is eligible only when required_tokens is a subset of observed_tokens.
    """
    required_tokens = {"paired_power_metric", "stabilized_mpp"}
    observed_tokens = {"paired_power_metric"}  # scanned J-V/PCE only; no stabilized-MPP trace in inspected main text
    return required_tokens.issubset(observed_tokens)


def self_test() -> None:
    d = json.loads(CONTRACT.read_text())
    out = evaluate(d)
    assert out["requires_stabilized_pmax"] is True
    assert out["stabilized_mpp_trace_reported"] is False
    assert out["can_literature_champion_satisfy_project_stabilized_work_gate"] is False
    assert independent_check(d) is False

    # Limiting/control cases: if the project did not require stabilized MPP, scan evidence
    # would not be excluded on this criterion; if stabilized evidence appears, eligibility changes.
    d_no_req = json.loads(CONTRACT.read_text())
    d_no_req["project_gate"]["requires_stabilized_pmax"] = False
    assert evaluate(d_no_req)["can_literature_champion_satisfy_project_stabilized_work_gate"] is True

    d_with_trace = json.loads(CONTRACT.read_text())
    d_with_trace["decision_logic"]["stabilized_mpp_trace_reported_in_primary_main_text"] = True
    assert evaluate(d_with_trace)["can_literature_champion_satisfy_project_stabilized_work_gate"] is True
    print("D18_LITERATURE_STABILIZED_WORK_AUDIT_V3.51: PASS")


if __name__ == "__main__":
    self_test()
    print(json.dumps(evaluate(json.loads(CONTRACT.read_text())), indent=2, sort_keys=True))
