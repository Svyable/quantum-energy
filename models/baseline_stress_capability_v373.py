#!/usr/bin/env python3
"""Baseline-only stress capability analyzer for v3.73.

Analyzes A0/B0 baseline log-retention across independent fabrication lots and
emits a planning MDE frontier for the future four-arm v3.72 interaction.
This is not a physical pass/fail model and cannot choose a scientific margin.
Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import NormalDist, mean, stdev

REQUIRED = {
    "lot_id", "arm", "stress", "substrate_id", "metric", "before", "after",
    "film_integrity_pass", "calibration_complete", "stress_history_match",
    "contact_control_pass", "optical_control_pass"
}
VALID_ARMS = {"A0", "B0"}
VALID_STRESS = {"T", "L"}
PRIMARY_METRIC = "Pmax"
N_GRID = [3, 5, 7, 9, 12]
M_GRID = [1.0, 1.5, 2.0]
ALPHA = 0.05
POWER = 0.80


def b(v: str) -> bool:
    return str(v).strip().lower() in {"1", "true", "yes", "y", "pass"}


def load_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as h:
        rd = csv.DictReader(h)
        missing = sorted(REQUIRED - set(rd.fieldnames or []))
        rows = list(rd)
    if missing:
        raise ValueError("missing columns: " + ", ".join(missing))
    if not rows:
        raise ValueError("empty input CSV")
    return rows


def analyze(rows):
    problems = []
    seen = set()
    by_cell_lot = defaultdict(list)

    for r in rows:
        arm = r["arm"].strip()
        stress = r["stress"].strip()
        metric = r["metric"].strip()
        key = (r["lot_id"], arm, stress, r["substrate_id"], metric)
        if key in seen:
            problems.append(f"duplicate_key:{'|'.join(key)}")
            continue
        seen.add(key)
        if arm not in VALID_ARMS or stress not in VALID_STRESS or metric != PRIMARY_METRIC:
            problems.append(f"invalid_scope:{'|'.join(key)}")
            continue
        try:
            before = float(r["before"])
            after = float(r["after"])
        except ValueError:
            problems.append(f"non_numeric_before_after:{'|'.join(key)}")
            continue
        if before <= 0 or after <= 0:
            problems.append(f"nonpositive_before_after:{'|'.join(key)}")
            continue
        if arm == "A0" and not b(r["film_integrity_pass"]):
            problems.append(f"A0_film_integrity_fail:{'|'.join(key)}")
        for field in ("calibration_complete", "stress_history_match", "contact_control_pass", "optical_control_pass"):
            if not b(r[field]):
                problems.append(f"{field}_fail:{'|'.join(key)}")
        by_cell_lot[(arm, stress, r["lot_id"])].append(math.log(after / before))

    cell_lot_means = defaultdict(dict)
    for (arm, stress, lot), vals in by_cell_lot.items():
        if len(vals) < 2:
            problems.append(f"too_few_substrates:{arm}|{stress}|{lot}")
        cell_lot_means[(arm, stress)][lot] = mean(vals)

    required_cells = [(a, s) for a in sorted(VALID_ARMS) for s in sorted(VALID_STRESS)]
    lot_sets = []
    cells = {}
    for cell in required_cells:
        lots = cell_lot_means.get(cell, {})
        lot_sets.append(set(lots))
        if len(lots) < 3:
            problems.append(f"too_few_lots:{cell[0]}|{cell[1]}:{len(lots)}")
        if len(lots) >= 2:
            vals = list(lots.values())
            cells[f"{cell[0]}_{cell[1]}"] = {
                "n_lots": len(vals),
                "mean_log_retention": mean(vals),
                "geometric_mean_retention": math.exp(mean(vals)),
                "sd_lot_mean_log_retention": stdev(vals),
            }
        else:
            cells[f"{cell[0]}_{cell[1]}"] = {"n_lots": len(lots)}

    if lot_sets:
        common = set.intersection(*lot_sets) if all(lot_sets) else set()
        union = set.union(*lot_sets) if any(lot_sets) else set()
        if common != union:
            problems.append("lot_ids_not_common_across_A0_B0_T_L")
    else:
        common = set()

    complete_sds = [v.get("sd_lot_mean_log_retention") for v in cells.values()]
    complete_sds = [x for x in complete_sds if x is not None]
    s_base = max(complete_sds) if len(complete_sds) == 4 else None

    frontier = []
    if s_base is not None:
        zsum = NormalDist().inv_cdf(1 - ALPHA / 2) + NormalDist().inv_cdf(POWER)
        for m in M_GRID:
            for n in N_GRID:
                se = 2.0 * m * s_base / math.sqrt(n)
                mde_log = zsum * se
                frontier.append({
                    "variance_multiplier": m,
                    "future_lots_per_arm": n,
                    "se_proxy_log_interaction": se,
                    "mde_log_interaction": mde_log,
                    "mde_ratio_of_ratios_minus_1": math.exp(mde_log) - 1.0,
                })

    baseline_contrasts = {}
    if common:
        for stress in sorted(VALID_STRESS):
            d = [
                cell_lot_means[("B0", stress)][lot] - cell_lot_means[("A0", stress)][lot]
                for lot in sorted(common)
            ]
            baseline_contrasts[f"B0_minus_A0_{stress}"] = {
                "n_lots": len(d),
                "mean_log_retention_difference": mean(d),
                "sd_log_retention_difference": stdev(d) if len(d) > 1 else None,
            }
        dt = [cell_lot_means[("B0", "T")][lot] - cell_lot_means[("A0", "T")][lot] for lot in sorted(common)]
        dl = [cell_lot_means[("B0", "L")][lot] - cell_lot_means[("A0", "L")][lot] for lot in sorted(common)]
        omega0 = [a - b_ for a, b_ in zip(dt, dl)]
        baseline_contrasts["baseline_stress_selectivity_T_minus_L"] = {
            "n_lots": len(omega0),
            "mean": mean(omega0),
            "sd": stdev(omega0) if len(omega0) > 1 else None,
        }

    status = "BASELINE_CAPABILITY_ESTIMATED" if not problems else "INCOMPLETE"
    return {
        "schema_version": "baseline-stress-capability-v3.73",
        "status": status,
        "physical_result": "NONE_BASELINE_CAPABILITY_ONLY",
        "physical_thresholds": "DEFERRED_UNTIL_REAL_BASELINE_PLUS_USEFUL_WORK_MARGIN",
        "problems": sorted(set(problems)),
        "common_lots": sorted(common),
        "cells": cells,
        "baseline_contrasts": baseline_contrasts,
        "s_base": s_base,
        "planning_frontier": frontier,
        "planning_boundary": "MDE values assume equal future lot counts and use m*s_base as a treatment-arm SD proxy; they are sensitivity scenarios, not guaranteed power.",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input_csv", type=Path)
    p.add_argument("--output-json", type=Path)
    ns = p.parse_args()
    result = analyze(load_rows(ns.input_csv))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if ns.output_json:
        ns.output_json.write_text(text, encoding="utf-8", newline="\n")
    else:
        print(text, end="")
    print(f"baseline stress capability v3.73: {result['status']}")
    if result["s_base"] is not None:
        print(f"s_base={result['s_base']:.15g}")
        f = next(x for x in result["planning_frontier"] if x["variance_multiplier"] == 1.0 and x["future_lots_per_arm"] == 5)
        print(f"mde_log_m1_n5={f['mde_log_interaction']:.15g}")
        print(f"mde_ratio_m1_n5={f['mde_ratio_of_ratios_minus_1']:.15g}")
    print("physical_thresholds=DEFERRED")
    return 0 if result["status"] == "BASELINE_CAPABILITY_ESTIMATED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
