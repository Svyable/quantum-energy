#!/usr/bin/env python3
"""Validate the v3.33 R2 dependency-aware gate/abort policy.

Standard-library only. No physical performance calculation is performed.
"""
from __future__ import annotations
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "technical/data/r2_gate_abort_policy_v3_33.json"
SOURCE = ROOT / "technical/data/r2_facility_capability_contract_v3_27.json"
STATUSES = ("PASS", "FAIL", "INCOMPLETE")


def load(path: Path):
    return json.loads(path.read_text())


def topo_sort(gates):
    deps = {g["id"]: set(g["depends_on"]) for g in gates}
    known = set(deps)
    for gid, ds in deps.items():
        unknown = ds - known
        if unknown:
            raise AssertionError(f"unknown dependencies for {gid}: {sorted(unknown)}")
    out = []
    while deps:
        ready = sorted(k for k, v in deps.items() if not v)
        if not ready:
            raise AssertionError("dependency cycle detected")
        out.extend(ready)
        for r in ready:
            deps.pop(r)
        for v in deps.values():
            v.difference_update(ready)
    return out


def runnable(gate_id, status, gate_map):
    return all(status.get(dep) == "PASS" for dep in gate_map[gate_id]["depends_on"])


def main():
    policy = load(POLICY)
    source = load(SOURCE)
    gates = policy["gates"]
    gate_map = {g["id"]: g for g in gates}
    assert len(gate_map) == len(gates) == 10
    assert policy["source_contract"] == "technical/data/r2_facility_capability_contract_v3_27.json"
    assert source["status_semantics"].keys() >= {"PASS", "FAIL", "INCOMPLETE"}

    # Exact dependency agreement for every dependency-controlled v3.27 gate.
    for gid, deps in source["gate_dependencies"].items():
        assert gid in gate_map, gid
        assert set(gate_map[gid]["depends_on"]) == set(deps), (gid, deps, gate_map[gid]["depends_on"])

    # v3.27 execution_order includes these two prerequisite stages but does not list
    # them as gate_dependency keys. v3.33 makes them explicit graph nodes.
    assert gate_map["packet_preflight"]["depends_on"] == []
    assert gate_map["reference_repeatability_freeze"]["depends_on"] == ["reference_repeatability_training"]
    assert "reference_repeatability_freeze" in source["execution_order"]

    topo = topo_sort(gates)
    assert topo.index("packet_preflight") < topo.index("instrument_temporal_fidelity")
    assert topo.index("instrument_temporal_fidelity") < topo.index("optical_dut_settling")
    assert topo.index("reference_repeatability_training") < topo.index("reference_repeatability_freeze")
    assert topo.index("reference_repeatability_freeze") < topo.index("reference_repeatability_holdout")
    assert topo.index("voc_intensity_monotonic") < topo.index("voc_intensity_randomized_order")
    assert topo[-1] == "combined_uncertainty_propagation"

    # Exhaustive local truth table: runnable iff every prerequisite is PASS.
    cases = 0
    for gid, gate in gate_map.items():
        deps = gate["depends_on"]
        if not deps:
            continue
        for values in itertools.product(STATUSES, repeat=len(deps)):
            status = dict(zip(deps, values))
            expected = all(v == "PASS" for v in values)
            assert runnable(gid, status, gate_map) == expected
            cases += 1
    assert cases == 81

    # Adversarial independent-branch checks.
    status = {"packet_preflight":"PASS","instrument_temporal_fidelity":"PASS","optical_dut_settling":"FAIL"}
    assert runnable("spectral_shape_gate", status, gate_map)
    assert runnable("reference_repeatability_training", status, gate_map)
    assert not runnable("voc_intensity_monotonic", status, gate_map)

    status = {"packet_preflight":"PASS","spectral_shape_gate":"FAIL"}
    assert runnable("instrument_temporal_fidelity", status, gate_map)
    assert runnable("reference_repeatability_training", status, gate_map)
    assert not runnable("voc_intensity_monotonic", status, gate_map)

    # Prospective holdout cannot run unless both training and freeze pass.
    status = {"reference_repeatability_training":"PASS","reference_repeatability_freeze":"INCOMPLETE"}
    assert not runnable("reference_repeatability_holdout", status, gate_map)

    # Complete uncertainty cannot run after failed prospective holdout.
    status = {"reference_repeatability_holdout":"FAIL","spectral_shape_gate":"PASS","voc_intensity_randomized_order":"PASS"}
    assert not runnable("combined_uncertainty_propagation", status, gate_map)

    assert all(g["salvage_on_fail"] for g in gates)
    assert "BLOCKED" in policy["status_semantics"]
    assert "open-quantum transport mechanism" in policy["claim_boundary"]["does_not_establish"]

    print(json.dumps({
        "schema_version": policy["schema_version"],
        "gate_count": len(gates),
        "dependency_truth_table_cases_checked": cases,
        "topological_order": topo,
        "status": "PASS"
    }, indent=2))

if __name__ == "__main__":
    main()
