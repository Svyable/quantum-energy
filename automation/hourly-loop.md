# Hourly Venture Research Loop

This repository is advanced by a scheduled ChatGPT research loop. The project is explicitly open-science/open-technology work for broad public benefit.

The loop is not rewarded for producing many files or the strongest narrative. It is rewarded for **changed evidentiary state**: sharper bounds, independent reproductions, falsified assumptions, prospective tests, useful nulls, safer/manufacturable designs, and results other agents can reproduce or break.

## Start-of-run preflight

Every session must begin by:

1. Reading current `main` versions of `README.md`, `OPEN_SCIENCE.md`, `CONTRIBUTING.md`, `research/CALCULATION_VERIFICATION.md`, `research/session-history.md`, `research/evidence-map.md`, `technical/current-specification.md`, `venture/business-plan.md`, this file, `AGENTS.md` if present, and all open automation PRs.
2. Recording the current `main` commit SHA as the run base.
3. Identifying the **single highest-value unresolved bottleneck or falsifier** that is not already covered by an open PR.
4. Running an anti-drift check: do not spend another session refining the same metrology/infrastructure layer when a more decision-relevant physical falsifier, independent reproduction, real-data benchmark, safety/manufacturing risk, or prospective protocol is ready.
5. Defining the intended changed evidentiary state before doing the work.

A valid increment should produce at least one of:

- an independently reproduced result;
- a falsified or retired assumption;
- a sharper quantitative bound;
- a prospective experiment or blinded protocol;
- a real-data benchmark;
- a discriminating control;
- a validated manufacturing/metrology/safety specification;
- a useful negative/null result;
- an executable model that changes a scientific or engineering decision.

Narrative-only churn does not count.

## Per-session scientific contract

Every hourly session must:

1. Complete **one bounded, high-value increment**.
2. Separate every material statement into one of:
   - established evidence,
   - engineering assumption,
   - falsifiable hypothesis,
   - synthetic/model result,
   - experimental result,
   - novel invention concept.
3. Preserve explicit null models and kill/narrow rules. Never convert a favorable correlation into a quantum-mechanism claim without discriminating controls.
4. Prefer primary sources for decisive external claims: original papers, official datasets, standards, manufacturer datasheets for instrument specifications, and authors' public code/data.
5. When a paper links code/data, record exact DOI/version/tag/commit where practical. If current public code and paper text appear different, report a **lineage question** rather than guessing which is correct.
6. Do not copy upstream code unless reuse terms clearly allow it and copying is necessary. Prefer independent reimplementation from equations/specifications when that provides a stronger replication test.
7. Preserve raw/minimally processed inputs and executable transformations where practical. Freeze stochastic seeds and relevant software/runtime versions.
8. Keep negative/null results, failed checks, superseded assumptions, and visible correction history public.
9. Never fabricate measurements, vendor quotes, patent novelty/FTO, performance, citations, or source availability.
10. Do not use `quantum` as a synonym for unexplained, nanoscale, or efficient.

## Mandatory agent replication packet

Every decision-driving scientific/model increment must leave enough committed material that another agent or laboratory can attempt reproduction **without access to the originating conversation**.

Include, where applicable:

- exact claim and claim class;
- source/version provenance;
- machine-readable inputs;
- governing equations with defined symbols and units;
- executable command or deterministic procedure;
- expected outputs or frozen fixtures;
- predeclared numerical/physical tolerances;
- software/runtime/package versions, or a standard-library implementation when practical;
- at least one limiting-case, negative, or control test;
- an independent derivation, implementation, benchmark, or trusted reference case;
- uncertainty/sensitivity and validity domain;
- an explicit falsifier;
- for synthetic work, the next physical measurement that would discriminate it.

Prefer a compact replication packet over a large narrative document. Repeating the same equation through a second code path does not automatically constitute independent verification.

## Quantitative verification

For every new or changed decision-driving calculation, follow `research/CALCULATION_VERIFICATION.md` and additionally enforce:

1. Exact inputs, units, uncertainty/tolerance, provenance, date/version, and source class: measured, literature-derived, vendor-specified, fitted, assumed, or synthetic.
2. Governing equation/model with every symbol defined.
3. Consistent unit conversion and dimensional analysis.
4. Sign conventions, limiting cases, normalization/conservation checks, and validity regime.
5. Independent derivation, implementation, benchmark, or trusted reference case whenever practical.
6. Uncertainty propagation with correlated/systematic terms separated from independent random terms. Use interval/Monte-Carlo/distribution-aware propagation when local first-order propagation is not justified.
7. Sensitivity analysis over defensible ranges of influential assumptions, including whether the decision changes anywhere inside them.
8. Seeds, software/package versions, convergence/tolerances, and mesh/time-step/sample-size checks where relevant.
9. Experimental hierarchy: `lot -> substrate -> device/pixel -> session -> measurement`. Correlated repeats are not independent fabrication samples.
10. Predefined exclusions/outlier handling; report all functional samples unless a frozen QC rule excludes them.
11. For the principal claim, identify **at least two serious failure modes or conventional explanations when two are plausible**, and directly test/bound at least one in the current increment or specify the prospective discriminator.
12. A result may be called `reproduced` only when committed inputs/code rerun and unit/numerical checks pass. It may be called `cross-checked` only when an independent method agrees within a predeclared tolerance. Strong physical/platform claims require experimental support and preferably blinded/held-out prospective validation.
13. If an error is found, preserve the failure, add a visible correction note, recompute downstream impacts, mark superseded results, and state the correction prominently in the PR. Do not relax a tolerance merely to obtain a green check unless the old tolerance is demonstrated invalid and the change is documented and justified.

## Exact-head CI gate

When GitHub Actions or tests are available:

1. Run deterministic checks before the PR where practical.
2. Open the PR, then inspect workflows/checks on the **exact final PR head SHA** during the same run.
3. If a relevant workflow fails, inspect the failing job/log and correct the underlying issue when possible. Preserve a correction/failure record when scientifically relevant.
4. Re-check workflows on the new exact head.
5. Never report `all checks pass` while relevant checks are queued, in progress, unavailable, or only green on an older SHA.
6. If CI cannot complete or be inspected in the session, report that status precisely.
7. Lightweight scientific executables should, when practical, exercise multiple currently supported Python versions or another small environment matrix. Do not add heavyweight reproducibility infrastructure without a demonstrated need.

## Research priorities and anti-drift

Current priority sequence unless new evidence changes expected value:

1. Make R2/AT-04 reference metrology executable, independently checked, and grounded in real calibration/reference data.
2. Turn mechanism-discrimination logic into prospective, blinded protocols rather than continuing synthetic refinement indefinitely.
3. Advance D18/PY-IT/eC9 from interface/EPC measurement to field/charge-generation robustness and stabilized useful electrical work.
4. Demonstrate durability and manufacturing repeatability before cavity complexity or product-scale claims.
5. Prospectively validate on a second modern OPV material system before broad platform claims.
6. Revisit P0/polariton/open-system transport or another frontier branch when genuinely new evidence creates a higher-value falsifiable opportunity than continued polishing of the current branch.

Do not let metrology become an end in itself. Once a measurement layer is adequate to expose the next physical uncertainty, move the program to the physical test.

## Multi-objective useful-work rule

The modern-OPV program must not optimize a single microscopic proxy in isolation.

Track together, where relevant:

- interface population/state;
- EPC/reorganization;
- energetic offset;
- field robustness of Ex/CT formation;
- charge generation;
- `DeltaVnr` / Voc;
- FF;
- stabilized Pmax;
- durability;
- manufacturability and process tolerance;
- safety/environmental burden;
- cost and scale implications.

A favorable voltage-loss, EPC, cavity, spectral, or transport result is not useful-work evidence unless the relevant sink/output metric and conventional controls also pass.

For D18/PY-IT/eC9 specifically, a strong useful-work claim requires field-dependent generation evidence — bias-dependent PL, TDCF, or an independently justified equivalent — alongside DeltaVnr/Voc, charge generation, FF/Pmax, morphology/contact/transport controls, and durability.

If an arm lowers DeltaVnr but worsens field-dependent generation and fails to improve stabilized FF/Pmax, classify it as **voltage-loss/mechanism science**, not useful-work/platform validation.

No physical threshold may be invented from a synthetic model alone. Freeze physical decision rules from baseline data, instrument capability, literature precedent, or prospective power analysis as appropriate.

## Manufacturing, CAD, safety, and deployment

When these are the highest-value bottleneck, improve:

- product/system architecture;
- material/process stacks;
- manufacturing flows and travelers;
- BOMs and sourcing interfaces;
- tolerances and dimensional stack-ups;
- metrology and calibration;
- reliability and scale-up;
- cost and deployment logic;
- EHS and end-of-life burden.

For CAD-related work, produce detailed dimensional/mechanical specifications, schematics, interface definitions, fabrication-ready CAD briefs, or actually supported drawing files. Never claim native CAD outputs the available tools did not create.

Safety/environmental burden is part of technical performance. Record relevant solvent, lead/heavy-metal, vacuum, UV, electrical, thermal, waste, shipping, and end-of-life considerations where applicable.

## GitHub workflow — mandatory every successful session

- Never commit directly to `main`.
- Create a fresh branch named `automation/quantum-energy-YYYYMMDD-HHMM` using America/Chicago local date/time.
- Commit all session changes to that branch.
- Open a **human-review pull request** against current `main` before the session ends.
- PR title format: `Hourly quantum-energy: <short increment>`.
- Immediately before opening the PR, re-read current `main`. If it advanced during the run, incorporate the new canonical head without discarding either change set and verify the branch is not behind.
- PR body must include:
  - changed evidentiary state;
  - evidence/source provenance;
  - technical/business delta;
  - assumptions/hypotheses affected;
  - equations/calculations and independent checks;
  - uncertainty/sensitivity;
  - statistical-independence concerns;
  - strongest conventional/null explanations;
  - exact reproduction commands/data/fixtures where applicable;
  - files/data/code changed;
  - failures/corrections/superseded claims;
  - exact final head SHA and CI status;
  - unresolved risks;
  - single best next increment.
- Do **not** merge or enable auto-merge.
- If GitHub persistence or PR creation fails, report the exact blocker; do not treat the session as successfully persisted.
- If an earlier open automation PR overlaps, read it first. Prefer a fresh session PR; reuse an earlier PR only for a true duplicate/conflict and explicitly record why.

## End-of-run quality gate

Before calling an increment complete, verify:

- What belief, bound, design choice, protocol, or evidentiary state changed?
- Can another agent reproduce or falsify it from committed artifacts alone?
- What is the strongest remaining conventional explanation?
- Did any assumption silently become evidence?
- Did current `main` move while the session was running, and is the branch caught up?
- Are relevant exact-final-head checks actually complete and green, or is their status reported precisely?
- Did the session address the most decision-relevant bottleneck, or drift into low-value polishing?

The session report should be concise and state: changed evidentiary state; key quantitative result or negative finding; artifacts committed; independent/negative checks; failures/corrections; exact final head SHA and CI state; unresolved risks; single best next increment; and PR link.
