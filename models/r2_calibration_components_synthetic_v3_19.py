#!/usr/bin/env python3
"""Deterministic synthetic/independent checks for v3.19 calibration decomposition."""
from __future__ import annotations
import math, random, copy, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import r2_calibration_components_v3_19 as c
import r2_covariance_power_v3_18 as u

SEED=20260826
TRUE_MEAN=(0.003,0.0015,0.0025)
TRUE_SD=(0.0010,0.0008,0.0006)
TRUE_POINT=0.0007
N_RUNS=24
N_POINTS=17


def synthetic_rows():
    rng=random.Random(SEED)
    phi=[0.05*(2.0/0.05)**(i/(N_POINTS-1)) for i in range(N_POINTS)]
    _,z,q,_=c.basis(phi)
    rows=[]
    for s in range(N_RUNS):
        a=TRUE_MEAN[0]+rng.gauss(0,TRUE_SD[0]); b=TRUE_MEAN[1]+rng.gauss(0,TRUE_SD[1]); cc=TRUE_MEAN[2]+rng.gauss(0,TRUE_SD[2])
        for i,p in enumerate(phi,1):
            e=a+b*z[i-1]+cc*q[i-1]+rng.gauss(0,TRUE_POINT)
            rows.append({'calibration_run_id':f'CAL-{s+1:02d}','sequence_index':str(i),'target_suns':repr(p),'calibrated_suns':repr(p*math.exp(e)),'reference_detector_id':'REF-SYN','qc_status':'PASS'})
    return rows


def direct_orthogonal_coeffs(rows):
    runs,target,_=c.group_runs(rows); _,z,q,_=c.basis(target)
    zz=sum(v*v for v in z); qq=sum(v*v for v in q); out=[]
    for rid,rr,_t,cal in runs:
        e=[math.log(x/t) for x,t in zip(cal,target)]
        out.append([sum(e)/len(e),sum(a*b for a,b in zip(e,z))/zz,sum(a*b for a,b in zip(e,q))/qq])
    return out


def main():
    rows=synthetic_rows(); result,target,fit=c.assess(rows)
    if result['overall_status']!='PASS': raise AssertionError(result)
    if result['n_runs']!=24 or result['n_points']!=17: raise AssertionError('count mismatch')
    expected_mean=[0.0032675399470160453,0.0015346758283856898,0.002554235070210397]
    got=[result['systematic_mean_coefficients_ln_axis'][k] for k in ('scale','stretch','quadratic')]
    if max(abs(a-b) for a,b in zip(got,expected_mean))>2e-14: raise AssertionError((got,expected_mean))
    expected_sd=[0.0008545192385496123,0.0007706828369580998,0.0005174055059946188]
    got_sd=[result['repeatability']['coefficient_sd'][k] for k in ('scale','stretch','quadratic')]
    if max(abs(a-b) for a,b in zip(got_sd,expected_sd))>2e-14: raise AssertionError((got_sd,expected_sd))
    if abs(result['repeatability']['pooled_point_residual_sd_ln_axis']-0.0007203222868709043)>2e-14: raise AssertionError('residual SD drift')
    if abs(result['heldout_validation']['coverage_95']-0.9485294117647058)>1e-14: raise AssertionError('coverage drift')
    if abs(result['heldout_validation']['normalized_rmse']-1.0465124301895217)>2e-14: raise AssertionError('LOSO drift')
    direct=direct_orthogonal_coeffs(rows)
    if max(abs(a-b) for aa,bb in zip(direct,fit['betas']) for a,b in zip(aa,bb))>3e-15: raise AssertionError('independent coefficient path mismatch')
    for est,true in zip(got_sd,TRUE_SD):
        if not (0.5*true <= est <= 1.5*true): raise AssertionError(('poor synthetic recovery',est,true))
    if not (0.5*TRUE_POINT <= result['repeatability']['pooled_point_residual_sd_ln_axis'] <= 1.5*TRUE_POINT): raise AssertionError('point recovery')
    five=[r for r in rows if int(r['calibration_run_id'].split('-')[1])<=5]
    five_result=c.assess(five); five_result=five_result[0] if isinstance(five_result,tuple) else five_result
    if five_result['overall_status']!='INCOMPLETE': raise AssertionError('insufficient-run gate failed')
    bad=copy.deepcopy(rows); _,z,_,_=c.basis(target); lookup={round(p,15):v for p,v in zip(target,z)}
    for r in bad:
        zz=lookup[round(float(r['target_suns']),15)]
        r['calibrated_suns']=repr(float(r['calibrated_suns'])*math.exp(0.003*zz**3))
    bad_result=c.assess(bad); bad_result=bad_result[0] if isinstance(bad_result,tuple) else bad_result
    if bad_result['overall_status']!='INCOMPLETE' or not any('systematic mean residual' in s for s in bad_result['reasons']): raise AssertionError('unmodeled-shape gate failed')
    mixed=copy.deepcopy(rows); mixed[-1]['reference_detector_id']='REF-OTHER'
    try: c.assess(mixed)
    except ValueError: pass
    else: raise AssertionError('mixed detector IDs should fail')
    root=Path(__file__).resolve().parent
    raw=u.load_raw(root/'fixtures'/'r2_covariance_fixture_v3_18.csv')
    comp=[]
    for rr in c.sidecar_rows(target,fit,'SYN'):
        comp.append(dict(zip(['sweep_id','sequence_index','variable','component_id','loading_1sigma','unit','note'],map(str,rr))))
    out=u.assess(raw,comp); sw=out['sweeps'][0]
    if not (0.0224 < sw['curvature_u_1sigma'] < 0.0225): raise AssertionError(sw['curvature_u_1sigma'])
    if not (0.9935 < sw['planning_power_effect_0p10'] < 0.9938): raise AssertionError(sw['planning_power_effect_0p10'])
    print(f"mean_scale={got[0]:.12g} mean_stretch={got[1]:.12g} mean_quadratic={got[2]:.12g}")
    print(f"sd_scale={got_sd[0]:.12g} sd_stretch={got_sd[1]:.12g} sd_quadratic={got_sd[2]:.12g}")
    print(f"point_residual_sd={result['repeatability']['pooled_point_residual_sd_ln_axis']:.12g}")
    print(f"loso_coverage95={result['heldout_validation']['coverage_95']:.12g} loso_nrmse={result['heldout_validation']['normalized_rmse']:.12g}")
    print(f"v318_combined_u={sw['curvature_u_1sigma']:.12g} v318_power={sw['planning_power_effect_0p10']:.12g}")
    print('PASS')
    return 0

if __name__=='__main__': raise SystemExit(main())
