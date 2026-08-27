#!/usr/bin/env python3
from __future__ import annotations
import copy,math,random,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import r2_absolute_systematic_budget_v3_21 as b
import r2_covariance_power_v3_18 as cov

ROOT=Path(__file__).resolve().parents[1]
FIX=ROOT/"models"/"fixtures"
RAW=FIX/"r2_covariance_fixture_v3_18.csv"
META=FIX/"r2_absolute_systematic_components_v3_21.csv"
SHAPES=FIX/"r2_absolute_systematic_shapes_v3_21.csv"

def load():
    return cov.load_raw(RAW), b.load_csv(META,b.META_REQUIRED), b.load_csv(SHAPES,b.SHAPE_REQUIRED)

def sd(v):
    m=sum(v)/len(v)
    return math.sqrt(sum((x-m)**2 for x in v)/(len(v)-1))

def axis_mc(raw,meta,shapes,reps=12000,seed=20260826):
    result=b.assess(raw,meta,shapes)
    corrected=result["corrected_rows"]
    side=result["sidecar_rows"]
    rows=[r for r in corrected if not cov.as_bool(r["anchor_flag"])]
    rows.sort(key=lambda r:float(r["target_suns"]))
    target=[float(r["target_suns"]) for r in rows]
    cal=[float(r["calibrated_suns"]) for r in rows]
    voc=[float(r["voc_V"]) for r in rows]
    seq=[r["sequence_index"] for r in rows]
    comps={}
    for r in side:
        comps.setdefault(r["component_id"],{})[r["sequence_index"]]=float(r["loading_1sigma"])
    rng=random.Random(seed)
    vals=[]
    for _ in range(reps):
        z={k:rng.gauss(0,1) for k in comps}
        pert=[]
        for q,p in zip(seq,cal):
            d=sum(comps[k].get(q,0.0)*z[k] for k in comps)
            pert.append(p*math.exp(d))
        vals.append(cov.curvature(target,pert,voc))
    return sd(vals)

def main():
    raw,meta,shapes=load()
    r=b.assess(raw,meta,shapes)
    s=r["sweeps"][0]
    exp={
      "correction_delta_curvature":0.002088789592134488,
      "abs_systematic_curvature_u_1sigma":0.0033673385387834737,
      "combined_curvature_u_1sigma_including_voc":0.02267761878965914,
      "planning_power_effect_0p10":0.9928506416958767,
    }
    for k,v in exp.items():
        if not math.isclose(s[k],v,rel_tol=1e-10,abs_tol=1e-11):
            raise AssertionError((k,s[k],v))
    cm={x["component_id"]:x["standard_u_1sigma"] for x in r["components"]}
    assert math.isclose(cm["responsivity_scale"],0.002,abs_tol=1e-15)
    assert math.isclose(cm["linearity_stretch"],0.0015/math.sqrt(3),abs_tol=1e-15)
    assert math.isclose(cm["spectral_shape"],0.004/math.sqrt(6),abs_tol=1e-15)

    # Limiting case: common multiplicative intensity scale is a constant shift
    # in ln(Phi), so it must not create derivative curvature.
    m2=copy.deepcopy(meta)
    for x in m2:
        x["uncertainty_value"]="0"; x["correction_ln_amplitude"]="0"
        if x["component_id"]=="responsivity_scale":
            x["uncertainty_value"]="0.01"; x["uncertainty_kind"]="standard_normal"
    rc=b.assess(raw,m2,shapes)
    u=rc["sweeps"][0]["abs_systematic_curvature_u_1sigma"]
    if u>1e-8: raise AssertionError(("common scale did not cancel",u))

    # Independent nonlinear propagation through the full curvature estimator.
    mc=axis_mc(raw,meta,shapes)
    lin=s["abs_systematic_curvature_u_1sigma"]
    rel=abs(mc-lin)/lin
    if rel>0.03: raise AssertionError(("MC mismatch",lin,mc,rel))

    # Sensitivity: double only the dominant spectral-shape uncertainty.
    m3=copy.deepcopy(meta)
    for x in m3:
        if x["component_id"]=="spectral_shape":
            x["uncertainty_value"]=str(2*float(x["uncertainty_value"]))
    r2=b.assess(raw,m3,shapes)["sweeps"][0]
    if not (r2["abs_systematic_curvature_u_1sigma"]>1.9*lin):
        raise AssertionError("spectral-shape sensitivity not dominant")
    print(f"linear_axis_u={lin:.12g}")
    print(f"mc_axis_u={mc:.12g}")
    print(f"relative_difference={rel:.6g}")
    print(f"double_spectral_axis_u={r2['abs_systematic_curvature_u_1sigma']:.12g}")
    print(f"double_spectral_combined_power={r2['planning_power_effect_0p10']:.12g}")
    print("PASS")
if __name__=="__main__": main()
