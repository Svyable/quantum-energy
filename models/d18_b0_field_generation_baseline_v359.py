#!/usr/bin/env python3
"""Validate and analyze the prospective D18:eC9 B0 field-generation baseline protocol.

With no --csv argument, validates the frozen protocol and runs synthetic logic fixtures.
With --csv, computes per-device descriptive TDCF retention/field-gain and normalized PL curves.
No B1/B2 physical acceptance threshold is emitted by design.
"""
from __future__ import annotations
import argparse, csv, json, math, statistics
from collections import defaultdict
from pathlib import Path

TOL = 1e-12
EXPECTED_U = (0.0, 0.25, 0.5, 0.75, 1.0)
REQ = ("lot_id","substrate_id","device_id","session_id","technique","u","signal","signal_unit","qc_status")

def load_contract(path: Path):
    d=json.loads(path.read_text())
    assert d["bias_coordinate"]["points"] == list(EXPECTED_U)
    assert d["baseline_gate_freeze_rule"]["status"] == "DEFERRED_PENDING_REAL_B0_DATA"
    assert d["scope"]["no_physical_threshold_from_synthetic_model"] is True
    return d

def tdcf_metrics(q0: float, q1: float):
    if q0 <= 0 or q1 <= 0:
        raise ValueError("TDCF endpoint signals must be positive")
    return q0/q1, q1/q0 - 1.0

def independent_retention(q0: float, q1: float):
    # Algebraically distinct log-domain check.
    return math.exp(math.log(q0)-math.log(q1))

def pl_norm(p: float, p0: float):
    if p0 <= 0:
        raise ValueError("PL reference signal must be positive")
    return p/p0

def fixtures():
    # Limiting case: field-invariant TDCF gives unit retention and zero gain.
    r,g = tdcf_metrics(2.0,2.0)
    assert abs(r-1.0) <= TOL and abs(g) <= TOL
    assert abs(r-independent_retention(2.0,2.0)) <= TOL
    # Negative/control: stronger short-circuit generation produces retention < 1.
    r,g = tdcf_metrics(1.0,2.0)
    assert abs(r-0.5) <= TOL and abs(g-1.0) <= TOL
    assert abs(r-independent_retention(1.0,2.0)) <= TOL
    # Sign-reversal control: if Q(Voc)>Q(0), metric can exceed 1; do not clamp.
    r,g = tdcf_metrics(2.0,1.0)
    assert abs(r-2.0) <= TOL and abs(g+0.5) <= TOL
    # PL normalization limiting case.
    assert abs(pl_norm(3.0,3.0)-1.0) <= TOL
    # Invalid endpoint is rejected.
    try:
        tdcf_metrics(0.0,1.0)
    except ValueError:
        pass
    else:
        raise AssertionError("non-positive TDCF endpoint was not rejected")
    return "PASS"

def analyze_csv(path: Path):
    rows=[]
    with path.open(newline="") as f:
        rd=csv.DictReader(f)
        if tuple(rd.fieldnames or ()) != REQ:
            raise ValueError(f"CSV columns must exactly equal {REQ}")
        for r in rd:
            if r["qc_status"] != "PASS":
                continue
            u=float(r["u"]); sig=float(r["signal"])
            if not any(abs(u-x)<=TOL for x in EXPECTED_U):
                raise ValueError(f"unexpected u={u}")
            if sig <= 0:
                raise ValueError("signals must be positive")
            rows.append({**r,"u":u,"signal":sig})
    groups=defaultdict(list)
    for r in rows:
        key=(r["lot_id"],r["substrate_id"],r["device_id"],r["session_id"],r["technique"])
        groups[key].append(r)
    out={"devices":[],"summary":{},"gate_status":"DEFERRED_PENDING_REAL_B0_DATA"}
    tdcf_ret=[]
    for key,rs in sorted(groups.items()):
        byu={r["u"]:r["signal"] for r in rs}
        if set(byu) != set(EXPECTED_U):
            raise ValueError(f"incomplete bias grid for {key}")
        rec={"lot_id":key[0],"substrate_id":key[1],"device_id":key[2],"session_id":key[3],"technique":key[4]}
        if key[4] == "TDCF":
            rr,gg=tdcf_metrics(byu[0.0],byu[1.0])
            if abs(rr-independent_retention(byu[0.0],byu[1.0])) > TOL:
                raise AssertionError("independent TDCF check failed")
            rec.update({"R_TDCF":rr,"G_TDCF":gg})
            tdcf_ret.append(rr)
        elif key[4] == "PL":
            p0=byu[0.0]
            rec["P_norm"]={str(u):pl_norm(byu[u],p0) for u in EXPECTED_U}
        else:
            raise ValueError(f"unknown technique {key[4]}")
        out["devices"].append(rec)
    if tdcf_ret:
        out["summary"]["tdcf_device_count"]=len(tdcf_ret)
        out["summary"]["R_TDCF_median"]=statistics.median(tdcf_ret)
        if len(tdcf_ret) >= 2:
            out["summary"]["R_TDCF_sample_sd"]=statistics.stdev(tdcf_ret)
    out["summary"]["independent_lots"]=len({r["lot_id"] for r in rows})
    out["summary"]["independent_substrates"]=len({(r["lot_id"],r["substrate_id"]) for r in rows})
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--contract", default="research/protocols/d18-b0-field-generation-baseline-v3.59.json")
    ap.add_argument("--csv")
    args=ap.parse_args()
    load_contract(Path(args.contract))
    status=fixtures()
    result={"protocol_validation":status,"physical_gate":"DEFERRED_PENDING_REAL_B0_DATA"}
    if args.csv:
        result["analysis"]=analyze_csv(Path(args.csv))
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
