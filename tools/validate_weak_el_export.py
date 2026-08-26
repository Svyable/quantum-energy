#!/usr/bin/env python3
"""Validate weak-EL facility export v1. Publication infrastructure only."""
import argparse,csv,hashlib,json,math
from collections import defaultdict
from pathlib import Path
Q=1.602176634e-19; KB=1.380649e-23
REQ={
"measurements.csv":{"measurement_id","temperature_K","temperature_standard_uncertainty_K","injection_current_A","injection_current_standard_uncertainty_A","active_area_m2"},
"spectra.csv":{"measurement_id","replicate_id","detector_channel","integration_time_s","sample_counts","background_counts","dark_counts"},
"wavelength_calibration.csv":{"detector_channel","wavelength_nm","wavelength_standard_uncertainty_nm","bin_width_nm"},
"radiometric_calibration.csv":{"detector_channel","emitted_photons_per_count","relative_standard_uncertainty","correlation_group"},
"linearity.csv":{"count_rate_cps","relative_response","relative_standard_uncertainty"}}
def rows(p):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def num(r,k):
 x=float(r[k]);
 if not math.isfinite(x):raise ValueError(f'nonfinite {k}')
 return x
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(root,expect=False):
 root=Path(root); m=json.loads((root/'manifest.json').read_text())
 if m.get('schema_name')!='quantum-energy.weak-el-facility-export' or m.get('schema_version')!='1.0.0':raise ValueError('unsupported schema')
 listed={x['path']:x for x in m['files']}; tab={}; warnings=[]
 if m.get('license_spdx_or_uri')=='NOASSERTION':warnings.append('NOASSERTION license: fixture only, not publication-ready')
 for fn,cols in REQ.items():
  p=root/fn
  if fn not in listed or not p.is_file() or h(p)!=listed[fn]['sha256']:raise ValueError(f'missing/hash mismatch {fn}')
  tab[fn]=rows(p)
  if not tab[fn] or cols-set(tab[fn][0]):raise ValueError(f'columns/empty {fn}')
 meas={r['measurement_id']:r for r in tab['measurements.csv']}
 if len(meas)!=len(tab['measurements.csv']):raise ValueError('duplicate measurement_id')
 for r in meas.values():
  if not(0<num(r,'temperature_K')<1000 and num(r,'temperature_standard_uncertainty_K')>=0 and num(r,'injection_current_A')>0 and num(r,'injection_current_standard_uncertainty_A')>=0 and num(r,'active_area_m2')>0):raise ValueError('bad measurement metadata')
 wc={r['detector_channel']:r for r in tab['wavelength_calibration.csv']}; rc={r['detector_channel']:r for r in tab['radiometric_calibration.csv']}
 if len(wc)!=len(tab['wavelength_calibration.csv']) or len(rc)!=len(tab['radiometric_calibration.csv']) or set(wc)!=set(rc):raise ValueError('calibration channel mismatch/duplicate')
 for ch in wc:
  if num(wc[ch],'wavelength_nm')<=0 or num(wc[ch],'bin_width_nm')<=0 or num(wc[ch],'wavelength_standard_uncertainty_nm')<0:raise ValueError('bad wavelength calibration')
  if num(rc[ch],'emitted_photons_per_count')<=0 or num(rc[ch],'relative_standard_uncertainty')<0 or not rc[ch]['correlation_group']:raise ValueError('bad radiometric calibration')
 lo=float(m['linearity_valid_count_rate_cps']['minimum']); hi=float(m['linearity_valid_count_rate_cps']['maximum']); lr=[num(r,'count_rate_cps') for r in tab['linearity.csv']]
 if lo<0 or hi<=lo or min(lr)>lo or max(lr)<hi:raise ValueError('bad linearity range')
 g=defaultdict(list)
 for r in tab['spectra.csv']:
  t=num(r,'integration_time_s'); s=num(r,'sample_counts'); b=num(r,'background_counts'); d=num(r,'dark_counts')
  if r['measurement_id'] not in meas or r['detector_channel'] not in wc or t<=0 or min(s,b,d)<0 or not(lo<=s/t<=hi):raise ValueError('bad spectrum row')
  g[(r['measurement_id'],r['replicate_id'])].append(r)
 out=[]
 for (mid,rep),rs in sorted(g.items()):
  if {r['detector_channel'] for r in rs}!=set(wc) or len(rs)!=len(wc):raise ValueError('incomplete/duplicate channels')
  total=integ=wrong=0.0
  for r in rs:
   ch=r['detector_channel']; rate=(num(r,'sample_counts')-num(r,'background_counts'))/num(r,'integration_time_s'); ph=rate*num(rc[ch],'emitted_photons_per_count'); bw=num(wc[ch],'bin_width_nm'); total+=ph; integ+=(ph/bw)*bw; wrong+=ph*bw
  if total<=0 or abs(integ-total)/total>1e-12:raise ValueError('photon conservation failed')
  T=num(meas[mid],'temperature_K'); I=num(meas[mid],'injection_current_A'); eqe=total/(I/Q)
  if not 0<eqe<=1:raise ValueError('EQE_EL outside (0,1]')
  out.append({'measurement_id':mid,'replicate_id':rep,'emitted_photon_rate_s-1':total,'eqe_el_fraction':eqe,'delta_vnr_V':-(KB*T/Q)*math.log(eqe),'legacy_no_binwidth_integral_ratio':wrong/total})
 if expect:
  e=m['synthetic_expected']; x=next(r for r in out if r['measurement_id']==e['measurement_id'])
  for a,b in [('emitted_photon_rate_s-1','emitted_photon_rate_s-1'),('eqe_el_fraction','eqe_el_fraction'),('delta_vnr_V','delta_vnr_300K_V')]:
   if not math.isclose(x[a],float(e[b]),rel_tol=1e-12,abs_tol=1e-12):raise ValueError(f'synthetic mismatch {a}')
 return out,warnings
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('package');ap.add_argument('--expect-synthetic',action='store_true');a=ap.parse_args();o,w=validate(a.package,a.expect_synthetic);print(json.dumps({'status':'PASS','derived':o,'warnings':w},indent=2,sort_keys=True))
