#!/usr/bin/env python3
"""Validate the v3.42 R2 transfer contact-state/ESD control contract.

Standard library only. Synthetic fixture values are software tests, not device data.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

REQUIRED_COLUMNS = {
    "lot_id", "substrate_id", "device_pixel_id", "session_id", "phase",
    "measurement_id", "timestamp_utc", "voltage_v", "current_a", "u_current_a",
    "rho_pre_post", "temperature_k", "fixture_id", "instrument_id", "config_hash",
    "raw_data_path", "sentinel_id", "sentinel_state", "visual_qc", "electrical_qc",
    "exclusion_flag", "exclusion_rule_id", "notes"
}


def u_difference(u_pre: float, u_post: float, rho: float) -> float:
    """Standard uncertainty of POST-PRE, including correlation."""
    value = u_pre * u_pre + u_post * u_post - 2.0 * rho * u_pre * u_post
    if value < -1e-30:
        raise ValueError("negative variance from invalid uncertainty/correlation inputs")
    return math.sqrt(max(0.0, value))


def metrics(i_pre, i_post, u_pre, u_post, rho):
    if not (len(i_pre) == len(i_post) == len(u_pre) == len(u_post)) or not i_pre:
        raise ValueError("paired non-empty arrays required")
    deltas = [post - pre for pre, post in zip(i_pre, i_post)]
    uncertainties = [u_difference(a, b, rho) for a, b in zip(u_pre, u_post)]
    if any(u <= 0 for u in uncertainties):
        raise ValueError("positive difference uncertainty required for standardized shift")
    rms = math.sqrt(sum(d * d for d in deltas) / len(deltas))
    max_z = max(abs(d) / u for d, u in zip(deltas, uncertainties))
    return rms, max_z


def validate_contract(contract: dict) -> None:
    if contract.get("schema_version") != "3.42":
        raise ValueError("schema_version must be 3.42")
    paired = contract["paired_metrics"]
    if paired.get("rho_unknown_default") != -1.0:
        raise ValueError("unknown correlation must default conservatively to rho=-1")
    if paired.get("max_standardized_shift_limit") is not None:
        raise ValueError("v3.42 must not invent a standardized-shift acceptance limit")
    if paired.get("rms_current_shift_limit_a") is not None:
        raise ValueError("v3.42 must not invent an RMS-current acceptance limit")
    dark = contract["dark_iv"]
    for field in ("voltage_grid_v", "current_compliance_a", "settling_time_s", "integration_setting", "temperature_k"):
        if dark.get(field) is not None:
            raise ValueError(f"{field} must remain null until prospectively qualified")
    if contract["esd_sentinel"].get("acceptance_threshold") is not None:
        raise ValueError("ESD-sentinel acceptance threshold must remain null without provenance")


def validate_csv_schema(path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
    missing = REQUIRED_COLUMNS - fields
    if missing:
        raise ValueError(f"CSV missing required columns: {sorted(missing)}")


def self_test(contract: dict) -> None:
    fixture = contract["synthetic_software_fixture"]
    rms, max_z = metrics(
        fixture["i_pre_a"], fixture["i_post_a"], fixture["u_pre_a"],
        fixture["u_post_a"], fixture["rho"]
    )
    tol = float(fixture["numerical_tolerance"])
    exp_rms = float(fixture["expected_rms_current_shift_a"])
    exp_max_z = float(fixture["expected_max_standardized_shift"])
    # Scale-aware tolerance for the ampere-valued metric; absolute for dimensionless z.
    if abs(rms - exp_rms) > tol * max(1.0, abs(exp_rms)):
        raise AssertionError((rms, exp_rms))
    if abs(max_z - exp_max_z) > tol:
        raise AssertionError((max_z, exp_max_z))

    # Independent limiting cases.
    # rho=-1 => u_delta = u_pre + u_post exactly for positive standard uncertainties.
    a, b = 0.4e-9, 0.7e-9
    if abs(u_difference(a, b, -1.0) - (a + b)) > 1e-24:
        raise AssertionError("rho=-1 conservative limiting case failed")
    # rho=+1 and equal terms => shared systematic cancels in a difference.
    if u_difference(2e-9, 2e-9, 1.0) != 0.0:
        raise AssertionError("rho=+1 equal-systematic limiting case failed")
    # No state change must produce exactly zero RMS shift.
    rms0, z0 = metrics([1.0, 2.0], [1.0, 2.0], [0.1, 0.1], [0.1, 0.1], 0.0)
    if rms0 != 0.0 or z0 != 0.0:
        raise AssertionError("zero-change limiting case failed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", default="machine/r2-contact-esd-control-v3.42.json")
    parser.add_argument("--csv", default="technical/data/r2_contact_esd_control_template_v3.42.csv")
    args = parser.parse_args()
    contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))
    validate_contract(contract)
    validate_csv_schema(Path(args.csv))
    self_test(contract)
    print("v3.42 contact-state/ESD contract: PASS (software/schema checks only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
