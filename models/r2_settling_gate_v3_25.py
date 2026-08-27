#!/usr/bin/env python3
"""R2 v3.25 intensity-step settling qualification.

This tool bounds acquisition-history bias before randomized-order Voc-intensity
curvature measurements. It does not infer a recombination mechanism.

Input hierarchy: step_class -> replicate -> elapsed time sample.
The primary gate is nonparametric: repeated step transients must demonstrate
that the mean response remains inside a voltage envelope derived from the frozen
curvature-bias budget. A single-exponential fit is reported only as a diagnostic.
"""
from __future__ import annotations
import argparse,csv,json,math,statistics,sys
from collections import defaultdict
from pathlib import Path

KB_EV_PER_K=8.617333262e-5
T_K=300.0
N_GRID=17
PHI_MIN=0.05
PHI_MAX=2.0
CURVATURE_BIAS_BUDGET=0.01
Z95=1.959963984540054
MIN_REPLICATES=6
MIN_TIMEPOINTS=6
PLATEAU_POINTS=3

REQ={"step_class","replicate_id","from_suns","to_suns","elapsed_s","voc_V","qc_status"}

def solve3(A,y):
    m=[list(r)+[v] for r,v in zip(A,y)]
    for c in range(3):
        p=max(range(c,3),key=lambda r:abs(m[r][c]));m[c],m[p]=m[p],m[c]
        s=m[c][c]
        if abs(s)<1e-18: raise ValueError("singular local fit")
        for j in range(c,4):m[c][j]/=s
        for r in range(3):
            if r==c:continue
            f=m[r][c]
            for j in range(c,4):m[r][j]-=f*m[c][j]
    return [m[i][3] for i in range(3)]

def local_weights(phi,anchor):
    x=[math.log(v) for v in phi]; half=3
    lo=max(0,min(anchor-half,len(x)-7)); hi=lo+7
    u=[x[j]-x[anchor] for j in range(lo,hi)]
    S=[sum(v**k for v in u) for k in range(5)]
    A=[[S[0],S[1],S[2]],[S[1],S[2],S[3]],[S[2],S[3],S[4]]]
    out=[0.0]*len(phi)
    for loc,j in enumerate(range(lo,hi)):
        beta=solve3(A,[u[loc]**k for k in range(3)])
        out[j]=beta[1]/(KB_EV_PER_K*T_K)
    return out

def curvature_weight_l1():
    r=(PHI_MAX/PHI_MIN)**(1/(N_GRID-1))
    phi=[PHI_MIN*r**i for i in range(N_GRID)]
    il=min(range(N_GRID),key=lambda i:abs(phi[i]-0.1))
    ih=min(range(N_GRID),key=lambda i:abs(phi[i]-1.0))
    wl=local_weights(phi,il); wh=local_weights(phi,ih)
    return sum(abs(b-a) for a,b in zip(wl,wh))

def analytic_geometric_l1():
    # For a symmetric 7-point quadratic derivative on an equally spaced
    # log-intensity grid, slope weights are j/(28 h), j=-3..3. The low/high
    # windows are disjoint here, so ||w_curv||_1 = 2*sum|j|/(28 h kBT/q).
    h=math.log(PHI_MAX/PHI_MIN)/(N_GRID-1)
    return 6.0/(7.0*h*KB_EV_PER_K*T_K)

def load(path):
    with open(path,newline="",encoding="utf-8") as f:
        rd=csv.DictReader(f); miss=sorted(REQ-set(rd.fieldnames or [])); rows=list(rd)
    if miss: raise ValueError("missing columns: "+", ".join(miss))
    if not rows: raise ValueError("empty input")
    return [r for r in rows if r["qc_status"].strip().upper()=="PASS"]

def sem(vals):
    if len(vals)<2:return float("inf")
    return statistics.stdev(vals)/math.sqrt(len(vals))

def linfit(x,y):
    xm=statistics.fmean(x);ym=statistics.fmean(y)
    sxx=sum((v-xm)**2 for v in x)
    if sxx<=0:return 0.0,ym
    b=sum((a-xm)*(c-ym) for a,c in zip(x,y))/sxx
    return b,ym-b*xm

def exp_tau(times,means,plateau):
    # Diagnostic only. Fit ln|V(t)-Vinf| vs t where deviation is positive.
    pts=[(t,abs(v-plateau)) for t,v in zip(times,means) if abs(v-plateau)>1e-12]
    if len(pts)<3:return None
    x=[p[0] for p in pts[:-PLATEAU_POINTS+1]] if len(pts)>PLATEAU_POINTS else [p[0] for p in pts]
    y=[math.log(p[1]) for p in pts[:len(x)]]
    if len(x)<3:return None
    slope,_=linfit(x,y)
    return (-1.0/slope) if slope<0 else None

def assess(rows):
    l1=curvature_weight_l1(); l1a=analytic_geometric_l1()
    if abs(l1-l1a)>1e-10: raise AssertionError("independent curvature L1 check failed")
    vtol=CURVATURE_BIAS_BUDGET/l1
    by=defaultdict(list)
    for r in rows:by[r["step_class"]].append(r)
    results=[];fail=[];inc=[]
    for cls,rr in sorted(by.items()):
        reps=sorted(set(r["replicate_id"] for r in rr))
        times=sorted(set(float(r["elapsed_s"]) for r in rr))
        if len(reps)<MIN_REPLICATES or len(times)<MIN_TIMEPOINTS:
            inc.append(cls);results.append({"step_class":cls,"status":"INCOMPLETE","n_replicates":len(reps),"n_timepoints":len(times)});continue
        # Require complete balanced records; missing points cannot be treated as settled.
        d={(r["replicate_id"],float(r["elapsed_s"])):float(r["voc_V"]) for r in rr}
        if any((rep,t) not in d for rep in reps for t in times):
            inc.append(cls);results.append({"step_class":cls,"status":"INCOMPLETE","note":"unbalanced replicate/time grid"});continue
        vals={t:[d[(rep,t)] for rep in reps] for t in times}
        means={t:statistics.fmean(vals[t]) for t in times}
        plateau_samples=[d[(rep,t)] for rep in reps for t in times[-PLATEAU_POINTS:]]
        plateau=statistics.fmean(plateau_samples)
        plateau_se=sem(plateau_samples)
        upper=[]
        for t in times:
            diff=means[t]-plateau
            u=math.sqrt(sem(vals[t])**2+plateau_se**2)
            upper.append((t,abs(diff)+Z95*u,diff,u))
        dwell=None
        for i,(t,_,_,_) in enumerate(upper):
            if all(q[1]<=vtol for q in upper[i:]):
                dwell=t;break
        # Late-window trend guard: deterministic drift across the plateau window
        # must consume no more than half the voltage envelope.
        late=times[-PLATEAU_POINTS:]
        slope,_=linfit(late,[means[t] for t in late])
        late_span=late[-1]-late[0]
        late_drift=abs(slope)*late_span
        tau=exp_tau(times,[means[t] for t in times],plateau)
        status="PASS" if dwell is not None and late_drift<=0.5*vtol else "FAIL"
        if status=="FAIL":fail.append(cls)
        results.append({
            "step_class":cls,"status":status,"n_replicates":len(reps),"n_timepoints":len(times),
            "from_suns":float(rr[0]["from_suns"]),"to_suns":float(rr[0]["to_suns"]),
            "plateau_voc_V":plateau,"plateau_se_V":plateau_se,"settling_voltage_limit_V":vtol,
            "qualified_dwell_s":dwell,"late_window_drift_V":late_drift,
            "diagnostic_single_exp_tau_s":tau,
            "max_post_dwell_95_upper_V":None if dwell is None else max(q[1] for q in upper if q[0]>=dwell),
        })
    overall="FAIL" if fail else ("INCOMPLETE" if inc else "PASS")
    dwells=[r["qualified_dwell_s"] for r in results if r.get("qualified_dwell_s") is not None]
    return {
        "schema_version":"r2-settling-gate-v3.25",
        "claim_boundary":"PASS qualifies intensity-step settling for the declared acquisition path only; it is not mechanism evidence.",
        "overall_status":overall,"failed_step_classes":fail,"incomplete_step_classes":inc,
        "curvature_bias_budget":CURVATURE_BIAS_BUDGET,
        "curvature_weight_l1_per_V":l1,
        "independent_analytic_l1_per_V":l1a,
        "point_settling_voltage_limit_V":vtol,
        "recommended_randomized_dwell_s":max(dwells) if overall=="PASS" and dwells else None,
        "step_classes":results,
    }

def main():
    p=argparse.ArgumentParser();p.add_argument("input_csv");p.add_argument("--output-json")
    ns=p.parse_args();out=assess(load(ns.input_csv));txt=json.dumps(out,sort_keys=True,indent=2)+"\n"
    if ns.output_json:Path(ns.output_json).write_text(txt,encoding="utf-8")
    else:sys.stdout.write(txt)
    return 0 if out["overall_status"]=="PASS" else 2
if __name__=="__main__":raise SystemExit(main())
