#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, re, sys
from pathlib import Path

SCHEMA_VERSION='r2-facility-packet-v3.22'
SHA_RE=re.compile(r'^[0-9a-f]{64}$')
COMMIT_RE=re.compile(r'^[0-9a-f]{40}([0-9a-f]{24})?$')
REQUIRED_ROLES={'voc_intensity_raw','reference_repeatability_raw','reference_certificate_metadata','reference_certificate_source','source_spectrum_metadata','source_spectrum_data','detector_linearity_metadata','detector_linearity_data','analysis_freeze_record'}
MANIFEST_FIELDS={'schema_version','packet_id','facility_id','created_utc','protocol_version','reference_detector_id','source_spectrum_id','instrument_configuration_id','files'}
CSV_CORE={'lot_id','substrate_id','pixel_id','session_id','sweep_id','sequence_index','target_suns','calibrated_suns','reference_detector_id','source_spectrum_id','voc_V','qc_status'}
REPEAT_CORE={'session_id','sweep_id','sequence_index','target_suns','calibrated_suns','reference_detector_id','source_spectrum_id','qc_status'}
CERT_FIELDS={'reference_detector_id','certificate_id','issuer','issue_date','valid_from','valid_to','uncertainty_statement','source_document_sha256'}
SPECTRUM_FIELDS={'source_spectrum_id','measurement_date','instrument_id','wavelength_unit','intensity_unit','data_sha256'}
LINEARITY_FIELDS={'reference_detector_id','measurement_date','instrument_configuration_id','range_or_gain_state','result_summary','data_sha256'}
FREEZE_FIELDS={'protocol_version','analysis_commit_sha','qc_rule_version','holdout_rule_version','instrument_configuration_id','frozen_utc'}

def digest(path):
    h=hashlib.sha256(); size=0
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            size += len(block); h.update(block)
    return h.hexdigest(), size

def is_safe_relative(p):
    pp=Path(p)
    return not pp.is_absolute() and '..' not in pp.parts and str(pp) not in {'','.'}

def load_json(path):
    with path.open(encoding='utf-8') as f: return json.load(f)

def nonempty(d, fields):
    return sorted(k for k in fields if k not in d or d[k] in (None,'',[]))

def csv_ids(path, core):
    with path.open(newline='',encoding='utf-8') as f:
        rd=csv.DictReader(f); missing=sorted(core-set(rd.fieldnames or [])); rows=list(rd)
    if missing: return None, {'missing_columns':missing}
    if not rows: return None, {'empty_csv':True}
    bad_qc=sorted({r['qc_status'].strip().upper() for r in rows if r['qc_status'].strip().upper() not in {'PASS','PENDING','EXCLUDED'}})
    det=sorted({r['reference_detector_id'].strip() for r in rows if r['reference_detector_id'].strip()})
    spec=sorted({r['source_spectrum_id'].strip() for r in rows if r['source_spectrum_id'].strip()})
    return {'n_rows':len(rows),'detector_ids':det,'spectrum_ids':spec,'bad_qc':bad_qc}, None

def assess(packet_dir, manifest_name='manifest.json'):
    failures=[]; incomplete=[]; checks={}
    manifest_path=packet_dir/manifest_name
    boundary='Packet readiness only; PASS means required files are present, byte-integrity checked, and declared identities are internally consistent. It does not qualify measurement uncertainty, device performance, or mechanism.'
    if not manifest_path.exists():
        return {'schema_version':SCHEMA_VERSION,'overall_status':'INCOMPLETE','claim_boundary':boundary,'failed_checks':[],'incomplete_checks':['manifest_present'],'checks':{'manifest_present':{'status':'INCOMPLETE'}}}
    try: m=load_json(manifest_path)
    except Exception as e:
        return {'schema_version':SCHEMA_VERSION,'overall_status':'FAIL','claim_boundary':boundary,'failed_checks':['manifest_parse'],'incomplete_checks':[],'checks':{'manifest_parse':{'status':'FAIL','note':str(e)}}}
    def setc(name,status,**kw):
        checks[name]={'status':status,**kw}
        if status=='FAIL': failures.append(name)
        elif status=='INCOMPLETE': incomplete.append(name)
    miss=nonempty(m,MANIFEST_FIELDS); setc('manifest_required_fields','INCOMPLETE' if miss else 'PASS',missing=miss)
    sv=m.get('schema_version'); setc('manifest_schema','PASS' if sv==SCHEMA_VERSION else ('INCOMPLETE' if sv in (None,'') else 'FAIL'),value=sv,expected=SCHEMA_VERSION)
    files=m.get('files') if isinstance(m.get('files'),list) else []
    roles=[x.get('role','') for x in files if isinstance(x,dict)]; paths=[x.get('path','') for x in files if isinstance(x,dict)]
    dup_roles=sorted({x for x in roles if x and roles.count(x)>1}); dup_paths=sorted({x for x in paths if x and paths.count(x)>1})
    setc('unique_roles','FAIL' if dup_roles else 'PASS',duplicates=dup_roles); setc('unique_paths','FAIL' if dup_paths else 'PASS',duplicates=dup_paths)
    missing_roles=sorted(REQUIRED_ROLES-set(roles)); setc('required_roles','INCOMPLETE' if missing_roles else 'PASS',missing=missing_roles)
    role_paths={}; inventory=[]
    for i,ent in enumerate(files):
        if not isinstance(ent,dict): setc(f'file_entry_{i}','FAIL',note='file entry is not an object'); continue
        role=ent.get('role',''); rel=ent.get('path',''); declared=ent.get('sha256',''); declared_bytes=ent.get('bytes')
        if not role or not rel or not declared or declared_bytes is None: setc(f'file_entry_{i}','INCOMPLETE',note='role/path/sha256/bytes required'); continue
        if not is_safe_relative(rel): setc(f'path_safe_{i}','FAIL',path=rel); continue
        if not SHA_RE.match(str(declared)): setc(f'sha_format_{i}','FAIL',value=declared); continue
        p=packet_dir/rel
        if not p.exists() or not p.is_file(): setc(f'file_present_{i}','INCOMPLETE',path=rel); continue
        actual,n=digest(p); ok=(actual==declared and n==declared_bytes)
        setc(f'integrity_{i}','PASS' if ok else 'FAIL',role=role,path=rel,sha256=actual,bytes=n)
        inventory.append({'role':role,'path':rel,'sha256':actual,'bytes':n}); role_paths[role]=p
    det=m.get('reference_detector_id',''); spec=m.get('source_spectrum_id',''); config=m.get('instrument_configuration_id','')
    if 'voc_intensity_raw' in role_paths:
        info,err=csv_ids(role_paths['voc_intensity_raw'],CSV_CORE)
        if err: setc('voc_schema','FAIL',**err)
        else:
            bad=bool(info['bad_qc']) or info['detector_ids'] != ([det] if det else []) or info['spectrum_ids'] != ([spec] if spec else [])
            setc('voc_identity_consistency','FAIL' if bad else 'PASS',**info)
    if 'reference_repeatability_raw' in role_paths:
        info,err=csv_ids(role_paths['reference_repeatability_raw'],REPEAT_CORE)
        if err: setc('repeatability_schema','FAIL',**err)
        else:
            bad=bool(info['bad_qc']) or info['detector_ids'] != ([det] if det else []) or info['spectrum_ids'] != ([spec] if spec else [])
            setc('repeatability_identity_consistency','FAIL' if bad else 'PASS',**info)
    specs=[('reference_certificate_metadata',CERT_FIELDS,{'reference_detector_id':det}),('source_spectrum_metadata',SPECTRUM_FIELDS,{'source_spectrum_id':spec}),('detector_linearity_metadata',LINEARITY_FIELDS,{'reference_detector_id':det,'instrument_configuration_id':config}),('analysis_freeze_record',FREEZE_FIELDS,{'protocol_version':m.get('protocol_version',''),'instrument_configuration_id':config})]
    for role,fields,expected in specs:
        if role not in role_paths: continue
        try: d=load_json(role_paths[role])
        except Exception as e: setc(role+'_parse','FAIL',note=str(e)); continue
        missing=nonempty(d,fields); setc(role+'_fields','INCOMPLETE' if missing else 'PASS',missing=missing)
        mism={k:{'manifest':v,'file':d.get(k)} for k,v in expected.items() if v and d.get(k)!=v}; setc(role+'_identity','FAIL' if mism else 'PASS',mismatches=mism)
        for k in ('source_document_sha256','data_sha256'):
            if k in d and d[k]: setc(role+'_'+k+'_format','PASS' if SHA_RE.match(str(d[k])) else 'FAIL',value=d[k])
        if 'analysis_commit_sha' in d and d['analysis_commit_sha']:
            setc(role+'_analysis_commit_sha_format','PASS' if COMMIT_RE.match(str(d['analysis_commit_sha'])) else 'FAIL',value=d['analysis_commit_sha'])
    links=[('reference_certificate_metadata','source_document_sha256','reference_certificate_source'),('source_spectrum_metadata','data_sha256','source_spectrum_data'),('detector_linearity_metadata','data_sha256','detector_linearity_data')]
    inv_by_role={x['role']:x for x in inventory}
    for meta_role,hash_field,data_role in links:
        if meta_role not in role_paths or data_role not in inv_by_role: continue
        try: d=load_json(role_paths[meta_role])
        except Exception: continue
        declared=d.get(hash_field,''); actual=inv_by_role[data_role]['sha256']
        setc(meta_role+'_source_hash','PASS' if declared==actual else 'FAIL',declared=declared,actual=actual,data_role=data_role)
    overall='FAIL' if failures else ('INCOMPLETE' if incomplete else 'PASS')
    return {'schema_version':SCHEMA_VERSION,'claim_boundary':boundary,'overall_status':overall,'failed_checks':sorted(set(failures)),'incomplete_checks':sorted(set(incomplete)),'checks':checks,'integrity_inventory':inventory}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('packet_dir'); ap.add_argument('--manifest',default='manifest.json'); ap.add_argument('--output-json'); ns=ap.parse_args()
    result=assess(Path(ns.packet_dir),ns.manifest); text=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if ns.output_json: Path(ns.output_json).write_text(text,encoding='utf-8')
    else: sys.stdout.write(text)
    return 0 if result['overall_status']=='PASS' else 2

if __name__=='__main__': raise SystemExit(main())
