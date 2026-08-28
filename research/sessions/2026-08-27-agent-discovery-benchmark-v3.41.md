# Session record — 2026-08-27 — v3.41 prospective agent discovery benchmark

## Increment

Built a Pages-ready public discovery surface plus an executable prospective benchmark for measuring whether unfamiliar agents can locate canonical project state without overstating the science.

## Startup audit

Read the current `main` governance/specification set required by `automation/hourly-loop.md`, including README, open-science/contribution/calculation rules, session/evidence records, current technical specification, venture plan, and automation contract.

Open automation PR #32 was inspected and is non-overlapping: it covers R2 transfer-sensor representativeness. Older open PR #7 is already recorded in `machine/analysis-registry.json` as superseded review provenance. This discovery increment therefore uses a fresh branch/PR.

Repository API state at start still showed no repository description, topics, homepage, Pages site, or detected license.

## Technical delta

Added:

- `machine/agent-discovery-benchmark-v3.41.json` — frozen prompt, response schema, expected canonical answers, scoring, penalties, validity boundary;
- `tools/score_agent_discovery_v3_41.py` — deterministic standard-library scorer;
- three software fixtures: perfect, safe-partial, and overclaiming;
- `docs/index.html`, `docs/index.md`, `docs/llms.txt`, `docs/.nojekyll` — static Pages-ready discovery surface;
- `.github/workflows/agent-discovery-benchmark.yml` — cross-Python scorer/site structural CI;
- evidence/session/venture records and discovery/index updates.

## Decision rule

Twenty exact items × 5 points = 100 base points.

Critical scientific/integrity misstatements incur 20 points each and, more importantly, force final status `FAIL` regardless of navigation score.

This intentionally values epistemic safety over raw retrieval completeness.

## Independent checks

CI independently verifies:

- rubric item count `6+6+4+4=20` and `20×5=100`;
- safe-partial fixture arithmetic `(3+6+4+2)×5=75`;
- overclaiming base arithmetic `(6+1+2+4)×5=65` and seven critical penalties floor the result at zero;
- the Pages-ready HTML has both `rel="describedby"` and Markdown `rel="alternate"` relations;
- required static files exist.

The independent arithmetic path does not import the production scorer.

## Synthetic/software results

- perfect fixture: 100 / PASS;
- safe-incomplete fixture: 75 / PARTIAL;
- overclaiming fixture: base 65, final 0 / FAIL.

No real external agent was tested in this session, so no real discoverability performance is claimed.

## Conventional/null explanations

Future benchmark failure may reflect indexing delay, browser/tool constraints, GitHub navigation, Pages configuration, or public-search coverage rather than deficient reasoning. Future benchmark success may be contaminated if the evaluated agent directly reads the public benchmark expected answers. URL trace review is required.

## Unresolved risks

- Pages is still not enabled in repository settings;
- repository description/topics remain unset;
- licensing remains unresolved;
- public benchmark code can contaminate a run if an agent finds it before answering;
- benchmark thresholds are engineering choices, not externally validated metrics;
- model/browser/search behavior will change over time and requires dated reruns.

## Single best next increment

After human review/merge, enable GitHub Pages from `main:/docs`, set the repository description/topics, and prospectively run the frozen v3.41 prompt against at least three independently configured public agents. Preserve model/version/tool/date and inspected-URL traces. Score responses unchanged and publish failures as well as successes.
