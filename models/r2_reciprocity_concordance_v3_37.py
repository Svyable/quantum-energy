#!/usr/bin/env python3
"""R2 v3.37 direct-vs-reciprocity delta_Vnr concordance screen.

Standard-library only. This is a metrology engineering screen, not a mechanism test.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

THRESHOLD_MV = 20.0
RHO_SENSITIVITY = (-0.5, 0.0, 0.5)
REQUIRED = (
    "lot_id", "substrate_id", "device_id", "pixel_id", "session_id",
    "temperature_target_K", "temperature_measured_K",
    "direct_delta_vnr_mV", "direct_u_mV", "direct_raw_ref", "direct_analysis_commit",
    "reciprocity_delta_vnr_mV", "reciprocity_u_mV", "reciprocity_raw_ref",
    "reciprocity_analysis_commit", "rho_shared_systematic", "configuration_match", "qc_status"
)


def combined_uncertainty(u_direct: float, u_recip: float, rho: float) -> float:
    """u_d = sqrt(u_d^2 + u_r^2 - 2 rho u_d u_r), all inputs/outputs in mV."""
    variance = u_direct * u_direct + u_recip * u_recip - 2.0 * rho * u_direct * u_recip
    if variance < -1e-12:
        raise ValueError("negative propagated variance")
    return math.sqrt(max(variance, 0.0))


def screen_pair(direct: float, reciprocity: float) -> tuple[float, str]:
    d = direct - reciprocity
    return d, "PASS" if abs(d) <= THRESHOLD_MV else "FAIL"


def independent_variance_check(u_direct: float, u_recip: float, rho: float) -> float:
    # Independent algebraic path: Var(X-Y)=Var(X)+Var(Y)-2Cov(X,Y), Cov=rho*uX*uY.
    cov = rho * u_direct * u_recip
    return (u_direct ** 2) + (u_recip ** 2) - (2.0 * cov)


def validate_row(row: dict[str, str]) -> dict[str, object]:
    missing = [k for k in REQUIRED if not row.get(k, "").strip()]
    if missing:
        return {"status": "INCOMPLETE", "reason": "missing:" + ",".join(missing)}
    if row["configuration_match"].upper() != "YES" or row["qc_status"].upper() != "PASS":
        return {"status": "INCOMPLETE", "reason": "configuration/QC not confirmed"}
    direct = float(row["direct_delta_vnr_mV"])
    recip = float(row["reciprocity_delta_vnr_mV"])
    ud = float(row["direct_u_mV"])
    ur = float(row["reciprocity_u_mV"])
    rho = float(row["rho_shared_systematic"])
    if ud < 0 or ur < 0 or not (-1.0 <= rho <= 1.0):
        return {"status": "FAIL", "reason": "invalid uncertainty/correlation input"}
    d, status = screen_pair(direct, recip)
    u = combined_uncertainty(ud, ur, rho)
    variance2 = independent_variance_check(ud, ur, rho)
    if abs(u * u - variance2) > 1e-12:
        raise AssertionError("independent uncertainty cross-check failed")
    sensitivity = {str(r): combined_uncertainty(ud, ur, r) for r in RHO_SENSITIVITY}
    return {"status": status, "difference_mV": d, "abs_difference_mV": abs(d), "u_difference_mV": u,
            "rho_sensitivity_u_mV": sensitivity}


def self_test() -> None:
    # Gate boundary and sign limiting cases.
    assert screen_pair(100.0, 100.0) == (0.0, "PASS")
    assert screen_pair(120.0, 100.0) == (20.0, "PASS")
    assert screen_pair(120.000001, 100.0)[1] == "FAIL"
    assert screen_pair(80.0, 100.0) == (-20.0, "PASS")
    # Known uncertainty limits: rho=0 gives root-sum-square; rho=1 with equal u cancels.
    assert abs(combined_uncertainty(3.0, 4.0, 0.0) - 5.0) <= 1e-12
    assert combined_uncertainty(5.0, 5.0, 1.0) == 0.0
    assert abs(combined_uncertainty(5.0, 5.0, -1.0) - 10.0) <= 1e-12
    # Sensitivity must decrease monotonically as positive correlation increases for positive u values.
    vals = [combined_uncertainty(4.0, 6.0, r) for r in RHO_SENSITIVITY]
    assert vals[0] > vals[1] > vals[2]
    print("v3.37 self-test PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", nargs="?")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.csv_path:
        parser.error("csv_path required unless --self-test is used")
    with Path(args.csv_path).open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for i, row in enumerate(rows, 1):
        print(i, validate_row(row))


if __name__ == "__main__":
    main()
