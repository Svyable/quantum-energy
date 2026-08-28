#!/usr/bin/env python3
"""Validate the v3.61 durability preregistration and its arithmetic fixtures.

Standard library only. Embedded fixture values are synthetic software-test data,
not expected D18/PY-IT/eC9 behavior or physical thresholds.
"""

from fractions import Fraction
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTRACT = HERE.parent / "research" / "protocols" / "d18-durability-mechanism-retention-v3.61.json"
TOL = 1e-12


def retention(p_t: float, p_0: float) -> float:
    if p_0 <= 0 or p_t < 0:
        raise ValueError("Pmax values require p0>0 and pt>=0")
    return p_t / p_0


def gain(arm_pmax: float, b0_pmax: float) -> float:
    if arm_pmax < 0 or b0_pmax <= 0:
        raise ValueError("Pmax comparison requires arm>=0 and B0>0")
    return arm_pmax / b0_pmax - 1.0


def exact_retention(pt_num: int, pt_den: int, p0_num: int, p0_den: int) -> Fraction:
    p_t = Fraction(pt_num, pt_den)
    p_0 = Fraction(p0_num, p0_den)
    if p_0 <= 0 or p_t < 0:
        raise ValueError("invalid exact Pmax values")
    return p_t / p_0


def validate_contract(d: dict) -> None:
    assert d["claim_class"] == "prospective protocol"
    assert d["canonical_project_gate"]["stabilized_pmax_relative_improvement"] == 0.05
    assert d["canonical_project_gate"]["independent_lots_min"] == 3
    stress_ids = {x["id"] for x in d["stress_arms"]}
    assert stress_ids == {"D2I_65C_DARK", "L1I_1SUN_RT"}
    d2 = next(x for x in d["stress_arms"] if x["id"] == "D2I_65C_DARK")
    assert d2["temperature_C"] == 65
    l1 = next(x for x in d["stress_arms"] if x["id"] == "L1I_1SUN_RT")
    assert l1["light_irradiance_W_m2_range"] == [800, 1000]
    assert d["horizon"]["primary"] == "T80 if observed; otherwise 1000 h"
    assert d["horizon"]["no_lifetime_extrapolation_without_model"] is True
    required = {
        "material_lot", "fabrication_lot", "substrate_id", "device_id", "arm",
        "stress_id", "time_h", "pmax_mW_cm2", "functional", "qc_exclusion_code"
    }
    assert set(d["required_columns"]) == required


def main() -> None:
    d = json.loads(CONTRACT.read_text(encoding="utf-8"))
    validate_contract(d)

    # Limiting case: unchanged stabilized Pmax has unit retention.
    assert retention(10.0, 10.0) == 1.0

    # Independent exact-arithmetic cross-check of a synthetic 8/10 retention.
    r_float = retention(8.0, 10.0)
    r_exact = exact_retention(8, 1, 10, 1)
    assert math.isclose(r_float, float(r_exact), rel_tol=0.0, abs_tol=TOL)
    assert r_exact == Fraction(4, 5)

    # Synthetic decision fixture: initial B1 advantage clears 5%, but at 1000 h it disappears.
    # This tests only fail-closed classification logic.
    initial_gain = gain(10.6, 10.0)
    final_gain = gain(7.8, 8.0)
    gate = d["canonical_project_gate"]["stabilized_pmax_relative_improvement"]
    assert initial_gain >= gate
    assert final_gain < gate
    assert final_gain < 0.0
    durable_useful_work = initial_gain >= gate and final_gain >= gate
    assert durable_useful_work is False

    # Negative-domain control: a non-positive baseline must fail instead of being normalized.
    rejected = False
    try:
        retention(1.0, 0.0)
    except ValueError:
        rejected = True
    assert rejected

    print(json.dumps({
        "protocol_validation": "PASS",
        "limiting_case_retention": 1.0,
        "independent_exact_retention": float(r_exact),
        "synthetic_initial_gain": initial_gain,
        "synthetic_final_gain": final_gain,
        "synthetic_durable_useful_work": durable_useful_work,
        "physical_result": "NONE_PROSPECTIVE_PROTOCOL_ONLY",
        "checks": "PASS"
    }, indent=2))


if __name__ == "__main__":
    main()
