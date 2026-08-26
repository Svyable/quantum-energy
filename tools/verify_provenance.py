#!/usr/bin/env python3
"""Verify scientific fixture provenance and emit an independent runtime fingerprint.

This is publication infrastructure, not physical evidence. It checks the repository-native
Git blob identity frozen in provenance/scientific-fixtures-v3.10.json and independently
computes SHA-256 digests of the same bytes for CI logs/review.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "provenance" / "scientific-fixtures-v3.10.json"


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def parse_requirements(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            raise RuntimeError(f"unfrozen requirement in {path}: {line}")
        name, version = line.split("==", 1)
        result[name.strip().lower()] = version.strip()
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stack", choices=("baseline", "current"), default=None)
    ap.add_argument("--write-runtime", default=None)
    args = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = manifest["files"]
    paths = [item["path"] for item in files]
    if len(paths) != len(set(paths)):
        raise SystemExit("PROVENANCE_FAIL duplicate manifest paths")

    anchor = manifest["anchor_commit"]
    try:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", anchor, "HEAD"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"PROVENANCE_FAIL anchor {anchor} is not an ancestor of HEAD") from exc

    runtime_files = []
    for item in files:
        rel = item["path"]
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f"PROVENANCE_FAIL missing {rel}")
        actual_blob = run("git", "hash-object", "--", rel)
        expected_blob = item["git_blob_sha1"]
        if actual_blob != expected_blob:
            raise SystemExit(
                f"PROVENANCE_FAIL {rel}: git blob {actual_blob} != expected {expected_blob}. "
                "Scientific fixture changes require an explicit manifest update and review."
            )
        payload = path.read_bytes()
        runtime_files.append(
            {
                "path": rel,
                "bytes": len(payload),
                "git_blob_sha1": actual_blob,
                "sha256": hashlib.sha256(payload).hexdigest(),
                "role": item["role"],
            }
        )

    packages: dict[str, str] = {}
    if args.stack:
        req_path = ROOT / "requirements" / f"ci-{args.stack}.txt"
        expected = parse_requirements(req_path)
        for name, wanted in expected.items():
            actual = importlib.metadata.version(name)
            packages[name] = actual
            if actual != wanted:
                raise SystemExit(
                    f"PROVENANCE_FAIL package {name}={actual}; expected {wanted} for {args.stack}"
                )

    runtime = {
        "status": "PASS",
        "manifest_version": manifest["manifest_version"],
        "git_head": run("git", "rev-parse", "HEAD"),
        "git_anchor": anchor,
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "github_image_os": os.environ.get("ImageOS"),
        "github_image_version": os.environ.get("ImageVersion"),
        "stack": args.stack,
        "packages": packages,
        "files": runtime_files,
    }
    text = json.dumps(runtime, sort_keys=True, indent=2)
    print(text)
    if args.write_runtime:
        out = Path(args.write_runtime)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
