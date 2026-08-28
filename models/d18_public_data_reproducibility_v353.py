#!/usr/bin/env python3
"""Fail-closed audit for v3.53 public raw-data reproducibility boundary."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
P = HERE / "machine" / "d18-public-data-reproducibility-v3.53.json"


def evaluate(d):
    obs = d["decision_rule"]["observed_publicly_in_this_run"]
    required = [
        obs["public_raw_or_minimally_processed_data"],
        obs["device_or_sample_identity_in_machine_readable_raw_data"],
        obs["processing_path_from_raw_to_decision_metric"],
    ]
    return all(required)


def main():
    d = json.loads(P.read_text())
    assert d["primary_source"]["article_doi"] == "10.1038/s41467-026-68731-7"
    assert d["primary_source"]["supplementary_information_size_mb_reported_by_pmc"] == 34.3
    assert d["primary_source"]["additional_data_access"] == "corresponding_author_on_request"
    assert evaluate(d) is False
    # Negative/control: one missing prerequisite must remain fail-closed.
    c = json.loads(json.dumps(d))
    c["decision_rule"]["observed_publicly_in_this_run"]["public_raw_or_minimally_processed_data"] = True
    assert evaluate(c) is False
    # Limiting positive fixture: all reproduction prerequisites present -> eligible.
    for k in ("public_raw_or_minimally_processed_data", "device_or_sample_identity_in_machine_readable_raw_data", "processing_path_from_raw_to_decision_metric"):
        c["decision_rule"]["observed_publicly_in_this_run"][k] = True
    assert evaluate(c) is True
    print("D18_PUBLIC_DATA_REPRODUCIBILITY_V3.53: PASS")
    print(d["decision_rule"]["status"])

if __name__ == "__main__":
    main()
