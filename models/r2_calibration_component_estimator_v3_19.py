#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,math,statistics,sys
from collections import defaultdict
from pathlib import Path
REPEAT_REQUIRED={"session_id","sweep_id","sequence_index","target_suns","calibrated_suns","qc_status"}
RAW_REQUIRED={"sweep_id","sequence_index","target_suns","anchor_flag","qc_status"}
GRID_RTOL=1e-6; MIN_SWEEPS=8; MIN_SESSIONS=3

def f(v): return float(str(v).strip())
def b(v): return str(v).strip().lower() in {"1","true","yes","y"}
def load_csv(path,required):
    with open(path,newline="",encoding="utf-8") as h:
        rd=csv.DictReader(h); miss=sorted(required-set(rd.fieldnames or [])); rows=list(rd)
    if miss: raise ValueError("missing columns: "+", ".join(miss))
    if not rows: raise ValueError("empty CSV")
    return rows

def basis(target):
    x=[math.log(v) for v in target]; xm=statistics.fmean(x); z0=[v-xm for v in x]; scale=max(abs(v) for v in z0)
    if scale<=0: raise ValueError("degenerate target grid")
    z=[v/scale for v in z0]; q0=[v*v for v in z]; qm=statistics.fmean(q0); q=[v-qm for v in q0]
    zz=sum(v*v for v in z); proj=sum(a*c for a,c in zip(q,z))/zz; q=[a-proj*c for a,c in zip(q,z)]
    return z,q

def fit_coeff(target,cal):
    z,q=basis(target); e=[math.log(c/t) for t,c in zip(target,cal)]
    a=statistics.fmean(e); bb=sum(v*y for v,y in zip(z,e))/sum(v*v for v in z); cc=sum(v*y for v,y in zip(q,e))/sum(v*v for v in q)
    pred=[a+bb*zi+cc*qi for zi,qi in zip(z,q)]; return [a,bb,cc],[y-p for y,p in zip(e,pred)]

def covariance(rows):
    n=len(rows); p=len(rows[0]); mu=[statistics.fmean(r[j] for r in rows) for j in range(p)]
    return [[sum((r[i]-mu[i])*(r[j]-mu[j]) for r in rows)/(n-1) for j in range(p)] for i in range(p)],mu

def cholesky_psd(A,tol=1e-18):
    n=len(A); L=[[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1):
            s=A[i][j]-sum(L[i][k]*L[j][k] for k in range(j))
            if i==j:
                if s < -tol: raise ValueError("coefficient covariance is not PSD")
                L[i][j]=math.sqrt(max(0.0,s))
            else: L[i][j]=0.0 if abs(L[j][j])<tol else s/L[j][j]
    return L

def pooled_within_covariance(coefs,sessions):
    groups=defaultdict(list)
    for c,sid in zip(coefs,sessions): groups[sid].append(c)
    J=len(groups); N=len(coefs)
    if J<MIN_SESSIONS: raise ValueError(f"need >= {MIN_SESSIONS} calibration sessions")
    if any(len(v)<2 for v in groups.values()): raise ValueError("need >=2 PASS sweeps per calibration session")
    C=[[0.0]*3 for _ in range(3)]
    for vals in groups.values():
        mu=[statistics.fmean(r[j] for r in vals) for j in range(3)]
        for r in vals:
            for i in range(3):
                for j in range(3): C[i][j]+=(r[i]-mu[i])*(r[j]-mu[j])
    den=N-J
    return [[v/den for v in row] for row in C],groups

def session_intercept_variance(coefs,sessions):
    groups=defaultdict(list)
    for c,sid in zip(coefs,sessions): groups[sid].append(c[0])
    J=len(groups); N=len(coefs); overall=statistics.fmean(c[0] for c in coefs)
    msw=sum(sum((v-statistics.fmean(vals))**2 for v in vals) for vals in groups.values())/(N-J)
    msb=sum(len(vals)*(statistics.fmean(vals)-overall)**2 for vals in groups.values())/(J-1)
    n0=(N-sum(len(vals)**2 for vals in groups.values())/N)/(J-1)
    return max(0.0,(msb-msw)/n0),msw,msb,n0

def collect_repeats(rows):
    by=defaultdict(list)
    for r in rows:
        if r["qc_status"].strip().upper()=="PASS": by[r["sweep_id"]].append(r)
    if len(by)<MIN_SWEEPS: raise ValueError(f"need >= {MIN_SWEEPS} PASS calibration sweeps")
    parsed=[]; ref=None
    for sid,rr in sorted(by.items()):
        rr=sorted(rr,key=lambda r:f(r["target_suns"])); t=[f(r["target_suns"]) for r in rr]; c=[f(r["calibrated_suns"]) for r in rr]
        sessions={r["session_id"].strip() for r in rr}
        if len(sessions)!=1 or not next(iter(sessions)): raise ValueError("each sweep must belong to exactly one nonempty session_id")
        session=next(iter(sessions))
        if any(x<=0 for x in t+c): raise ValueError("intensities must be >0")
        if ref is None: ref=t
        if len(t)!=len(ref) or any(abs(a-b)>GRID_RTOL*max(abs(a),abs(b),1e-12) for a,b in zip(t,ref)): raise ValueError("calibration sweeps do not share one target grid")
        parsed.append((session,sid,t,c))
    if len(ref)<7: raise ValueError("need >=7 target intensities")
    return ref,parsed

def estimate(repeat_rows):
    target,parsed=collect_repeats(repeat_rows); coefs=[]; residuals=[]; sessions=[]
    for session,_,t,c in parsed:
        cf,res=fit_coeff(t,c); coefs.append(cf); residuals.append(res); sessions.append(session)
    C_within,groups=pooled_within_covariance(coefs,sessions); L=cholesky_psd(C_within); z,q=basis(target); B=[[1.0,zi,qi] for zi,qi in zip(z,q)]
    smooth=[[sum(B[i][j]*L[j][k] for j in range(3)) for i in range(len(target))] for k in range(3)]
    session_var,msw,msb,n0=session_intercept_variance(coefs,sessions); session_sd=math.sqrt(session_var)
    n=len(target); zz=sum(v*v for v in z); qq=sum(v*v for v in q)
    leverage=[1/n+zi*zi/zz+qi*qi/qq for zi,qi in zip(z,q)]
    raw_resid_sd=[statistics.stdev(r[i] for r in residuals) for i in range(n)]
    point_sd=[sd/math.sqrt(max(1e-12,1-h)) for sd,h in zip(raw_resid_sd,leverage)]
    mu=[statistics.fmean(r[j] for r in coefs) for j in range(3)]
    return {"schema_version":"r2-calibration-components-v3.19","status":"PASS","n_pass_sweeps":len(parsed),"n_sessions":len(groups),"n_grid_points":len(target),"target_suns":target,
      "basis":{"z":z,"q":q,"leverage":leverage},"coefficient_mean_ln_ratio":{"common":mu[0],"stretch":mu[1],"quadratic":mu[2]},"within_session_coefficient_covariance":C_within,"within_session_coefficient_cholesky":L,
      "session_common_scale_sd_ln":session_sd,"session_anova":{"MS_within":msw,"MS_between":msb,"n0":n0},"smooth_mode_loadings":smooth,"point_residual_sd_ln":point_sd,
      "method_note":"Between-session common-scale variance uses a one-way random-effects ANOVA moment estimate. Within-session common/stretch/quadratic covariance is retained by Cholesky latent modes. Point residual SD is leverage-corrected and treated as independent after low-order removal; that diagonal residual assumption must be challenged with real facility data.",
      "claim_boundary":"These are empirical calibration-error components from repeated reference sweeps. They quantify the declared calibration model only and are not mechanism evidence."}

def nearest_grid(target,value):
    j=min(range(len(target)),key=lambda i:abs(target[i]-value))
    if abs(target[j]-value)>GRID_RTOL*max(abs(value),abs(target[j]),1e-12): raise ValueError(f"raw target_suns {value} not represented in calibration grid")
    return j

def write_components(report,raw_rows,path):
    if report["status"]!="PASS": raise ValueError("estimator status is not PASS; refuse sidecar generation")
    out=[]
    for r in raw_rows:
        if b(r["anchor_flag"]) or r["qc_status"].strip().upper() not in {"PASS","PENDING"}: continue
        j=nearest_grid(report["target_suns"],f(r["target_suns"])); sid=r["sweep_id"]; seq=r["sequence_index"]
        out.append([sid,seq,"ln_calibrated_suns","cal_empirical_session_scale",report["session_common_scale_sd_ln"],"1","between-session common scale from random-effects ANOVA"])
        for k,loads in enumerate(report["smooth_mode_loadings"],1): out.append([sid,seq,"ln_calibrated_suns",f"cal_empirical_within_smooth_{k}",loads[j],"1","within-session covariance mode from repeated calibration sweeps"])
        out.append([sid,seq,"ln_calibrated_suns",f"cal_empirical_residual:{sid}:{seq}",report["point_residual_sd_ln"][j],"1","leverage-corrected diagonal point residual"])
    with open(path,"w",newline="",encoding="utf-8") as h:
        wr=csv.writer(h); wr.writerow(["sweep_id","sequence_index","variable","component_id","loading_1sigma","unit","note"]); wr.writerows(out)

def main():
    p=argparse.ArgumentParser(); p.add_argument("calibration_repeats_csv"); p.add_argument("--apply-to"); p.add_argument("--output-components"); p.add_argument("--output-json"); ns=p.parse_args()
    if bool(ns.apply_to)!=bool(ns.output_components): p.error("--apply-to and --output-components must be supplied together")
    report=estimate(load_csv(ns.calibration_repeats_csv,REPEAT_REQUIRED))
    if ns.apply_to: write_components(report,load_csv(ns.apply_to,RAW_REQUIRED),ns.output_components)
    txt=json.dumps(report,sort_keys=True,indent=2)+"\n"
    if ns.output_json: Path(ns.output_json).write_text(txt,encoding="utf-8",newline="\n")
    else: sys.stdout.write(txt)
    return 0 if report["status"]=="PASS" else 2
if __name__=="__main__": raise SystemExit(main())
