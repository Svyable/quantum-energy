# Session record — 2026-08-27 — v3.20 agent and machine discovery

## Increment

Added a standards-aware discovery layer so humans, coding agents, research agents, citation systems, and research-software indexes can enter the repository through predictable, machine-readable paths without weakening the project's scientific claim boundaries.

## Repository gap observed

At session start, GitHub's repository API reported no description, no topics, no homepage, and no detected license. The connected automation can edit repository files, branches, issues, and pull requests but does not expose repository-description/topic settings, so those settings are tracked separately rather than falsely reported as changed.

## Files added or updated

- `README.md` — adds precise technical vocabulary, explicit non-claims, and an agent/machine discovery section.
- `AGENTS.md` — predictable working instructions for coding/research agents.
- `llms.txt` — compact LLM navigation index following the llms.txt v2 Markdown structure.
- `CITATION.cff` — root machine-readable citation metadata.
- `codemeta.json` — CodeMeta 3.0 JSON-LD metadata.
- `machine/project-index.json` — project-specific research domains, search phrases, canonical paths, contribution targets, and claim boundaries.
- `DISCOVERY.md` — discovery strategy, limits, recommended GitHub metadata, and anti-spam rule.
- `tools/validate_discovery_metadata.py` — standard-library structural consistency checks.
- `.github/workflows/discovery-metadata.yml` — cross-Python metadata CI.
- `research/evidence/agent-discovery-v3.20.md` — standards/source note.
- `research/sessions/2026-08-27-agent-discovery-v3.20.md` — this record.

## External standards/conventions used

- GitHub repository topics for subject-area discovery.
- GitHub `CITATION.cff` support.
- AGENTS.md open agent-instructions convention.
- llms.txt v2 proposal, including its web-discovery limitation.
- CodeMeta 3.0 JSON-LD for research-software metadata exchange.

## Scientific-integrity protections

The discovery metadata explicitly states that the repository has not established:

- a commercial quantum-energy breakthrough;
- a universal room-temperature quantum computer;
- a unique quantum mechanism for every photovoltaic or transport effect;
- commercially superior power conversion or lifetime.

The machine index preserves the established-evidence / engineering-assumption / hypothesis / synthetic-model / experimental-result / invention-concept distinction.

## Reuse-rights protection

No `license` field is added to CodeMeta or Citation metadata while the repository lacks selected explicit licenses. CI fails if machine metadata starts advertising a license without a root `LICENSE` file. Public visibility is not treated as permission to reuse.

## Discovery limitations

- These artifacts improve navigability and metadata; they do not guarantee ranking or indexing by any agent/search engine.
- Root `llms.txt` is useful to repository-aware tools, but GitHub does not expose this repo as a project-controlled `/llms.txt` website origin with llms.txt v2 link relations.
- GitHub description and topics still require a repository-settings write path.
- Formal DOI/version metadata should wait for a real release/archive rather than inventing one.

## Next best increment

After this PR is reviewed, set precise GitHub repository description/topics and create a project-controlled documentation/Pages surface that exposes a true web `/llms.txt`, Markdown alternatives, and v2 discovery links. In parallel, resolve explicit software/data/hardware licensing before claiming open-source reuse rights.
