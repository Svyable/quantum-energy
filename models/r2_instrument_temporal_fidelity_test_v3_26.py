#!/usr/bin/env python3
from __future__ import annotations
import math, random, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import r2_instrument_temporal_fidelity_v3_26 as m

A=0.100
TAU=0.200
DELAY=0.050
TIMES=[0,0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0,2.5,3.0]

def rows(tau=TAU, delay=DELAY, reps=8, autorange=False, seed=20260827):
    rng=random.Random(seed); out=[]
    for j in range(reps):
        for t in TIMES:
            age=max(0.0,t-delay)
            resid=-A*math.exp(-age/tau)
            noise=rng.gauss(0,1.0e-6)
            out.append({'replicate_id':f'R{j+1}','elapsed_s':str(t),'commanded_V':'0.1',
              'measured_V':repr(0.1+resid+noise),'timestamp_u_s':'0.0005',
              'reference_step_u_V':'0.0000005','range_id':'100mV','filter_id':'fixed-1kHz',
              'aperture_s':'0.001','autorange_enabled':'true' if autorange else 'false','qc_status':'PASS'})
    return out

def main():
    # Independent first-order limiting-case dwell: delay + tau ln(A/limit).
    analytic=DELAY+TAU*math.log(A/m.INSTRUMENT_LIMIT_V)
    expected=1.5032424657756777
    if abs(analytic-expected)>1e-12: raise AssertionError((analytic,expected))

    clean=m.assess(rows())
    if clean['overall_status']!='PASS': raise AssertionError(clean)
    if clean['qualified_instrument_dwell_s'] < analytic:
        raise AssertionError((clean['qualified_instrument_dwell_s'],analytic))
    if clean['qualified_instrument_dwell_s'] > 2.0:
        raise AssertionError('unexpectedly slow qualified dwell')

    slow=m.assess(rows(tau=2.0))
    if slow['overall_status']!='FAIL' or 'instrument_residual_not_settled' not in slow['failed_gates']:
        raise AssertionError(slow)

    few=m.assess(rows(reps=5))
    if few['overall_status']!='INCOMPLETE': raise AssertionError(few)

    auto=m.assess(rows(autorange=True))
    if auto['overall_status']!='FAIL' or 'autorange_enabled' not in auto['failed_gates']:
        raise AssertionError(auto)

    # Known limiting case: zero residual at all times is immediately qualified even with fixed absolute offset.
    z=rows();
    for r in z: r['measured_V']=r['commanded_V']
    zz=m.assess(z)
    if zz['qualified_instrument_dwell_s'] != 0.0: raise AssertionError(zz)

    # Numerical diagnostic tau should recover the injected value within 2%; it is not the PASS criterion.
    tau=clean['first_order_tau_diagnostic_s']
    if tau is None or abs(tau-TAU)/TAU>0.02: raise AssertionError(tau)

    print(f'instrument_limit_uV={m.INSTRUMENT_LIMIT_V*1e6:.9f}')
    print(f'analytic_min_dwell_s={analytic:.12g}')
    print(f'sampled_qualified_dwell_s={clean["qualified_instrument_dwell_s"]:.12g}')
    print(f'fit_tau_s={tau:.12g}')
    print('PASS')
    return 0

if __name__=='__main__': raise SystemExit(main())
