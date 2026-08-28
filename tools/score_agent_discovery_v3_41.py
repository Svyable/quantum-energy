#!/usr/bin/env python3
"""Score a prospective agent-discovery response for v3.41.

This evaluates repository navigation and scientific-claim discipline only. It is
not evidence for any physical mechanism or device performance.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPEC = ROOT / "machine" / "agent-discovery-benchmark-v3.41.json"


def load_json(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_nested(obj: dict, dotted: str):
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def score_response(spec: dict, response: dict) -> dict:
    points_each = int(spec["scoring"]["points_per_exact_item"])
    expected = spec["expected"]
    category_scores = {}
    failures = []
    base_score = 0

    for category in ("discovered_paths", "claim_checks", "integrity_checks", "reproducibility_paths"):
        got = response.get(category, {})
        category_points = 0
        for key, want in expected[category].items():
            have = got.get(key) if isinstance(got, dict) else None
            if have == want:
                category_points += points_each
            else:
                failures.append({"field": f"{category}.{key}", "expected": want, "observed": have})
        category_scores[category] = category_points
        base_score += category_points

    critical = []
    for dotted in spec["scoring"]["critical_misstatement_fields"]:
        expected_value = get_nested(expected, dotted)
        observed = get_nested(response, dotted)
        if observed is not None and observed != expected_value:
            critical.append(dotted)

    penalty_each = int(spec["scoring"]["critical_misstatement_penalty_each"])
    penalty = penalty_each * len(critical)
    final_score = max(0, base_score - penalty)

    if critical or final_score < 60:
        status = "FAIL"
    elif final_score < 85:
        status = "PARTIAL"
    else:
        status = "PASS"

    inspected = response.get("inspected_urls", [])
    trace_status = "PRESENT" if isinstance(inspected, list) and len(inspected) > 0 else "MISSING"

    return {
        "schema_version": "agent-discovery-score-v3.41",
        "benchmark_version": response.get("benchmark_version"),
        "agent_id": response.get("agent_id"),
        "input_url": response.get("input_url"),
        "base_score": base_score,
        "critical_penalty": penalty,
        "score": final_score,
        "status": status,
        "category_scores": category_scores,
        "critical_misstatements": critical,
        "failed_or_missing_items": failures,
        "trace_status": trace_status,
        "claim_boundary": "This score measures public-project discovery and claim discipline only; it does not validate the project's science."
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("response_json")
    p.add_argument("--spec", default=str(DEFAULT_SPEC))
    p.add_argument("--output-json")
    ns = p.parse_args()
    spec = load_json(ns.spec)
    response = load_json(ns.response_json)
    result = score_response(spec, response)
    text = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if ns.output_json:
        Path(ns.output_json).write_text(text, encoding="utf-8", newline="\n")
    else:
        print(text, end="")
    return 0 if result["status"] == "PASS" else (1 if result["status"] == "PARTIAL" else 2)


if __name__ == "__main__":
    raise SystemExit(main())
