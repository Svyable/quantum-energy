#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,math,random,statistics,sys
from pathlib import Path

KB=8.617333262e-5
T_K=300.0
WINDOW=7
LOW=0.1
HIGH=1.0
SEED=20260827
MIN_BLOCKS=4
MAX_MODEL_U=0.01
MAX_RESIDUAL_SD_V=0.0005
REQ={'block_id','sequence_index','target_suns','calibrated_suns','voc_V','elapsed_s','qc_status'}

def solve(A,b):
    n=len(A); m=[list(A[i])+[b[i]] for i in range(n)]
    for c in range(n):
        p=max(range(c,n),key=lambda r:abs(m[r][c]))
        m[c],m[p]=m[p],m[c]
        s=m[c][c]
        if abs(s)<1e-14: raise ValueError('singular normal matrix')
        for j in range(c,n+1): m[c][j]/=s
        for r in range(n):
            if r==c: continue
            q=m[r][c]
            if q:
                for j in range(c,n+1): m[r][j]-=q*m[c][j]
    return [m[i][n] for i in range(n)]

def invert(A):
    n=len(A); cols=[]
    for k in range(n):
        e=[0.0]*n; e[k]=1.0; cols.append(solve(A,e))
    return [[cols[j][i] for j in range(n)] for i in range(n)]

def mat_xtx(X):
    p=len(X[0]); return [[sum(r[i]*r[j] for r in X) for j in range(p)] for i in range(p)]
def mat_xty(X,y): return [sum(r[i]*v for r,v in zip(X,y)) for i in range(len(X[0]))]
def mv(M,v): return [sum(a*b for a,b in zip(r,v)) for r in M]
def dot(a,b): return sum(x*y for x,y in zip(a,b))

def nearest(a,t): return min(range(len(a)),key=lambda i:abs(a[i]-t))
def solve3(A,y): return solve(A,y)
def local_weights(phi,idx):
    order=sorted(range(len(phi)),key=lambda i:phi[i]); p=[phi[i] for i in order]; idxs=order.index(idx)
    x=[math.log(v) for v in p]; half=WINDOW//2; lo=max(0,min(idxs-half,len(x)-WINDOW)); hi=lo+WINDOW
    u=[x[j]-x[idxs] for j in range(lo,hi)]
    S=[sum(v**k for v in u) for k in range(5)]
    A=[[S[0],S[1],S[2]],[S[1],S[2],S[3]],[S[2],S[3],S[4]]]
    w=[0.0]*len(phi)
    for loc,j in enumerate(range(lo,hi)):
        rhs=[u[loc]**k for k in range(3)]
        coef=solve3(A,rhs)
        w[order[j]]=coef[1]/(KB*T_K)
    return w

def curvature_weights(target,cal):
    il=nearest(target,LOW); ih=nearest(target,HIGH)
    wl=local_weights(cal,il); wh=local_weights(cal,ih)
    return [b-a for a,b in zip(wl,wh)]
def curvature(target,cal,voc): return dot(curvature_weights(target,cal),voc)

def schedule(seed=SEED,n=17):
    rng=random.Random(seed)
    p=list(range(n)); rng.shuffle(p)
    q=list(range(n)); rng.shuffle(q)
    return [p,list(reversed(p)),q,list(reversed(q))]

def schedule_diagnostics(perms):
    n=len(perms[0]); B=len(perms)
    ranks=[[0]*n for _ in range(B)]
    for b,p in enumerate(perms):
        for rank,i in enumerate(p): ranks[b][i]=rank
    mean_rank=[statistics.fmean(ranks[b][i] for b in range(B)) for i in range(n)]
    mean_sq=[statistics.fmean(ranks[b][i]**2 for b in range(B)) for i in range(n)]
    return {'max_mean_rank_deviation':max(abs(v-(n-1)/2) for v in mean_rank),
            'mean_rank_sd':statistics.pstdev(mean_rank),
            'mean_rank2_cv':statistics.pstdev(mean_sq)/statistics.fmean(mean_sq)}

def load(path):
    with open(path,newline='',encoding='utf-8') as h:
        rd=csv.DictReader(h); miss=sorted(REQ-set(rd.fieldnames or [])); rows=list(rd)
    if miss: raise ValueError('missing columns: '+', '.join(miss))
    if not rows: raise ValueError('empty input')
    return [r for r in rows if r['qc_status'].strip().upper()=='PASS']

def design(rows):
    blocks=sorted({r['block_id'] for r in rows})
    if len(blocks)<MIN_BLOCKS: raise ValueError('need >=4 complete randomized blocks')
    grid=sorted({float(r['target_suns']) for r in rows})
    if len(grid)<WINDOW: raise ValueError('need >=7 unique intensities')
    gidx={round(v,12):i for i,v in enumerate(grid)}; bidx={b:i for i,b in enumerate(blocks)}
    for b in blocks:
        vals=[round(float(r['target_suns']),12) for r in rows if r['block_id']==b]
        if sorted(vals)!=sorted(gidx): raise ValueError('each block must contain the identical complete target grid once')
    stats={}
    for b in blocks:
        ts=[float(r['elapsed_s']) for r in rows if r['block_id']==b]
        mu=statistics.fmean(ts); span=max(ts)-min(ts)
        if span<=0: raise ValueError('elapsed_s must vary inside each block')
        tau=[(t-mu)/(span/2) for t in ts]
        qmu=statistics.fmean(v*v for v in tau)
        stats[b]=(mu,span,qmu)
    X=[]; y=[]; order=[]
    for r in rows:
        i=gidx[round(float(r['target_suns']),12)]; b=bidx[r['block_id']]
        mu,span,qmu=stats[r['block_id']]; tau=(float(r['elapsed_s'])-mu)/(span/2); q=tau*tau-qmu
        row=[0.0]*len(grid); row[i]=1.0
        row += [1.0 if b==j else 0.0 for j in range(1,len(blocks))]
        for j in range(len(blocks)):
            row += [tau if b==j else 0.0,q if b==j else 0.0]
        X.append(row); y.append(float(r['voc_V'])); order.append((b,i))
    return X,y,grid,blocks,stats,order

def analyze(rows):
    X,y,grid,blocks,stats,order=design(rows); xtx=mat_xtx(X); inv=invert(xtx); beta=mv(inv,mat_xty(X,y)); pred=[dot(r,beta) for r in X]
    resid=[a-b for a,b in zip(y,pred)]; dof=len(y)-len(beta)
    if dof<=0: raise ValueError('no residual degrees of freedom')
    sigma2=sum(v*v for v in resid)/dof
    alpha=beta[:len(grid)]
    cal=[]
    for g in grid:
        vals=[float(r['calibrated_suns']) for r in rows if round(float(r['target_suns']),12)==round(g,12)]
        cal.append(statistics.fmean(vals))
    w=curvature_weights(grid,cal); curv=dot(w,alpha)
    cov_alpha=[[sigma2*inv[i][j] for j in range(len(grid))] for i in range(len(grid))]
    u=math.sqrt(max(0.0,dot(w,mv(cov_alpha,w))))
    naive=[]
    for b in blocks:
        rr=sorted((r for r in rows if r['block_id']==b),key=lambda r:float(r['target_suns']))
        naive.append(curvature([float(r['target_suns']) for r in rr],[float(r['calibrated_suns']) for r in rr],[float(r['voc_V']) for r in rr]))
    start=len(grid)+(len(blocks)-1); drift=[]
    for j,b in enumerate(blocks):
        l=beta[start+2*j]; q=beta[start+2*j+1]
        vals=[l*t+q*(t*t-stats[b][2]) for t in (-1.0,0.0,1.0)]
        drift.append({'block_id':b,'linear_V_per_tau':l,'quadratic_V_per_tau2':q,'fitted_peak_to_peak_V':max(vals)-min(vals)})
    return {'schema_version':'r2-order-drift-v3.24','n_blocks':len(blocks),'n_points':len(rows),'curvature':curv,'curvature_u_1sigma':u,
            'residual_sd_V':math.sqrt(sigma2),'naive_block_curvatures':naive,'naive_curvature_range':max(naive)-min(naive),
            'drift_fits':drift,'gate':{'status':'PASS' if (u<=MAX_MODEL_U and math.sqrt(sigma2)<=MAX_RESIDUAL_SD_V) else 'FAIL','curvature_u_limit':MAX_MODEL_U,'residual_sd_V_limit':MAX_RESIDUAL_SD_V},
            'claim_boundary':'PASS bounds smooth acquisition-order drift under the declared randomized-block model; it does not identify recombination mechanism, EPC, or open-quantum transport.'}

def synthetic_rows(seed=SEED,linear_pp_V=0.002,quad_pp_V=0.001,noise_sd_V=0.0002):
    rng=random.Random(seed); n=17; ratio=(2/0.05)**(1/(n-1)); phi=[0.05*ratio**i for i in range(n)]; x=[math.log(v) for v in phi]
    il=nearest(phi,LOW); ih=nearest(phi,HIGH); bcurv=0.10/(x[ih]-x[il]); base=[KB*T_K*(xx+0.5*bcurv*xx*xx) for xx in x]
    rows=[]; perms=schedule(SEED,n)
    for bi,p in enumerate(perms):
        for rank,i in enumerate(p):
            tau=-1+2*rank/(n-1); q=tau*tau-0.375
            drift=(linear_pp_V/2)*tau+(quad_pp_V/2)*q
            rows.append({'block_id':f'R{bi+1}','sequence_index':str(rank+1),'target_suns':repr(phi[i]),'calibrated_suns':repr(phi[i]),
                         'voc_V':repr(base[i]+drift+rng.gauss(0,noise_sd_V)),'elapsed_s':repr(rank*8.0),'qc_status':'PASS'})
    return rows,phi,base

def monotonic_bias(phi,base,linear_pp_V=0.002,quad_pp_V=0.001):
    n=len(phi); obs=[]
    qmean=statistics.fmean((-1+2*r/(n-1))**2 for r in range(n))
    for rank in range(n):
        tau=-1+2*rank/(n-1); q=tau*tau-qmean
        obs.append(base[rank]+(linear_pp_V/2)*tau+(quad_pp_V/2)*q)
    return curvature(phi,phi,obs)-curvature(phi,phi,base)

def selftest():
    rows,phi,base=synthetic_rows(); out=analyze(rows); true=curvature(phi,phi,base); bias=out['curvature']-true; mono=monotonic_bias(phi,base)
    if abs(true-0.10)>1e-10: raise AssertionError(true)
    if abs(bias)>0.01: raise AssertionError(('randomized corrected bias',bias))
    if abs(mono)<0.01: raise AssertionError(('monotonic stress too weak',mono))
    rr,pp,bb=synthetic_rows(noise_sd_V=0.0); oo=analyze(rr)
    if abs(oo['curvature']-curvature(pp,pp,bb))>1e-9: raise AssertionError(('noise-free recovery',oo['curvature']))
    diag=schedule_diagnostics(schedule())
    if diag['max_mean_rank_deviation']>1e-12: raise AssertionError(diag)
    return {'true_curvature':true,'randomized_estimate':out['curvature'],'randomized_bias':bias,'randomized_u_1sigma':out['curvature_u_1sigma'],
            'monotonic_same_drift_bias':mono,'schedule':diag,'seed':SEED,'software':'Python standard library'}

def main():
    p=argparse.ArgumentParser(); p.add_argument('input_csv',nargs='?'); p.add_argument('--self-test',action='store_true'); p.add_argument('--schedule-csv'); p.add_argument('--output-json')
    ns=p.parse_args()
    if ns.schedule_csv:
        n=17; ratio=(2/0.05)**(1/(n-1)); phi=[0.05*ratio**i for i in range(n)]; perms=schedule()
        with open(ns.schedule_csv,'w',newline='',encoding='utf-8') as h:
            w=csv.writer(h); w.writerow(['block_id','sequence_index','target_suns'])
            for b,p in enumerate(perms,1):
                for rank,i in enumerate(p,1): w.writerow([f'R{b}',rank,repr(phi[i])])
    if ns.self_test: result=selftest()
    elif ns.input_csv: result=analyze(load(ns.input_csv))
    else: result={'schedule_diagnostics':schedule_diagnostics(schedule()),'seed':SEED}
    txt=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if ns.output_json: Path(ns.output_json).write_text(txt,encoding='utf-8')
    else: sys.stdout.write(txt)
    return 0
if __name__=='__main__': raise SystemExit(main())
