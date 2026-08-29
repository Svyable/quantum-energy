#!/usr/bin/env python3
"""v3.72 dual-path stress tomography.

Prospective method validation only. Synthetic fixture values test arithmetic and
fail-closed logic; they are not physical thresholds or expected device results.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

CONTRACT = Path(__file__).resolve().parents[1] / "machine" / "dual-path-stress-tomography-v3.72.json"
EXPECTED = Path(__file__).with_name("dual_path_stress_tomography_expected_v372.csv")
TOL = 1e-12


def log_retention(after: float, before: float) -> float:
    if after <= 0 or before <= 0:
        raise ValueError("before/after metric must be positive for log retention")
    return math.log(after / before)


def contrasts(retentions: dict[str, float]) -> dict[str, float]:
    missing = {"A0", "A2", "B0", "B2"} - set(retentions)
    if missing:
        raise ValueError(f"missing arms: {sorted(missing)}")
    for arm, r in retentions.items():
        if r <= 0:
            raise ValueError(f"retention for {arm} must be > 0")
    y = {arm: math.log(r) for arm, r in retentions.items()}
    delta_a = y["A2"] - y["A0"]
    delta_b = y["B2"] - y["B0"]
    psi = delta_b - delta_a
    ratio_identity = (retentions["B2"] / retentions["B0"]) / (retentions["A2"] / retentions["A0"])
    return {
        "Delta_A": delta_a,
        "Delta_B": delta_b,
        "Psi": psi,
        "exp_Psi": math.exp(psi),
        "ratio_identity": ratio_identity,
    }


def physical_status(contract: dict) -> str:
    thresholds = contract["physical_thresholds"]
    numeric_keys = [
        "minimum_resolved_log_retention_effect",
        "minimum_resolved_Psi",
        "minimum_resolved_Omega",
        "minimum_Pmax_retention",
    ]
    if any(thresholds[k] is None for k in numeric_keys):
        return "INCOMPLETE_THRESHOLDS_DEFERRED"
    return "READY_FOR_PROSPECTIVE_CLASSIFICATION"


def generate_rows(contract: dict) -> tuple[list[dict[str, float | str]], float]:
    fixture = contract["synthetic_fixture"]["retentions"]
    rows = []
    psis = {}
    for stress in ("T", "L"):
        c = contrasts(fixture[stress])
        psis[stress] = c["Psi"]
        for arm in ("A0", "A2", "B0", "B2"):
            rows.append({
                "stress": stress,
                "arm": arm,
                "retention": fixture[stress][arm],
                "Delta_A": c["Delta_A"],
                "Delta_B": c["Delta_B"],
                "Psi": c["Psi"],
                "exp_Psi": c["exp_Psi"],
                "ratio_identity": c["ratio_identity"],
            })
    return rows, psis["T"] - psis["L"]


def csv_text(rows: list[dict[str, float | str]], omega: float) -> str:
    from io import StringIO
    buf = StringIO()
    fieldnames = ["stress", "arm", "retention", "Delta_A", "Delta_B", "Psi", "exp_Psi", "ratio_identity", "Omega"]
    writer = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        out = dict(row)
        out["retention"] = f"{float(out['retention']):.12f}"
        for key in ("Delta_A", "Delta_B", "Psi", "exp_Psi", "ratio_identity"):
            out[key] = f"{float(out[key]):.15g}"
        out["Omega"] = f"{omega:.15g}"
        writer.writerow(out)
    return buf.getvalue()


def internal_checks(contract: dict) -> None:
    rows, omega = generate_rows(contract)
    expected = contract["synthetic_fixture"]["expected"]
    by_stress = {}
    for row in rows:
        by_stress.setdefault(row["stress"], row)
    for stress, key in (("T", "Psi_T"), ("L", "Psi_L")):
        if abs(float(by_stress[stress]["Psi"]) - expected[key]) > TOL:
            raise AssertionError(f"{key} changed")
    if abs(float(by_stress["T"]["exp_Psi"]) - expected["exp_Psi_T"]) > TOL:
        raise AssertionError("exp_Psi_T changed")
    if abs(float(by_stress["L"]["exp_Psi"]) - expected["exp_Psi_L"]) > TOL:
        raise AssertionError("exp_Psi_L changed")
    if abs(omega - expected["Omega"]) > TOL:
        raise AssertionError("Omega changed")

    for stress in ("T", "L"):
        c = contrasts(contract["synthetic_fixture"]["retentions"][stress])
        if abs(c["exp_Psi"] - c["ratio_identity"]) > TOL:
            raise AssertionError("log-ratio and raw-ratio paths disagree")

    # Direct before/after limiting check.
    if abs(log_retention(0.8, 1.0) - math.log(0.8)) > TOL:
        raise AssertionError("log retention limiting case failed")

    if physical_status(contract) != "INCOMPLETE_THRESHOLDS_DEFERRED":
        raise AssertionError("synthetic protocol must fail closed before physical margins are frozen")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--contract", type=Path, default=CONTRACT)
    p.add_argument("--expected", type=Path, default=EXPECTED)
    p.add_argument("--write-expected", action="store_true")
    p.add_argument("--check-expected", action="store_true")
    args = p.parse_args()

    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    internal_checks(contract)
    rows, omega = generate_rows(contract)
    generated = csv_text(rows, omega)

    if args.write_expected:
        args.expected.write_text(generated, encoding="utf-8", newline="\n")
    if args.check_expected:
        frozen = args.expected.read_text(encoding="utf-8").replace("\r\n", "\n")
        if generated != frozen:
            raise AssertionError("generated CSV differs from frozen v3.72 fixture")

    print("dual-path stress tomography v3.72: PASS")
    print(f"synthetic_Psi_T={contract['synthetic_fixture']['expected']['Psi_T']:.12f}")
    print(f"synthetic_Psi_L={contract['synthetic_fixture']['expected']['Psi_L']:.12f}")
    print(f"synthetic_Omega={omega:.12f}")
    print(f"physical_status={physical_status(contract)}")
    print("physical_result=NONE_PROSPECTIVE_PROTOCOL_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
