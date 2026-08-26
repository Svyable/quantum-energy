#!/usr/bin/env python3
"""CI gate for weak-EL facility export v1; fixture is synthetic."""
import importlib.util,math,shutil,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; Q=1.602176634e-19; KB=1.380649e-23
spec=importlib.util.spec_from_file_location('weak_el_validator',ROOT/'tools/validate_weak_el_export.py'); mod=importlib.util.module_from_spec(spec); sys.modules[spec.name]=mod; spec.loader.exec_module(mod)
pkg=ROOT/'examples/weak_el_facility_export_v1'; rows,warnings=mod.validate(pkg,True)
if len(rows)!=2:raise AssertionError('expected two synthetic measurements')
x=next(r for r in rows if r['measurement_id']=='M001')
# Independent hand construction: net rates 100/200/300 count/s, K=1e8 photon/count.
ph=(100+200+300)*1e8; eqe=ph/(1e-4/Q); dv=-(KB*300/Q)*math.log(eqe)
if not math.isclose(x['emitted_photon_rate_s-1'],ph,rel_tol=0,abs_tol=1e-6):raise AssertionError('photon-rate cross-check')
if not math.isclose(x['eqe_el_fraction'],eqe,rel_tol=0,abs_tol=1e-15):raise AssertionError('EQE_EL cross-check')
if not math.isclose(x['delta_vnr_V'],dv,rel_tol=0,abs_tol=1e-14):raise AssertionError('DeltaVnr cross-check')
# Two-nm bins: correct density/bin handling conserves rate; old implicit-bin path is exactly 2x.
if not math.isclose(x['legacy_no_binwidth_integral_ratio'],2.0,rel_tol=0,abs_tol=1e-12):raise AssertionError('bin-width failure control')
# Tamper one raw count without updating the manifest; SHA-256 verification must reject it.
with tempfile.TemporaryDirectory() as td:
 c=Path(td)/'pkg'; shutil.copytree(pkg,c); p=c/'spectra.csv'; p.write_text(p.read_text().replace('1100,100,60','1101,100,60',1))
 try:mod.validate(c,False)
 except ValueError as exc:
  if 'hash mismatch' not in str(exc):raise AssertionError(f'tamper rejected for wrong reason: {exc}')
 else:raise AssertionError('tampered package passed')
if not any('NOASSERTION' in w for w in warnings):raise AssertionError('fixture license warning missing')
print('WEAK_EL_FACILITY_EXPORT_GATE=PASS')
