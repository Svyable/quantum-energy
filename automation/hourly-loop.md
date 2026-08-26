# Hourly Venture Research Loop

This repository is updated by a scheduled ChatGPT research loop. The project is explicitly open-science/open-technology work for broad public benefit.

## Per-session contract

Every hourly session must:

1. Read `README.md`, `OPEN_SCIENCE.md`, `CONTRIBUTING.md`, `research/CALCULATION_VERIFICATION.md`, `research/session-history.md`, `research/evidence-map.md`, `technical/current-specification.md`, `venture/business-plan.md`, this file, and any open automation PRs before changing the program.
2. Complete **one bounded, high-value increment**. Prefer a falsifiable experiment, quantitative model, independent reproduction, manufacturing/control specification, evidence update, IP/prior-art boundary, safety improvement, or venture stage-gate improvement over narrative churn.
3. Separate every material claim into one of:
   - established evidence,
   - engineering assumption,
   - falsifiable hypothesis,
   - synthetic/model result,
   - experimental result,
   - novel invention concept.
4. Preserve explicit null models and kill/narrow rules. Never convert a favorable correlation into a quantum-mechanism claim without discriminating controls.
5. Update canonical repo files first. Use Git-friendly Markdown/CSV/code for durable records; binary artifacts may be supplemental but should not be the only record of important results.
6. Add dated source/provenance entries for new external claims and prefer primary sources for decisive statements.
7. For every new or changed decision-driving calculation, follow `research/CALCULATION_VERIFICATION.md`: explicit equation, symbols/units, dimensional check, independent recomputation or benchmark, limiting cases, uncertainty propagation, sensitivity to influential assumptions, numerical/conservation checks, and validity-domain statement.
8. Treat an arithmetic rerun using the same formula/code path as **verification**, not an independent cross-check. Seek a separate derivation, implementation, trusted benchmark, or physically known limiting case.
9. Preserve raw/minimally processed inputs and executable transformations where practical. Freeze stochastic seeds and record relevant software/package versions.
10. Check statistical independence and hierarchy. Do not count pixels, repeated sessions, or correlated observations as independent fabrication samples.
11. Run an adversarial claim audit: identify at least one plausible conventional explanation or counterexample for the principal scientific claim and state what evidence distinguishes it.
12. Keep negative/null results, superseded assumptions, and visible correction history in the repository.
13. Record what changed, checks performed, unresolved risks, and the single best next increment.

## Publication readiness

A session may mark a quantitative result `reproduced` only when committed inputs/code rerun and unit/numerical checks pass. Mark it `cross-checked` only when an independent method agrees inside a predeclared tolerance. Strong physical/platform claims require experimental support and preferably prospective/blinded validation. Exploratory and synthetic results must never be worded as measured performance.

## GitHub workflow — mandatory every session

- Never commit directly to `main`.
- Create a fresh branch named `automation/quantum-energy-YYYYMMDD-HHMM` using the session's local America/Chicago date/time.
- Commit all session changes to that branch.
- Open a **human-review pull request** against `main` before the session ends.
- PR title format: `Hourly quantum-energy: <short increment>`.
- PR body must include:
  - evidence added/changed and source provenance,
  - technical/business delta,
  - assumptions/hypotheses affected,
  - equations/calculations and independent checks performed,
  - uncertainty/sensitivity and statistical-independence issues,
  - conventional/null explanations considered,
  - files/data/code changed,
  - corrections or superseded claims,
  - unresolved risks,
  - next recommended increment.
- Do **not** merge automatically.
- If a GitHub write or PR creation fails, report the exact blocker; do not silently treat the session as successfully persisted.
- If the repo has an earlier open automation PR, read it for context, but still create a new session branch/PR unless doing so would create duplicate/conflicting work; in that case update the earlier PR and explicitly state why the session re-used it.

## Research priorities

Current order of operations unless evidence changes it:

1. Make R2/AT-04 reference metrology executable, independently checked, and reproducible.
2. Validate mechanism-discrimination and optical soft-sensor logic prospectively.
3. Release D18/PY-IT/eC9 causal experiment only after metrology/identifiability passes.
4. Demonstrate useful-work and durability gains before adding cavity complexity.
5. Generalize to a second modern OPV material system before broad platform claims.
6. Revisit cavity/polariton and quantum-information branches only after the energy/process-control branch has hard evidence or when a new result materially changes the expected value.

## Integrity rules

- Do not claim background/asynchronous work outside the scheduled run.
- Do not invent vendor quotes, measured device values, patent novelty, or experimental results.
- Synthetic/model values must be labeled as synthetic/planning assumptions.
- Never hide a failed calculation or nonphysical output; diagnose it and preserve the correction trail.
- Keep failures and null results in the repository.
- Prefer prospective predictions and blind/held-out checks to post-hoc curve fitting.
- Use the narrowest accurate scientific wording; `quantum` is not a substitute for unexplained, nanoscale, or efficient.
