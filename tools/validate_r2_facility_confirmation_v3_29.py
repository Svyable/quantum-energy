#!/usr/bin/env python3
"""Validate the frozen v3.29 R2 facility confirmation questionnaire and response template."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "technical/data/r2_facility_capability_contract_v3_27.json"
QUESTIONNAIRE = ROOT / "technical/data/r2_facility_confirmation_questionnaire_v3_29.json"
TEMPLATE = ROOT / "technical/data/r2_facility_confirmation_response_template_v3_29.csv"

EXPECTED_GLOBAL = {f"G{i:02d}" for i in range(1, 9)}
EXPECTED_CAP_QUESTION_IDS = {f"C{i:02d}{suffix}" for i in range(1, 8) for suffix in ("A", "B")}
ALLOWED_RESPONSES = {"YES", "NO", "CONDITIONAL", "UNKNOWN"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    contract = load_json(CONTRACT)
    questionnaire = load_json(QUESTIONNAIRE)

    contract_caps = {item["id"] for item in contract["required_capabilities"]}
    q_caps = {item["capability_id"] for item in questionnaire["capability_questions"]}
    assert q_caps == contract_caps, (q_caps, contract_caps)

    assert questionnaire["response_vocabulary"] == ["YES", "NO", "CONDITIONAL", "UNKNOWN"]
    assert set(questionnaire["configuration_fields_to_confirm"]) == set(contract["frozen_configuration_fields"])

    global_ids = {item["id"] for item in questionnaire["global_questions"]}
    assert global_ids == EXPECTED_GLOBAL
    assert all(item.get("required") is True for item in questionnaire["global_questions"])

    capability_question_ids = set()
    role_union = set()
    for item in questionnaire["capability_questions"]:
        ids = {q["id"] for q in item["questions"]}
        assert len(ids) == 2
        capability_question_ids |= ids
        role_union |= set(item["required_evidence_roles"])
        contract_item = next(x for x in contract["required_capabilities"] if x["id"] == item["capability_id"])
        assert set(item["required_evidence_roles"]) == set(contract_item["evidence_roles"])

    assert capability_question_ids == EXPECTED_CAP_QUESTION_IDS
    assert role_union <= set(contract["required_packet_roles"])

    semantics = questionnaire["decision_semantics"]
    assert set(semantics) == {"CONFIRMED", "CONDITIONAL", "UNAVAILABLE", "NEEDS_CONFIRMATION"}
    assert "UNKNOWN" in semantics["NEEDS_CONFIRMATION"]
    assert "NO" in semantics["UNAVAILABLE"]
    assert "identical questionnaire" in questionnaire["anti_bias_rule"].lower()

    with TEMPLATE.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    expected_ids = EXPECTED_GLOBAL | EXPECTED_CAP_QUESTION_IDS
    assert len(rows) == len(expected_ids) == 22
    assert {row["question_id"] for row in rows} == expected_ids
    assert len({row["question_id"] for row in rows}) == 22
    assert all(row["response"] in ALLOWED_RESPONSES for row in rows)
    assert all(row["response"] == "UNKNOWN" for row in rows), "Blank template must not pre-answer candidates"

    rows_by_id = {row["question_id"]: row for row in rows}
    for gid in EXPECTED_GLOBAL:
        assert rows_by_id[gid]["capability_id"] == "GLOBAL"

    qid_to_cap = {}
    for item in questionnaire["capability_questions"]:
        for q in item["questions"]:
            qid_to_cap[q["id"]] = item["capability_id"]
    for qid, cap in qid_to_cap.items():
        assert rows_by_id[qid]["capability_id"] == cap

    hierarchy_text = " -> ".join(contract["statistical_hierarchy"])
    assert hierarchy_text == "lot -> substrate -> device_or_pixel -> session -> sweep_or_step_replicate -> measurement"

    nonclaims = set(questionnaire["claim_boundary"]["does_not_establish"])
    assert "R2 device performance" in nonclaims
    assert "open-quantum transport mechanism" in nonclaims

    print("v3.29 facility confirmation protocol validation: PASS")
    print(f"capabilities={len(contract_caps)} global_questions={len(EXPECTED_GLOBAL)} capability_questions={len(EXPECTED_CAP_QUESTION_IDS)} rows={len(rows)}")


if __name__ == "__main__":
    main()
