#!/usr/bin/env python3
"""Validate/analyze the v3.63 D18:eC9 transport-loss companion protocol.

Standard-library only. Synthetic fixtures test arithmetic and fail-closed logic;
they are not D18/PY-IT/eC9 measurements, material constants, or thresholds.
"""
from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import json
import math
from pathlib import Path

TOL = 1e-12
REQ = (
    "material_lot",
    "fabrication_lot",
    "substrate_id",
    "device_id",
    "session_id",
    "measured_ff_fraction",
    "pseudo_ff_fraction",
    "jsc_ma_cm2",
    "voc_v",
    "pmax_mw_cm2",
    "qc_status",
    "qc_exclusion_code",
)


def transport_metrics(ff: float, pff: float) -> tuple[float, float]:
    """Return (pFF-FF, FF/pFF) and fail closed on inconsistent accepted rows."""
    if not (0.0 < ff <= 1.0 and 0.0 < pff <= 1.0):
        raise ValueError("FF and pFF must both lie in (0,1]")
    if pff + TOL < ff:
        raise ValueError("accepted transport summary requires pFF >= FF within tolerance")
    loss = pff - ff
    if abs(loss) <= TOL:
        loss = 0.0
    return loss, ff / pff


def validate_contract(path: Path) -> dict:
    d = json.loads(path.read_text(encoding="utf-8"))
    assert d["claim_class"] == "prospective experiment/protocol"
    assert d["baseline_gate_freeze_rule"]["status"] == "DEFERRED_PENDING_REAL_B0_DATA"
    assert d["physical_result"] == "NONE_PROSPECTIVE_PROTOCOL_ONLY"
    assert tuple(d["required_summary_columns"]) == REQ
    assert d["derived_metrics"]["transport_ff_loss"]["equation"] == "DeltaFF_tr = pFF - FF"
    return d


def fixtures() -> dict:
    # Limiting case: no transport-associated FF gap.
    loss0, ret0 = transport_metrics(0.80, 0.80)
    assert loss0 == 0.0
    assert ret0 == 1.0

    # Synthetic arithmetic fixture. This is deliberately not a physical target.
    loss, retention = transport_metrics(0.75, 0.85)
    exact_loss = Fraction(85, 100) - Fraction(75, 100)
    exact_retention = Fraction(75, 85)
    assert math.isclose(loss, float(exact_loss), rel_tol=0.0, abs_tol=TOL)
    assert math.isclose(retention, float(exact_retention), rel_tol=0.0, abs_tol=TOL)

    # Negative/control: method-inconsistent pFF < FF must remain visible and fail.
    rejected = False
    try:
        transport_metrics(0.85, 0.80)
    except ValueError:
        rejected = True
    assert rejected

    # Invalid domain must fail rather than normalize silently.
    try:
        transport_metrics(0.0, 0.80)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid FF domain was not rejected")

    return {
        "limiting_case_loss": loss0,
        "limiting_case_retention": ret0,
        "synthetic_loss": loss,
        "synthetic_retention": retention,
        "pff_less_than_ff_rejected": rejected,
        "checks": "PASS",
    }


def analyze_csv(path: Path) -> dict:
    rows = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != REQ:
            raise ValueError(f"CSV columns must exactly equal {REQ}")
        for raw in reader:
            if raw["qc_status"] not in {"PASS", "EXCLUDE_PREDECLARED"}:
                raise ValueError("qc_status must be PASS or EXCLUDE_PREDECLARED")
            if raw["qc_status"] == "EXCLUDE_PREDECLARED":
                if not raw["qc_exclusion_code"].strip():
                    raise ValueError("excluded row requires qc_exclusion_code")
                continue
            ff = float(raw["measured_ff_fraction"])
            pff = float(raw["pseudo_ff_fraction"])
            jsc = float(raw["jsc_ma_cm2"])
            voc = float(raw["voc_v"])
            pmax = float(raw["pmax_mw_cm2"])
            if jsc <= 0 or voc <= 0 or pmax <= 0:
                raise ValueError("accepted Jsc, Voc, and stabilized/accepted Pmax summary values must be positive")
            loss, retention = transport_metrics(ff, pff)
            rows.append({
                "material_lot": raw["material_lot"],
                "fabrication_lot": raw["fabrication_lot"],
                "substrate_id": raw["substrate_id"],
                "device_id": raw["device_id"],
                "session_id": raw["session_id"],
                "DeltaFF_tr": loss,
                "R_FF": retention,
                "measured_ff_fraction": ff,
                "pseudo_ff_fraction": pff,
                "pmax_mw_cm2": pmax,
            })

    return {
        "accepted_rows": rows,
        "accepted_device_count": len({(r["material_lot"], r["fabrication_lot"], r["substrate_id"], r["device_id"]) for r in rows}),
        "independent_material_lots": len({r["material_lot"] for r in rows}),
        "physical_gate": "DEFERRED_PENDING_REAL_B0_DATA",
        "note": "Per-device descriptive outputs only; do not pool correlated rows as independent lots.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", default="research/protocols/d18-b0-transport-loss-companion-v3.63.json")
    parser.add_argument("--csv")
    args = parser.parse_args()

    validate_contract(Path(args.contract))
    out = {
        "protocol_validation": "PASS",
        "fixtures": fixtures(),
        "physical_result": "NONE_PROSPECTIVE_PROTOCOL_ONLY",
        "physical_gate": "DEFERRED_PENDING_REAL_B0_DATA",
    }
    if args.csv:
        out["analysis"] = analyze_csv(Path(args.csv))
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
