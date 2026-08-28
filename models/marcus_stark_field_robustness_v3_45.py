#!/usr/bin/env python3
"""Reproduce the v3.45 Marcus-Stark field-robustness audit.

This is a normalized-rate planning model derived from the published
field-dependent Marcus equation. It is not a device FF or Pmax predictor.
Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

KB_EV_K = 8.617333262145e-5
DEFAULT_CONTRACT = Path(__file__).resolve().parents[1] / "machine" / "marcus-stark-field-robustness-v3.45.json"
DEFAULT_EXPECTED = Path(__file__).with_name("marcus_stark_field_robustness_expected_v3_45.csv")


def log_rate_exponent(lambda_ev: float, delta_g_ev: float, delta_ev: float, temperature_k: float) -> float:
    """Return the dimensionless Marcus exponent log(k/prefactor)."""
    if lambda_ev <= 0:
        raise ValueError("lambda_eV must be > 0")
    if temperature_k <= 0:
        raise ValueError("temperature_K must be > 0")
    a = lambda_ev + delta_g_ev + delta_ev
    return -(a * a) / (4.0 * lambda_ev * KB_EV_K * temperature_k)


def direct_rate_ratio(lambda_ev: float, delta_g_ev: float, delta_ev: float, temperature_k: float) -> float:
    """Compute k(delta)/k(0) by subtracting two Marcus log exponents."""
    return math.exp(
        log_rate_exponent(lambda_ev, delta_g_ev, delta_ev, temperature_k)
        - log_rate_exponent(lambda_ev, delta_g_ev, 0.0, temperature_k)
    )


def closed_form_rate_ratio(lambda_ev: float, delta_g_ev: float, delta_ev: float, temperature_k: float) -> float:
    """Exact algebraic k(delta)/k(0), with the unknown prefactor cancelled."""
    a0 = lambda_ev + delta_g_ev
    return math.exp(-(2.0 * a0 * delta_ev + delta_ev * delta_ev) / (4.0 * lambda_ev * KB_EV_K * temperature_k))


def orientation_metrics(lambda_ev: float, delta_g_ev: float, delta_abs_ev: float, temperature_k: float) -> dict[str, float]:
    if delta_abs_ev < 0:
        raise ValueError("delta_abs_eV must be >= 0")
    r_plus = closed_form_rate_ratio(lambda_ev, delta_g_ev, +delta_abs_ev, temperature_k)
    r_minus = closed_form_rate_ratio(lambda_ev, delta_g_ev, -delta_abs_ev, temperature_k)
    r_worst = min(r_plus, r_minus)
    log_asym = abs(math.log(r_plus / r_minus))
    ratio = max(r_plus, r_minus) / min(r_plus, r_minus)
    return {
        "R_plus": r_plus,
        "R_minus": r_minus,
        "R_worst": r_worst,
        "abs_log_orientation_asymmetry": log_asym,
        "max_min_rate_ratio": ratio,
    }


def field_energy_shift_ev(field_v_per_m: float, separation_nm: float) -> float:
    """First-order one-electron energy shift in eV; q cancels in J->eV."""
    return abs(field_v_per_m) * separation_nm * 1e-9


def analytic_log_asymmetry(lambda_ev: float, delta_g_ev: float, delta_abs_ev: float, temperature_k: float) -> float:
    a0 = lambda_ev + delta_g_ev
    return abs(a0 * delta_abs_ev / (lambda_ev * KB_EV_K * temperature_k))


def rows(contract: dict) -> list[dict[str, float]]:
    fixture = contract["synthetic_fixture"]
    out = []
    for delta_ev in fixture["delta_sensitivity_eV"]:
        for lambda_ev in fixture["lambda_grid_eV"]:
            m = orientation_metrics(lambda_ev, fixture["delta_g_eV"], delta_ev, fixture["temperature_K"])
            out.append({"lambda_eV": lambda_ev, "delta_eV": delta_ev, **m})
    return out


def check_internal(contract: dict) -> None:
    tol = contract["software_checks"]["absolute_tolerance"]
    anchor = contract["published_scale_anchor"]
    derived = field_energy_shift_ev(anchor["field_V_per_m"], anchor["ct_separation_nm"])
    if abs(derived - anchor["derived_first_order_shift_eV"]) > tol:
        raise AssertionError(f"field-energy anchor mismatch: {derived}")

    fixture = contract["synthetic_fixture"]
    T = fixture["temperature_K"]
    dG = fixture["delta_g_eV"]

    for lambda_ev in fixture["lambda_grid_eV"]:
        for delta_ev in fixture["delta_sensitivity_eV"]:
            for signed in (+delta_ev, -delta_ev):
                a = direct_rate_ratio(lambda_ev, dG, signed, T)
                b = closed_form_rate_ratio(lambda_ev, dG, signed, T)
                if abs(a - b) > tol * max(1.0, abs(a), abs(b)):
                    raise AssertionError("direct and closed-form rate ratios disagree")

    for lambda_ev in fixture["lambda_grid_eV"]:
        if abs(closed_form_rate_ratio(lambda_ev, dG, 0.0, T) - 1.0) > tol:
            raise AssertionError("zero-field limiting case failed")

    lambda_star = -dG
    delta = anchor["derived_first_order_shift_eV"]
    m = orientation_metrics(lambda_star, dG, delta, T)
    if abs(m["R_plus"] - m["R_minus"]) > tol:
        raise AssertionError("activationless orientation symmetry failed")

    expected_activationless = math.exp(-(delta * delta) / (4.0 * lambda_star * KB_EV_K * T))
    if abs(m["R_worst"] - expected_activationless) > tol:
        raise AssertionError("activationless closed form failed")

    for lambda_ev in fixture["lambda_grid_eV"]:
        m = orientation_metrics(lambda_ev, dG, delta, T)
        a = analytic_log_asymmetry(lambda_ev, dG, delta, T)
        if abs(m["abs_log_orientation_asymmetry"] - a) > tol:
            raise AssertionError("orientation asymmetry identity failed")

    h = 1e-7
    lambda_test = 0.15
    fd = (
        log_rate_exponent(lambda_test, dG, h, T)
        - log_rate_exponent(lambda_test, dG, -h, T)
    ) / (2.0 * h)
    analytic = -(lambda_test + dG) / (2.0 * lambda_test * KB_EV_K * T)
    if abs(fd - analytic) > contract["software_checks"]["derivative_tolerance_eV_inv"]:
        raise AssertionError(f"finite-difference derivative mismatch: {fd} vs {analytic}")

    optimization_grid = fixture["optimization_lambda_grid_eV"]
    scored = [(orientation_metrics(lam, dG, delta, T)["R_worst"], lam) for lam in optimization_grid]
    best = max(scored)
    if abs(best[1] - lambda_star) > tol:
        raise AssertionError(f"synthetic grid optimum changed: lambda={best[1]}")


def csv_text(records: list[dict[str, float]]) -> str:
    from io import StringIO
    buf = StringIO()
    fieldnames = [
        "lambda_eV", "delta_eV", "R_plus", "R_minus", "R_worst",
        "abs_log_orientation_asymmetry", "max_min_rate_ratio",
    ]
    writer = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for rec in records:
        writer.writerow({
            "lambda_eV": f"{rec['lambda_eV']:.6f}",
            "delta_eV": f"{rec['delta_eV']:.6f}",
            "R_plus": f"{rec['R_plus']:.15g}",
            "R_minus": f"{rec['R_minus']:.15g}",
            "R_worst": f"{rec['R_worst']:.15g}",
            "abs_log_orientation_asymmetry": f"{rec['abs_log_orientation_asymmetry']:.15g}",
            "max_min_rate_ratio": f"{rec['max_min_rate_ratio']:.15g}",
        })
    return buf.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--expected", type=Path, default=DEFAULT_EXPECTED)
    parser.add_argument("--write-expected", action="store_true")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()

    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    check_internal(contract)
    generated = csv_text(rows(contract))

    if args.write_expected:
        args.expected.write_text(generated, encoding="utf-8", newline="\n")

    if args.check_expected:
        frozen = args.expected.read_text(encoding="utf-8").replace("\r\n", "\n")
        if generated != frozen:
            raise AssertionError("generated expected CSV differs from frozen fixture")

    fixture = contract["synthetic_fixture"]
    delta = contract["published_scale_anchor"]["derived_first_order_shift_eV"]
    print("Marcus-Stark field-robustness v3.45: PASS")
    print(f"kBT_eV={KB_EV_K * fixture['temperature_K']:.15g}")
    print(f"published_scale_delta_eV={delta:.15g}")
    for lam in (0.05, 0.10, 0.15):
        m = orientation_metrics(lam, fixture["delta_g_eV"], delta, fixture["temperature_K"])
        print(
            f"lambda_eV={lam:.2f} R_worst={m['R_worst']:.12f} "
            f"orientation_rate_ratio={m['max_min_rate_ratio']:.12f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
