#!/usr/bin/env python3
from __future__ import annotations
import math,random,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import r2_settling_gate_v3_25 as m

TIMES=[0.25,0.5,1,2,4,8,16,24,32,48]

def make(tau=2.0,reps=8,noise=5e-6,tail_amp=0.0,tail_tau=30.0,seed=20260827):
    rng=random.Random(seed); rows=[]
    # Worst frozen-grid Voc step for n=1 at 300 K, 0.05 -> 2 sun.
    dv=m.KB_EV_PER_K*m.T_K*math.log(m.PHI_MAX/m.PHI_MIN)
    for cls,sgn,fr,to in [("up",-1,0.05,2.0),("down",1,2.0,0.05)]:
        plateau=0.80 if cls=="up" else 0.70
        for rep in range(reps):
            for j,t in enumerate(TIMES):
                transient=sgn*dv*math.exp(-t/tau)+sgn*tail_amp*math.exp(-t/tail_tau)
                rows.append({"step_class":cls,"replicate_id":f"R{rep+1:02d}","from_suns":str(fr),"to_suns":str(to),"elapsed_s":str(t),"voc_V":repr(plateau+transient+rng.gauss(0,noise)),"qc_status":"PASS"})
    return rows

def main():
    # Independent algebraic L1 norm for geometric 17-point / symmetric 7-point fit.
    numeric=m.curvature_weight_l1(); analytic=m.analytic_geometric_l1()
    if abs(numeric-analytic)>1e-10: raise AssertionError((numeric,analytic))
    if abs(numeric-143.8085097637075)>1e-10: raise AssertionError(numeric)
    vtol=m.CURVATURE_BIAS_BUDGET/numeric
    if abs(vtol-6.953691416753467e-05)>1e-16: raise AssertionError(vtol)

    clean=m.assess(make())
    if clean["overall_status"]!="PASS": raise AssertionError(clean)
    if clean["recommended_randomized_dwell_s"] not in {16.0,24.0}: raise AssertionError(clean["recommended_randomized_dwell_s"])

    # Independent exponential dwell formula: |Delta V| exp(-t/tau) <= voltage limit.
    dv=m.KB_EV_PER_K*m.T_K*math.log(m.PHI_MAX/m.PHI_MIN)
    t_exact=2.0*math.log(dv/vtol)
    if abs(t_exact-14.447216456801229)>1e-12: raise AssertionError(t_exact)
    if clean["recommended_randomized_dwell_s"] < t_exact: raise AssertionError("qualified dwell precedes analytic limiting dwell")

    # Too few independent step replicates cannot qualify.
    small=m.assess(make(reps=5))
    if small["overall_status"]!="INCOMPLETE": raise AssertionError(small)

    # Long hidden tail must fail within the frozen 48 s observation window.
    slow=m.assess(make(tau=2.0,tail_amp=0.002,tail_tau=80.0,noise=0.0))
    if slow["overall_status"]!="FAIL": raise AssertionError(slow)

    # Common offset to every time sample changes plateau voltage but not settling.
    shifted=make(noise=0.0)
    for r in shifted:r["voc_V"]=repr(float(r["voc_V"])+0.123)
    a=m.assess(make(noise=0.0)); b=m.assess(shifted)
    if a["recommended_randomized_dwell_s"]!=b["recommended_randomized_dwell_s"]: raise AssertionError("offset limiting case failed")

    print(f"curvature_weight_l1_per_V={numeric:.12g}")
    print(f"settling_voltage_limit_uV={1e6*vtol:.12g}")
    print(f"analytic_tau2_worst_step_dwell_s={t_exact:.12g}")
    print(f"qualified_sampled_dwell_s={clean['recommended_randomized_dwell_s']:.12g}")
    print("PASS")
    return 0
if __name__=="__main__":raise SystemExit(main())
