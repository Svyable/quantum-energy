#!/usr/bin/env python3
import json, csv, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=ROOT/'technical/data/r2_transfer_fixture_protocol_v3_35.json'
CSV=ROOT/'technical/data/r2_transfer_fixture_inspection_v3_35.csv'
TOL=1e-12

def main():
    d=json.loads(SPEC.read_text())
    s=d['source_geometry']; f=d['fixture']; q=d['qualification_plan']
    c=(f['substrate_pocket_width_mm']-s['substrate_width_mm'])/2
    e=(s['substrate_width_mm']-f['central_keepout_width_mm'])/2
    assert abs(c-d['dimensional_checks']['pocket_clearance_expected_mm'])<TOL
    assert abs(e-d['dimensional_checks']['edge_support_expected_mm'])<TOL
    assert c>=0.05 and e>=2.0
    assert f['central_keepout_width_mm']>=d['shipping_insert']['minimum_clearance_above_device_mm'] # independent sanity: keepout larger than vertical clearance scalar
    assert q['minimum_remount_cycles_per_dummy']==10 and q['minimum_dummy_count']==3
    assert q['dummy_first'] is True
    rows=list(csv.DictReader(CSV.open()))
    assert [r['leg'] for r in rows]==['A1','B','A2']
    assert all(r['status']=='INCOMPLETE' for r in rows)
    assert d['inspection']['status_semantics']['INCOMPLETE'].startswith('Required provenance')
    print('PASS v3.35 structural fixture checks')
    print(f'planar_clearance_per_side_mm={c:.6f}')
    print(f'edge_support_band_mm={e:.6f}')
    print('screening_cycles_total=',q['minimum_remount_cycles_per_dummy']*q['minimum_dummy_count'])

if __name__=='__main__': main()
