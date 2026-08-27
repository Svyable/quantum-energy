#!/usr/bin/env python3
"""Validate machine/analysis-registry.json using only the Python standard library."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "machine" / "analysis-registry.json"
PROJECT_INDEX = ROOT / "machine" / "project-index.json"

EXPECTED_ID = "r2_calibration_covariance_v3_19"
EXPECTED_PR = 6
EXPECTED_MERGE = "4d315b65b8cb131b3a62eb352cb0cee6ff77ebcf"
EXPECTED_CANONICAL = {
    "models/r2_calibration_component_estimator_v3_19.py",
    "models/r2_calibration_component_test_v3_19.py",
    "models/fixtures/r2_calibration_repeats_template_v3_19.csv",
    "technical/r2-calibration-components-v3.19.md",
    "research/evidence/r2-calibration-components-v3.19.md",
    "research/sessions/2026-08-26-r2-calibration-components-v3.19.md",
    ".github/workflows/r2-calibration-components.yml",
}
EXPECTED_SUPERSEDED = {
    "models/r2_calibration_components_v3_19.py",
    "models/r2_calibration_components_synthetic_v3_19.py",
    "technical/r2-calibration-component-estimator-v3.19.md",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("schema_version") != "quantum-energy-analysis-registry-v1":
        fail("unexpected schema version")
    if data.get("canonical_branch") != "main":
        fail("canonical branch must be main")

    analyses = data.get("analyses", [])
    if len(analyses) != 1:
        fail("v1 registry must contain exactly one reconciled analysis")
    item = analyses[0]
    if item.get("analysis_id") != EXPECTED_ID:
        fail("unexpected analysis id")
    if item.get("status") != "CANONICAL_MERGED":
        fail("canonical analysis must be marked CANONICAL_MERGED")
    if item.get("source_pull_request") != EXPECTED_PR:
        fail("source PR does not match merged implementation")
    if item.get("merge_commit") != EXPECTED_MERGE:
        fail("merge commit does not match merged PR #6")

    canonical = set(item.get("canonical_files", []))
    if canonical != EXPECTED_CANONICAL:
        fail(f"canonical file set mismatch: {canonical ^ EXPECTED_CANONICAL}")
    missing = sorted(path for path in canonical if not (ROOT / path).is_file())
    if missing:
        fail(f"canonical files missing from branch: {missing}")

    candidates = item.get("superseded_review_candidates", [])
    if len(candidates) != 1 or candidates[0].get("pull_request") != 7:
        fail("PR #7 must remain explicit superseded-review provenance")
    if candidates[0].get("status_as_of_2026_08_27") != "OPEN_NONMERGEABLE":
        fail("PR #7 status provenance changed without registry review")
    superseded = set(candidates[0].get("distinct_paths_not_canonical", []))
    if superseded != EXPECTED_SUPERSEDED:
        fail("superseded distinct-path set mismatch")
    accidentally_present = sorted(path for path in superseded if (ROOT / path).exists())
    if accidentally_present:
        fail(f"superseded alternate paths unexpectedly present on canonical branch: {accidentally_present}")

    if not item.get("claim_boundary"):
        fail("claim boundary is required")
    if len(item.get("unresolved_model_risks", [])) < 1:
        fail("unresolved risks must remain visible")

    project = json.loads(PROJECT_INDEX.read_text(encoding="utf-8"))
    entrypoints = {x.get("path") for x in project.get("agent_entrypoints", [])}
    if "machine/analysis-registry.json" not in entrypoints:
        fail("project index must expose the analysis registry to agents")

    print("PASS: canonical analysis registry is internally consistent")
    print(f"canonical_files={len(canonical)} superseded_distinct_paths={len(superseded)}")


if __name__ == "__main__":
    main()
