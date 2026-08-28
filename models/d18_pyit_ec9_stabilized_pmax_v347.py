#!/usr/bin/env python3
"""Prospective stabilized-Pmax useful-work gate for D18/PY-IT/eC9 v3.47.
Standard library only. Synthetic fixtures are arithmetic tests, not device evidence.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path

TOL = 1e-12
MIN_LOTS = 3
TARGET = 0.05

def gain(pa: float, pb: float) -> float:
    if pb <= 0 or pa < 0:
        raise ValueError("Pmax values must satisfy B0>0 and arm>=0")
    return pa / pb - 1.0

def gain_log_crosscheck(pa: float, pb: float) -> float:
    if pa <= 0 or pb <= 0:
        raise ValueError("log cross-check requires positive powers")
    return math.exp(math.log(pa) - math.log(pb)) - 1.0

def lower_gain(pa: float, ua: float, pb: float, ub: float) -> float:
    if min(ua, ub) < 0 or pa - ua <= 0 or pb + ub <= 0:
        raise ValueError("invalid uncertainty interval")
    return (pa - ua) / (pb + ub) - 1.0

def evaluate(b0, arm, ub0, uarm):
    n = len(b0)
    if not (n == len(arm) == len(ub0) == len(uarm)):
        raise ValueError("length mismatch")
    gs = [gain(a, b) for a, b in zip(arm, b0)]
    gs2 = [gain_log_crosscheck(a, b) for a, b in zip(arm, b0)]
    if any(abs(x-y) > TOL for x, y in zip(gs, gs2)):
        raise AssertionError("independent log-ratio cross-check failed")
    lows = [lower_gain(a, ua, b, ub) for a, ua, b, ub in zip(arm, uarm, b0, ub0)]
    mean_g = sum(gs) / n
    mean_low = sum(lows) / n
    passed = n >= MIN_LOTS and all(x > 0 for x in gs) and mean_g >= TARGET and mean_low >= TARGET
    return {"n_lots": n, "lot_gains": gs, "lot_lower_gains": lows, "mean_gain": mean_g,
            "mean_lower_gain": mean_low, "result": "PASS" if passed else "FAIL"}

def self_test():
    b0=[1.00,1.02,0.98]; arm=[1.08,1.09,1.04]; u=[0.005]*3
    out=evaluate(b0,arm,u,u)
    assert abs(out["mean_gain"]-0.06995064692543689) <= TOL
    assert abs(out["mean_lower_gain"]-0.05964991599306124) <= TOL
    assert out["result"] == "PASS"
    neg=evaluate(b0,[1.08,0.99,1.04],u,u)
    assert neg["result"] == "FAIL"
    unit_scaled=evaluate([100*x for x in b0],[100*x for x in arm],[100*x for x in u],[100*x for x in u])
    assert abs(unit_scaled["mean_gain"]-out["mean_gain"]) <= TOL
    assert gain(1.0,1.0) == 0.0
    print(json.dumps({"fixture":out,"negative":neg,"status":"PASS_SYNTHETIC_FIXTURE"},indent=2))

def main():
    p=argparse.ArgumentParser(); p.add_argument("--self-test",action="store_true"); args=p.parse_args()
    if args.self_test: self_test()
    else: p.error("use --self-test; real-data parser intentionally deferred until frozen acquisition columns are populated")
if __name__ == "__main__": main()
