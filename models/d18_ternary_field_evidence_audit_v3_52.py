#!/usr/bin/env python3
"""Fail-closed audit for D18/PY-IT/eC9 ternary field-generation evidence.

Standard library only. This verifies the machine-readable claim boundary; it does not
reproduce the underlying experiments or infer absence from uninspected supplements.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT = Path("machine/d18-ternary-field-evidence-audit-v3.52.json")


def load_contract(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def evaluate(contract: dict) -> dict:
    rule = contract["fail_closed_rule"]
    eligible = bool(
        rule["ternary_specific"]
        and rule["field_dependent"]
        and rule["provenance_complete"]
    )
    return {
        "eligible_for_field_robustness_claim": eligible,
        "status": "PASS" if eligible else "INCOMPLETE",
    }


def self_test(contract: dict) -> None:
    result = evaluate(contract)
    assert result["status"] == "INCOMPLETE"
    assert result["eligible_for_field_robustness_claim"] is False
    assert contract["audit_status"] == "INCOMPLETE"

    # Negative/control: satisfying only ternary specificity is insufficient.
    probe = json.loads(json.dumps(contract))
    probe["fail_closed_rule"].update(
        ternary_specific=True,
        field_dependent=False,
        provenance_complete=True,
    )
    assert evaluate(probe)["status"] == "INCOMPLETE"

    # Limiting positive case: all three prerequisites true is sufficient for this
    # evidence-eligibility rule. This is a logic fixture, not a physical result.
    probe["fail_closed_rule"].update(
        ternary_specific=True,
        field_dependent=True,
        provenance_complete=True,
    )
    assert evaluate(probe)["status"] == "PASS"

    # Claim-discipline invariant: the approximate 20 meV literature value cannot
    # silently become a project threshold.
    q = contract["source_observations"][1]["quantitative_inputs"][0]
    assert q["uncertainty"] is None
    assert "not used as a physical acceptance threshold" in q["decision_use"]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--contract", type=Path, default=DEFAULT)
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    contract = load_contract(args.contract)
    result = evaluate(contract)
    if args.check:
        self_test(contract)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
