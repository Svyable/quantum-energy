#!/usr/bin/env python3
"""v3.46 prospective field-generation estimator.

Standard-library only. Real analysis requires preregistered protocol values and raw data.
The built-in fixture is synthetic and exercises arithmetic/sign conventions only.
"""
from __future__ import annotations
import argparse, csv, json, math, sys
from pathlib import Path

TOL = 1e-12


def retention(values, ref_index=0):
    ref = values[ref_index]
    if not math.isfinite(ref) or ref <= 0:
        raise ValueError("reference eta_FC must be finite and > 0")
    out = [v / ref for v in values]
    if any((not math.isfinite(v)) or v < 0 for v in out):
        raise ValueError("retention must be finite and nonnegative")
    return out


def field_loss(ret):
    if not ret:
        raise ValueError("empty retention series")
    return max(1.0 - r for r in ret)


def field_loss_independent(ret):
    # Independent algebraic identity: max(1-r)=1-min(r).
    return 1.0 - min(ret)


def synthetic_self_test():
    b0 = [1.0, 0.98, 0.94, 0.88]
    b2 = [1.0, 0.97, 0.90, 0.75]
    l0 = field_loss(b0)
    l2 = field_loss(b2)
    d2 = l2 - l0
    assert abs(l0 - 0.12) <= TOL
    assert abs(l2 - 0.25) <= TOL
    assert abs(d2 - 0.13) <= TOL
    assert abs(l0 - field_loss_independent(b0)) <= TOL
    assert abs(l2 - field_loss_independent(b2)) <= TOL
    # Limiting cases: field-independent retention has zero loss; worse retention increases loss.
    assert field_loss([1.0, 1.0, 1.0]) == 0.0
    assert field_loss([1.0, 0.9]) > field_loss([1.0, 0.95])
    return {"L_B0": l0, "L_B2": l2, "D_B2": d2, "status": "PASS_SYNTHETIC_FIXTURE"}


def analyze_csv(path: Path):
    rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
    required = {"lot_id", "arm_code", "device_id", "prebias_V", "eta_FC", "qc_include"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"CSV requires columns: {sorted(required)}")
    groups = {}
    for row in rows:
        if row["qc_include"].strip().lower() not in {"true", "1", "yes"}:
            continue
        key = (row["lot_id"], row["arm_code"], row["device_id"])
        groups.setdefault(key, []).append((float(row["prebias_V"]), float(row["eta_FC"])))
    out = []
    for key, vals in sorted(groups.items()):
        vals.sort(key=lambda x: x[0])
        etas = [x[1] for x in vals]
        # This generic executable uses the first sorted bias as reference only for arithmetic.
        # A real release analysis must replace this with the frozen V_ref from the preregistration.
        ret = retention(etas, 0)
        loss = field_loss(ret)
        out.append({"lot_id": key[0], "arm_code": key[1], "device_id": key[2], "field_loss": loss})
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--csv", type=Path)
    args = p.parse_args()
    if args.self_test or args.csv is None:
        print(json.dumps(synthetic_self_test(), sort_keys=True))
    if args.csv is not None:
        print(json.dumps(analyze_csv(args.csv), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
