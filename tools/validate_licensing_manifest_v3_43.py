#!/usr/bin/env python3
import json
from pathlib import Path

MANIFEST = Path("machine/licensing-manifest-v3.43.json")
REQUIRED_CLASSES = {
    "software": "Apache-2.0",
    "documentation_and_research_text": "CC-BY-4.0",
    "structured_data": "CC-BY-4.0",
    "hardware_and_cad": "CERN-OHL-W-2.0",
}
REQUIRED_GATES = {
    "license_files_committed",
    "per_file_or_directory_notices_committed",
    "third_party_inventory_reviewed",
    "contributor_rights_process_reviewed",
    "human_approval_recorded",
    "formal_release_allowed",
}


def main() -> None:
    data = json.loads(MANIFEST.read_text())
    assert data["status"] == "PROPOSED_FOR_HUMAN_REVIEW"
    assert data["effective_date"] is None

    classes = {item["class"]: item for item in data["artifact_classes"]}
    assert set(classes) == set(REQUIRED_CLASSES)
    for name, expected in REQUIRED_CLASSES.items():
        item = classes[name]
        assert item["recommended_license"] == expected
        assert item["status"] == "PENDING_HUMAN_APPROVAL"
        assert item["paths"], f"{name} must have at least one path pattern"

    gate = data["release_gate"]
    assert set(gate) == REQUIRED_GATES
    assert all(value is False for value in gate.values())
    assert gate["formal_release_allowed"] is False

    exceptions = "\n".join(data["exceptions"]).lower()
    assert "third-party" in exceptions
    assert "not licensed" in exceptions

    assert len(data["source_provenance"]) >= 3
    print("v3.43 licensing manifest validation: PASS")
    print(f"artifact classes checked: {len(classes)}")
    print(f"release gates checked: {len(gate)}")


if __name__ == "__main__":
    main()
