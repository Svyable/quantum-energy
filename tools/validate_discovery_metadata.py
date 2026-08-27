#!/usr/bin/env python3
"""Validate agent/research discovery metadata without third-party dependencies.

This is a structural and consistency check, not a substitute for the official
CFF or CodeMeta validators and not evidence for any scientific claim.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/Svyable/quantum-energy"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: str) -> str:
    p = ROOT / path
    require(p.is_file(), f"missing file: {path}")
    return p.read_text(encoding="utf-8")


def validate_json() -> dict:
    codemeta = json.loads(read("codemeta.json"))
    require(codemeta["@context"] == "https://w3id.org/codemeta/3.0", "unexpected CodeMeta context")
    require(codemeta["@type"] == "SoftwareSourceCode", "unexpected CodeMeta type")
    require(codemeta["codeRepository"] == REPO, "CodeMeta repository mismatch")
    require(codemeta["issueTracker"] == REPO + "/issues", "CodeMeta issue tracker mismatch")
    require(codemeta.get("isAccessibleForFree") is True, "public accessibility metadata missing")

    index = json.loads(read("machine/project-index.json"))
    require(index["project"]["repository"] == REPO, "project index repository mismatch")
    require(index["project"]["canonical_branch"] == "main", "canonical branch must be main")
    require(index["licensing"]["status"] == "unresolved", "license status drifted without review")
    require(len(index["research_domains"]) >= 8, "research-domain index unexpectedly sparse")
    require(len(index["search_terms"]) >= 8, "search-term index unexpectedly sparse")

    for entry in index["agent_entrypoints"]:
        path = entry["path"]
        require((ROOT / path).is_file(), f"project index points to missing file: {path}")

    if not (ROOT / "LICENSE").exists():
        require("license" not in codemeta, "CodeMeta claims a license but root LICENSE is unresolved")

    return index


def validate_citation() -> None:
    text = read("CITATION.cff")
    required = [
        "cff-version: 1.2.0",
        "title: Quantum Energy Venture Lab",
        "type: software",
        "authors:",
        "repository-code: " + REPO,
    ]
    for token in required:
        require(token in text, f"CITATION.cff missing: {token}")
    require("license:" not in text, "CITATION.cff must not invent unresolved license")


def validate_agent_files() -> None:
    agents = read("AGENTS.md")
    for token in [
        "OPEN_SCIENCE.md",
        "research/CALCULATION_VERIFICATION.md",
        "established evidence",
        "engineering assumption",
        "synthetic/model result",
        "Never convert one class into another",
        "Never commit directly to `main`",
    ]:
        require(token in agents, f"AGENTS.md missing critical instruction: {token}")

    readme = read("README.md")
    for token in ["AGENTS.md", "llms.txt", "machine/project-index.json", "codemeta.json", "CITATION.cff"]:
        require(token in readme, f"README discovery section missing {token}")


def validate_llms() -> None:
    text = read("llms.txt")
    lines = text.splitlines()
    require(lines and lines[0] == "# Quantum Energy Venture Lab", "llms.txt must start with project H1")
    require(any(line.startswith("> ") for line in lines[1:6]), "llms.txt needs summary blockquote near top")

    urls = re.findall(r"\[[^\]]+\]\((https://github\.com/Svyable/quantum-energy/[^)]+)\)", text)
    require(len(urls) >= 10, "llms.txt link index unexpectedly sparse")
    for url in urls:
        if "/blob/main/" in url:
            path = unquote(url.split("/blob/main/", 1)[1])
            require((ROOT / path).is_file(), f"llms.txt blob link points to missing file: {path}")
        elif "/tree/main/" in url:
            path = unquote(url.split("/tree/main/", 1)[1])
            require((ROOT / path).is_dir(), f"llms.txt tree link points to missing directory: {path}")
        else:
            require(url in {REPO + "/pulls"}, f"unreviewed llms.txt project URL shape: {url}")


def validate_claim_boundary(index: dict) -> None:
    not_established = " ".join(index["claim_boundary"]["not_established"]).lower()
    for phrase in ["commercial quantum-energy breakthrough", "universal room-temperature quantum computer"]:
        require(phrase in not_established, f"missing explicit non-claim: {phrase}")

    discovery = read("DISCOVERY.md").lower()
    require("anti-spam" in discovery, "DISCOVERY.md needs anti-spam rule")
    require("description: unset" in discovery, "repository-metadata gap must remain explicit until changed")
    require("topics: none" in discovery, "repository-topic gap must remain explicit until changed")


def main() -> int:
    index = validate_json()
    validate_citation()
    validate_agent_files()
    validate_llms()
    validate_claim_boundary(index)
    print("discovery metadata structural consistency: PASS")
    print(f"agent entrypoints: {len(index['agent_entrypoints'])}")
    print(f"research domains: {len(index['research_domains'])}")
    print(f"search terms: {len(index['search_terms'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
