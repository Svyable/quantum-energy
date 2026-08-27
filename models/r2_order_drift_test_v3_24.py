#!/usr/bin/env python3
from __future__ import annotations
import math,statistics,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import r2_order_drift_v3_24 as m

def analytic_quadratic_alias(phi,quad_pp_V):
    x=[math.log(v) for v in phi]; il=m.nearest(phi,m.LOW); ih=m.nearest(phi,m.HIGH)
    A=quad_pp_V/2.0; span=x[-1]-x[0]
    return 8.0*A*(x[ih]-x[il])/(span*span*m.KB*m.T_K)

def main():
    rows,phi,base=m.synthetic_rows(noise_sd_V=0.0)
    true=m.curvature(phi,phi,base)
    linear_only=m.monotonic_bias(phi,base,linear_pp_V=0.002,quad_pp_V=0.0)
    if abs(linear_only)>1e-10: raise AssertionError(linear_only)
    numeric=m.monotonic_bias(phi,base,linear_pp_V=0.002,quad_pp_V=0.001)
    analytic=analytic_quadratic_alias(phi,0.001)
    if abs(numeric-analytic)>1e-12: raise AssertionError((numeric,analytic))
    corrected=m.analyze(rows)['curvature']
    if abs(corrected-true)>1e-9: raise AssertionError((corrected,true))

    n=400; covered=0; abs_bias=[]
    for k in range(n):
        rr,pp,bb=m.synthetic_rows(seed=700000+k,noise_sd_V=0.0002)
        out=m.analyze(rr); truth=m.curvature(pp,pp,bb); b=out['curvature']-truth
        abs_bias.append(abs(b))
        covered += abs(b) <= 1.96*out['curvature_u_1sigma']
    coverage=covered/n; p95=sorted(abs_bias)[int(0.95*n)-1]
    if not (0.91 <= coverage <= 0.99): raise AssertionError(('coverage',coverage))
    if p95>0.012: raise AssertionError(('p95_abs_bias',p95))

    diag=m.schedule_diagnostics(m.schedule())
    if diag['max_mean_rank_deviation']>1e-12: raise AssertionError(diag)
    print(f'true_curvature={true:.12g}')
    print(f'linear_only_monotonic_bias={linear_only:.12g}')
    print(f'quadratic_monotonic_bias_numeric={numeric:.12g}')
    print(f'quadratic_monotonic_bias_analytic={analytic:.12g}')
    print(f'randomized_noise_free_bias={corrected-true:.12g}')
    print(f'mc_replicates={n}')
    print(f'mc_95_interval_coverage={coverage:.6f}')
    print(f'mc_p95_abs_bias={p95:.12g}')
    print('PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
