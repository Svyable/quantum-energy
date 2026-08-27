#!/usr/bin/env python3
from __future__ import annotations
import csv,json,math,random,statistics,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import r2_calibration_component_estimator_v3_19 as e
try:
    import r2_covariance_power_v3_18 as c
except ImportError:
    c=None
SEED=20260826
N_SESSIONS=12
SWEEPS_PER_SESSION=5
N_SWEEPS=N_SESSIONS*SWEEPS_PER_SESSION
SESSION_SD=0.0025
COMMON_SD=0.0015
STRETCH_SD=0.0012
QUAD_SD=0.0018
POINT_SD=0.0008
CORR=[[1.0,0.4,0.1],[0.4,1.0,-0.2],[0.1,-0.2,1.0]]

def mvn3(rng):
    scales=[COMMON_SD,STRETCH_SD,QUAD_SD]
    C=[[CORR[i][j]*scales[i]*scales[j] for j in range(3)] for i in range(3)]
    L=e.cholesky_psd(C); z=[rng.gauss(0,1) for _ in range(3)]
    return [sum(L[i][k]*z[k] for k in range(i+1)) for i in range(3)]

def grid(n=17):
    r=(2.0/0.05)**(1/(n-1)); return [0.05*r**i for i in range(n)]

def synth_rows():
    rng=random.Random(SEED); t=grid(); z,q=e.basis(t); rows=[]; sweep=0
    for sess in range(N_SESSIONS):
        session_shift=rng.gauss(0,SESSION_SD)
        for _ in range(SWEEPS_PER_SESSION):
            sweep+=1; a,b,c0=mvn3(rng); a+=session_shift
            for i,(tt,zz,qq) in enumerate(zip(t,z,q),1):
                eps=a+b*zz+c0*qq+rng.gauss(0,POINT_SD)
                rows.append({"session_id":f"SES{sess+1:02d}","sweep_id":f"CAL{sweep:03d}","sequence_index":str(i),"target_suns":repr(tt),"calibrated_suns":repr(tt*math.exp(eps)),"qc_status":"PASS"})
    return rows

def reconstruct(L):
    return [[sum(L[i][k]*L[j][k] for k in range(3)) for j in range(3)] for i in range(3)]

def axis_direct_u(report,jac):
    z=report['basis']['z']; q=report['basis']['q']; C=report['within_session_coefficient_covariance']; B=[sum(jac),sum(g*zz for g,zz in zip(jac,z)),sum(g*qq for g,qq in zip(jac,q))]
    var=(sum(jac)*report['session_common_scale_sd_ln'])**2 + sum(B[i]*C[i][j]*B[j] for i in range(3) for j in range(3))
    var += sum((g*u)**2 for g,u in zip(jac,report['point_residual_sd_ln']))
    return math.sqrt(var)

def axis_sidecar_u(report,jac):
    var=(sum(jac)*report['session_common_scale_sd_ln'])**2 + sum(sum(g*l for g,l in zip(jac,mode))**2 for mode in report['smooth_mode_loadings'])
    var += sum((g*u)**2 for g,u in zip(jac,report['point_residual_sd_ln']))
    return math.sqrt(var)

def mc_u(report,target,voc,reps=10000):
    rng=random.Random(SEED+1); L=report['within_session_coefficient_cholesky']; z=report['basis']['z']; q=report['basis']['q']; vals=[]
    for _ in range(reps):
        zz=[rng.gauss(0,1) for _ in range(3)]
        coef=[sum(L[i][k]*zz[k] for k in range(i+1)) for i in range(3)]
        coef[0]+=rng.gauss(0,report['session_common_scale_sd_ln'])
        pp=[]
        for i,t in enumerate(target):
            eps=coef[0]+coef[1]*z[i]+coef[2]*q[i]+rng.gauss(0,report['point_residual_sd_ln'][i])
            pp.append(t*math.exp(eps))
        vals.append(c.curvature(target,pp,voc))
    return statistics.stdev(vals)

def main():
    if c is None: raise RuntimeError('r2_covariance_power_v3_18 import unavailable')
    report=e.estimate(synth_rows())
    L=report['within_session_coefficient_cholesky']; R=reconstruct(L); C=report['within_session_coefficient_covariance']
    err=max(abs(R[i][j]-C[i][j]) for i in range(3) for j in range(3))
    if err>1e-15: raise AssertionError(('cholesky reconstruction',err))
    est_sd=[math.sqrt(C[i][i]) for i in range(3)]; true_sd=[COMMON_SD,STRETCH_SD,QUAD_SD]
    rel=[abs(a-b)/b for a,b in zip(est_sd,true_sd)]
    if max(rel)>0.30: raise AssertionError(('known-mode recovery',est_sd,rel))
    if abs(report['session_common_scale_sd_ln']-SESSION_SD)/SESSION_SD>0.40: raise AssertionError(('session recovery',report['session_common_scale_sd_ln']))
    med_res=statistics.median(report['point_residual_sd_ln'])
    if abs(med_res-POINT_SD)/POINT_SD>0.20: raise AssertionError(('point residual recovery',med_res))
    target=grid(); x=[math.log(v) for v in target]; il=c.nearest(target,0.1); ih=c.nearest(target,1.0); beta=0.10/(x[ih]-x[il])
    voc=[c.KB_EV_PER_K*c.T_K*(xx+0.5*beta*xx*xx) for xx in x]
    jac=c.axis_jacobian(target,target,voc)
    u1=axis_sidecar_u(report,jac); u2=axis_direct_u(report,jac)
    if abs(u1-u2)>1e-12: raise AssertionError(('direct covariance mismatch',u1,u2))
    umc=mc_u(report,target,voc)
    if abs(umc-u1)/u1>0.05: raise AssertionError(('MC mismatch',u1,umc))
    print(json.dumps({"seed":SEED,"n_sessions":N_SESSIONS,"n_sweeps":N_SWEEPS,"estimated_session_sd":report['session_common_scale_sd_ln'],"estimated_sd_common":est_sd[0],"estimated_sd_stretch":est_sd[1],"estimated_sd_quadratic":est_sd[2],"median_point_residual_sd":med_res,"curvature_axis_u_linear":u1,"curvature_axis_u_mc":umc,"mc_draws":10000},sort_keys=True,indent=2))
    print('PASS')
if __name__=='__main__': main()
