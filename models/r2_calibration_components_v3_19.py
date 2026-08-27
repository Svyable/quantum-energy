#!/usr/bin/env python3
"""Estimate empirical calibration covariance modes from repeated reference sweeps.

The estimator separates:
- systematic mean calibration shape (correction target, not random uncertainty),
- between-run coefficient covariance in an orthogonal [scale, stretch, quadratic] basis,
- pooled point residual uncertainty,
then emits a v3.18 signed-component sidecar for a future sweep.

Claim boundary: this estimates repeatability covariance from the supplied calibration
runs. It cannot infer the absolute systematic uncertainty of the reference detector
or prove that the chosen basis spans all real facility errors.
"""
from __future__ import annotations
import argparse, csv, json, math, statistics, sys
from pathlib import Path

REQ={"calibration_run_id","sequence_index","target_suns","calibrated_suns","reference_detector_id","qc_status"}
MIN_RUNS=8


def solve3(A,y):
    m=[list(r)+[v] for r,v in zip(A,y)]
    for c in range(3):
        p=max(range(c,3), key=lambda r:abs(m[r][c]))
        m[c],m[p]=m[p],m[c]
        s=m[c][c]
        if abs(s)<1e-18: raise ValueError("singular 3x3 system")
        for j in range(c,4): m[c][j]/=s
        for r in range(3):
            if r==c: continue
            q=m[r][c]
            for j in range(c,4): m[r][j]-=q*m[c][j]
    return [m[i][3] for i in range(3)]


def inverse3(A):
    cols=[]
    for k in range(3):
        e=[0.0,0.0,0.0]; e[k]=1.0
        cols.append(solve3(A,e))
    return [[cols[j][i] for j in range(3)] for i in range(3)]


def cholesky3(A):
    L=[[0.0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(i+1):
            s=A[i][j]-sum(L[i][k]*L[j][k] for k in range(j))
            if i==j:
                if s<=1e-20: raise ValueError("adjusted coefficient covariance is not positive definite")
                L[i][j]=math.sqrt(s)
            else:
                L[i][j]=s/L[j][j]
    return L


def basis(target):
    x=[math.log(v) for v in target]
    xm=statistics.fmean(x)
    z0=[v-xm for v in x]
    scale=max(abs(v) for v in z0)
    z=[v/scale for v in z0]
    q0=[v*v for v in z]
    qm=statistics.fmean(q0)
    zz=sum(v*v for v in z)
    q1=[v-qm for v in q0]
    proj=sum(a*b for a,b in zip(q1,z))/zz
    q1=[a-proj*b for a,b in zip(q1,z)]
    qscale=max(abs(v) for v in q1)
    q=[v/qscale for v in q1]
    X=[[1.0,z[i],q[i]] for i in range(len(target))]
    return x,z,q,X


def normal_matrix(X):
    return [[sum(r[i]*r[j] for r in X) for j in range(3)] for i in range(3)]


def fit_coeff(X,y):
    A=normal_matrix(X)
    rhs=[sum(r[k]*yy for r,yy in zip(X,y)) for k in range(3)]
    return solve3(A,rhs)


def matvec(X,b):
    return [sum(r[j]*b[j] for j in range(3)) for r in X]


def sample_cov(rows):
    n=len(rows); p=len(rows[0]); means=[statistics.fmean(r[j] for r in rows) for j in range(p)]
    return [[sum((r[i]-means[i])*(r[j]-means[j]) for r in rows)/(n-1) for j in range(p)] for i in range(p)],means


def load(path):
    with open(path,newline="",encoding="utf-8") as h:
        rd=csv.DictReader(h); miss=sorted(REQ-set(rd.fieldnames or [])); rows=list(rd)
    if miss: raise ValueError("missing columns: "+", ".join(miss))
    if not rows: raise ValueError("empty calibration dataset")
    if any(r['qc_status'].strip().upper()!='PASS' for r in rows):
        raise ValueError("all calibration rows must have qc_status=PASS")
    return rows


def group_runs(rows):
    by={}
    for r in rows:
        rid=r['calibration_run_id'].strip()
        by.setdefault(rid,[]).append(r)
    out=[]; canonical=None; detector=None
    for rid in sorted(by):
        rr=sorted(by[rid], key=lambda r:float(r['target_suns']))
        target=[float(r['target_suns']) for r in rr]
        cal=[float(r['calibrated_suns']) for r in rr]
        if any(v<=0 for v in target+cal): raise ValueError("intensities must be positive")
        if canonical is None: canonical=target
        elif len(target)!=len(canonical) or max(abs(a-b) for a,b in zip(target,canonical))>1e-12:
            raise ValueError("all calibration runs must share one target grid")
        ids={r['reference_detector_id'].strip() for r in rr}
        if len(ids)!=1: raise ValueError("each run must use one reference detector")
        this=next(iter(ids))
        if detector is None: detector=this
        elif this!=detector: raise ValueError("v3.19 estimator requires one detector ID across runs")
        out.append((rid,rr,target,cal))
    return out,canonical,detector


def fit_dataset(runs,target):
    _,z,q,X=basis(target); A=normal_matrix(X); invA=inverse3(A)
    betas=[]; residuals=[]
    for rid,rr,_t,cal in runs:
        e=[math.log(c/t) for c,t in zip(cal,target)]
        b=fit_coeff(X,e); pred=matvec(X,b); res=[a-bb for a,bb in zip(e,pred)]
        betas.append(b); residuals.append(res)
    nrun=len(runs); npt=len(target)
    dof=nrun*(npt-3)
    sigma_res=math.sqrt(sum(v*v for rr in residuals for v in rr)/dof)
    obs_cov,mean_beta=sample_cov(betas)
    adj=[[obs_cov[i][j]-sigma_res*sigma_res*invA[i][j] for j in range(3)] for i in range(3)]
    L=cholesky3(adj)
    cor=[]
    for i in range(3):
        for j in range(i+1,3):
            den=math.sqrt(obs_cov[i][i]*obs_cov[j][j])
            cor.append(obs_cov[i][j]/den if den else 0.0)
    pairs=[(rr[i],rr[i+1]) for rr in residuals for i in range(npt-1)]
    if pairs:
        ma=statistics.fmean(x for x,_ in pairs); mb=statistics.fmean(y for _,y in pairs)
        den=math.sqrt(sum((a-ma)**2 for a,_ in pairs)*sum((b-mb)**2 for _,b in pairs))
        lag=sum((a-ma)*(b-mb) for a,b in pairs)/den if den else 0.0
    else: lag=0.0
    mean_res=math.sqrt(statistics.fmean(statistics.fmean(residuals[s][i] for s in range(nrun))**2 for i in range(npt)))
    return {'z':z,'q':q,'X':X,'invA':invA,'betas':betas,'residuals':residuals,'sigma_res':sigma_res,'obs_cov':obs_cov,'adj_cov':adj,'mean_beta':mean_beta,'L':L,'max_abs_observed_coeff_corr':max(abs(v) for v in cor) if cor else 0.0,'mean_residual_rms':mean_res,'pooled_residual_lag1_corr':lag}


def predictive_variance(Xrow,adj_cov,sigma_res):
    v=sum(Xrow[i]*adj_cov[i][j]*Xrow[j] for i in range(3) for j in range(3))+sigma_res*sigma_res
    return max(v,0.0)


def loso(runs,target):
    errs=[]; vars_=[]; inside=0; total=0; fold_sds=[]
    for hold in range(len(runs)):
        train=[r for i,r in enumerate(runs) if i!=hold]
        try: fit=fit_dataset(train,target)
        except ValueError: continue
        _,_,_,X=basis(target)
        rid,rr,_t,cal=runs[hold]
        e=[math.log(c/t) for c,t in zip(cal,target)]
        pred=matvec(X,fit['mean_beta'])
        for xr,obs,mu in zip(X,e,pred):
            var=predictive_variance(xr,fit['adj_cov'],fit['sigma_res'])
            if var<=0: continue
            er=obs-mu; errs.append(er); vars_.append(var); total+=1
            if abs(er)<=1.96*math.sqrt(var): inside+=1
        fold_sds.append([math.sqrt(max(fit['adj_cov'][i][i],0.0)) for i in range(3)]+[fit['sigma_res']])
    if not vars_: return {'coverage_95':None,'normalized_rmse':None,'fold_component_sd_minmax':None}
    nr=math.sqrt(statistics.fmean((e*e)/v for e,v in zip(errs,vars_)))
    mins=[min(r[j] for r in fold_sds) for j in range(4)]
    maxs=[max(r[j] for r in fold_sds) for j in range(4)]
    return {'coverage_95':inside/total,'normalized_rmse':nr,'fold_component_sd_minmax':list(zip(mins,maxs))}


def sidecar_rows(target,fit,sweep_id):
    _,z,q,X=basis(target); rows=[]
    for k in range(3):
        cid=f"empirical_session_mode_{k+1}"
        for i,xr in enumerate(X,1):
            loading=sum(xr[j]*fit['L'][j][k] for j in range(3))
            rows.append([sweep_id,i,'ln_calibrated_suns',cid,loading,'1','estimated between-run calibration mode'])
    for i in range(1,len(target)+1):
        rows.append([sweep_id,i,'ln_calibrated_suns',f'empirical_point_residual_{i}',fit['sigma_res'],'1','pooled independent point residual'])
    return rows


def assess(rows):
    runs,target,detector=group_runs(rows)
    status='PASS'; reasons=[]
    if len(runs)<MIN_RUNS:
        status='INCOMPLETE'; reasons.append(f'need >= {MIN_RUNS} independent calibration runs')
    try: fit=fit_dataset(runs,target)
    except ValueError as e:
        return {'schema_version':'r2-calibration-components-v3.19','overall_status':'INCOMPLETE','reasons':[str(e)]}
    val=loso(runs,target)
    if val['coverage_95'] is not None:
        if not (0.80<=val['coverage_95']<=1.0): status='INCOMPLETE'; reasons.append('LOSO 95% predictive coverage below 0.80')
        if not (0.6<=val['normalized_rmse']<=1.5): status='INCOMPLETE'; reasons.append('LOSO normalized RMSE outside planning band 0.6–1.5')
    if fit['max_abs_observed_coeff_corr']>0.80:
        status='INCOMPLETE'; reasons.append('basis coefficient correlation >0.80; richer/coupled model recommended')
    if fit['mean_residual_rms'] > 0.5*fit['sigma_res']:
        status='INCOMPLETE'; reasons.append('systematic mean residual shape exceeds 0.5x pooled residual SD')
    if abs(fit['pooled_residual_lag1_corr']) > 0.40:
        status='INCOMPLETE'; reasons.append('pooled residual lag-1 correlation exceeds 0.40; point-residual independence inadequate')
    return {'schema_version':'r2-calibration-components-v3.19','overall_status':status,'reasons':reasons,'claim_boundary':'Repeat-sweep decomposition estimates calibration repeatability covariance only; reference-detector absolute systematic uncertainty is not identifiable from repeats alone.','reference_detector_id':detector,'n_runs':len(runs),'n_points':len(target),'basis':{'stretch':'centered normalized ln(target_suns)','quadratic':'orthogonalized normalized stretch^2'},'systematic_mean_coefficients_ln_axis':{'scale':fit['mean_beta'][0],'stretch':fit['mean_beta'][1],'quadratic':fit['mean_beta'][2]},'repeatability':{'adjusted_coefficient_covariance':fit['adj_cov'],'coefficient_sd':{'scale':math.sqrt(fit['adj_cov'][0][0]),'stretch':math.sqrt(fit['adj_cov'][1][1]),'quadratic':math.sqrt(fit['adj_cov'][2][2])},'pooled_point_residual_sd_ln_axis':fit['sigma_res'],'max_abs_observed_coefficient_correlation':fit['max_abs_observed_coeff_corr'],'mean_residual_rms_ln_axis':fit['mean_residual_rms'],'mean_residual_rms_over_point_sd':fit['mean_residual_rms']/fit['sigma_res'],'pooled_residual_lag1_correlation':fit['pooled_residual_lag1_corr']},'heldout_validation':val,'identifiability':{'reference_detector_absolute_scale_systematic_estimated':False,'mean_shape_should_be_corrected_or_separately_budgeted':True,'sidecar_encodes_repeatability_not_absolute_reference_accuracy':True}},target,fit


def main():
    p=argparse.ArgumentParser(); p.add_argument('input_csv'); p.add_argument('--output-json'); p.add_argument('--output-sidecar'); p.add_argument('--sweep-id',default='FUTURE')
    ns=p.parse_args(); out=assess(load(ns.input_csv))
    if isinstance(out,tuple): result,target,fit=out
    else: result=out; target=fit=None
    txt=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if ns.output_json: Path(ns.output_json).write_text(txt,encoding='utf-8',newline='\n')
    else: sys.stdout.write(txt)
    if ns.output_sidecar:
        if fit is None: raise SystemExit('cannot emit sidecar from incomplete fit')
        with open(ns.output_sidecar,'w',newline='',encoding='utf-8') as h:
            w=csv.writer(h,lineterminator='\n'); w.writerow(['sweep_id','sequence_index','variable','component_id','loading_1sigma','unit','note']); w.writerows(sidecar_rows(target,fit,ns.sweep_id))
    return 0 if result.get('overall_status')=='PASS' else 2

if __name__=='__main__': raise SystemExit(main())
