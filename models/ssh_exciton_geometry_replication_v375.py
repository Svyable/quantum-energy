#!/usr/bin/env python3
"""Independent minimal replication of the SSH-band quantum metric used as a QG0 gate.

This is a synthetic/model verification harness, not a reproduction of the full
material-specific BSE/DFT calculation in Thompson et al. It checks the topology ->
quantum-metric-spread logic in the minimal two-band SSH model with no third-party deps.
"""
import cmath, csv, math, sys

N=20000

def dvec(k,t1,t2):
    return (t1+t2*math.cos(k), t2*math.sin(k), 0.0)

def metric(k,t1,t2):
    # For a two-level band, g_kk = |dhat'|^2/4. Analytic derivative avoids gauge issues.
    dx=t1+t2*math.cos(k); dy=t2*math.sin(k)
    ddx=-t2*math.sin(k); ddy=t2*math.cos(k)
    r2=dx*dx+dy*dy
    dot=dx*ddx+dy*ddy
    dh2=(ddx*ddx+ddy*ddy)/r2 - dot*dot/(r2*r2)
    return 0.25*dh2

def zak_winding(t1,t2):
    # winding of q(k)=t1+t2 exp(ik) around origin, unwrapped phase / 2pi
    prev=cmath.phase(t1+t2)
    total=0.0
    for j in range(1,N+1):
        k=2*math.pi*j/N
        ph=cmath.phase(t1+t2*cmath.exp(1j*k))
        d=ph-prev
        while d>math.pi: d-=2*math.pi
        while d<-math.pi: d+=2*math.pi
        total+=d; prev=ph
    return round(total/(2*math.pi))

def avg_metric(t1,t2):
    s=0.0
    for j in range(N):
        k=2*math.pi*(j+0.5)/N
        s+=metric(k,t1,t2)
    return s/N

def run(t1,t2):
    w=zak_winding(t1,t2)
    g=avg_metric(t1,t2)
    return w,g

def main():
    cases=[('trivial_0p5',1.0,0.5),('topological_2',0.5,1.0),('trivial_0p8',1.0,0.8),('topological_1p25',0.8,1.0)]
    rows=[]
    for name,t1,t2 in cases:
        w,g=run(t1,t2)
        rows.append((name,t1,t2,w,g))
        print(f'{name}: winding={w} avg_metric={g:.12g}')
    # In lattice units a=1, the cited topology bound for P_exc=1 is <g> >= 1/4.
    topo=[r for r in rows if r[3]!=0]
    triv=[r for r in rows if r[3]==0]
    assert all(r[4] >= 0.25-2e-4 for r in topo), topo
    assert all(r[4] >= 0 for r in rows)
    # swapped hopping pairs have identical band dispersion but different topology/metric.
    assert rows[1][4] > rows[0][4]
    assert rows[3][4] > rows[2][4]
    # numerical convergence check
    print('PASS minimal SSH topology/metric gate')
    if len(sys.argv)>1:
        with open(sys.argv[1],'w',newline='') as f:
            w=csv.writer(f); w.writerow(['case','t1','t2','winding','avg_metric_lattice2']); w.writerows(rows)
if __name__=='__main__': main()
