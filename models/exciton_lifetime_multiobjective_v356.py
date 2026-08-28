#!/usr/bin/env python3
import json
import math
import pathlib
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "research" / "benchmarks" / "exciton-lifetime-multiobjective-v3.56.json"
TOL = 1e-12


def rel_change(arm, ref):
    return arm / ref - 1.0


def half_resolution_interval(value, resolution):
    return value - resolution / 2.0, value + resolution / 2.0


def main():
    d = json.loads(DATA.read_text())
    x = d["inputs"]
    l8 = x["PM6_L8BO"]
    y18 = x["PM6_Y18C3"]
    ter = x["PM6_L8BO_Y18C3_0p86_0p14"]

    def v(row, key):
        return row[key]["value"]

    # Primary floating-point calculation.
    y_tau = rel_change(v(ter, "exciton_lifetime_ps"), v(y18, "exciton_lifetime_ps"))
    y_ff = rel_change(v(ter, "FF_fraction"), v(y18, "FF_fraction"))
    y_ff_abs = v(ter, "FF_fraction") - v(y18, "FF_fraction")
    y_vloss = v(ter, "voltage_loss_V") - v(y18, "voltage_loss_V")

    l_tau = rel_change(v(ter, "exciton_lifetime_ps"), v(l8, "exciton_lifetime_ps"))
    l_ff = rel_change(v(ter, "FF_fraction"), v(l8, "FF_fraction"))
    l_ff_abs = v(ter, "FF_fraction") - v(l8, "FF_fraction")
    l_vloss = v(ter, "voltage_loss_V") - v(l8, "voltage_loss_V")

    exp_y = d["expected"]["Y18C3_to_ternary"]
    exp_l = d["expected"]["L8BO_to_ternary"]
    checks = [
        math.isclose(y_tau, exp_y["exciton_lifetime_relative_change"], abs_tol=TOL, rel_tol=0),
        math.isclose(y_ff, exp_y["FF_relative_change"], abs_tol=TOL, rel_tol=0),
        math.isclose(y_ff_abs, exp_y["FF_absolute_change_fraction"], abs_tol=TOL, rel_tol=0),
        math.isclose(y_vloss, exp_y["voltage_loss_change_V"], abs_tol=TOL, rel_tol=0),
        math.isclose(l_tau, exp_l["exciton_lifetime_relative_change"], abs_tol=TOL, rel_tol=0),
        math.isclose(l_ff, exp_l["FF_relative_change"], abs_tol=TOL, rel_tol=0),
        math.isclose(l_ff_abs, exp_l["FF_absolute_change_fraction"], abs_tol=TOL, rel_tol=0),
        math.isclose(l_vloss, exp_l["voltage_loss_change_V"], abs_tol=TOL, rel_tol=0),
    ]
    assert all(checks)

    # Independent exact-rational recomputation from the reported decimal values.
    tau_ratio_exact = Fraction(870, 990) - 1
    ff_ratio_exact = Fraction(811, 795) - 1
    assert math.isclose(float(tau_ratio_exact), l_tau, abs_tol=TOL, rel_tol=0)
    assert math.isclose(float(ff_ratio_exact), l_ff, abs_tol=TOL, rel_tol=0)

    # Decision-driving ordinal counterexample: shorter lifetime yet higher FF and lower voltage loss.
    counterexample = (
        v(ter, "exciton_lifetime_ps") < v(l8, "exciton_lifetime_ps")
        and v(ter, "FF_fraction") > v(l8, "FF_fraction")
        and v(ter, "voltage_loss_V") < v(l8, "voltage_loss_V")
    )
    assert counterexample is True

    # Reporting-resolution interval check (not measurement uncertainty).
    t_tau = half_resolution_interval(v(ter, "exciton_lifetime_ps"), ter["exciton_lifetime_ps"]["reported_resolution_ps"])
    l_tau_i = half_resolution_interval(v(l8, "exciton_lifetime_ps"), l8["exciton_lifetime_ps"]["reported_resolution_ps"])
    t_ff = half_resolution_interval(v(ter, "FF_fraction"), ter["FF_fraction"]["reported_resolution_fraction"])
    l_ff_i = half_resolution_interval(v(l8, "FF_fraction"), l8["FF_fraction"]["reported_resolution_fraction"])
    t_v = half_resolution_interval(v(ter, "voltage_loss_V"), ter["voltage_loss_V"]["reported_resolution_V"])
    l_v_i = half_resolution_interval(v(l8, "voltage_loss_V"), l8["voltage_loss_V"]["reported_resolution_V"])
    assert t_tau[1] < l_tau_i[0]
    assert t_ff[0] > l_ff_i[1]
    assert t_v[1] < l_v_i[0]

    # Negative/control test: a synthetic monotonic fixture must NOT trigger the counterexample.
    synthetic = {"ref_tau": 900.0, "arm_tau": 1000.0, "ref_ff": 0.75, "arm_ff": 0.80, "ref_v": 0.54, "arm_v": 0.52}
    synthetic_counterexample = (
        synthetic["arm_tau"] < synthetic["ref_tau"]
        and synthetic["arm_ff"] > synthetic["ref_ff"]
        and synthetic["arm_v"] < synthetic["ref_v"]
    )
    assert synthetic_counterexample is False

    print(json.dumps({
        "Y18C3_to_ternary": {
            "lifetime_relative_change": y_tau,
            "FF_relative_change": y_ff,
            "FF_absolute_change": y_ff_abs,
            "voltage_loss_change_V": y_vloss
        },
        "L8BO_to_ternary": {
            "lifetime_relative_change": l_tau,
            "FF_relative_change": l_ff,
            "FF_absolute_change": l_ff_abs,
            "voltage_loss_change_V": l_vloss,
            "ordinal_counterexample": counterexample
        },
        "reporting_resolution_counterexample_robust": True,
        "checks": "PASS"
    }, indent=2))


if __name__ == "__main__":
    main()
