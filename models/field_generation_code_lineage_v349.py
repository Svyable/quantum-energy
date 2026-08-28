#!/usr/bin/env python3
"""Independent arithmetic audit for v3.49 field-generation code lineage.

This file does not copy upstream MATLAB code. It independently evaluates the
paper-text first-order Stark scale and the inspected public-code quadratic
polarizability expression from the frozen machine contract.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[1] / "machine" / "field-generation-code-lineage-v3.49.json"


def paper_first_order_shift_eV(field_v_per_m: float, separation_nm: float) -> float:
    # q*F*r joules divided by q joules/eV -> F*r eV.
    return abs(field_v_per_m) * separation_nm * 1e-9


def upstream_quadratic_shift_eV(
    field_v_per_m: float,
    d_ct_nm: float,
    epsilon0: float,
    q_c: float,
    alpha_prime_a3: float,
    d_ref_m: float,
) -> tuple[float, float]:
    d_ct_m = d_ct_nm * 1e-9
    scale = (d_ct_m / d_ref_m) ** 4
    implied_alpha_a3 = alpha_prime_a3 * scale
    alpha_si = 4.0 * math.pi * epsilon0 * alpha_prime_a3 * 1e-30
    alpha_ct_si = alpha_si * scale
    shift = 0.5 * alpha_ct_si * field_v_per_m * abs(field_v_per_m) / q_c
    return shift, implied_alpha_a3


def assert_close(name: str, actual: float, expected: float, tol: float) -> None:
    if abs(actual - expected) > tol * max(1.0, abs(actual), abs(expected)):
        raise AssertionError(f"{name}: {actual!r} != {expected!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=DEFAULT)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    c = json.loads(args.contract.read_text(encoding="utf-8"))
    paper = c["primary_source"]["paper_model_statements"]
    code = c["public_author_code"]["observed_helper_model"]
    const = c["independent_reimplementation"]["constants"]
    exp = c["independent_reimplementation"]["expected_outputs"]
    tol = c["independent_reimplementation"]["absolute_tolerance"]

    first = paper_first_order_shift_eV(paper["field_V_per_m"], paper["first_order_ct_separation_nm"])
    q15, alpha15 = upstream_quadratic_shift_eV(
        paper["field_V_per_m"], code["example_RCT_nm"], const["epsilon0_F_per_m"],
        const["q_C"], code["alpha_prime_TCNQ_A3"], code["d_TCNQ_m"]
    )
    q35, _ = upstream_quadratic_shift_eV(
        paper["field_V_per_m"], paper["first_order_ct_separation_nm"], const["epsilon0_F_per_m"],
        const["q_C"], code["alpha_prime_TCNQ_A3"], code["d_TCNQ_m"]
    )
    second_upper = paper["reported_second_order_shift_eV_range"][1]
    ratio15 = q15 / second_upper
    ratio35first = q35 / first

    assert_close("paper first-order scale", first, exp["paper_first_order_shift_eV_at_3p5nm_1e7Vpm"], tol)
    assert_close("upstream quadratic 1.5 nm", q15, exp["upstream_quadratic_shift_eV_at_1p5nm_1e7Vpm"], tol)
    assert_close("implied alpha 1.5 nm", alpha15, exp["upstream_implied_alpha_A3_at_1p5nm"], tol)
    assert_close("ratio to paper second-order upper", ratio15, exp["ratio_upstream_1p5nm_shift_to_paper_second_order_upper"], tol)
    assert_close("upstream quadratic 3.5 nm", q35, exp["upstream_quadratic_shift_eV_at_3p5nm_1e7Vpm"], tol)
    assert_close("ratio 3.5 nm quadratic / paper first-order", ratio35first, exp["ratio_upstream_3p5nm_shift_to_paper_first_order"], tol)

    # Limiting/negative controls.
    assert_close("zero field first order", paper_first_order_shift_eV(0.0, 3.5), 0.0, tol)
    zq, _ = upstream_quadratic_shift_eV(0.0, 1.5, const["epsilon0_F_per_m"], const["q_C"], code["alpha_prime_TCNQ_A3"], code["d_TCNQ_m"])
    assert_close("zero field quadratic", zq, 0.0, tol)
    half, _ = upstream_quadratic_shift_eV(paper["field_V_per_m"] / 2, 1.5, const["epsilon0_F_per_m"], const["q_C"], code["alpha_prime_TCNQ_A3"], code["d_TCNQ_m"])
    assert_close("quadratic F^2 scaling", half / q15, 0.25, tol)

    print("FIELD_GENERATION_CODE_LINEAGE_V3.49: PASS")
    print(f"paper_first_order_shift_eV={first:.15g}")
    print(f"public_code_quadratic_shift_1p5nm_eV={q15:.15g}")
    print(f"public_code_implied_alpha_1p5nm_A3={alpha15:.15g}")
    print(f"ratio_to_paper_second_order_upper={ratio15:.15g}")
    print(f"public_code_quadratic_shift_3p5nm_eV={q35:.15g}")
    print(f"ratio_3p5nm_quadratic_to_paper_first_order={ratio35first:.15g}")
    print("decision=LINEAGE_UNRESOLVED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
