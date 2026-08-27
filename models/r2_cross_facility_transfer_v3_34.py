#!/usr/bin/env python3
"""R2 cross-facility A->B->A transfer screening, v3.34.

Standard-library only. This is an engineering screening implementation, not a
publication-grade equivalence test and not evidence of a quantum mechanism.
"""
from __future__ import annotations

import csv
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

MARGIN_MV = 5.0
MIN_DEVICES = 3
LEGS = ("A1", "B", "A2")

@dataclass(frozen=True)
class Row:
    device_id: str
    leg: str
    facility_id: str
    elapsed_h: float
    value_mV: float
    qc_status: str
    config_id: str


def residual(a1: float, b: float, a2: float, t1: float, tb: float, t2: float) -> float:
    if not (t1 < tb < t2):
        raise ValueError("required time order is t_A1 < t_B < t_A2")
    w = (tb - t1) / (t2 - t1)
    a_interp = (1.0 - w) * a1 + w * a2
    return b - a_interp


def parse_csv(path: Path) -> list[Row]:
    rows: list[Row] = []
    with path.open(newline="", encoding="utf-8") as f:
        for raw in csv.DictReader(f):
            if raw["qc_status"] != "PASS":
                continue
            rows.append(Row(
                device_id=raw["device_id"].strip(),
                leg=raw["leg"].strip(),
                facility_id=raw["facility_id"].strip(),
                elapsed_h=float(raw["elapsed_h"]),
                value_mV=float(raw["DeltaVnr_mV"]),
                qc_status=raw["qc_status"].strip(),
                config_id=raw["config_id"].strip(),
            ))
    return rows


def evaluate(rows: list[Row]) -> dict:
    by_device: dict[str, dict[str, Row]] = defaultdict(dict)
    for row in rows:
        if row.leg not in LEGS:
            return {"status": "FAIL", "reason": f"unknown leg {row.leg}"}
        if row.leg in by_device[row.device_id]:
            return {"status": "FAIL", "reason": f"duplicate leg {row.device_id}/{row.leg}"}
        by_device[row.device_id][row.leg] = row

    complete = {d: legs for d, legs in by_device.items() if set(legs) == set(LEGS)}
    if len(complete) < MIN_DEVICES:
        return {"status": "INCOMPLETE", "reason": "fewer than three complete PASS primary devices"}

    rs: list[float] = []
    per_device = []
    for device_id, legs in sorted(complete.items()):
        a1, b, a2 = legs["A1"], legs["B"], legs["A2"]
        if a1.facility_id != a2.facility_id or b.facility_id == a1.facility_id:
            return {"status": "FAIL", "reason": f"facility identity conflict for {device_id}"}
        if not (a1.config_id and b.config_id and a2.config_id):
            return {"status": "INCOMPLETE", "reason": f"missing config_id for {device_id}"}
        try:
            r = residual(a1.value_mV, b.value_mV, a2.value_mV,
                         a1.elapsed_h, b.elapsed_h, a2.elapsed_h)
        except ValueError as exc:
            return {"status": "FAIL", "reason": f"{device_id}: {exc}"}
        w = (b.elapsed_h - a1.elapsed_h) / (a2.elapsed_h - a1.elapsed_h)
        rs.append(r)
        per_device.append({"device_id": device_id, "w": w, "residual_mV": r,
                           "home_drift_mV": a2.value_mV - a1.value_mV})

    mean_r = sum(rs) / len(rs)
    rms_r = math.sqrt(sum(x*x for x in rs) / len(rs))
    status = "PASS" if abs(mean_r) <= MARGIN_MV and rms_r <= MARGIN_MV else "FAIL"
    return {"status": status, "n_devices": len(rs), "mean_bias_mV": mean_r,
            "rms_residual_mV": rms_r, "per_device": per_device,
            "margin_mV": MARGIN_MV}


def self_test() -> None:
    # Independent algebraic check: for midpoint timing, residual = B-(A1+A2)/2.
    r1 = residual(10.0, 13.0, 12.0, 0.0, 1.0, 2.0)
    r2 = 13.0 - (10.0 + 12.0) / 2.0
    assert abs(r1 - r2) < 1e-12

    # Limiting case: pure linear home-facility drift, B on interpolation -> zero residual.
    assert abs(residual(100.0, 105.0, 110.0, 0.0, 1.0, 2.0)) < 1e-12

    def synth(offset: float) -> list[Row]:
        out = []
        for i, base in enumerate((100.0, 102.0, 98.0), 1):
            d = f"D{i}"
            out.extend([
                Row(d, "A1", "A", 0.0, base, "PASS", "cfgA"),
                Row(d, "B", "B", 1.0, base + 1.0 + offset, "PASS", "cfgB"),
                Row(d, "A2", "A", 2.0, base + 2.0, "PASS", "cfgA"),
            ])
        return out

    p = evaluate(synth(3.0))
    assert p["status"] == "PASS" and abs(p["mean_bias_mV"] - 3.0) < 1e-12
    f = evaluate(synth(7.0))
    assert f["status"] == "FAIL" and abs(f["mean_bias_mV"] - 7.0) < 1e-12

    incomplete = evaluate(synth(3.0)[:6])
    assert incomplete["status"] == "INCOMPLETE"

    bad_time = synth(3.0)
    bad_time[1] = Row("D1", "B", "B", 3.0, 104.0, "PASS", "cfgB")
    assert evaluate(bad_time)["status"] == "FAIL"

    # Sensitivity boundary: exactly 5 mV passes, infinitesimally above fails.
    assert evaluate(synth(5.0))["status"] == "PASS"
    assert evaluate(synth(5.000001))["status"] == "FAIL"
    print("v3.34 self-test PASS: algebra, drift limiting case, gate boundary, adversarial cases")


def main(argv: list[str]) -> int:
    if len(argv) == 1 or argv[1] == "--self-test":
        self_test()
        return 0
    result = evaluate(parse_csv(Path(argv[1])))
    print(result)
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
