#!/usr/bin/env python3
"""Generate deterministic synthetic fixtures for the v3.23 spectral-shape gate."""
from __future__ import annotations
import argparse,csv,math
from pathlib import Path

def g(x,c,s): return math.exp(-0.5*((x-c)/s)**2)

def main():
    p=argparse.ArgumentParser(); p.add_argument('output_dir'); ns=p.parse_args(); out=Path(ns.output_dir); out.mkdir(parents=True,exist_ok=True)
    wl=list(range(400,901,10))
    with open(out/'r2_spectral_responsivity_fixture_v3_23.csv','w',newline='',encoding='utf-8') as h:
        w=csv.writer(h); w.writerow(['wavelength_nm','reference_responsivity_A_W','dut_responsivity_A_W'])
        for x in wl:
            rr=0.05+0.7*max(0,min(1,(x-380)/250))*max(0,min(1,(1050-x)/250))
            rt=0.75*g(x,700,100)+0.35*g(x,520,70)+0.02
            w.writerow([x,format(rr,'.12g'),format(rt,'.12g')])
    n=17; lo=.05; hi=2.0; ratio=(hi/lo)**(1/(n-1)); targets=[lo*ratio**i for i in range(n)]
    with open(out/'r2_spectral_sweep_fixture_v3_23.csv','w',newline='',encoding='utf-8') as h:
        w=csv.writer(h); w.writerow(['spectrum_id','target_suns','wavelength_nm','spectral_irradiance_W_m2_nm'])
        for i,t in enumerate(targets,1):
            lx=math.log(t)
            for x in wl:
                shape=.55*(1+.005*lx)*g(x,500,70)+(1+.012*lx*lx)*g(x,720,110)+.08
                w.writerow([f'SP{i:02d}',format(t,'.15g'),x,format(t*shape,'.15g')])
    with open(out/'r2_spectral_components_fixture_v3_23.csv','w',newline='',encoding='utf-8') as h:
        w=csv.writer(h); w.writerow(['component_id','quantity','spectrum_id','wavelength_nm','loading_1sigma','note'])
        for x in wl:
            z=(x-650)/250
            w.writerow(['common_source_scale','source_ln','*',x,'0.005','synthetic 0.5% common radiometric scale; should cancel'])
            w.writerow(['reference_responsivity_tilt','reference_responsivity_ln','*',x,format(.002*z,'.12g'),'synthetic reference-response tilt'])
            w.writerow(['dut_responsivity_tilt','dut_responsivity_ln','*',x,format(.003*z,'.12g'),'synthetic DUT-response tilt'])
        denom=max(abs(math.log(targets[0])),abs(math.log(targets[-1])))
        for i,t in enumerate(targets,1):
            xi=math.log(t)/denom
            for x in wl:
                z=(x-650)/250; load=.0025*xi*z
                w.writerow(['source_intensity_shape','source_ln',f'SP{i:02d}',x,format(load,'.12g'),'synthetic correlated intensity-dependent spectral-shape uncertainty'])
    return 0
if __name__=='__main__': raise SystemExit(main())
