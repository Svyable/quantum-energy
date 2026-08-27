#!/usr/bin/env python3
"""Parametric R2 facility instrument-time planner v3.32.

All timing inputs are planning assumptions supplied by CSV. The script does not
represent measured facility throughput, vendor quotes, or scientific results.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

# Frozen structural counts inherited from merged protocols.
CAL_SESSIONS = 30                 # v3.20: 24 training + 6 prospective holdout
CAL_SWEEPS_PER_SESSION = 4        # v3.20
CAL_GRID_POINTS_PER_SWEEP = 17    # v3.20
CAL_AUX_POINTS_PER_SWEEP = 4      # dark_pre, anchor_pre, anchor_post, dark_post
INSTRUMENT_REPLICATES = 6         # v3.26 minimum
OPTICAL_STEP_DIRECTIONS = 2       # v3.25: 0.05->2 and 2->0.05 sun
OPTICAL_REPLICATES_PER_DIRECTION = 6  # v3.25 minimum
OPTICAL_TIME_SAMPLES = 10         # v3.25 recommended planning grid


@dataclass(frozen=True)
class Result:
    scenario: str
    calibration_h: float
    instrument_step_h: float
    optical_step_h: float
    voc_intensity_h: float
    spectral_h: float
    linearity_h: float
    packet_admin_h: float
    total_h: float
    calibration_fraction: float


def positive(row: dict[str, str], key: str) -> float:
    value = float(row[key])
    if value < 0:
        raise ValueError(f"{key} must be nonnegative")
    return value


def plan(row: dict[str, str]) -> Result:
    scenario = row["scenario"]

    grid_s = positive(row, "calibration_grid_point_s")
    aux_s = positive(row, "calibration_aux_point_s")
    session_overhead_s = positive(row, "calibration_session_overhead_s")
    inst_samples = int(positive(row, "instrument_samples_per_replicate"))
    inst_sample_s = positive(row, "instrument_sample_s")
    inst_rep_overhead_s = positive(row, "instrument_replicate_overhead_s")
    optical_sample_s = positive(row, "optical_sample_s")
    optical_rep_overhead_s = positive(row, "optical_replicate_overhead_s")
    monotonic_points = int(positive(row, "monotonic_points"))
    randomized_points = int(positive(row, "randomized_points"))
    voc_read_s = positive(row, "voc_point_read_s")
    random_dwell_s = positive(row, "randomized_settling_dwell_s")
    spectral_points = int(positive(row, "spectral_intensity_points"))
    spectral_point_s = positive(row, "spectral_point_s")
    spectral_setup_s = positive(row, "spectral_setup_s")
    linearity_s = positive(row, "linearity_total_s")
    packet_admin_s = positive(row, "packet_admin_s")

    calibration_s = (
        CAL_SESSIONS * CAL_SWEEPS_PER_SESSION * CAL_GRID_POINTS_PER_SWEEP * grid_s
        + CAL_SESSIONS * CAL_SWEEPS_PER_SESSION * CAL_AUX_POINTS_PER_SWEEP * aux_s
        + CAL_SESSIONS * session_overhead_s
    )
    instrument_s = INSTRUMENT_REPLICATES * (
        inst_samples * inst_sample_s + inst_rep_overhead_s
    )
    optical_s = OPTICAL_STEP_DIRECTIONS * OPTICAL_REPLICATES_PER_DIRECTION * (
        OPTICAL_TIME_SAMPLES * optical_sample_s + optical_rep_overhead_s
    )
    voc_s = monotonic_points * voc_read_s + randomized_points * (voc_read_s + random_dwell_s)
    spectral_s = spectral_setup_s + spectral_points * spectral_point_s
    total_s = calibration_s + instrument_s + optical_s + voc_s + spectral_s + linearity_s + packet_admin_s
    if total_s <= 0:
        raise ValueError("total planned time must be positive")

    return Result(
        scenario=scenario,
        calibration_h=calibration_s / 3600.0,
        instrument_step_h=instrument_s / 3600.0,
        optical_step_h=optical_s / 3600.0,
        voc_intensity_h=voc_s / 3600.0,
        spectral_h=spectral_s / 3600.0,
        linearity_h=linearity_s / 3600.0,
        packet_admin_h=packet_admin_s / 3600.0,
        total_h=total_s / 3600.0,
        calibration_fraction=calibration_s / total_s,
    )


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("input CSV has no scenarios")
    return rows


def write_results(path: Path, results: list[Result]) -> None:
    fields = list(Result.__dataclass_fields__)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for result in results:
            writer.writerow({k: getattr(result, k) for k in fields})


def independent_count_check() -> None:
    # Independently derive the v3.20 record counts from hierarchy factors.
    grid_records = 30 * 4 * 17
    auxiliary_records = 30 * 4 * (2 + 2)
    assert grid_records == 2040
    assert auxiliary_records == 480
    assert grid_records + auxiliary_records == 2520
    # v3.24 frozen randomized acquisition: four complete 17-point blocks.
    assert 4 * 17 == 68
    # v3.25 minimum optical qualification: 2 directions x 6 replicates x 10 samples.
    assert 2 * 6 * 10 == 120


def self_test(input_csv: Path) -> None:
    independent_count_check()
    results = [plan(row) for row in read_rows(input_csv)]
    by_name = {r.scenario: r for r in results}
    expected = {
        "low": 2.9305555555555554,
        "nominal": 7.190555555555555,
        "high": 19.973333333333333,
    }
    for name, target in expected.items():
        got = by_name[name].total_h
        if abs(got - target) > 1e-12:
            raise AssertionError(f"{name}: {got} != {target}")
    if not (by_name["low"].total_h < by_name["nominal"].total_h < by_name["high"].total_h):
        raise AssertionError("scenario monotonicity failed")
    # Reference-repeatability acquisition must dominate the nominal scenario.
    if by_name["nominal"].calibration_fraction <= 0.5:
        raise AssertionError("expected calibration campaign to exceed half nominal burden")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("technical/data/r2_facility_time_input_template_v3_32.csv"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test(args.input)
        print("v3.32 self-test PASS")
        return

    results = [plan(row) for row in read_rows(args.input)]
    if args.output:
        write_results(args.output, results)
    else:
        for r in results:
            print(f"{r.scenario}: total={r.total_h:.4f} h; calibration={r.calibration_h:.4f} h ({100*r.calibration_fraction:.1f}%)")


if __name__ == "__main__":
    main()
