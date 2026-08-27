#!/usr/bin/env python3
"""Validate and self-test the v3.30 synthetic R2 facility dry-run packet.

Standard-library only. A STRUCTURAL_PASS is software/interoperability verification,
never a scientific or facility-capability PASS.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V327 = ROOT / "technical/data/r2_facility_capability_contract_v3_27.json"
V330 = ROOT / "technical/data/r2_facility_dryrun_contract_v3_30.json"
MANIFEST_COLUMNS = ["role", "relative_path", "sha256", "byte_count", "evidence_state", "provenance_note"]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def safe_relative_path(value: str) -> bool:
    if not value or os.path.isabs(value):
        return False
    p = Path(value)
    return ".." not in p.parts and str(p) not in {".", ""}


def load_contracts():
    v327 = json.loads(V327.read_text(encoding="utf-8"))
    v330 = json.loads(V330.read_text(encoding="utf-8"))
    return v327, v330


def validate_contract() -> None:
    v327, v330 = load_contracts()
    required = v327["required_packet_roles"]
    if len(required) != 15 or len(set(required)) != 15:
        raise AssertionError(f"v3.27 required_packet_roles changed: expected 15 unique, got {len(required)}")
    cap_roles = []
    for cap in v327["required_capabilities"]:
        cap_roles.extend(cap["evidence_roles"])
    if len(set(cap_roles)) != 13:
        raise AssertionError(f"Expected 13 unique capability evidence roles, got {len(set(cap_roles))}")
    administrative = set(required) - set(cap_roles)
    if administrative != {"analysis_freeze_record", "packet_manifest"}:
        raise AssertionError(f"Unexpected administrative roles: {sorted(administrative)}")
    if v330["manifest_columns"] != MANIFEST_COLUMNS:
        raise AssertionError("v3.30 manifest column contract drifted")
    forbidden = {"PASS", "SCIENTIFIC_PASS", "FACILITY_PASS"}
    if forbidden.intersection(v330["dryrun_status_semantics"]):
        raise AssertionError("Dry-run contract may not expose a scientific PASS status")
    if v330["statistical_hierarchy_inherited"] != v327["statistical_hierarchy"]:
        raise AssertionError("Statistical hierarchy differs from v3.27")


def read_manifest(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != MANIFEST_COLUMNS:
            raise ValueError("manifest columns do not match v3.30 contract")
        return list(reader)


def validate_packet(packet_dir: Path) -> tuple[str, list[str]]:
    v327, v330 = load_contracts()
    required = set(v327["required_packet_roles"])
    manifest = packet_dir / "packet_manifest.csv"
    if not manifest.exists():
        return "INCOMPLETE", ["packet_manifest.csv missing"]
    try:
        rows = read_manifest(manifest)
    except Exception as exc:
        return "FAIL", [f"manifest invalid: {exc}"]

    errors, missing = [], []
    roles = [r["role"] for r in rows]
    duplicate_roles = sorted({r for r in roles if roles.count(r) > 1})
    if duplicate_roles:
        errors.append(f"duplicate roles: {duplicate_roles}")
    row_roles = set(roles)
    missing.extend(sorted(required - row_roles))
    extra = sorted(row_roles - required)
    if extra:
        errors.append(f"unexpected roles: {extra}")

    allowed_states = set(v330["allowed_evidence_states"])
    for row in rows:
        role = row["role"]
        rel = row["relative_path"]
        state = row["evidence_state"]
        if state not in allowed_states:
            errors.append(f"{role}: invalid evidence_state {state}")
            continue
        if state == "MISSING":
            missing.append(role)
            continue
        if not row["provenance_note"].strip():
            missing.append(f"{role}:provenance_note")
        if not safe_relative_path(rel):
            errors.append(f"{role}: unsafe relative_path {rel!r}")
            continue
        obj = packet_dir / rel
        if not obj.exists() or not obj.is_file():
            missing.append(role)
            continue
        try:
            expected_bytes = int(row["byte_count"])
        except ValueError:
            errors.append(f"{role}: byte_count not integer")
            continue
        observed_bytes = obj.stat().st_size
        if observed_bytes != expected_bytes:
            errors.append(f"{role}: byte_count mismatch {observed_bytes} != {expected_bytes}")
        digest = row["sha256"]
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            errors.append(f"{role}: invalid SHA-256 syntax")
        elif sha256_file(obj) != digest:
            errors.append(f"{role}: SHA-256 mismatch")

    if errors:
        return "FAIL", errors
    if missing:
        return "INCOMPLETE", sorted(set(missing))
    return "STRUCTURAL_PASS", []


def make_synthetic_packet(dest: Path) -> Path:
    v327, _ = load_contracts()
    dest.mkdir(parents=True, exist_ok=True)
    rows = []
    for role in v327["required_packet_roles"]:
        rel = "packet_manifest.csv" if role == "packet_manifest" else f"objects/{role}.txt"
        if role == "packet_manifest":
            continue
        obj = dest / rel
        obj.parent.mkdir(parents=True, exist_ok=True)
        body = (
            "SYNTHETIC PLACEHOLDER ONLY\n"
            f"role={role}\n"
            "schema=v3.30\n"
            "claim=structural interoperability test; not facility evidence\n"
        ).encode("utf-8")
        obj.write_bytes(body)
        rows.append({
            "role": role,
            "relative_path": rel,
            "sha256": hashlib.sha256(body).hexdigest(),
            "byte_count": str(len(body)),
            "evidence_state": "SYNTHETIC_PLACEHOLDER",
            "provenance_note": "deterministic v3.30 synthetic self-test object",
        })
    # Manifest self-role is represented by a deterministic sidecar so the manifest cannot hash itself recursively.
    sidecar = dest / "objects/packet_manifest.txt"
    sidecar.parent.mkdir(parents=True, exist_ok=True)
    sidecar_body = b"SYNTHETIC PLACEHOLDER ONLY\nrole=packet_manifest\nschema=v3.30\n"
    sidecar.write_bytes(sidecar_body)
    rows.append({
        "role": "packet_manifest",
        "relative_path": "objects/packet_manifest.txt",
        "sha256": hashlib.sha256(sidecar_body).hexdigest(),
        "byte_count": str(len(sidecar_body)),
        "evidence_state": "SYNTHETIC_PLACEHOLDER",
        "provenance_note": "manifest-role sidecar; packet_manifest.csv is the transport manifest",
    })
    manifest = dest / "packet_manifest.csv"
    with manifest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=MANIFEST_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return manifest


def self_test() -> None:
    validate_contract()
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "packet"
        make_synthetic_packet(base)
        status, issues = validate_packet(base)
        assert status == "STRUCTURAL_PASS", (status, issues)

        # Missing required role -> INCOMPLETE.
        missing_case = Path(td) / "missing"
        shutil.copytree(base, missing_case)
        rows = read_manifest(missing_case / "packet_manifest.csv")
        rows = [r for r in rows if r["role"] != "source_spectrum_data"]
        with (missing_case / "packet_manifest.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=MANIFEST_COLUMNS); w.writeheader(); w.writerows(rows)
        assert validate_packet(missing_case)[0] == "INCOMPLETE"

        # Byte tamper -> FAIL.
        tamper_case = Path(td) / "tamper"
        shutil.copytree(base, tamper_case)
        with (tamper_case / "objects/voc_intensity_raw.txt").open("ab") as f:
            f.write(b"tamper")
        assert validate_packet(tamper_case)[0] == "FAIL"

        # Duplicate role -> FAIL.
        dup_case = Path(td) / "duplicate"
        shutil.copytree(base, dup_case)
        rows = read_manifest(dup_case / "packet_manifest.csv")
        rows.append(dict(rows[0]))
        with (dup_case / "packet_manifest.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=MANIFEST_COLUMNS); w.writeheader(); w.writerows(rows)
        assert validate_packet(dup_case)[0] == "FAIL"

        # Path traversal -> FAIL.
        path_case = Path(td) / "path"
        shutil.copytree(base, path_case)
        rows = read_manifest(path_case / "packet_manifest.csv")
        rows[0]["relative_path"] = "../escape.txt"
        with (path_case / "packet_manifest.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=MANIFEST_COLUMNS); w.writeheader(); w.writerows(rows)
        assert validate_packet(path_case)[0] == "FAIL"

        # Synthetic packet must never produce scientific PASS.
        assert validate_packet(base)[0] == "STRUCTURAL_PASS"
        assert validate_packet(base)[0] != "PASS"

    print("v3.30 facility dry-run contract: all structural/adversarial checks passed")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--packet", type=Path)
    ap.add_argument("--generate-synthetic", type=Path)
    args = ap.parse_args()
    if args.self_test:
        self_test(); return 0
    validate_contract()
    if args.generate_synthetic:
        make_synthetic_packet(args.generate_synthetic)
        print(args.generate_synthetic)
    if args.packet:
        status, issues = validate_packet(args.packet)
        print(json.dumps({"status": status, "issues": issues}, indent=2))
        return 0 if status == "STRUCTURAL_PASS" else 2
    if not args.generate_synthetic and not args.packet:
        ap.error("choose --self-test, --packet, or --generate-synthetic")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
