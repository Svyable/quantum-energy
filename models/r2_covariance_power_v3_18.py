#!/usr/bin/env python3
"""Covariance-aware uncertainty propagation for R2 local-ideality curvature (v3.18).

Scientific boundary:
- propagates declared measurement/calibration uncertainty through the frozen
  local-ideality curvature estimator;
- does not infer a recombination mechanism;
- first-order covariance propagation is a local approximation and must be
  checked against Monte Carlo when nonlinearity is material.
"""
from __future__ import annotations
import argparse, csv, json, math, sys
from collections import defaultdict
from pathlib import Path

KB_EV_PER_K = 8.617333262e-5
T_K = 300.0
WINDOW = 7
LOW_SUN = 0.1
HIGH_SUN = 1.0
PLANNING_EFFECT = 0.10
Z_CRIT = 1.959963984540054

RAW_REQUIRED = {
    "sweep_id","sweep_direction","sequence_index","target_suns","calibrated_suns",
    "calibration_relative_u_1sigma","calibration_correlation_group",
    "voc_V","voc_u_V","anchor_flag","qc_status",
    "source_spectrum_id","spectral_mismatch_u_rel"
}
COMP_REQUIRED = {
    "sweep_id","sequence_index","variable","component_id",
    "loading_1sigma","unit","note"
}

def as_bool(v: str) -> bool:
    return str(v).strip().lower() in {"1","true","yes","y"}

def f(v: str) -> float | None:
    s=str(v).strip()
    return None if s=="" else float(s)

def solve3(A, y):
    m=[list(r)+[v] for r,v in zip(A,y)]
    for c in range(3):
        p=max(range(c,3), key=lambda r: abs(m[r][c]))
        m[c],m[p]=m[p],m[c]
        s=m[c][c]
        if abs(s)<1e-18:
            raise ValueError("singular local quadratic")
        for j in range(c,4):
            m[c][j]/=s
        for r in range(3):
            if r==c:
                continue
            q=m[r][c]
            for j in range(c,4):
                m[r][j]-=q*m[c][j]
    return [m[i][3] for i in range(3)]

def nearest(values, target):
    return min(range(len(values)), key=lambda i: abs(values[i]-target))

def local_weights(phi, anchor_idx, window=WINDOW):
    """Exact linear weights mapping Voc values [V] to local n_id [1]."""
    order=sorted(range(len(phi)), key=lambda i: phi[i])
    p=[phi[i] for i in order]
    anchor_sorted=order.index(anchor_idx)
    x=[math.log(v) for v in p]
    half=window//2
    lo=max(0, min(anchor_sorted-half, len(x)-window))
    hi=lo+window
    u=[x[j]-x[anchor_sorted] for j in range(lo,hi)]
    S=[sum(v**k for v in u) for k in range(5)]
    A=[[S[0],S[1],S[2]],[S[1],S[2],S[3]],[S[2],S[3],S[4]]]
    weights=[0.0]*len(phi)
    for loc, sorted_col in enumerate(range(lo,hi)):
        rhs=[u[loc]**k for k in range(3)]
        beta=solve3(A,rhs)
        weights[order[sorted_col]]=beta[1]/(KB_EV_PER_K*T_K)
    return weights

def curvature_weights(target_suns, calibrated_suns):
    """Freeze anchor row identities from target_suns; fit x from calibrated_suns."""
    il=nearest(target_suns, LOW_SUN)
    ih=nearest(target_suns, HIGH_SUN)
    wl=local_weights(calibrated_suns, il)
    wh=local_weights(calibrated_suns, ih)
    return [b-a for a,b in zip(wl,wh)], il, ih

def curvature(target_suns, calibrated_suns, voc):
    w,_,_=curvature_weights(target_suns, calibrated_suns)
    return sum(a*b for a,b in zip(w,voc))

def axis_jacobian(target_suns, calibrated_suns, voc, eps=1e-6):
    """d(curvature)/d ln(calibrated_suns_i), centered finite difference."""
    out=[]
    for i in range(len(calibrated_suns)):
        pp=list(calibrated_suns); pm=list(calibrated_suns)
        pp[i]*=math.exp(eps); pm[i]*=math.exp(-eps)
        out.append(
            (curvature(target_suns,pp,voc)-curvature(target_suns,pm,voc))/(2*eps)
        )
    return out

def power_two_sided(effect, se):
    if se<=0:
        return 1.0
    cdf=lambda z: 0.5*(1.0+math.erf(z/math.sqrt(2.0)))
    mu=abs(effect)/se
    return cdf(-Z_CRIT-mu)+1.0-cdf(Z_CRIT-mu)

def load_raw(path):
    with open(path,newline="",encoding="utf-8") as h:
        rd=csv.DictReader(h)
        missing=sorted(RAW_REQUIRED-set(rd.fieldnames or []))
        rows=list(rd)
    if missing:
        raise ValueError("missing raw columns: "+", ".join(missing))
    if not rows:
        raise ValueError("empty raw CSV")
    return rows

def load_components(path):
    with open(path,newline="",encoding="utf-8") as h:
        rd=csv.DictReader(h)
        missing=sorted(COMP_REQUIRED-set(rd.fieldnames or []))
        rows=list(rd)
    if missing:
        raise ValueError("missing component columns: "+", ".join(missing))
    return rows

def sweep_rows(rows):
    out=defaultdict(list)
    for r in rows:
        if as_bool(r.get("anchor_flag","false")):
            continue
        if r.get("qc_status","").strip().upper() not in {"PASS","PENDING"}:
            continue
        out[r["sweep_id"]].append(r)
    for sid in out:
        out[sid].sort(key=lambda r: float(r["target_suns"]))
    return out

def raw_axis_components(rows):
    """Interpret v3.17 scalar uncertainties as one latent per declared group."""
    comps=defaultdict(dict)
    for r in rows:
        key=int(r["sequence_index"])
        u=f(r["calibration_relative_u_1sigma"])
        g=r.get("calibration_correlation_group","").strip()
        if u is not None and g:
            comps[("ln_calibrated_suns","cal:"+g)][key]=u
        su=f(r.get("spectral_mismatch_u_rel",""))
        sid=r.get("source_spectrum_id","").strip()
        if su is not None and sid:
            comps[("ln_calibrated_suns","spectral:"+sid)][key]=su
    return comps

def sidecar_axis_components(component_rows, sweep_id):
    comps=defaultdict(dict)
    for r in component_rows:
        if r["sweep_id"] != sweep_id:
            continue
        var=r["variable"].strip()
        if var not in {"ln_calibrated_suns","voc_V"}:
            raise ValueError("unsupported component variable: "+var)
        unit=r["unit"].strip()
        if var=="ln_calibrated_suns" and unit not in {"1","fraction","dimensionless"}:
            raise ValueError("ln_calibrated_suns component must be dimensionless")
        if var=="voc_V" and unit!="V":
            raise ValueError("voc_V component must use V")
        comps[(var,r["component_id"].strip())][int(r["sequence_index"])]=float(r["loading_1sigma"])
    return comps

def component_contributions(rows, component_rows=None):
    target=[float(r["target_suns"]) for r in rows]
    cal=[float(r["calibrated_suns"]) for r in rows]
    voc=[float(r["voc_V"]) for r in rows]
    seq=[int(r["sequence_index"]) for r in rows]
    idx={q:i for i,q in enumerate(seq)}
    w, il, ih=curvature_weights(target,cal)
    j=axis_jacobian(target,cal,voc)

    sidecar=sidecar_axis_components(component_rows,rows[0]["sweep_id"]) if component_rows is not None else None
    comps=defaultdict(dict)
    explicit_voc = sidecar is not None and any(k[0]=="voc_V" for k in sidecar)
    if not explicit_voc:
        for r in rows:
            u=f(r["voc_u_V"])
            if u is not None:
                q=int(r["sequence_index"])
                comps[("voc_V","voc_point:"+str(q))][q]=u

    if sidecar is None:
        for k,v in raw_axis_components(rows).items():
            comps[k].update(v)
    else:
        for k,v in sidecar.items():
            comps[k].update(v)

    contributions=[]
    total_var=0.0
    for (var,cid), loadmap in sorted(comps.items()):
        sens=w if var=="voc_V" else j
        projection=0.0
        used=0
        for q,loading in loadmap.items():
            if q in idx:
                projection += sens[idx[q]]*loading
                used += 1
        varc=projection*projection
        total_var += varc
        contributions.append({
            "variable":var,
            "component_id":cid,
            "n_rows":used,
            "signed_output_loading_1sigma":projection,
            "variance_contribution":varc,
            "sd_contribution_abs":abs(projection),
        })
    return {
        "sweep_id":rows[0]["sweep_id"],
        "direction":rows[0].get("sweep_direction",""),
        "n_points":len(rows),
        "curvature":curvature(target,cal,voc),
        "low_anchor_target_suns":target[il],
        "high_anchor_target_suns":target[ih],
        "curvature_u_1sigma":math.sqrt(total_var),
        "planning_power_effect_0p10":power_two_sided(PLANNING_EFFECT,math.sqrt(total_var)),
        "components":contributions,
        "axis_jacobian_sum":sum(j),
        "axis_jacobian_eps":1e-6,
    }

def assess(raw_rows, component_rows=None):
    by=sweep_rows(raw_rows)
    if not by:
        raise ValueError("no non-anchor sweeps")
    sweeps=[component_contributions(rows,component_rows) for _,rows in sorted(by.items())]
    worst=max(sweeps,key=lambda d:d["curvature_u_1sigma"])
    return {
        "schema_version":"r2-covariance-power-v3.18",
        "claim_boundary":"Uncertainty propagation qualifies precision of the declared curvature measurement only; it does not identify a recombination mechanism, EPC, or open-quantum transport.",
        "uncertainty_source_mode":"v3.18-components-sidecar" if component_rows is not None else "v3.17-raw-groups",
        "method":{
            "linear_covariance":"u_y^2 = g^T C g, represented as sum of squared latent-component projections",
            "axis_derivative":"centered finite difference in ln(calibrated_suns), eps=1e-6",
            "power":"two-sided normal planning power, alpha=0.05, effect=0.10",
            "correlation_rule":"Rows sharing a component_id are perfectly correlated through one latent standard-normal component with signed per-row loadings.",
        },
        "sweeps":sweeps,
        "power_model_inputs":{
            "worst_sweep_curvature_u_1sigma":worst["curvature_u_1sigma"],
            "worst_sweep_power_effect_0p10":worst["planning_power_effect_0p10"],
            "no_sqrtN_credit_for_sweep_repeats":True,
        },
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("input_csv")
    p.add_argument("--components")
    p.add_argument("--output-json")
    ns=p.parse_args()
    comp=load_components(ns.components) if ns.components else None
    result=assess(load_raw(ns.input_csv),comp)
    txt=json.dumps(result,sort_keys=True,indent=2)+"\n"
    if ns.output_json:
        Path(ns.output_json).write_text(txt,encoding="utf-8",newline="\n")
    else:
        sys.stdout.write(txt)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
