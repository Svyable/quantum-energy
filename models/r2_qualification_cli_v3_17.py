#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,math,statistics,sys
from collections import defaultdict
from pathlib import Path

KB=8.617333262e-5; T=300.0; WINDOW=7; LOW=0.1; HIGH=1.0; STRESS=0.10
G={'cal_res':0.005,'cal_bias':0.01,'ref_drift':0.002,'voc_drift':0.0005,'hyst_voc':0.0005,'hyst_curv':0.03,'temp_sd':0.25,'temp_exc':0.5,'voc_sd':0.0005,'smf_dev':0.01,'smf_u':0.005}
REQ={'lot_id','substrate_id','pixel_id','session_id','sweep_id','sweep_direction','sequence_index','target_suns','reference_detector_id','reference_signal_raw','reference_signal_unit','reference_dark_raw','calibrated_suns','calibration_relative_u_1sigma','calibration_correlation_group','dut_temperature_K','dut_temperature_u_K','voc_V','voc_u_V','anchor_flag','prepost_anchor_pair_id','qc_status','deviation_note','source_spectrum_id','spectral_mismatch_factor','spectral_mismatch_u_rel'}

def b(v): return str(v).strip().lower() in {'1','true','yes','y'}
def fv(r,k):
    s=r.get(k,'').strip(); return None if s=='' else float(s)
def nearest(a,t): return min(range(len(a)),key=lambda i:abs(a[i]-t))

def solve3(A,y):
    m=[r[:] + [v] for r,v in zip(A,y)]
    for c in range(3):
        p=max(range(c,3),key=lambda r:abs(m[r][c])); m[c],m[p]=m[p],m[c]
        s=m[c][c]
        if abs(s)<1e-18: raise ValueError('singular local fit')
        for j in range(c,4): m[c][j]/=s
        for r in range(3):
            if r==c: continue
            f=m[r][c]
            for j in range(c,4): m[r][j]-=f*m[c][j]
    return [m[i][3] for i in range(3)]

def local_nid(phi,voc,idx):
    order=sorted(range(len(phi)),key=lambda i:phi[i]); p=[phi[i] for i in order]; y=[voc[i] for i in order]
    idx=order.index(idx) if idx in order else idx
    x=[math.log(v) for v in p]; half=WINDOW//2; lo=max(0,min(idx-half,len(x)-WINDOW)); hi=lo+WINDOW
    u=[x[j]-x[idx] for j in range(lo,hi)]; yy=y[lo:hi]
    S=[sum(v**k for v in u) for k in range(5)]
    rhs=[sum(yy[j]*(u[j]**k) for j in range(len(u))) for k in range(3)]
    A=[[S[0],S[1],S[2]],[S[1],S[2],S[3]],[S[2],S[3],S[4]]]
    return solve3(A,rhs)[1]/(KB*T)

def curvature(phi,voc):
    order=sorted(range(len(phi)),key=lambda i:phi[i]); p=[phi[i] for i in order]; y=[voc[i] for i in order]
    if len(p)<WINDOW: raise ValueError('need >=7 points')
    il,ih=nearest(p,LOW),nearest(p,HIGH)
    return local_nid(p,y,ih)-local_nid(p,y,il)

def linfit(x,y):
    xm=statistics.fmean(x); ym=statistics.fmean(y); sxx=sum((v-xm)**2 for v in x)
    bb=sum((a-xm)*(c-ym) for a,c in zip(x,y))/sxx; aa=ym-bb*xm
    return aa,bb,[c-(aa+bb*a) for a,c in zip(x,y)]

def cal_bias(target,measured):
    order=sorted(range(len(target)),key=lambda i:target[i]); t=[target[i] for i in order]; m=[measured[i] for i in order]
    x=[math.log(v) for v in t]; il,ih=nearest(t,LOW),nearest(t,HIGH); beta=STRESS/(x[ih]-x[il])
    voc=[KB*T*(xx+0.5*beta*xx*xx) for xx in x]
    return curvature(m,voc)-curvature(t,voc)

def metric(status,value=None,limit=None,unit=None,note=None):
    d={'status':status}
    if value is not None:d['value']=value
    if limit is not None:d['limit']=limit
    if unit:d['unit']=unit
    if note:d['note']=note
    return d

def load(path):
    with open(path,newline='',encoding='utf-8') as f: r=csv.DictReader(f); miss=sorted(REQ-set(r.fieldnames or [])); rows=list(r)
    if miss: raise ValueError('missing columns: '+', '.join(miss))
    if not rows: raise ValueError('empty input')
    if any(x['qc_status'].strip().upper() not in {'PASS','PENDING'} for x in rows): raise ValueError('non-PASS/PENDING qc_status present')
    return rows

def assess(rows):
    n=[r for r in rows if not b(r['anchor_flag'])]; a=[r for r in rows if b(r['anchor_flag'])]
    M={}; fail=[]; inc=[]
    def setg(name,status,value=None,limit=None,unit=None,note=None):
        M[name]=metric(status,value,limit,unit,note)
        if status=='FAIL': fail.append(name)
        if status=='INCOMPLETE': inc.append(name)
    raw_t=[fv(r,'target_suns') for r in n]; raw_c=[fv(r,'calibrated_suns') for r in n]
    grouped=defaultdict(list)
    for tv,cv in zip(raw_t,raw_c):
        if tv is not None and cv is not None and tv>0 and cv>0: grouped[round(tv,12)].append(cv)
    t=sorted(grouped); c=[statistics.fmean(grouped[k]) for k in t]
    if len(t)<7 or len(grouped)<len(set(v for v in raw_t if v is not None)):
        setg('calibration_residual','INCOMPLETE'); setg('calibration_curvature_bias','INCOMPLETE')
    else:
        _,gain,res=linfit([math.log(v) for v in t],[math.log(v) for v in c]); rr=max(abs(math.exp(v)-1) for v in res); cb=cal_bias(t,c)
        M['calibration_log_gain']=metric('INFO',gain-1,unit='fraction')
        setg('calibration_residual','PASS' if rr<=G['cal_res'] else 'FAIL',rr,G['cal_res'],'fraction')
        setg('calibration_curvature_bias','PASS' if abs(cb)<=G['cal_bias'] else 'FAIL',cb,G['cal_bias'],'dimensionless')
    vu=[fv(r,'voc_u_V') for r in n]
    if not vu or any(v is None for v in vu): setg('point_voc_sd','INCOMPLETE')
    else:
        x=max(vu); setg('point_voc_sd','PASS' if x<=G['voc_sd'] else 'FAIL',x,G['voc_sd'],'V')
    by=defaultdict(list)
    for r in n:
        v=fv(r,'dut_temperature_K')
        if v is not None: by[r['sweep_id']].append(v)
    if not by or any(len(v)<2 for v in by.values()): setg('temperature_sd','INCOMPLETE'); setg('temperature_excursion','INCOMPLETE')
    else:
        sd=max(statistics.pstdev(v) for v in by.values()); ex=max(abs(x-T) for v in by.values() for x in v)
        setg('temperature_sd','PASS' if sd<=G['temp_sd'] else 'FAIL',sd,G['temp_sd'],'K')
        setg('temperature_excursion','PASS' if ex<=G['temp_exc'] else 'FAIL',ex,G['temp_exc'],'K')
    pairs=defaultdict(list)
    for r in a:
        if r['prepost_anchor_pair_id'].strip(): pairs[r['prepost_anchor_pair_id']].append(r)
    rd=[]; vd=[]
    for rr in pairs.values():
        if len(rr)!=2: continue
        rr=sorted(rr,key=lambda r:int(r['sequence_index'])); s=[fv(x,'reference_signal_raw') for x in rr]; d=[fv(x,'reference_dark_raw') for x in rr]; v=[fv(x,'voc_V') for x in rr]
        if None not in s+d and s[0]!=d[0]: rd.append(abs((s[1]-d[1])/(s[0]-d[0])-1))
        if None not in v: vd.append(abs(v[1]-v[0]))
    if rd:
        x=max(rd); setg('reference_anchor_drift','PASS' if x<=G['ref_drift'] else 'FAIL',x,G['ref_drift'],'fraction')
    else:setg('reference_anchor_drift','INCOMPLETE')
    if vd:
        x=max(vd); setg('voc_anchor_drift','PASS' if x<=G['voc_drift'] else 'FAIL',x,G['voc_drift'],'V')
    else:setg('voc_anchor_drift','INCOMPLETE')
    D=defaultdict(list)
    for r in n:D[r['sweep_direction'].strip().lower()].append(r)
    if not D['ascending'] or not D['descending']:
        setg('sweep_median_voc_difference','INCOMPLETE'); setg('sweep_curvature_difference','INCOMPLETE')
    else:
        ma={round(fv(r,'target_suns'),9):r for r in D['ascending']}; md={round(fv(r,'target_suns'),9):r for r in D['descending']}; ks=sorted(set(ma)&set(md))
        if len(ks)<7:setg('sweep_median_voc_difference','INCOMPLETE'); setg('sweep_curvature_difference','INCOMPLETE')
        else:
            diff=[abs(fv(ma[k],'voc_V')-fv(md[k],'voc_V')) for k in ks]; med=statistics.median(diff)
            ca=curvature([fv(ma[k],'calibrated_suns') for k in ks],[fv(ma[k],'voc_V') for k in ks]); cd=curvature([fv(md[k],'calibrated_suns') for k in ks],[fv(md[k],'voc_V') for k in ks]); dc=abs(ca-cd)
            setg('sweep_median_voc_difference','PASS' if med<=G['hyst_voc'] else 'FAIL',med,G['hyst_voc'],'V')
            setg('sweep_curvature_difference','PASS' if dc<=G['hyst_curv'] else 'FAIL',dc,G['hyst_curv'],'dimensionless'); M['ascending_curvature']=metric('INFO',ca,unit='dimensionless'); M['descending_curvature']=metric('INFO',cd,unit='dimensionless')
    sm=[fv(r,'spectral_mismatch_factor') for r in n]; su=[fv(r,'spectral_mismatch_u_rel') for r in n]; sid=[r['source_spectrum_id'].strip() for r in n]
    if not sm or any(v is None for v in sm+su) or any(not x for x in sid): setg('spectral_mismatch','INCOMPLETE')
    else:
        dev=max(abs(v-1) for v in sm); umax=max(su); changed=len(set(sid))>1; ok=dev<=G['smf_dev'] and umax<=G['smf_u'] and not changed
        setg('spectral_mismatch','PASS' if ok else 'FAIL',dev,G['smf_dev'],'fraction',f'max_u={umax:.6g}; source_spectrum_id_count={len(set(sid))}')
    groups=defaultdict(list)
    for r in n:
        g=r['calibration_correlation_group'].strip() or 'UNSPECIFIED'; u=fv(r,'calibration_relative_u_1sigma')
        if u is not None: groups[g].append(u)
    group_summary={g:{'max_relative_u_1sigma':max(v),'n_points':len(v)} for g,v in sorted(groups.items())}
    overall='FAIL' if fail else ('INCOMPLETE' if inc else 'PASS')
    return {'schema_version':'r2-voc-intensity-qualification-v3.17','claim_boundary':'PASS qualifies the measurement path only; it does not identify H3, EPC, or open-quantum transport.','overall_status':overall,'failed_gates':sorted(set(fail)),'incomplete_gates':sorted(set(inc)),'metrics':M,'power_model_inputs':{'max_point_voc_sd_V':M.get('point_voc_sd',{}).get('value'),'calibration_curvature_bias_abs':abs(M.get('calibration_curvature_bias',{}).get('value',0)) if M.get('calibration_curvature_bias',{}).get('value') is not None else None,'calibration_uncertainty_groups':group_summary}}

def main():
    p=argparse.ArgumentParser(); p.add_argument('input_csv'); p.add_argument('--output-json'); ns=p.parse_args(); cert=assess(load(ns.input_csv)); txt=json.dumps(cert,sort_keys=True,indent=2)+'\n'
    if ns.output_json: Path(ns.output_json).write_text(txt,encoding='utf-8')
    else: sys.stdout.write(txt)
    return 0 if cert['overall_status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
