#!/usr/bin/env python3
"""v3.71 dual-path charge-generation robustness model.

Exploratory phenomenological model only. It does not claim that any project
device has a measured donor-independent generation fraction.
"""
from __future__ import annotations

import argparse
import csv
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "machine" / "dual-path-generation-robustness-v3.71.json"
DEFAULT_EXPECTED = Path(__file__).with_name("dual_path_generation_robustness_expected_v371.csv")
TOL = 1e-12


def retention(f_bulk: float, r_interface: float, r_bulk: float) -> float:
    for name, value in (("f_bulk", f_bulk), ("r_interface", r_interface), ("r_bulk", r_bulk)):
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be in [0,1]")
    return (1.0 - f_bulk) * r_interface + f_bulk * r_bulk


def inverse_bulk_fraction(R: float, r_interface: float, r_bulk: float) -> float:
    if not (0.0 <= R <= 1.0 and 0.0 <= r_interface <= 1.0 and 0.0 <= r_bulk <= 1.0):
        raise ValueError("retention inputs must be in [0,1]")
    if r_bulk <= r_interface:
        raise ValueError("inverse requires r_bulk > r_interface")
    lo, hi = r_interface, r_bulk
    if not lo - TOL <= R <= hi + TOL:
        raise ValueError("R must be bracketed by route retention factors")
    return (R - r_interface) / (r_bulk - r_interface)


def exact_retention(f_num: int, f_den: int, ri_num: int, ri_den: int, rb_num: int, rb_den: int) -> Fraction:
    f = Fraction(f_num, f_den)
    ri = Fraction(ri_num, ri_den)
    rb = Fraction(rb_num, rb_den)
    return (1 - f) * ri + f * rb


def generated_rows(contract: dict) -> list[dict[str, str]]:
    fixture = contract["synthetic_fixture"]
    ri = float(fixture["r_I"])
    rb = float(fixture["r_B"])
    rows = []
    for f_bulk in fixture["f_B_grid"]:
        R = retention(float(f_bulk), ri, rb)
        rows.append({
            "f_B": f"{float(f_bulk):.6f}",
            "r_I": f"{ri:.6f}",
            "r_B": f"{rb:.6f}",
            "R": f"{R:.12f}",
            "retention_advantage_vs_interface_only": f"{R-ri:.12f}",
        })
    return rows


def render_csv(rows: list[dict[str, str]]) -> str:
    from io import StringIO
    buf = StringIO()
    fields = ["f_B", "r_I", "r_B", "R", "retention_advantage_vs_interface_only"]
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


def run_checks(contract: dict) -> None:
    fixture = contract["synthetic_fixture"]
    ri = float(fixture["r_I"])
    rb = float(fixture["r_B"])

    # Endpoint limits.
    assert abs(retention(0.0, ri, rb) - ri) < TOL
    assert abs(retention(1.0, ri, rb) - rb) < TOL

    # Frozen synthetic fixture.
    for f_bulk, expected in zip(fixture["f_B_grid"], fixture["expected_R"]):
        got = retention(float(f_bulk), ri, rb)
        assert abs(got - float(expected)) < TOL, (f_bulk, got, expected)

    # Independent exact-rational route for the central 40% example.
    exact = exact_retention(2, 5, 1, 2, 9, 10)
    assert exact == Fraction(33, 50)
    assert abs(retention(0.4, 0.5, 0.9) - float(exact)) < TOL

    # Analytic sensitivity dR/df = rB-ri versus finite difference.
    f0 = 0.37
    h = 1e-7
    fd = (retention(f0 + h, ri, rb) - retention(f0 - h, ri, rb)) / (2 * h)
    analytic = rb - ri
    assert abs(fd - analytic) < 1e-9, (fd, analytic)

    # Inverse limiting check.
    recovered = inverse_bulk_fraction(0.66, 0.5, 0.9)
    assert abs(recovered - 0.4) < TOL

    # Negative/control: if the secondary route is less robust, adding it must hurt retention.
    assert retention(0.4, 0.8, 0.3) < retention(0.0, 0.8, 0.3)

    # Equal-route limit: route fraction is irrelevant when both respond identically.
    assert abs(retention(0.1, 0.7, 0.7) - retention(0.9, 0.7, 0.7)) < TOL

    # Fail closed for invalid inverse use.
    try:
        inverse_bulk_fraction(0.6, 0.8, 0.5)
    except ValueError:
        pass
    else:
        raise AssertionError("inverse must fail when r_bulk <= r_interface")

    # Ensure no synthetic fixture became a physical threshold.
    thresholds = contract["measurement_policy"]["thresholds"]
    assert all(value is None for value in thresholds.values())


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    p.add_argument("--expected", type=Path, default=DEFAULT_EXPECTED)
    p.add_argument("--write-expected", action="store_true")
    p.add_argument("--check-expected", action="store_true")
    ns = p.parse_args()

    contract = json.loads(ns.contract.read_text(encoding="utf-8"))
    run_checks(contract)
    text = render_csv(generated_rows(contract))

    if ns.write_expected:
        ns.expected.write_text(text, encoding="utf-8", newline="\n")
    if ns.check_expected:
        frozen = ns.expected.read_text(encoding="utf-8").replace("\r\n", "\n")
        if text != frozen:
            raise AssertionError("generated CSV differs from frozen v3.71 fixture")

    print("dual-path generation robustness v3.71: PASS")
    print("synthetic_R_fB0.40=0.660000000000")
    print("analytic_dR_dfB=0.400000000000")
    print("inverse_fB_from_R0.66=0.400000000000")
    print("physical_thresholds=DEFERRED_PENDING_REAL_BASELINE_AND_PERTURBATION_DATA")
    print("physical_result=NONE_EXPLORATORY_MODEL_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
