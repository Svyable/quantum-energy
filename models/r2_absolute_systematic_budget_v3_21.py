#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,math,sys
from collections import defaultdict
from pathlib import Path
import r2_covariance_power_v3_18 as cov

META_REQUIRED={
 "component_id","source_category","uncertainty_value","uncertainty_kind","coverage_factor",
 "correction_ln_amplitude","provenance_class","provenance","version_date","validity_status","note"
}
SHAPE_REQUIRED={"component_id","target_suns","shape_loading"}
VALID_KINDS={"standard_normal","expanded_normal","rectangular_half_width","triangular_half_width"}
VALID_PROVENANCE={"calibration_certificate","manufacturer_specification","literature","engineering_assumption","synthetic_assumption"}
VALIDITY_OK={"CURRENT","NOT_APPLICABLE"}

def load_csv(path, required):
    with open(path,newline="",encoding="utf-8") as h:
        rd=csv.DictReader(h); missing=sorted(required-set(rd.fieldnames or [])); rows=list(rd)
    if missing: raise ValueError("missing columns: "+", ".join(missing))
    if not rows: raise ValueError("empty CSV: "+str(path))
    return rows

def standard_u(row):
    v=float(row["uncertainty_value"])
    if v<0: raise ValueError("uncertainty_value must be nonnegative")
    kind=row["uncertainty_kind"].strip()
    if kind not in VALID_KINDS: raise ValueError("unsupported uncertainty_kind: "+kind)
    if kind=="standard_normal": return v
    if kind=="expanded_normal":
        k=float(row["coverage_factor"])
        if k<=0: raise ValueError("expanded_normal requires coverage_factor > 0")
        return v/k
    if kind=="rectangular_half_width": return v/math.sqrt(3.0)
    return v/math.sqrt(6.0)

def keyed_shapes(rows):
    out=defaultdict(dict)
    for r in rows:
        cid=r["component_id"].strip()
        key=round(float(r["target_suns"]),12)
        if key in out[cid]: raise ValueError(f"duplicate shape row {cid} {key}")
        out[cid][key]=float(r["shape_loading"])
    return out

def active_rows(rows):
    return [r for r in rows if not cov.as_bool(r.get("anchor_flag","false")) and r.get("qc_status","").strip().upper() in {"PASS","PENDING"}]

def assess(raw_rows, meta_rows, shape_rows):
    meta={}
    incomplete=[]
    for r in meta_rows:
        cid=r["component_id"].strip()
        if not cid or cid in meta: raise ValueError("blank/duplicate component_id")
        if r["provenance_class"].strip() not in VALID_PROVENANCE:
            raise ValueError("unsupported provenance_class: "+r["provenance_class"])
        if not r["provenance"].strip() or not r["version_date"].strip():
            incomplete.append(cid+":missing_provenance_or_version")
        if r["validity_status"].strip().upper() not in VALIDITY_OK:
            incomplete.append(cid+":validity_"+r["validity_status"].strip())
        meta[cid]=dict(r)
        meta[cid]["standard_u_1sigma"]=standard_u(r)
        meta[cid]["correction_ln_amplitude"]=float(r["correction_ln_amplitude"])
    shapes=keyed_shapes(shape_rows)
    if set(shapes)!=set(meta):
        raise ValueError("component IDs differ between metadata and shapes")
    target_keys=sorted({round(float(r["target_suns"]),12) for r in active_rows(raw_rows)})
    for cid,mp in shapes.items():
        missing=[k for k in target_keys if k not in mp]
        extra=[k for k in mp if k not in target_keys]
        if missing or extra: raise ValueError(f"shape grid mismatch for {cid}: missing={missing} extra={extra}")

    corrected=[]
    sidecar=[]
    for r in raw_rows:
        rr=dict(r)
        if cov.as_bool(r.get("anchor_flag","false")) or r.get("qc_status","").strip().upper() not in {"PASS","PENDING"}:
            corrected.append(rr); continue
        key=round(float(r["target_suns"]),12)
        total_corr=0.0
        for cid,m in meta.items():
            s=shapes[cid][key]
            total_corr += m["correction_ln_amplitude"]*s
            sidecar.append({
                "sweep_id":r["sweep_id"],"sequence_index":r["sequence_index"],
                "variable":"ln_calibrated_suns","component_id":"abs:"+cid,
                "loading_1sigma":repr(m["standard_u_1sigma"]*s),"unit":"1",
                "note":f"{m['source_category']}; {m['provenance_class']}; {m['provenance']}; {m['version_date']}"
            })
        c=float(r["calibrated_suns"])
        rr["calibrated_suns"]=repr(c*math.exp(-total_corr))
        corrected.append(rr)

    before=cov.assess(raw_rows,None)
    after=cov.assess(corrected,sidecar)
    by_before={s["sweep_id"]:s for s in before["sweeps"]}
    correction=[]
    for s in after["sweeps"]:
        b=by_before[s["sweep_id"]]["curvature"]
        correction.append({
            "sweep_id":s["sweep_id"],
            "uncorrected_curvature":b,
            "corrected_curvature":s["curvature"],
            "correction_delta_curvature":s["curvature"]-b,
            "abs_systematic_curvature_u_1sigma":math.sqrt(sum(
                c["variance_contribution"] for c in s["components"] if c["variable"]=="ln_calibrated_suns"
            )),
            "combined_curvature_u_1sigma_including_voc":s["curvature_u_1sigma"],
            "planning_power_effect_0p10":s["planning_power_effect_0p10"],
        })
    max_corr=max(abs(x["correction_delta_curvature"]) for x in correction)
    status="INCOMPLETE" if incomplete else ("FAIL" if max_corr>0.01 else "PASS")
    dominance=[]
    for s in after["sweeps"]:
        comps=[c for c in s["components"] if c["variable"]=="ln_calibrated_suns"]
        total=sum(c["variance_contribution"] for c in comps)
        for c in comps:
            dominance.append({
                "sweep_id":s["sweep_id"],"component_id":c["component_id"],
                "sd_contribution_abs":c["sd_contribution_abs"],
                "variance_fraction":0.0 if total==0 else c["variance_contribution"]/total
            })
    return {
        "schema_version":"r2-absolute-systematic-budget-v3.21",
        "status":status,
        "incomplete_reasons":sorted(incomplete),
        "claim_boundary":"This budget propagates declared external/reference systematic terms. It does not estimate repeatability from repetitions and does not identify DUT physics.",
        "gate":{"max_abs_correction_delta_curvature":0.01,"basis":"existing v3.16 calibration-curvature-bias project engineering gate"},
        "normalization":{
            "standard_normal":"u=value",
            "expanded_normal":"u=U/k",
            "rectangular_half_width":"u=a/sqrt(3)",
            "triangular_half_width":"u=a/sqrt(6)"
        },
        "components":[{
            "component_id":cid,"source_category":m["source_category"],
            "standard_u_1sigma":m["standard_u_1sigma"],
            "correction_ln_amplitude":m["correction_ln_amplitude"],
            "provenance_class":m["provenance_class"],"provenance":m["provenance"],
            "version_date":m["version_date"],"validity_status":m["validity_status"]
        } for cid,m in sorted(meta.items())],
        "sweeps":correction,
        "dominance":sorted(dominance,key=lambda d:(d["sweep_id"],-d["variance_fraction"],d["component_id"])),
        "sidecar_rows":sidecar,
        "corrected_rows":corrected
    }

def write_csv(path,rows,fieldnames):
    with open(path,"w",newline="",encoding="utf-8") as h:
        w=csv.DictWriter(h,fieldnames=fieldnames); w.writeheader(); w.writerows(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("measurement_csv"); p.add_argument("component_metadata_csv"); p.add_argument("component_shapes_csv")
    p.add_argument("--output-json"); p.add_argument("--output-sidecar"); p.add_argument("--output-corrected-csv")
    ns=p.parse_args()
    raw=cov.load_raw(ns.measurement_csv)
    result=assess(raw,load_csv(ns.component_metadata_csv,META_REQUIRED),load_csv(ns.component_shapes_csv,SHAPE_REQUIRED))
    side=result.pop("sidecar_rows"); corrected=result.pop("corrected_rows")
    if ns.output_sidecar:
        write_csv(ns.output_sidecar,side,["sweep_id","sequence_index","variable","component_id","loading_1sigma","unit","note"])
    if ns.output_corrected_csv:
        write_csv(ns.output_corrected_csv,corrected,list(corrected[0].keys()))
    txt=json.dumps(result,sort_keys=True,indent=2)+"\n"
    if ns.output_json: Path(ns.output_json).write_text(txt,encoding="utf-8",newline="\n")
    else: sys.stdout.write(txt)
    return 0 if result["status"]=="PASS" else 2
if __name__=="__main__": raise SystemExit(main())
