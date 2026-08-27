#!/usr/bin/env python3
"""Validate the v3.27 R2 facility capability contract.

Standard-library only. This validator checks structural completeness, dependency
acyclicity, status semantics, and preservation of claim/statistical-integrity
boundaries. It does not certify a facility or evaluate measurement quality.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Set

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "technical" / "data" / "r2_facility_capability_contract_v3_27.json"

REQUIRED_STATUS = {"PASS", "FAIL", "INCOMPLETE"}
REQUIRED_HIERARCHY = [
    "lot",
    "substrate",
    "device_or_pixel",
    "session",
    "sweep_or_step_replicate",
    "measurement",
]
REQUIRED_CAPABILITIES = {
    "reference_detector_traceability",
    "spectral_characterization",
    "linearity_characterization",
    "repeatability_campaign",
    "electrical_step_characterization",
    "optical_step_characterization",
    "voc_intensity_acquisition",
}


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def assert_acyclic(graph: Dict[str, List[str]]) -> None:
    visiting: Set[str] = set()
    visited: Set[str] = set()

    def visit(node: str) -> None:
        if node in visited:
            return
        if node in visiting:
            fail(f"dependency cycle detected at {node}")
        visiting.add(node)
        for dep in graph.get(node, []):
            visit(dep)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)


def main() -> None:
    if not CONTRACT.exists():
        fail(f"missing contract: {CONTRACT.relative_to(ROOT)}")

    data = json.loads(CONTRACT.read_text(encoding="utf-8"))

    if data.get("schema_version") != "3.27":
        fail("schema_version must be 3.27")

    capabilities = data.get("required_capabilities")
    if not isinstance(capabilities, list):
        fail("required_capabilities must be a list")

    ids = {item.get("id") for item in capabilities if isinstance(item, dict)}
    missing_caps = REQUIRED_CAPABILITIES - ids
    if missing_caps:
        fail(f"missing capabilities: {sorted(missing_caps)}")

    roles = data.get("required_packet_roles")
    if not isinstance(roles, list) or len(roles) != len(set(roles)):
        fail("required_packet_roles must be a unique list")

    for cap in capabilities:
        for role in cap.get("evidence_roles", []):
            if role not in roles:
                fail(f"capability {cap.get('id')} references undeclared role {role}")

    statuses = data.get("status_semantics", {})
    if set(statuses) != REQUIRED_STATUS:
        fail(f"status semantics must be exactly {sorted(REQUIRED_STATUS)}")
    if "may not be represented as zero uncertainty or PASS" not in statuses["INCOMPLETE"]:
        fail("INCOMPLETE semantics must prohibit implicit zero uncertainty/PASS")
    if "must remain visible" not in statuses["FAIL"]:
        fail("FAIL semantics must preserve negative results")

    hierarchy = data.get("statistical_hierarchy")
    if hierarchy != REQUIRED_HIERARCHY:
        fail("statistical hierarchy changed or collapsed")

    graph = data.get("gate_dependencies")
    if not isinstance(graph, dict):
        fail("gate_dependencies must be an object")
    assert_acyclic(graph)

    order = data.get("execution_order")
    if not isinstance(order, list) or len(order) != len(set(order)):
        fail("execution_order must be a unique list")
    positions = {name: i for i, name in enumerate(order)}
    for gate, deps in graph.items():
        if gate not in positions:
            fail(f"dependency gate {gate} missing from execution_order")
        for dep in deps:
            if dep not in positions:
                fail(f"dependency {dep} missing from execution_order")
            if positions[dep] >= positions[gate]:
                fail(f"dependency order invalid: {dep} must precede {gate}")

    boundary = data.get("claim_boundary", {})
    nonclaims = set(boundary.get("does_not_establish", []))
    required_nonclaims = {
        "R2 device performance",
        "electron-phonon coupling mechanism",
        "open-quantum transport mechanism",
        "commercial photovoltaic performance",
    }
    if not required_nonclaims.issubset(nonclaims):
        fail("claim boundary lost one or more mandatory non-claims")

    integrity = data.get("data_integrity", {})
    if integrity.get("manifest_hash") != "SHA-256":
        fail("manifest_hash must be SHA-256")
    for key in (
        "raw_processed_separation_required",
        "immutable_source_files_required",
        "excluded_rows_retained_with_reason",
    ):
        if integrity.get(key) is not True:
            fail(f"{key} must remain true")

    print("PASS: v3.27 facility capability contract is structurally consistent")


if __name__ == "__main__":
    main()
