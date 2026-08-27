#!/usr/bin/env python3
"""Validate the v3.28 prospective facility capability audit using stdlib only."""
from __future__ import annotations
import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "research/data/r2_candidate_facility_audit_v3_28.csv"
FACILITIES = {"NREL PVDPC", "Fraunhofer ISE CalLab PV Cells", "IPVF"}
CAPABILITIES = {
    "reference_detector_traceability", "spectral_characterization",
    "linearity_characterization", "repeatability_campaign",
    "electrical_step_characterization", "optical_step_characterization",
    "voc_intensity_acquisition",
}
STATUSES = {"PUBLICLY_SUPPORTED", "PARTIAL_PUBLIC_SUPPORT", "NEEDS_CONFIRMATION"}
EXPECTED = {
    "NREL PVDPC": Counter(PUBLICLY_SUPPORTED=3, PARTIAL_PUBLIC_SUPPORT=1, NEEDS_CONFIRMATION=3),
    "Fraunhofer ISE CalLab PV Cells": Counter(PUBLICLY_SUPPORTED=2, PARTIAL_PUBLIC_SUPPORT=1, NEEDS_CONFIRMATION=4),
    "IPVF": Counter(PUBLICLY_SUPPORTED=1, PARTIAL_PUBLIC_SUPPORT=2, NEEDS_CONFIRMATION=4),
}

def main() -> None:
    with CSV.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 21, f"expected 21 rows, got {len(rows)}"
    assert {r["facility"] for r in rows} == FACILITIES
    seen = set()
    counts = defaultdict(Counter)
    for r in rows:
        key = (r["facility"], r["capability"])
        assert key not in seen, f"duplicate {key}"
        seen.add(key)
        assert r["capability"] in CAPABILITIES, r["capability"]
        assert r["status"] in STATUSES, r["status"]
        assert r["public_evidence_date"] == "2026-08-27"
        assert r["evidence_url"].startswith("https://")
        assert r["evidence_summary"].strip()
        assert r["critical_unknown"].strip()
        counts[r["facility"]][r["status"]] += 1
    for facility in FACILITIES:
        actual_caps = {r["capability"] for r in rows if r["facility"] == facility}
        assert actual_caps == CAPABILITIES, (facility, actual_caps ^ CAPABILITIES)
        assert counts[facility] == EXPECTED[facility], (facility, counts[facility])
        assert sum(counts[facility].values()) == 7
    assert sum(sum(c.values()) for c in counts.values()) == 21
    # Negative-result preservation: nobody is allowed to appear execution-ready from public evidence alone.
    assert all(counts[f]["NEEDS_CONFIRMATION"] > 0 for f in FACILITIES)
    print("v3.28 facility audit validation: PASS")
    for f in sorted(FACILITIES):
        print(f, dict(counts[f]))

if __name__ == "__main__":
    main()
