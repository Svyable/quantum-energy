#!/usr/bin/env python3
"""R2 v3.39 dummy-package logger bandwidth qualification.

Standard-library only. This is an engineering qualification calculator, not an
experimental result. It evaluates first-order temperature/RH step-response time
constants and conservative acceleration pulse capture against the machine contract.
"""
from __future__ import annotations
import argparse, csv, json, math, statistics
from pathlib import Path


def fit_tau_known_endpoints(times, values, y0, yinf, t0=0.0):
    """Estimate tau by linearizing ln((y-yinf)/(y0-yinf)) = -(t-t0)/tau.

    Uses only interior points with a physically valid positive normalized residual.
    Returns tau [s] and RMS residual in y units.
    """
    xs=[]; zs=[]
    denom=y0-yinf
    if denom == 0:
        raise ValueError('zero step amplitude')
    for t,y in zip(times,values):
        r=(y-yinf)/denom
        if t>t0 and 0<r<1:
            xs.append(t-t0); zs.append(math.log(r))
    if len(xs)<2:
        raise ValueError('insufficient interior points')
    # through-origin physical model after endpoint normalization
    slope=sum(x*z for x,z in zip(xs,zs))/sum(x*x for x in xs)
    if slope>=0:
        raise ValueError('non-decaying response')
    tau=-1.0/slope
    pred=[yinf+(y0-yinf)*math.exp(-(t-t0)/tau) for t in times]
    rms=math.sqrt(sum((a-b)**2 for a,b in zip(values,pred))/len(values))
    return tau,rms


def tau_pairwise(times, values, yinf):
    """Independent tau cross-check from point pairs: tau=-(dt)/ln(r2/r1)."""
    vals=[]
    for i in range(len(times)-1):
        a=values[i]-yinf; b=values[i+1]-yinf
        if a*b>0 and abs(b)<abs(a) and times[i+1]>times[i]:
            vals.append(-(times[i+1]-times[i])/math.log(abs(b/a)))
    if not vals:
        raise ValueError('no valid pairwise tau estimates')
    return statistics.median(vals)


def conservative_peak_ratio(a_logger,u_logger,a_ref,u_ref):
    if any(x<0 for x in (u_logger,u_ref)) or a_ref<=0:
        raise ValueError('invalid uncertainty/reference amplitude')
    return max(0.0,(a_logger-u_logger)/(a_ref+u_ref))


def derived_gap(tau_min,samples_per_tau=5):
    if tau_min<=0 or samples_per_tau<=0:
        raise ValueError('positive inputs required')
    return tau_min/samples_per_tau


def self_test():
    # Synthetic exact first-order thermal fixture: tau=120 s, 20->40 C.
    tau_true=120.0; y0=20.0; yinf=40.0
    times=[0,30,60,120,240,360]
    values=[yinf+(y0-yinf)*math.exp(-t/tau_true) for t in times]
    tau,rms=fit_tau_known_endpoints(times,values,y0,yinf)
    tau2=tau_pairwise(times,values,yinf)
    assert abs(tau-tau_true)<1e-10, (tau,tau_true)
    assert abs(tau2-tau_true)<1e-10, (tau2,tau_true)
    assert rms<1e-12
    gap=derived_gap(tau)
    assert abs(gap-24.0)<1e-12

    # Limiting/sign checks.
    try: fit_tau_known_endpoints([0,1,2],[1,1.1,1.2],1,0)
    except ValueError: pass
    else: raise AssertionError('non-decay should fail')
    assert abs(conservative_peak_ratio(1.0,0.0,1.0,0.0)-1.0)<1e-15
    r=conservative_peak_ratio(0.95,0.03,1.0,0.02)
    assert abs(r-(0.92/1.02))<1e-15
    assert r>0.90
    r_fail=conservative_peak_ratio(0.94,0.03,1.0,0.02)
    assert r_fail<0.90

    # Sensitivity: slower sensor -> larger permissible gap; fastest qualified tau governs.
    taus=[60.0,120.0,300.0]
    gaps=[derived_gap(t) for t in taus]
    assert gaps==[12.0,24.0,60.0]
    assert derived_gap(min(taus))==12.0

    # Dimensional check encoded numerically: seconds / dimensionless = seconds.
    assert isinstance(derived_gap(100.0,5),float) and derived_gap(100.0,5)==20.0
    print('synthetic_tau_primary_s=120')
    print('synthetic_tau_independent_s=120')
    print('synthetic_gap_max_s=24')
    print(f'synthetic_accel_conservative_pass_ratio={r:.12g}')
    print(f'synthetic_accel_conservative_fail_ratio={r_fail:.12g}')
    print('PASS')


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--self-test',action='store_true')
    args=p.parse_args()
    if args.self_test:
        self_test(); return 0
    p.error('Only --self-test is implemented in v3.39; real-data ingestion is frozen by the CSV schema for a later hardware run.')

if __name__=='__main__':
    raise SystemExit(main())
