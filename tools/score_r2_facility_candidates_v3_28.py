#!/usr/bin/env python3
"""Validate and summarize the prospective R2 facility capability audit v3.28.

Standard-library only. This script scores *publicly evidenced coverage*, not real facility
competence. NEEDS_CONFIRMATION is deliberately not promoted to KNOWN_AVAILABLE.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "technical/data/r2_facility_candidate_matrix_v3_28.csv"
CONTRACT = ROOT / "technical/data/r2_facility_capability_contract_v3_27.json"
OUTPUT = ROOT / "technical/data/r2_facility_candidate_summary_v3_28.json"

ALLOWED = {"KNOWN_AVAILABLE", "NEEDS_CONFIRMATION", "UNAVAILABLE"}


def load_rows():
    with MATRIX.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    required = [x["id"] for x in contract["required_capabilities"]]
    rows = load_rows()
    assert rows, "candidate matrix is empty"

    by_candidate = defaultdict(dict)
    for row in rows:
        cid = row["candidate_id"]
        cap = row["capability_id"]
        status = row["status"]
        assert status in ALLOWED, (cid, cap, status)
        assert cap in required, (cid, cap)
        assert row["evidence_url"].startswith("https://"), (cid, cap)
        assert row["evidence_checked_date"] == "2026-08-27", (cid, cap)
        assert cap not in by_candidate[cid], (cid, cap, "duplicate")
        by_candidate[cid][cap] = row

    assert len(by_candidate) >= 3, "prospective audit requires >=3 candidates"
    for cid, caps in by_candidate.items():
        assert set(caps) == set(required), (cid, sorted(set(required) - set(caps)))

    candidates = {}
    union_known = set()
    for cid, caps in sorted(by_candidate.items()):
        counts = Counter(row["status"] for row in caps.values())
        known = sorted(cap for cap, row in caps.items() if row["status"] == "KNOWN_AVAILABLE")
        union_known.update(known)
        candidates[cid] = {
            "known_available": counts["KNOWN_AVAILABLE"],
            "needs_confirmation": counts["NEEDS_CONFIRMATION"],
            "unavailable": counts["UNAVAILABLE"],
            "publicly_evidenced_fraction": counts["KNOWN_AVAILABLE"] / len(required),
            "known_capabilities": known,
        }

    summary = {
        "schema_version": "3.28",
        "classification": "prospective_public_evidence_audit",
        "evidence_checked_date": "2026-08-27",
        "required_capability_count": len(required),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "union_known_capabilities": sorted(union_known),
        "union_known_count": len(union_known),
        "complete_candidate_publicly_confirmed": any(
            x["known_available"] == len(required) for x in candidates.values()
        ),
        "claim_boundary": (
            "Counts describe only capabilities explicitly supported by reviewed public sources; "
            "they do not certify service availability, configuration compatibility, measurement "
            "uncertainty, scheduling, cost, or a facility's willingness to execute the R2 protocol."
        ),
    }

    expected = json.loads(OUTPUT.read_text(encoding="utf-8"))
    assert summary == expected, "frozen summary does not match recomputation"

    # Adversarial semantic checks.
    assert not summary["complete_candidate_publicly_confirmed"]
    assert all(x["needs_confirmation"] > 0 for x in candidates.values())
    assert summary["union_known_count"] < len(required)

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
