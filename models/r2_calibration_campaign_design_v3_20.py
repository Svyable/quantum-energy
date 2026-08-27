#!/usr/bin/env python3
"""Prospective R2 reference-detector repeatability campaign design, v3.20.

This tool is estimator-agnostic. It freezes a facility-neutral acquisition schedule and
quantifies the finite-sample precision of a balanced one-way random-effects estimate
of between-session scale variability under explicitly synthetic planning ratios.

No output from this program is experimental evidence.
"""
from __future__ import annotations
import argparse,csv,json,math,random,statistics,sys
from pathlib import Path

SEED=20260826
REPS=20000
SESSIONS_MIN=24
SESSIONS_EXTENDED=30
DAY_BLOCKS=6
SWEEPS_PER_SESSION=4
POINTS_PER_SWEEP=17
CANDIDATE_SESSIONS=(12,16,20,24,30)
WITHIN_TO_BETWEEN_RATIOS=(0.25,0.50,0.75,1.00,1.50)
P90_RELERR_GATE=0.30
RATIO_SCREEN_GATE=0.75


def q(values,p):
    s=sorted(values); x=(len(s)-1)*p; i=int(math.floor(x)); j=min(i+1,len(s)-1); w=x-i
    return s[i]*(1-w)+s[j]*w


def random_effects_variance(groups):
    """Balanced one-way random-effects method-of-moments variance component."""
    J=len(groups); m=len(groups[0])
    if J<2 or m<2 or any(len(g)!=m for g in groups): raise ValueError('balanced groups with J>=2,m>=2 required')
    flat=[x for g in groups for x in g]; overall=statistics.fmean(flat)
    msw=sum(sum((v-statistics.fmean(g))**2 for v in g) for g in groups)/(J*(m-1))
    msb=sum(m*(statistics.fmean(g)-overall)**2 for g in groups)/(J-1)
    return max(0.0,(msb-msw)/m),msb,msw


def precision_case(n_sessions,ratio,reps=REPS,seed=SEED):
    """Set true between-session SD=1; ratio is within/between SD."""
    rng=random.Random(seed+1000*n_sessions+int(round(ratio*100)))
    sd=[]; var=[]
    for _ in range(reps):
        groups=[]
        for _j in range(n_sessions):
            session=rng.gauss(0.0,1.0)
            groups.append([session+rng.gauss(0.0,ratio) for _ in range(SWEEPS_PER_SESSION)])
        v,_,_=random_effects_variance(groups); var.append(v); sd.append(math.sqrt(v))
    absrel=[abs(v-1.0) for v in sd]
    return {
        'n_sessions':n_sessions,
        'sweeps_per_session':SWEEPS_PER_SESSION,
        'within_to_between_sd_ratio':ratio,
        'mc_reps':reps,
        'seed':seed,
        'median_estimated_sd_over_true':statistics.median(sd),
        'p025_estimated_sd_over_true':q(sd,0.025),
        'p975_estimated_sd_over_true':q(sd,0.975),
        'p90_abs_relative_sd_error':q(absrel,0.90),
        'p95_abs_relative_sd_error':q(absrel,0.95),
        'zero_variance_boundary_rate':sum(v==0.0 for v in sd)/reps,
        'mean_estimated_variance_over_true_variance':statistics.fmean(var),
    }


def sensitivity_table():
    return [precision_case(n,r) for n in CANDIDATE_SESSIONS for r in WITHIN_TO_BETWEEN_RATIOS]


def schedule_rows(n_sessions=SESSIONS_MIN,seed=SEED):
    if n_sessions % DAY_BLOCKS: raise ValueError('n_sessions must be divisible by DAY_BLOCKS')
    per_day=n_sessions//DAY_BLOCKS; rng=random.Random(seed)
    rows=[]; sweep_no=0
    for session_index in range(n_sessions):
        day=1+session_index//per_day; session_in_day=1+session_index%per_day
        session_id=f'D{day:02d}-S{session_in_day:02d}'
        directions=['ascending','ascending','descending','descending']; rng.shuffle(directions)
        for order,direction in enumerate(directions,1):
            sweep_no+=1
            rows.append({
                'day_block':day,'session_id':session_id,'session_order_global':session_index+1,
                'session_order_in_day':session_in_day,'sweep_id':f'CAL-{sweep_no:03d}',
                'sweep_order_in_session':order,'sweep_direction':direction,
                'reference_detector_id':'FILL_AT_FACILITY','source_spectrum_id':'FILL_AT_FACILITY',
                'detector_gain_state':'LOCK_AND_RECORD','geometry_state':'LOCK_AND_RECORD',
                'pre_dark_required':1,'pre_anchor_required':1,'post_anchor_required':1,'post_dark_required':1,
            })
    return rows


def decision(table):
    by={(r['n_sessions'],r['within_to_between_sd_ratio']):r for r in table}
    base=by[(SESSIONS_MIN,RATIO_SCREEN_GATE)]
    stress=by[(SESSIONS_MIN,1.0)]
    extended=by[(SESSIONS_EXTENDED,1.0)]
    return {
        'minimum_campaign_sessions':SESSIONS_MIN,
        'minimum_campaign_sweeps':SESSIONS_MIN*SWEEPS_PER_SESSION,
        'minimum_campaign_grid_points':SESSIONS_MIN*SWEEPS_PER_SESSION*POINTS_PER_SWEEP,
        'day_blocks':DAY_BLOCKS,
        'planning_acceptance_condition':f'after {SESSIONS_MIN} sessions, accept session-count precision only if fitted within/between SD ratio <= {RATIO_SCREEN_GATE} and stationarity/held-out gates pass',
        'extension_rule':f'if ratio > {RATIO_SCREEN_GATE}, variance estimate hits zero boundary, or stationarity/held-out gates fail, extend to >= {SESSIONS_EXTENDED} sessions or redesign before DUT interpretation',
        'p90_relative_error_at_24_ratio_0p75':base['p90_abs_relative_sd_error'],
        'p90_relative_error_at_24_ratio_1p0':stress['p90_abs_relative_sd_error'],
        'p90_relative_error_at_30_ratio_1p0':extended['p90_abs_relative_sd_error'],
        'gate':P90_RELERR_GATE,
        'claim_boundary':'Synthetic planning only. Real repeatability covariance and independence must be demonstrated prospectively.'
    }


def write_csv(path,rows,fields):
    with open(path,'w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=fields,lineterminator='\n'); w.writeheader(); w.writerows(rows)


def main():
    p=argparse.ArgumentParser(); p.add_argument('--output-json'); p.add_argument('--output-precision-csv'); p.add_argument('--output-schedule-csv')
    ns=p.parse_args(); table=sensitivity_table(); out={
        'schema_version':'r2-reference-repeatability-campaign-v3.20',
        'software':'Python standard library only',
        'seed':SEED,'mc_reps_per_case':REPS,
        'governing_model':'y_sj = mu + A_s + e_sj; A_s~N(0,sigma_between^2), e_sj~N(0,sigma_within^2)',
        'variance_estimator':'max(0,(MS_between-MS_within)/m) for balanced m sweeps/session',
        'dimensional_check':'all simulated values are normalized dimensionless log-intensity errors; SD ratios and relative errors are dimensionless',
        'known_limit_check':'E[MS_between]=sigma_within^2+m*sigma_between^2 and E[MS_within]=sigma_within^2, so the unconstrained estimator targets sigma_between^2',
        'decision':decision(table),'precision_sensitivity':table,
    }
    text=json.dumps(out,sort_keys=True,indent=2)+'\n'
    if ns.output_json: Path(ns.output_json).write_text(text,encoding='utf-8',newline='\n')
    else: sys.stdout.write(text)
    if ns.output_precision_csv:
        fields=list(table[0]); write_csv(ns.output_precision_csv,table,fields)
    if ns.output_schedule_csv:
        rows=schedule_rows(); fields=list(rows[0]); write_csv(ns.output_schedule_csv,rows,fields)
    return 0

if __name__=='__main__': raise SystemExit(main())
