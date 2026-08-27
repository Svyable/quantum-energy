#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, shutil, tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('preflight',HERE/'r2_facility_packet_preflight_v3_22.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def h(path):
    b=path.read_bytes(); return hashlib.sha256(b).hexdigest(),len(b)

def write_json(p,d): p.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n',encoding='utf-8')

def make_packet(root):
    root.mkdir(parents=True,exist_ok=True)
    voc=root/'voc.csv'
    voc.write_text('lot_id,substrate_id,pixel_id,session_id,sweep_id,sequence_index,target_suns,calibrated_suns,reference_detector_id,source_spectrum_id,voc_V,qc_status\nSYNLOT,S01,A,SES01,SW1,1,0.1,0.1001,SYN-REF,SYN-SPEC,0.70,PASS\nSYNLOT,S01,A,SES01,SW1,2,1.0,1.001,SYN-REF,SYN-SPEC,0.80,PASS\n',encoding='utf-8')
    rep=root/'repeatability.csv'
    rep.write_text('session_id,sweep_id,sequence_index,target_suns,calibrated_suns,reference_detector_id,source_spectrum_id,qc_status\nCAL01,C1,1,0.1,0.1000,SYN-REF,SYN-SPEC,PASS\nCAL01,C1,2,1.0,1.0000,SYN-REF,SYN-SPEC,PASS\n',encoding='utf-8')
    certsrc=root/'certificate-source.txt'; certsrc.write_text('SYNTHETIC PLACEHOLDER CERTIFICATE SOURCE — NOT A REAL CALIBRATION CERTIFICATE.\n',encoding='utf-8')
    specdata=root/'spectrum-data.csv'; specdata.write_text('wavelength_nm,relative_intensity\n500,1.0\n600,0.9\n',encoding='utf-8')
    lindata=root/'linearity-data.csv'; lindata.write_text('nominal_fraction,response_fraction\n0.1,0.1001\n1.0,1.0000\n',encoding='utf-8')
    cert=root/'certificate.json'; write_json(cert,{'reference_detector_id':'SYN-REF','certificate_id':'SYN-CERT-NOT-REAL','issuer':'SYNTHETIC FIXTURE','issue_date':'2026-08-27','valid_from':'2026-08-27','valid_to':'2026-08-28','uncertainty_statement':'Synthetic fixture only; no physical uncertainty claim.','source_document_sha256':h(certsrc)[0]})
    spectrum=root/'spectrum.json'; write_json(spectrum,{'source_spectrum_id':'SYN-SPEC','measurement_date':'2026-08-27','instrument_id':'SYN-INSTRUMENT','wavelength_unit':'nm','intensity_unit':'relative','data_sha256':h(specdata)[0]})
    linearity=root/'linearity.json'; write_json(linearity,{'reference_detector_id':'SYN-REF','measurement_date':'2026-08-27','instrument_configuration_id':'SYN-CONFIG','range_or_gain_state':'SYN-RANGE','result_summary':'Synthetic fixture only.','data_sha256':h(lindata)[0]})
    freeze=root/'freeze.json'; write_json(freeze,{'protocol_version':'SYN-PROTOCOL','analysis_commit_sha':'0'*40,'qc_rule_version':'SYN-QC','holdout_rule_version':'SYN-HOLDOUT','instrument_configuration_id':'SYN-CONFIG','frozen_utc':'2026-08-27T06:00:00Z'})
    roles=[('voc_intensity_raw',voc),('reference_repeatability_raw',rep),('reference_certificate_metadata',cert),('reference_certificate_source',certsrc),('source_spectrum_metadata',spectrum),('source_spectrum_data',specdata),('detector_linearity_metadata',linearity),('detector_linearity_data',lindata),('analysis_freeze_record',freeze)]
    manifest={'schema_version':m.SCHEMA_VERSION,'packet_id':'SYN-PACKET-V3.22','facility_id':'SYNTHETIC-FACILITY-NOT-REAL','created_utc':'2026-08-27T06:00:00Z','protocol_version':'SYN-PROTOCOL','reference_detector_id':'SYN-REF','source_spectrum_id':'SYN-SPEC','instrument_configuration_id':'SYN-CONFIG','files':[]}
    for role,p in roles:
        sha,n=h(p); manifest['files'].append({'role':role,'path':p.name,'sha256':sha,'bytes':n})
    write_json(root/'manifest.json',manifest)

def assert_status(d,status,check=None):
    if d['overall_status']!=status: raise AssertionError((status,d))
    if check and check not in d['failed_checks']+d['incomplete_checks']: raise AssertionError((check,d))

def main():
    with tempfile.TemporaryDirectory() as td:
        base=Path(td)/'base'; make_packet(base)
        assert_status(m.assess(base),'PASS')
        t=Path(td)/'tamper'; shutil.copytree(base,t); (t/'voc.csv').write_text((t/'voc.csv').read_text()+'\n',encoding='utf-8')
        assert_status(m.assess(t),'FAIL','integrity_0')
        q=Path(td)/'missing'; shutil.copytree(base,q); man=json.loads((q/'manifest.json').read_text()); man['files']=[x for x in man['files'] if x['role']!='reference_certificate_source']; write_json(q/'manifest.json',man)
        assert_status(m.assess(q),'INCOMPLETE','required_roles')
        r=Path(td)/'identity'; shutil.copytree(base,r); txt=(r/'repeatability.csv').read_text().replace('SYN-REF','OTHER-REF'); (r/'repeatability.csv').write_text(txt,encoding='utf-8'); man=json.loads((r/'manifest.json').read_text())
        for x in man['files']:
            if x['role']=='reference_repeatability_raw': x['sha256'],x['bytes']=h(r/'repeatability.csv')
        write_json(r/'manifest.json',man); assert_status(m.assess(r),'FAIL','repeatability_identity_consistency')
        s=Path(td)/'traversal'; shutil.copytree(base,s); man=json.loads((s/'manifest.json').read_text()); man['files'][0]['path']='../voc.csv'; write_json(s/'manifest.json',man)
        assert_status(m.assess(s),'FAIL','path_safe_0')
        u=Path(td)/'binding'; shutil.copytree(base,u); (u/'certificate-source.txt').write_text('DIFFERENT SYNTHETIC SOURCE\n',encoding='utf-8'); man=json.loads((u/'manifest.json').read_text())
        for x in man['files']:
            if x['role']=='reference_certificate_source': x['sha256'],x['bytes']=h(u/'certificate-source.txt')
        write_json(u/'manifest.json',man); assert_status(m.assess(u),'FAIL','reference_certificate_metadata_source_hash')
        print('PASS: complete, tamper, missing, identity, traversal, source-binding checks')
    return 0

if __name__=='__main__': raise SystemExit(main())
