#!/usr/bin/env python3
"""R2 v3.38 transfer-environment validator.

Standard-library only. This code validates provenance/completeness and evaluates only
engineering limits explicitly supplied in the JSON contract. It does not infer safe
shipping limits or device stability.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_NUMERIC = [
    "temperature_c", "temperature_u_c", "rh_percent", "rh_u_percent",
    "acceleration_g", "acceleration_u_g",
]
REQUIRED_TEXT = [
    "transfer_id", "arm", "substrate_id", "timestamp_utc", "logger_id",
    "logger_model", "logger_calibration_reference", "logger_calibration_date",
    "logger_timebase", "transfer_start_utc", "transfer_end_utc", "carrier_id",
    "package_id",
]


def parse_utc(text: str) -> datetime:
    dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError(f"timestamp lacks timezone: {text}")
    return dt.astimezone(timezone.utc)


def load_contract(path: Path) -> dict:
    data = json.loads(path.read_text())
    gap = data["planning_assumptions"]["max_allowed_sample_gap_s"]
    if not isinstance(gap, (int, float)) or gap <= 0:
        raise ValueError("max_allowed_sample_gap_s must be positive")
    return data


def load_rows(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    rows = [r for r in rows if any((v or "").strip() for v in r.values())]
    if not rows:
        raise ValueError("no data rows")
    return rows


def validate(rows: list[dict], contract: dict) -> dict:
    defects: list[str] = []
    parsed = []
    for idx, row in enumerate(rows, start=2):
        for key in REQUIRED_TEXT:
            if not (row.get(key) or "").strip():
                defects.append(f"row {idx}: missing {key}")
        nums = {}
        for key in REQUIRED_NUMERIC:
            try:
                nums[key] = float(row[key])
            except Exception:
                defects.append(f"row {idx}: invalid {key}")
                nums[key] = math.nan
        if all(math.isfinite(nums[k]) for k in REQUIRED_NUMERIC):
            if nums["temperature_u_c"] < 0 or nums["rh_u_percent"] < 0 or nums["acceleration_u_g"] < 0:
                defects.append(f"row {idx}: uncertainty must be non-negative")
        try:
            t = parse_utc(row["timestamp_utc"])
            start = parse_utc(row["transfer_start_utc"])
            end = parse_utc(row["transfer_end_utc"])
        except Exception as exc:
            defects.append(f"row {idx}: {exc}")
            continue
        parsed.append((t, start, end, row, nums))

    if not parsed:
        return {"log_status": "INCOMPLETE", "defects": defects, "limit_status": "LIMITS_UNKNOWN"}

    invariants = [
        "transfer_id", "arm", "substrate_id", "logger_id", "logger_model",
        "logger_calibration_reference", "logger_calibration_date", "logger_timebase",
        "transfer_start_utc", "transfer_end_utc", "carrier_id", "package_id",
    ]
    for key in invariants:
        vals = {(r.get(key) or "").strip() for _, _, _, r, _ in parsed}
        if len(vals) != 1:
            defects.append(f"inconsistent invariant field: {key}")

    parsed.sort(key=lambda x: x[0])
    times = [x[0] for x in parsed]
    start, end = parsed[0][1], parsed[0][2]
    if end <= start:
        defects.append("transfer_end_utc must be after transfer_start_utc")
    if times[0] > start:
        defects.append("first sample occurs after declared transfer start")
    if times[-1] < end:
        defects.append("last sample occurs before declared transfer end")

    gaps = [(b - a).total_seconds() for a, b in zip(times, times[1:])]
    max_gap = max(gaps, default=0.0)
    gap_limit = float(contract["planning_assumptions"]["max_allowed_sample_gap_s"])
    if max_gap > gap_limit:
        defects.append(f"max sample gap {max_gap:.6g}s exceeds {gap_limit:.6g}s")

    # Independent completeness cross-check: every adjacent sample interval must be <= gap limit.
    interval_flags = [g <= gap_limit for g in gaps]
    complete_by_all = all(interval_flags)
    complete_by_max = max_gap <= gap_limit
    if complete_by_all != complete_by_max:
        defects.append("internal completeness cross-check disagreement")

    valid_num = [x for x in parsed if all(math.isfinite(x[4][k]) for k in REQUIRED_NUMERIC)]
    metrics = {}
    if valid_num:
        metrics = {
            "temperature_observed_min_c": min(x[4]["temperature_c"] for x in valid_num),
            "temperature_observed_max_c": max(x[4]["temperature_c"] for x in valid_num),
            "temperature_conservative_min_c": min(x[4]["temperature_c"] - x[4]["temperature_u_c"] for x in valid_num),
            "temperature_conservative_max_c": max(x[4]["temperature_c"] + x[4]["temperature_u_c"] for x in valid_num),
            "rh_observed_max_percent": max(x[4]["rh_percent"] for x in valid_num),
            "rh_conservative_max_percent": max(x[4]["rh_percent"] + x[4]["rh_u_percent"] for x in valid_num),
            "acceleration_observed_max_g": max(x[4]["acceleration_g"] for x in valid_num),
            "acceleration_conservative_max_g": max(x[4]["acceleration_g"] + x[4]["acceleration_u_g"] for x in valid_num),
            "max_sample_gap_s": max_gap,
            "sample_count": len(valid_num),
        }

    limits = contract["optional_engineering_limits"]
    checks = []
    if metrics:
        mapping = [
            ("temperature_lower_c", metrics["temperature_conservative_min_c"], lambda x, lim: x >= lim),
            ("temperature_upper_c", metrics["temperature_conservative_max_c"], lambda x, lim: x <= lim),
            ("rh_upper_percent", metrics["rh_conservative_max_percent"], lambda x, lim: x <= lim),
            ("acceleration_upper_g", metrics["acceleration_conservative_max_g"], lambda x, lim: x <= lim),
        ]
        for name, value, fn in mapping:
            lim = limits.get(name)
            if lim is not None:
                checks.append((name, fn(value, float(lim)), value, float(lim)))
    if not checks or any(limits.get(k) is None for k in ["temperature_lower_c", "temperature_upper_c", "rh_upper_percent", "acceleration_upper_g"]):
        limit_status = "LIMITS_UNKNOWN"
    elif all(ok for _, ok, _, _ in checks):
        limit_status = "WITHIN_DECLARED_LIMITS"
    else:
        limit_status = "EXCEEDS_DECLARED_LIMIT"

    return {
        "log_status": "LOG_COMPLETE" if not defects else "INCOMPLETE",
        "limit_status": limit_status,
        "defects": defects,
        "metrics": metrics,
        "limit_checks": [
            {"limit": n, "pass": ok, "conservative_value": v, "declared_limit": lim}
            for n, ok, v, lim in checks
        ],
    }


def self_test() -> None:
    contract = {
        "planning_assumptions": {"max_allowed_sample_gap_s": 900},
        "optional_engineering_limits": {
            "temperature_lower_c": 0.0, "temperature_upper_c": 40.0,
            "rh_upper_percent": 80.0, "acceleration_upper_g": 5.0,
        },
    }
    base = {
        "transfer_id": "T1", "arm": "TRAVEL", "substrate_id": "S1",
        "logger_id": "L1", "logger_model": "synthetic", "logger_calibration_reference": "synthetic",
        "logger_calibration_date": "2026-08-27", "logger_timebase": "UTC",
        "transfer_start_utc": "2026-08-27T00:00:00Z", "transfer_end_utc": "2026-08-27T00:30:00Z",
        "carrier_id": "C1", "package_id": "P1",
    }
    rows = []
    for minute in range(0, 31, 5):
        r = dict(base)
        r.update({
            "timestamp_utc": f"2026-08-27T00:{minute:02d}:00Z",
            "temperature_c": "25", "temperature_u_c": "0.5",
            "rh_percent": "40", "rh_u_percent": "2",
            "acceleration_g": "1", "acceleration_u_g": "0.1",
        })
        rows.append(r)
    out = validate(rows, contract)
    assert out["log_status"] == "LOG_COMPLETE"
    assert out["limit_status"] == "WITHIN_DECLARED_LIMITS"
    assert out["metrics"]["sample_count"] == 7
    assert out["metrics"]["max_sample_gap_s"] == 300
    assert out["metrics"]["temperature_conservative_max_c"] == 25.5
    # Known limiting case: a 20-minute gap must fail the 15-minute completeness screen.
    bad = [rows[0], rows[1], rows[-1]]
    bad_out = validate(bad, contract)
    assert bad_out["log_status"] == "INCOMPLETE"
    # Uncertainty must tighten, not relax, an upper-limit decision.
    edge = [dict(r) for r in rows]
    edge[3]["temperature_c"] = "39.8"
    edge[3]["temperature_u_c"] = "0.5"
    edge_out = validate(edge, contract)
    assert edge_out["limit_status"] == "EXCEEDS_DECLARED_LIMIT"
    # Null limits can never produce a safety/material-compatibility pass.
    no_limits = json.loads(json.dumps(contract))
    for k in no_limits["optional_engineering_limits"]:
        no_limits["optional_engineering_limits"][k] = None
    assert validate(rows, no_limits)["limit_status"] == "LIMITS_UNKNOWN"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract", type=Path)
    ap.add_argument("--csv", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        self_test()
        print("v3.38 self-test PASS")
        return 0
    if not args.contract or not args.csv:
        ap.error("--contract and --csv are required unless --self-test is used")
    out = validate(load_rows(args.csv), load_contract(args.contract))
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out["log_status"] == "LOG_COMPLETE" else 2


if __name__ == "__main__":
    sys.exit(main())
