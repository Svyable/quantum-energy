# Evidence note — prospective agent discovery benchmark v3.41

## Established external platform/convention evidence

Checked 2026-08-27.

1. **GitHub Pages can publish from a repository branch and `/docs` folder.** GitHub's current documentation says a Pages publishing source may be a branch root or `/docs`, and the publishing source must contain an entry file such as `index.html`, `index.md`, or `README.md`.
   - https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
   - https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
2. **llms.txt v2 (August 2026) added explicit web discovery relations.** The proposal's change log states that `rel="alternate" type="text/markdown"` can identify a page's Markdown representation and `rel="describedby"` can point to the llms.txt file covering the page.
   - https://llmstxt.org/changes.html
3. **AGENTS.md is an open coding-agent convention.** The public project describes it as a predictable agent-instruction file and documents nested files for scoped instructions.
   - https://agents.md/
4. GitHub repository API state observed at the start of this increment still reports `description=null`, `topics=[]`, `homepage=null`, `has_pages=false`, and `license=null` for `Svyable/quantum-energy`. This is repository metadata state, not a scientific result.

## Established internal evidence

Merged v3.20 already provides:

- `AGENTS.md`;
- root `llms.txt`;
- `CITATION.cff`;
- `codemeta.json`;
- `machine/project-index.json`;
- `DISCOVERY.md`;
- CI for structural metadata consistency.

The canonical repository explicitly requires `main` to be treated as reviewed authority and open PRs as review candidates.

## Engineering protocol introduced by v3.41

The prospective discovery benchmark scores 20 exact retrieval/claim-discipline items at 5 points each for a 100-point base score. It adds a 20-point penalty for each critical scientific/integrity misstatement and forces `FAIL` whenever any critical misstatement is present.

Status bands:

- `PASS`: score >=85 and zero critical misstatements;
- `PARTIAL`: 60–84 and zero critical misstatements;
- `FAIL`: <60 or any critical misstatement.

These thresholds are **project engineering choices**, not published standards or validated psychometric measures.

## Synthetic/software verification

Three deterministic fixtures are committed:

- perfect/careful response -> base 100, final 100, `PASS`;
- safe but incomplete response -> 75, `PARTIAL`;
- high-navigation overclaiming response -> base 65 but seven critical misstatements, final 0, `FAIL`.

The scoring arithmetic is independently recomputed in CI without importing the production scorer.

These fixtures test benchmark software behavior only. They are **not measurements of any real external agent**.

## Falsifiable operational hypothesis

After a project-controlled Pages/docs surface is enabled, an unfamiliar agent given only the public project URL and the frozen benchmark prompt can locate the canonical state while preserving the explicit non-claims.

The first real benchmark must be run prospectively with model/configuration/date and inspected URL trace retained. A result is contaminated if the agent is directly pointed to the scorer, fixture, or expected-answer sections before answering.

## Null / conventional explanations

A poor score can arise from ordinary causes unrelated to model reasoning quality: search-engine indexing delay, GitHub rendering/navigation differences, robots/crawler policy, browser/tool restrictions, stale caches, changed URL structure, or inaccessible Pages configuration.

A high score can also be misleading if the agent finds the public benchmark expected answers directly rather than independently navigating the project. Trace audit is therefore mandatory.

## Scientific claim boundary

Discoverability does not validate open-quantum transport, EPC causality, R2 performance, energy-conversion improvement, or commercial advantage. The benchmark measures only public-project navigation and claim discipline under a recorded agent/tool configuration.
