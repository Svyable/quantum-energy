#!/usr/bin/env python3
from __future__ import annotations
import csv,math,tempfile
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import r2_spectral_shape_gate_v3_23 as m
import r2_spectral_shape_fixture_generator_v3_23 as gen

HERE=Path(__file__).resolve().parent

def g(x,c,s): return math.exp(-0.5*((x-c)/s)**2)

def write_spectra(path,scale):
    wl=list(range(400,901,10)); n=17; lo=.05; hi=2.0; r=(hi/lo)**(1/(n-1)); ts=[lo*r**i for i in range(n)]
    with open(path,'w',newline='',encoding='utf-8') as h:
        w=csv.writer(h); w.writerow(['spectrum_id','target_suns','wavelength_nm','spectral_irradiance_W_m2_nm'])
        for i,t in enumerate(ts,1):
            xlog=math.log(t)
            for x in wl:
                shape=.55*(1+scale*.005*xlog)*g(x,500,70)+(1+scale*.012*xlog*xlog)*g(x,720,110)+.08
                w.writerow([f'SP{i:02d}',repr(t),x,repr(t*shape)])

def main():
    root=Path(tempfile.mkdtemp(prefix='v323-fixture-'))
    old=sys.argv[:]; sys.argv=['generator',str(root)]
    try: gen.main()
    finally: sys.argv=old
    spectra=root/'r2_spectral_sweep_fixture_v3_23.csv'; resp=root/'r2_spectral_responsivity_fixture_v3_23.csv'; comps=root/'r2_spectral_components_fixture_v3_23.csv'
    d=m.assess(spectra,resp,comps,'SP14',True)
    assert d['overall_status']=='PASS'
    assert abs(d['metrics']['synthetic_curvature_bias']-0.0012150763546945748)<1e-12
    assert abs(d['metrics']['spectral_curvature_u_1sigma']-1.739868418986084e-05)<1e-12
    assert d['monte_carlo']['relative_difference_vs_first_order']<m.MC_TOL_REL
    common=next(c for c in d['uncertainty_components'] if c['component_id']=='common_source_scale')
    assert common['max_abs_ln_smm_loading']<1e-8

    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        p0=td/'scaled.csv'; write_spectra(p0,0.0)
        z=m.assess(p0,resp,comps,'SP14',False)
        assert z['gates']['spectral_mismatch_deviation']['value']<1e-12
        assert abs(z['metrics']['synthetic_curvature_bias'])<1e-10

        same=td/'same_resp.csv'
        with open(resp,newline='',encoding='utf-8') as src, open(same,'w',newline='',encoding='utf-8') as dst:
            rd=csv.DictReader(src); wr=csv.DictWriter(dst,fieldnames=rd.fieldnames); wr.writeheader()
            for r in rd:
                r['dut_responsivity_A_W']=r['reference_responsivity_A_W']; wr.writerow(r)
        q=m.assess(spectra,same,comps,'SP14',False)
        assert q['gates']['spectral_mismatch_deviation']['value']<1e-12
        assert abs(q['metrics']['synthetic_curvature_bias'])<1e-10

        p2=td/'two.csv'; p4=td/'four.csv'; write_spectra(p2,2.0); write_spectra(p4,4.0)
        d2=m.assess(p2,resp,comps,'SP14',False); d4=m.assess(p4,resp,comps,'SP14',False)
        assert d2['overall_status']=='PASS'
        assert d4['gates']['spectral_mismatch_deviation']['status']=='FAIL'
        assert d4['gates']['spectral_mismatch_deviation']['value']>0.01

    print('nominal_bias=',d['metrics']['synthetic_curvature_bias'])
    print('nominal_spectral_u=',d['metrics']['spectral_curvature_u_1sigma'])
    print('mc_u=',d['monte_carlo']['curvature_u_1sigma'])
    print('mc_rel_difference=',d['monte_carlo']['relative_difference_vs_first_order'])
    print('PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
