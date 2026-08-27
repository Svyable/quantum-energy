#!/usr/bin/env python3
"""Independent synthetic checks for r2_covariance_power_v3_18."""
from __future__ import annotations
import math, random, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import r2_covariance_power_v3_18 as m

def grid(n=17):
    r=(2.0/0.05)**(1/(n-1))
    return [0.05*r**i for i in range(n)]

def rows(voc_u=0.0005):
    phi=grid()
    x=[math.log(v) for v in phi]
    il=m.nearest(phi,0.1); ih=m.nearest(phi,1.0)
    beta=0.10/(x[ih]-x[il])
    voc=[m.KB_EV_PER_K*m.T_K*(xx+0.5*beta*xx*xx) for xx in x]
    out=[]
    for i,(p,v) in enumerate(zip(phi,voc),1):
        out.append({
            "sweep_id":"SYN","sweep_direction":"ascending","sequence_index":str(i),
            "target_suns":repr(p),"calibrated_suns":repr(p),
            "calibration_relative_u_1sigma":"0","calibration_correlation_group":"",
            "voc_V":repr(v),"voc_u_V":repr(voc_u),"anchor_flag":"false",
            "qc_status":"PASS","source_spectrum_id":"SYN","spectral_mismatch_u_rel":"0"
        })
    return out

def sidecar(loadings, variable="ln_calibrated_suns", prefix="mode"):
    return [{
        "sweep_id":"SYN","sequence_index":str(i+1),"variable":variable,
        "component_id":prefix if not isinstance(prefix,list) else prefix[i],
        "loading_1sigma":repr(loadings[i]),"unit":"V" if variable=="voc_V" else "1",
        "note":"synthetic"
    } for i in range(len(loadings))]

def analytic(rows0, comps):
    return m.assess(rows0,comps)["sweeps"][0]["curvature_u_1sigma"]

def mc_axis(rows0, loading, reps=12000, seed=20260826):
    phi=[float(r["calibrated_suns"]) for r in rows0]
    target=[float(r["target_suns"]) for r in rows0]
    voc=[float(r["voc_V"]) for r in rows0]
    rng=random.Random(seed)
    vals=[]
    for _ in range(reps):
        z=rng.gauss(0,1)
        pp=[p*math.exp(a*z) for p,a in zip(phi,loading)]
        vals.append(m.curvature(target,pp,voc))
    mu=sum(vals)/len(vals)
    return math.sqrt(sum((v-mu)**2 for v in vals)/(len(vals)-1))

def main():
    rr=rows(voc_u=0.0)
    n=len(rr)
    common=[0.005]*n
    x=[math.log(float(r["target_suns"])) for r in rr]
    xn=[(v-sum(x)/n)/max(abs(q-sum(x)/n) for q in x) for v in x]
    quad=[0.005*v*v for v in xn]
    indep_ids=[f"pt{i}" for i in range(n)]

    u_common=analytic(rr,sidecar(common,prefix="common"))
    u_quad=analytic(rr,sidecar(quad,prefix="quad"))
    u_ind=analytic(rr,sidecar([0.005]*n,prefix=indep_ids))
    mc_quad=mc_axis(rr,quad)

    if u_common > 1e-8:
        raise AssertionError(f"common scale should cancel: {u_common}")
    if not (0.005 < u_ind < 0.006):
        raise AssertionError(f"independent axis uncertainty unexpected: {u_ind}")
    if not (0.006 < u_quad < 0.007):
        raise AssertionError(f"quadratic shape uncertainty unexpected: {u_quad}")
    if abs(u_quad-mc_quad)/u_quad > 0.04:
        raise AssertionError(f"linear covariance vs MC mismatch: {u_quad} vs {mc_quad}")

    rr_v=rows(voc_u=0.0005)
    raw=m.assess(rr_v,None)["sweeps"][0]
    expected=m.curvature_weights(
        [float(r["target_suns"]) for r in rr_v],
        [float(r["calibrated_suns"]) for r in rr_v]
    )[0]
    exact=math.sqrt(sum(w*w for w in expected))*0.0005
    if abs(raw["curvature_u_1sigma"]-exact)>1e-12:
        raise AssertionError((raw["curvature_u_1sigma"],exact))

    target=[float(r["target_suns"]) for r in rr]
    phi=[float(r["calibrated_suns"]) for r in rr]
    voc=[float(r["voc_V"]) for r in rr]
    j1=m.axis_jacobian(target,phi,voc,1e-6)
    j2=m.axis_jacobian(target,phi,voc,5e-7)
    if max(abs(a-b) for a,b in zip(j1,j2))>2e-7:
        raise AssertionError("axis Jacobian did not converge")

    print(f"common_scale_u={u_common:.12g}")
    print(f"independent_axis_u={u_ind:.12g}")
    print(f"quadratic_shape_u={u_quad:.12g}")
    print(f"quadratic_shape_mc_u={mc_quad:.12g}")
    print(f"voc_0p5mV_u={raw['curvature_u_1sigma']:.12g}")
    print(f"voc_0p5mV_power={raw['planning_power_effect_0p10']:.12g}")
    print("PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
