# Hourly Venture Research Loop

This repository is updated by a scheduled ChatGPT research loop.

## Per-session contract

Every hourly session must:

1. Read `README.md`, `research/session-history.md`, `research/evidence-map.md`, `technical/current-specification.md`, `venture/business-plan.md`, this file, and any open automation PRs before changing the program.
2. Complete **one bounded, high-value increment**. Prefer a falsifiable experiment, quantitative model, manufacturing/control specification, evidence update, IP/prior-art boundary, or venture stage-gate improvement over narrative churn.
3. Separate every material claim into one of:
   - established evidence,
   - engineering assumption,
   - falsifiable hypothesis,
   - novel invention concept.
4. Preserve explicit null models and kill/narrow rules. Never convert a favorable correlation into a quantum-mechanism claim without the controls already defined by the program.
5. Update canonical repo files first. Use Git-friendly Markdown/CSV/code for durable records; binary artifacts may be supplemental but should not be the only record of important results.
6. Add dated evidence/source entries for new external claims.
7. Record what changed, unresolved risks, and the single best next increment.

## GitHub workflow — mandatory every session

- Never commit directly to `main`.
- Create a fresh branch named `automation/quantum-energy-YYYYMMDD-HHMM` using the session's local America/Chicago date/time.
- Commit all session changes to that branch.
- Open a **human-review pull request** against `main` before the session ends.
- PR title format: `Hourly quantum-energy: <short increment>`.
- PR body must include:
  - evidence added/changed,
  - technical/business delta,
  - assumptions/hypotheses affected,
  - checks or calculations performed,
  - files changed,
  - unresolved risks,
  - next recommended increment.
- Do **not** merge automatically.
- If a GitHub write or PR creation fails, report the exact blocker; do not silently treat the session as successfully persisted.
- If the repo has an earlier open automation PR, read it for context, but still create a new session branch/PR unless doing so would create duplicate/conflicting work; in that case update the earlier PR and explicitly state why the session re-used it.

## Research priorities

Current order of operations unless evidence changes it:

1. Make R2/AT-04 reference metrology executable and reproducible.
2. Validate mechanism-discrimination and optical soft-sensor logic prospectively.
3. Release D18/PY-IT/eC9 causal experiment only after metrology/identifiability passes.
4. Demonstrate useful-work and durability gains before adding cavity complexity.
5. Generalize to a second modern OPV material system before broad platform/IP claims.
6. Revisit cavity/polariton and quantum-information branches only after the energy/process-control branch has hard evidence or when a new result materially changes the expected value.

## Integrity rules

- Do not claim background/asynchronous work outside the scheduled run.
- Do not invent vendor quotes, measured device values, patent novelty, or experimental results.
- Synthetic/model values must be labeled as synthetic/planning assumptions.
- Keep failures and null results in the repository.
- Prefer prospective predictions and blind/held-out checks to post-hoc curve fitting.
