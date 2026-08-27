# Discovery and indexing

This repository is intentionally designed to be discoverable by **humans, search engines, research-software indexes, citation systems, and AI/coding/research agents** without weakening scientific claim discipline.

## Discovery surfaces committed in-repo

### Human and GitHub search

`README.md` uses the project's actual technical vocabulary rather than vague "quantum energy" marketing. Important terms include open quantum systems, environment-assisted quantum transport (ENAQT), exciton transport, exciton polaritons, organic photovoltaics, electron-phonon coupling, spectroscopy, metrology, and uncertainty quantification.

### Coding and research agents

`AGENTS.md` is the predictable agent-oriented working-instructions file. It tells an agent what to read first, how claims are classified, how calculations must be checked, and how pull requests should be produced.

The AGENTS.md convention is an open format used across many coding-agent ecosystems. It should be treated as working instructions, not evidence about the science.

### LLM navigation

`llms.txt` is a compact Markdown index based on the llms.txt v2 proposal. It links agents to the smallest set of high-value Markdown and machine-readable resources.

Important limitation: the llms.txt proposal is a **web-site path convention** and v2 recommends HTTP/HTML link relations for automatic discovery. A file committed to a GitHub repository is still useful to repository-aware agents and code search, but GitHub does not expose our repository root as a project-controlled web origin with those link relations. Full web-native llms.txt discovery therefore requires a project-controlled documentation site or GitHub Pages deployment.

### Scholarly and research-software metadata

`CITATION.cff` gives GitHub and citation-aware tools machine-readable citation metadata. GitHub automatically exposes a "Cite this repository" surface when a valid `CITATION.cff` is present on the default branch.

`codemeta.json` uses CodeMeta 3.0 JSON-LD to describe the repository to research-software indexes and interoperable metadata systems.

`machine/project-index.json` is project-specific, not a standards claim. It is a compact index of canonical files, research domains, contribution targets, search phrases, and explicit claim boundaries.

## GitHub repository metadata still needed

At the time of this discovery pass, GitHub's repository API reported:

- description: unset;
- topics: none;
- homepage: unset;
- license: none detected.

The connected GitHub write surface available to this automation can change files, branches, issues, and pull requests but does not currently expose repository-description/topic settings. Those settings therefore require an administrator action in the GitHub UI or another authorized API path.

### Recommended GitHub description

> Open, evidence-first research on open quantum transport, ENAQT, exciton/polariton systems, organic photovoltaics, electron-phonon coupling, and reproducible metrology.

### Recommended GitHub topics

Use a precise subset rather than keyword stuffing; GitHub allows up to 20 topics. Recommended set:

- `open-science`
- `reproducible-research`
- `open-quantum-systems`
- `quantum-transport`
- `environment-assisted-quantum-transport`
- `exciton-transport`
- `exciton-polaritons`
- `organic-photovoltaics`
- `electron-phonon-coupling`
- `photovoltaics`
- `spectroscopy`
- `metrology`
- `uncertainty-quantification`
- `materials-science`
- `scientific-computing`
- `research-software`

## Future high-value discovery work

1. Merge the in-repo discovery metadata so GitHub, agents, and indexers see it on `main`.
2. Set the GitHub description and topics above.
3. Select explicit licenses for software, data/documentation, and hardware/CAD before claiming open-source reuse rights.
4. Create a project-controlled documentation site or GitHub Pages surface with `/llms.txt`, clean Markdown representations, and llms.txt v2 `rel="describedby"` / `rel="alternate"` link discovery.
5. When the first formal release is ready, archive/release it through a DOI-capable repository and add the DOI/version to `CITATION.cff` and `codemeta.json`.
6. Keep metadata synchronized in CI so an agent never follows a stale or missing canonical path.

## Anti-spam / scientific-integrity rule

Discoverability must not be improved by manufacturing citations, fake stars, synthetic social proof, misleading keywords, hidden text, inflated performance claims, or mass unsolicited posting. The best discovery strategy for this project is a precise vocabulary, useful open artifacts, reproducible results, valid metadata, and independent reproduction by others.
