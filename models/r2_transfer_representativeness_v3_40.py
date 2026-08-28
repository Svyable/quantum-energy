#!/usr/bin/env python3
"""R2 v3.40 transfer-sensor representativeness validator.

Standard-library only. Synthetic fixtures are software tests, not measurements.
"""
from __future__ import annotations

import csv
import math
import sys
from collections import defaultdict

PASS = "QUALIFIED_FOR_DECLARED_REPRESENTATIVENESS"
INCOMPLETE = "INCOMPLETE"
FAIL = "FAIL_REPRESENTATIVENESS"
REQUIRED_CHANNELS = {"temperature_C", "relative_humidity_percent"}
REQUIRED_DIRECTIONS = {"UP", "DOWN"}
MIN_RUNS = 3


def difference_uncertainty(u_ref: float, u_logger: float, rho: float) -> float:
    if u_ref < 0 or u_logger < 0 or not -1.0 <= rho <= 1.0:
        raise ValueError("uncertainties must be nonnegative and rho in [-1,1]")
    var = u_ref * u_ref + u_logger * u_logger - 2.0 * rho * u_ref * u_logger
    if var < -1e-15:
        raise ValueError("negative variance")
    return math.sqrt(max(0.0, var))


def conservative_error(abs_difference: float, u_ref: float, u_logger: float, rho: float | None) -> float:
    if abs_difference < 0:
        raise ValueError("absolute difference must be nonnegative")
    gate_rho = -1.0 if rho is None else rho
    return abs_difference + difference_uncertainty(u_ref, u_logger, gate_rho)


def synthetic_self_test() -> None:
    tol = 1e-12
    # Independent algebraic limiting case: rho=-1 => u_diff = u_ref + u_logger.
    u = difference_uncertainty(0.1, 0.1, -1.0)
    assert abs(u - 0.2) <= tol
    assert abs(conservative_error(0.6, 0.1, 0.1, None) - 0.8) <= tol
    assert abs(conservative_error(0.9, 0.1, 0.1, None) - 1.1) <= tol
    # Correlation sensitivity: positive correlation cannot increase difference uncertainty
    # relative to the deliberately conservative rho=-1 case for nonnegative u values.
    vals = [difference_uncertainty(0.1, 0.1, r) for r in (-1.0, 0.0, 1.0)]
    assert vals[0] >= vals[1] >= vals[2]
    # Known common-mode limit: equal uncertainties with rho=+1 cancel in a difference.
    assert difference_uncertainty(0.1, 0.1, 1.0) <= tol


def _f(row: dict[str, str], key: str) -> float:
    value = row.get(key, "").strip()
    if value == "":
        raise ValueError(f"missing {key}")
    return float(value)


def validate_csv(path: str, thresholds: dict[str, float | None]) -> tuple[str, dict[str, float]]:
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    if not rows:
        return INCOMPLETE, {}
    if any(thresholds.get(ch) is None for ch in REQUIRED_CHANNELS):
        return INCOMPLETE, {}

    by_key: dict[tuple[str, str], set[str]] = defaultdict(set)
    channel_errors: dict[str, list[float]] = defaultdict(list)

    for row in rows:
        ch = row.get("channel", "")
        direction = row.get("direction", "")
        run_id = row.get("run_id", "").strip()
        if ch not in REQUIRED_CHANNELS or direction not in REQUIRED_DIRECTIONS or not run_id:
            return INCOMPLETE, {}
        if row.get("qc_status", "").strip() not in {"PASS", "INCLUDE"}:
            return INCOMPLETE, {}
        for field in ("logger_calibration_id", "reference_calibration_id", "placement_id", "carrier_id", "package_id", "dummy_id"):
            if not row.get(field, "").strip():
                return INCOMPLETE, {}
        try:
            logger = _f(row, "logger_value")
            reference = _f(row, "reference_value")
            u_logger = _f(row, "logger_uncertainty")
            u_ref = _f(row, "reference_uncertainty")
            pairing = _f(row, "pairing_gap_s")
            qualified_gap = _f(row, "v3_39_qualified_gap_s")
            rho_txt = row.get("correlation_rho", "").strip()
            rho = None if rho_txt == "" else float(rho_txt)
        except (ValueError, TypeError):
            return INCOMPLETE, {}
        if pairing < 0 or qualified_gap <= 0 or pairing > qualified_gap:
            return INCOMPLETE, {}
        try:
            e = conservative_error(abs(reference - logger), u_ref, u_logger, rho)
        except ValueError:
            return INCOMPLETE, {}
        channel_errors[ch].append(e)
        by_key[(ch, direction)].add(run_id)

    for ch in REQUIRED_CHANNELS:
        for direction in REQUIRED_DIRECTIONS:
            if len(by_key[(ch, direction)]) < MIN_RUNS:
                return INCOMPLETE, {}

    maxima = {ch: max(channel_errors[ch]) for ch in REQUIRED_CHANNELS}
    status = PASS if all(maxima[ch] <= float(thresholds[ch]) for ch in REQUIRED_CHANNELS) else FAIL
    return status, maxima


def main() -> int:
    synthetic_self_test()
    if len(sys.argv) == 1:
        print("v3.40 synthetic self-test PASS")
        return 0
    print("CSV validation requires caller-supplied prospective thresholds; no defaults are invented.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
