#!/usr/bin/env python3
"""Wavelength-resolved spectral-mismatch gate for the R2 Voc-intensity path (v3.23).

This tool evaluates intensity-dependent source-spectrum shape against explicit
reference- and DUT-responsivity curves. It does not infer a DUT mechanism.
All uncertainty components are represented as signed log-space latent modes.
"""
from __future__ import annotations
import argparse,csv,json,math,random,statistics,sys
from collections import defaultdict
from pathlib import Path

KB_EV_PER_K=8.617333262e-5
T_K=300.0
WINDOW=7
LOW_SUN=0.1
HIGH_SUN=1.0

def nearest(values,target):
    return min(range(len(values)),key=lambda i:abs(values[i]-target))

def solve3(A,y):
    m=[list(r)+[v] for r,v in zip(A,y)]
    for c in range(3):
        q=max(range(c,3),key=lambda r:abs(m[r][c])); m[c],m[q]=m[q],m[c]
        z=m[c][c]
        if abs(z)<1e-18: raise ValueError("singular local quadratic")
        for j in range(c,4): m[c][j]/=z
        for r in range(3):
            if r==c: continue
            f=m[r][c]
            for j in range(c,4): m[r][j]-=f*m[c][j]
    return [m[i][3] for i in range(3)]

def local_weights(phi,anchor_idx):
    order=sorted(range(len(phi)),key=lambda i:phi[i]); p=[phi[i] for i in order]; a=order.index(anchor_idx)
    x=[math.log(v) for v in p]; h=WINDOW//2; lo=max(0,min(a-h,len(x)-WINDOW)); hi=lo+WINDOW
    u=[x[j]-x[a] for j in range(lo,hi)]; S=[sum(v**k for v in u) for k in range(5)]
    A=[[S[0],S[1],S[2]],[S[1],S[2],S[3]],[S[2],S[3],S[4]]]; out=[0.0]*len(phi)
    for loc,j in enumerate(range(lo,hi)):
        beta=solve3(A,[u[loc]**k for k in range(3)])
        out[order[j]]=beta[1]/(KB_EV_PER_K*T_K)
    return out

def curvature_weights(target,axis):
    il=nearest(target,LOW_SUN); ih=nearest(target,HIGH_SUN); wl=local_weights(axis,il); wh=local_weights(axis,ih)
    return [b-a for a,b in zip(wl,wh)]

def curvature(target,axis,voc):
    return sum(a*b for a,b in zip(curvature_weights(target,axis),voc))

def axis_jacobian(target,axis,voc,eps=1e-6):
    out=[]
    for i in range(len(axis)):
        pp=list(axis); pm=list(axis); pp[i]*=math.exp(eps); pm[i]*=math.exp(-eps)
        out.append((curvature(target,pp,voc)-curvature(target,pm,voc))/(2*eps))
    return out

REQ_SPECTRA={"spectrum_id","target_suns","wavelength_nm","spectral_irradiance_W_m2_nm"}
REQ_RESP={"wavelength_nm","reference_responsivity_A_W","dut_responsivity_A_W"}
REQ_COMP={"component_id","quantity","spectrum_id","wavelength_nm","loading_1sigma","note"}
SMM_DEV_LIMIT=0.01
CURV_BIAS_LIMIT=0.01
CURV_U_LIMIT=0.01
STRESS_CURVATURE=0.10
FD_EPS=1e-4
MC_DRAWS=12000
MC_SEED=20260827
MC_TOL_REL=0.03


def load_csv(path, required):
    with open(path,newline="",encoding="utf-8") as h:
        rd=csv.DictReader(h); missing=sorted(required-set(rd.fieldnames or [])); rows=list(rd)
    if missing: raise ValueError("missing columns: "+", ".join(missing))
    if not rows: raise ValueError("empty CSV: "+str(path))
    return rows


def trapz(w,y):
    return sum((w[i+1]-w[i])*(y[i+1]+y[i])*0.5 for i in range(len(w)-1))


def load_inputs(spectra_path,resp_path,comp_path):
    sr=load_csv(spectra_path,REQ_SPECTRA); rr=load_csv(resp_path,REQ_RESP); cr=load_csv(comp_path,REQ_COMP)
    by=defaultdict(list); targets={}
    for r in sr:
        sid=r["spectrum_id"].strip(); t=float(r["target_suns"]); wl=float(r["wavelength_nm"]); e=float(r["spectral_irradiance_W_m2_nm"])
        if t<=0 or e<0: raise ValueError("target_suns must be >0 and spectral irradiance >=0")
        if sid in targets and not math.isclose(targets[sid],t,rel_tol=0,abs_tol=1e-12): raise ValueError("one target_suns required per spectrum_id")
        targets[sid]=t; by[sid].append((wl,e))
    resp=[]
    for r in rr:
        wl=float(r["wavelength_nm"]); a=float(r["reference_responsivity_A_W"]); b=float(r["dut_responsivity_A_W"])
        if a<0 or b<0: raise ValueError("responsivity must be >=0")
        resp.append((wl,a,b))
    resp.sort(); w=[x[0] for x in resp]; ref=[x[1] for x in resp]; dut=[x[2] for x in resp]
    if len(w)<5 or any(w[i+1]<=w[i] for i in range(len(w)-1)): raise ValueError("responsivity wavelength grid must be strictly increasing with >=5 points")
    spectra={}
    for sid,pts in by.items():
        pts.sort(); ws=[x[0] for x in pts]
        if ws!=w: raise ValueError(f"spectrum {sid} wavelength grid must exactly match responsivity grid")
        spectra[sid]=[x[1] for x in pts]
    comps=defaultdict(dict)
    allowed={"source_ln","reference_responsivity_ln","dut_responsivity_ln"}
    for r in cr:
        cid=r["component_id"].strip(); q=r["quantity"].strip(); sid=r["spectrum_id"].strip() or "*"; wl=float(r["wavelength_nm"]); val=float(r["loading_1sigma"])
        if not cid or q not in allowed: raise ValueError("invalid component_id/quantity")
        if wl not in w: raise ValueError(f"component wavelength {wl} not on spectral grid")
        comps[(cid,q,sid)][wl]=val
    return w,ref,dut,spectra,targets,comps


def mismatch(E,E0,ref,dut,w):
    a=trapz(w,[x*y for x,y in zip(E,dut)])
    b=trapz(w,[x*y for x,y in zip(E,ref)])
    c=trapz(w,[x*y for x,y in zip(E0,ref)])
    d=trapz(w,[x*y for x,y in zip(E0,dut)])
    if min(a,b,c,d)<=0: raise ValueError("spectral integrals must be positive")
    return (a/b)*(c/d)


def apply_component(w,ref,dut,spectra,comps,cid,z):
    r=list(ref); d=list(dut); ss={k:list(v) for k,v in spectra.items()}
    for (cc,q,sid),load in comps.items():
        if cc!=cid: continue
        vec=[load.get(x,0.0) for x in w]
        if q=="reference_responsivity_ln":
            if sid!="*": raise ValueError("responsivity components must use spectrum_id='*'")
            r=[x*math.exp(z*a) for x,a in zip(r,vec)]
        elif q=="dut_responsivity_ln":
            if sid!="*": raise ValueError("responsivity components must use spectrum_id='*'")
            d=[x*math.exp(z*a) for x,a in zip(d,vec)]
        else:
            ids=ss.keys() if sid=="*" else [sid]
            for s in ids:
                if s not in ss: raise ValueError("component references unknown spectrum_id "+s)
                ss[s]=[x*math.exp(z*a) for x,a in zip(ss[s],vec)]
    return r,d,ss


def nominal_smm(w,ref,dut,spectra,targets,reference_id):
    E0=spectra[reference_id]
    return {sid:mismatch(E,E0,ref,dut,w) for sid,E in spectra.items()}


def component_smm_loadings(w,ref,dut,spectra,targets,comps,reference_id):
    cids=sorted(set(k[0] for k in comps)); out={}
    for cid in cids:
        rp,dp,sp=apply_component(w,ref,dut,spectra,comps,cid,FD_EPS)
        rm,dm,sm=apply_component(w,ref,dut,spectra,comps,cid,-FD_EPS)
        mp=nominal_smm(w,rp,dp,sp,targets,reference_id); mm=nominal_smm(w,rm,dm,sm,targets,reference_id)
        out[cid]={sid:(math.log(mp[sid])-math.log(mm[sid]))/(2*FD_EPS) for sid in spectra}
    return out


def synthetic_voc(target):
    x=[math.log(v) for v in target]; il=nearest(target,LOW_SUN); ih=nearest(target,HIGH_SUN)
    beta=STRESS_CURVATURE/(x[ih]-x[il])
    return [KB_EV_PER_K*T_K*(xx+0.5*beta*xx*xx) for xx in x]


def ordered(targets):
    return sorted(targets,key=lambda sid:targets[sid])


def shape_rms(E,E0,w):
    a=trapz(w,E); b=trapz(w,E0)
    en=[x/a for x in E]; e0=[x/b for x in E0]
    mean=1.0/(w[-1]-w[0])
    return math.sqrt(statistics.fmean(((x-y)/mean)**2 for x,y in zip(en,e0)))


def curvature_metrics(targets,smm,loadings):
    ids=ordered(targets); target=[targets[s] for s in ids]; m=[smm[s] for s in ids]; eff=[a*b for a,b in zip(target,m)]
    voc=synthetic_voc(target)
    truth=curvature(target,target,voc); measured=curvature(target,eff,voc); bias=measured-truth
    j=axis_jacobian(target,eff,voc)
    contrib=[]; var=0.0
    for cid,vals in sorted(loadings.items()):
        l=[vals[s] for s in ids]; proj=sum(a*b for a,b in zip(j,l)); vv=proj*proj; var+=vv
        contrib.append({"component_id":cid,"curvature_loading_1sigma":proj,"variance_contribution":vv,"max_abs_ln_smm_loading":max(abs(x) for x in l)})
    return ids,target,eff,truth,measured,bias,math.sqrt(var),contrib


def monte_carlo(w,ref,dut,spectra,targets,comps,reference_id,draws=MC_DRAWS,seed=MC_SEED):
    rng=random.Random(seed); cids=sorted(set(k[0] for k in comps)); ids=ordered(targets); target=[targets[s] for s in ids]; voc=synthetic_voc(target); vals=[]
    for _ in range(draws):
        rr=list(ref); dd=list(dut); ss={k:list(v) for k,v in spectra.items()}
        for cid in cids:
            z=rng.gauss(0.0,1.0); rr,dd,ss=apply_component(w,rr,dd,ss,comps,cid,z)
        mm=nominal_smm(w,rr,dd,ss,targets,reference_id); eff=[targets[s]*mm[s] for s in ids]
        vals.append(curvature(target,eff,voc))
    mu=statistics.fmean(vals); return statistics.stdev(vals),mu


def assess(spectra_path,resp_path,comp_path,reference_id=None,run_mc=False,sweep_id="SPECTRAL"):
    w,ref,dut,spectra,targets,comps=load_inputs(spectra_path,resp_path,comp_path)
    if reference_id is None: reference_id=min(targets,key=lambda s:abs(targets[s]-1.0))
    if reference_id not in spectra: raise ValueError("unknown reference spectrum_id")
    smm=nominal_smm(w,ref,dut,spectra,targets,reference_id); loads=component_smm_loadings(w,ref,dut,spectra,targets,comps,reference_id)
    ids,target,eff,truth,measured,bias,u,contrib=curvature_metrics(targets,smm,loads)
    dev=max(abs(smm[s]-1.0) for s in ids); srms=max(shape_rms(spectra[s],spectra[reference_id],w) for s in ids)
    gates={
        "spectral_mismatch_deviation":{"status":"PASS" if dev<=SMM_DEV_LIMIT else "FAIL","value":dev,"limit":SMM_DEV_LIMIT,"unit":"fraction"},
        "spectral_curvature_bias":{"status":"PASS" if abs(bias)<=CURV_BIAS_LIMIT else "FAIL","value":bias,"limit":CURV_BIAS_LIMIT,"unit":"dimensionless"},
        "spectral_curvature_u_1sigma":{"status":"PASS" if u<=CURV_U_LIMIT else "FAIL","value":u,"limit":CURV_U_LIMIT,"unit":"dimensionless"},
    }
    mc=None
    if run_mc:
        mcu,mcm=monte_carlo(w,ref,dut,spectra,targets,comps,reference_id); rel=abs(mcu-u)/u if u>0 else (0.0 if mcu<1e-12 else math.inf)
        gates["linearization_mc"]={"status":"PASS" if rel<=MC_TOL_REL else "FAIL","value":rel,"limit":MC_TOL_REL,"unit":"fraction"}
        mc={"draws":MC_DRAWS,"seed":MC_SEED,"curvature_u_1sigma":mcu,"curvature_mean":mcm,"relative_difference_vs_first_order":rel}
    overall="FAIL" if any(g["status"]=="FAIL" for g in gates.values()) else "PASS"
    sidecar=[]
    for cid,vals in sorted(loads.items()):
        for seq,s in enumerate(ids,1):
            sidecar.append({"sweep_id":sweep_id,"sequence_index":seq,"variable":"ln_calibrated_suns","component_id":"spectral:"+cid,"loading_1sigma":vals[s],"unit":"1","note":f"v3.23 wavelength-resolved SMM; target_suns={targets[s]:.12g}"})
    return {
        "schema_version":"r2-spectral-shape-gate-v3.23",
        "claim_boundary":"PASS qualifies wavelength-resolved source-spectrum/mismatch behavior for the declared reference+DUT responsivities only; it is not mechanism evidence.",
        "reference_spectrum_id":reference_id,
        "wavelength_nm":{"min":w[0],"max":w[-1],"n_points":len(w)},
        "overall_status":overall,"gates":gates,
        "metrics":{"max_normalized_shape_rms":srms,"synthetic_truth_curvature":truth,"synthetic_smm_distorted_curvature":measured,"synthetic_curvature_bias":bias,"spectral_curvature_u_1sigma":u},
        "spectra":[{"spectrum_id":s,"target_suns":targets[s],"spectral_mismatch_factor":smm[s],"effective_dut_suns":targets[s]*smm[s],"normalized_shape_rms_vs_reference":shape_rms(spectra[s],spectra[reference_id],w)} for s in ids],
        "uncertainty_components":contrib,
        "monte_carlo":mc,
        "sidecar_rows":sidecar,
        "method":{"spectral_mismatch":"M=(int Es Rt/int Es Rr)*(int Eref Rr/int Eref Rt)","effective_axis":"Phi_eff=Phi_reference*M","first_order_uncertainty":"latent log-space spectral/responsivity components -> dlnM/dz -> v3.18 axis Jacobian","fd_eps":FD_EPS},
    }


def main():
    p=argparse.ArgumentParser(); p.add_argument("spectra_csv"); p.add_argument("responsivity_csv"); p.add_argument("components_csv"); p.add_argument("--reference-spectrum-id"); p.add_argument("--sweep-id",default="SPECTRAL"); p.add_argument("--monte-carlo",action="store_true"); p.add_argument("--output-json"); p.add_argument("--output-sidecar")
    ns=p.parse_args(); d=assess(ns.spectra_csv,ns.responsivity_csv,ns.components_csv,ns.reference_spectrum_id,ns.monte_carlo,ns.sweep_id)
    txt=json.dumps(d,sort_keys=True,indent=2)+"\n"; (Path(ns.output_json).write_text(txt,encoding="utf-8") if ns.output_json else sys.stdout.write(txt))
    if ns.output_sidecar:
        with open(ns.output_sidecar,"w",newline="",encoding="utf-8") as h:
            f=csv.DictWriter(h,fieldnames=["sweep_id","sequence_index","variable","component_id","loading_1sigma","unit","note"]); f.writeheader(); f.writerows(d["sidecar_rows"])
    return 0 if d["overall_status"]=="PASS" else 2
if __name__=="__main__": raise SystemExit(main())
