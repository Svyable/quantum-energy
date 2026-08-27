#!/usr/bin/env python3
"""R2 v3.26 instrument-chain temporal fidelity gate.

Qualifies the electrical measurement path separately from DUT/source settling.
All default numerical limits are project engineering allocations, not NIST/IEC limits.
"""
from __future__ import annotations
import argparse, csv, json, math, statistics, sys
from collections import defaultdict
from pathlib import Path

SETTLING_ENVELOPE_V = 69.53691416753467e-6  # derived in open v3.25 work
INSTRUMENT_BUDGET_FRACTION = 0.20
INSTRUMENT_LIMIT_V = SETTLING_ENVELOPE_V * INSTRUMENT_BUDGET_FRACTION
Z95 = 1.959963984540054
MIN_REPLICATES = 6
MIN_TIMES = 6
MAX_AUTORANGE_TRUE = 0
REQ = {
    'replicate_id','elapsed_s','commanded_V','measured_V','timestamp_u_s',
    'reference_step_u_V','range_id','filter_id','aperture_s','autorange_enabled','qc_status'
}

def b(v): return str(v).strip().lower() in {'1','true','yes','y'}

def load(path):
    with open(path,newline='',encoding='utf-8') as h:
        rd=csv.DictReader(h); missing=sorted(REQ-set(rd.fieldnames or [])); rows=list(rd)
    if missing: raise ValueError('missing columns: '+', '.join(missing))
    if not rows: raise ValueError('empty input')
    return rows

def sem(xs):
    if len(xs)<2: return math.inf
    return statistics.stdev(xs)/math.sqrt(len(xs))

def first_order_tau(times, residuals):
    pairs=[(t,abs(r)) for t,r in zip(times,residuals) if abs(r)>0]
    if len(pairs)<3: return None
    x=[p[0] for p in pairs]; y=[math.log(p[1]) for p in pairs]
    xm=statistics.fmean(x); ym=statistics.fmean(y); sxx=sum((v-xm)**2 for v in x)
    if sxx<=0: return None
    slope=sum((a-xm)*(c-ym) for a,c in zip(x,y))/sxx
    return None if slope>=0 else -1.0/slope

def assess(rows):
    good=[r for r in rows if r['qc_status'].strip().upper()=='PASS']
    reps=sorted(set(r['replicate_id'] for r in good))
    times=sorted(set(float(r['elapsed_s']) for r in good))
    inc=[]; fail=[]
    if len(reps)<MIN_REPLICATES: inc.append('replicate_count')
    if len(times)<MIN_TIMES: inc.append('elapsed_time_count')
    ranges=set(r['range_id'].strip() for r in good); filters=set(r['filter_id'].strip() for r in good)
    apertures=set(round(float(r['aperture_s']),12) for r in good)
    if len(ranges)!=1: fail.append('range_configuration_changed')
    if len(filters)!=1: fail.append('filter_configuration_changed')
    if len(apertures)!=1: fail.append('aperture_configuration_changed')
    if sum(b(r['autorange_enabled']) for r in good)>MAX_AUTORANGE_TRUE: fail.append('autorange_enabled')

    by=defaultdict(list)
    for r in good: by[float(r['elapsed_s'])].append(r)
    stats=[]
    prev=None
    for t in times:
        rr=by[t]
        resid=[float(r['measured_V'])-float(r['commanded_V']) for r in rr]
        mean=statistics.fmean(resid)
        u_rep=sem(resid)
        u_ref=max(float(r['reference_step_u_V']) for r in rr)
        u_t=max(float(r['timestamp_u_s']) for r in rr)
        slope=0.0
        if prev is not None and t>prev['elapsed_s']:
            slope=(mean-prev['mean_residual_V'])/(t-prev['elapsed_s'])
        u_time=abs(slope)*u_t
        u=math.sqrt(u_rep*u_rep + u_ref*u_ref + u_time*u_time)
        upper=abs(mean)+Z95*u
        d={'elapsed_s':t,'mean_residual_V':mean,'replicate_sem_V':u_rep,'reference_step_u_V':u_ref,
           'timestamp_u_s':u_t,'local_slope_V_per_s':slope,'timestamp_voltage_u_V':u_time,
           'combined_u_V':u,'upper_abs_residual_95_V':upper}
        stats.append(d); prev=d

    qualified=None
    for i,s in enumerate(stats):
        if all(q['upper_abs_residual_95_V']<=INSTRUMENT_LIMIT_V for q in stats[i:]):
            qualified=s['elapsed_s']; break
    if not inc and qualified is None: fail.append('instrument_residual_not_settled')

    mean_curve=[s['mean_residual_V'] for s in stats]
    tau=first_order_tau(times,mean_curve) if len(times)==len(mean_curve) else None
    overall='FAIL' if fail else ('INCOMPLETE' if inc else 'PASS')
    return {
      'schema_version':'r2-instrument-temporal-fidelity-v3.26',
      'claim_boundary':'PASS qualifies only the configured electrical acquisition chain; it does not qualify source/DUT settling or any device mechanism.',
      'overall_status':overall,'failed_gates':sorted(set(fail)),'incomplete_gates':sorted(set(inc)),
      'configuration':{'range_id':next(iter(ranges)) if len(ranges)==1 else None,
                       'filter_id':next(iter(filters)) if len(filters)==1 else None,
                       'aperture_s':next(iter(apertures)) if len(apertures)==1 else None,
                       'autorange_enabled':any(b(r['autorange_enabled']) for r in good)},
      'engineering_limits':{'parent_settling_envelope_V':SETTLING_ENVELOPE_V,
                            'instrument_budget_fraction':INSTRUMENT_BUDGET_FRACTION,
                            'instrument_upper_residual_limit_V':INSTRUMENT_LIMIT_V,
                            'minimum_replicates':MIN_REPLICATES},
      'n_replicates':len(reps),'n_elapsed_times':len(times),'qualified_instrument_dwell_s':qualified,
      'first_order_tau_diagnostic_s':tau,'timepoint_statistics':stats
    }

def main():
    p=argparse.ArgumentParser(); p.add_argument('input_csv'); p.add_argument('--output-json'); ns=p.parse_args()
    out=assess(load(ns.input_csv)); txt=json.dumps(out,sort_keys=True,indent=2)+'\n'
    if ns.output_json: Path(ns.output_json).write_text(txt,encoding='utf-8',newline='\n')
    else: sys.stdout.write(txt)
    return 0 if out['overall_status']=='PASS' else 2

if __name__=='__main__': raise SystemExit(main())
