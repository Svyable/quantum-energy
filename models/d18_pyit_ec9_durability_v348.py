#!/usr/bin/env python3
"""v3.48 stabilized-Pmax durability arithmetic; standard library only."""
from __future__ import annotations
import argparse, json, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "machine" / "d18-pyit-ec9-durability-v3.48.json"

def metrics(t, b0, arm):
    if not (len(t) == len(b0) == len(arm) and len(t) >= 2):
        raise ValueError("matched series with >=2 points required")
    if any(x <= 0 for x in b0 + arm):
        raise ValueError("Pmax must be positive")
    if any(t[i+1] <= t[i] for i in range(len(t)-1)):
        raise ValueError("time must be strictly increasing")
    rb = [x / b0[0] for x in b0]
    ra = [x / arm[0] for x in arm]
    T = t[-1] - t[0]
    ab = sum((t[i+1]-t[i])*(rb[i]+rb[i+1])/2 for i in range(len(t)-1))/T
    aa = sum((t[i+1]-t[i])*(ra[i]+ra[i+1])/2 for i in range(len(t)-1))/T
    return {
        "initial_gain": arm[0]/b0[0]-1,
        "endpoint_gain": arm[-1]/b0[-1]-1,
        "endpoint_retention_penalty": rb[-1]-ra[-1],
        "B0_integrated_retention": ab,
        "arm_integrated_retention": aa,
        "integrated_retention_penalty": ab-aa,
    }

def independent_ratios(b0, arm):
    # Distinct numerical path: log-ratio/exponential rather than direct division.
    return math.exp(math.log(arm[0])-math.log(b0[0]))-1, math.exp(math.log(arm[-1])-math.log(b0[-1]))-1

def self_test(path=DEFAULT):
    spec = json.loads(path.read_text())
    f = spec["synthetic_fixture"]
    got = metrics(f["time_h"], f["B0_pmax_arb"], f["arm_pmax_arb"])
    tol = f["tolerance"]
    for k, exp in f["expected"].items():
        if abs(got[k]-exp) > tol:
            raise AssertionError((k, got[k], exp))
    g0, gT = independent_ratios(f["B0_pmax_arb"], f["arm_pmax_arb"])
    if abs(g0-got["initial_gain"]) > tol or abs(gT-got["endpoint_gain"]) > tol:
        raise AssertionError("independent ratio path mismatch")
    # Limiting case: identical constant trajectories => zero gain/penalty, unit retention.
    z = metrics([0.0, 1.0], [1.0, 1.0], [1.0, 1.0])
    if any(abs(z[k]) > tol for k in ("initial_gain","endpoint_gain","endpoint_retention_penalty","integrated_retention_penalty")):
        raise AssertionError("zero-case failed")
    # Negative/control test: initial +5% advantage is gone by endpoint in the synthetic fixture.
    if not (got["initial_gain"] > 0 and got["endpoint_gain"] < 0):
        raise AssertionError("crossover fixture failed")
    # Unit-scale invariance.
    s = metrics(f["time_h"], [100*x for x in f["B0_pmax_arb"]], [100*x for x in f["arm_pmax_arb"]])
    for k in got:
        if abs(s[k]-got[k]) > tol:
            raise AssertionError("scale invariance failed")
    print(json.dumps(got, sort_keys=True))
    print("PASS_SYNTHETIC_FIXTURE")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--spec", type=pathlib.Path, default=DEFAULT)
    a = p.parse_args()
    if a.self_test:
        self_test(a.spec)
    else:
        p.error("use --self-test")
