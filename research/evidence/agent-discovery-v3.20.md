# Evidence note — agent and research-software discovery v3.20

## External evidence

### GitHub topics

GitHub documents repository topics as a mechanism to help people find projects, contribute, and discover related solutions. GitHub allows up to 20 topics and recommends terms related to a repository's purpose, subject area, community, or language.

Source: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics

### GitHub citation metadata

GitHub supports a root `CITATION.cff` file as machine-readable citation metadata. When present on the default branch, GitHub exposes a "Cite this repository" surface and can render citation formats.

Source: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files

### AGENTS.md

AGENTS.md is an open convention for giving coding agents predictable project instructions. The published format describes it as a README-like file for agents and documents adoption across multiple coding-agent ecosystems.

Source: https://agents.md/

### llms.txt v2

The llms.txt v2 proposal defines a compact Markdown file at a website path to guide agents to high-value content. The August 2026 revision recommends standard link relations (`rel="describedby"` and `rel="alternate" type="text/markdown"`) so agents can discover llms.txt and Markdown representations without guessing.

Source: https://llmstxt.org/

Important project-specific inference: committing `llms.txt` to a GitHub repository improves repository-aware agent navigation, but it does not by itself provide a project-controlled website origin or the recommended HTTP/HTML link relations. Full v2 web discovery would require a project-controlled documentation surface such as GitHub Pages or another site.

### CodeMeta

CodeMeta provides JSON-LD metadata for scientific software and is intended to support metadata exchange, archiving, sharing, indexing, citation, and discovery across repositories and organizations. CodeMeta 3.0 is the current context used in this repository.

Sources:
- https://codemeta.github.io/developer-guide/
- https://w3id.org/codemeta/3.0

## Repository observation at session start

GitHub's public repository API reported:

- `description: null`;
- `topics: []`;
- `homepage: null`;
- `license: null`.

These are direct repository metadata observations, not scientific results.

## Engineering decision

Use multiple complementary discovery mechanisms rather than pretending there is one universal "AI discovery" standard:

1. precise technical language in `README.md` for GitHub/search indexing;
2. `AGENTS.md` for coding/research-agent working instructions;
3. `llms.txt` as a compact agent navigation index;
4. `CITATION.cff` for GitHub/citation systems;
5. `codemeta.json` for research-software metadata exchange;
6. `machine/project-index.json` for project-specific structured claim boundaries and canonical paths;
7. CI to catch stale paths and accidental false license metadata.

## Claim boundary

This work improves metadata and navigability. It does not demonstrate that a particular search engine, foundation model, crawler, or agent will index or rank the repository, and it must not be represented as guaranteed discoverability.
