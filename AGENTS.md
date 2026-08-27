# AGENTS.md

## Project

This repository is an open, evidence-first research and engineering program studying **programmable open-quantum transport** and adjacent energy/materials systems, including open quantum systems, environment-assisted transport, exciton and polariton transport, organic photovoltaics, electron-phonon coupling, spectroscopy, metrology, manufacturing controls, and reproducible scientific software.

The project is intentionally public for broad societal benefit. The goal is not to make the word "quantum" fit a preferred narrative. The goal is to discover which mechanisms are real, useful, reproducible, scalable, safe, and economically deployable.

Repository: https://github.com/Svyable/quantum-energy

## Read first

Before changing scientific or technical content, read:

1. `README.md` — mission and top-level orientation.
2. `OPEN_SCIENCE.md` — evidence classes and publication rules.
3. `research/CALCULATION_VERIFICATION.md` — mandatory calculation, uncertainty, and correction protocol.
4. `CONTRIBUTING.md` — contribution and wording standards.
5. `research/session-history.md` — chronological research history.
6. `research/evidence-map.md` — evidence and source map.
7. `technical/current-specification.md` — current engineering specification.
8. `automation/hourly-loop.md` — automated research workflow.

For machine-oriented navigation, also read `llms.txt`, `codemeta.json`, `CITATION.cff`, and `machine/project-index.json`.

## Scientific claim discipline

Always distinguish these classes explicitly:

- established evidence;
- engineering assumption;
- falsifiable hypothesis;
- synthetic/model result;
- experimental result;
- novel invention concept.

Never convert one class into another by wording alone.

Do not claim that:

- long-lived room-temperature electronic coherence is required for robust excitation transport;
- unexplained behavior is automatically quantum;
- a model is a measurement;
- vendor specifications are independent validation;
- an accelerated-aging duration is a field lifetime without a validated acceleration model;
- a single ideality factor, spectrum, or cavity response uniquely identifies a mechanism;
- this repository has demonstrated a commercial energy breakthrough, fault-tolerant quantum computer, or platform-level quantum advantage without prospective experimental evidence.

Keep conventional optical, morphological, electrostatic, contact, tunneling, transport, thermal, measurement, and statistical explanations live until discriminating evidence rules them down.

## Calculation rules

For every decision-driving quantitative result:

1. Record exact inputs, SI units, uncertainty, provenance, and whether each value is measured, literature, vendor, fitted, assumed, or synthetic.
2. State the equation and define symbols.
3. Perform dimensional analysis.
4. Check sign conventions, limiting cases, normalization/conservation, and validity regime.
5. Independently recompute using a different derivation, implementation, benchmark, or reference case.
6. Propagate uncertainty, including correlated/systematic terms when relevant.
7. Sweep influential assumptions and state whether the decision changes.
8. Record seeds, package/runtime versions, numerical tolerances, and convergence checks.
9. Preserve hierarchy such as lot -> substrate -> pixel/device -> session -> measurement.
10. Keep null models and conventional explanations visible.
11. Publish corrections visibly and recompute downstream results when needed.

Use the terms `reproduced`, `cross-checked`, `experimentally supported`, and `prospectively validated` only at the evidence levels defined in `OPEN_SCIENCE.md`.

## Working with code and data

- Prefer standard-library Python when it keeps the scientific calculation transparent; otherwise pin and record dependencies.
- Keep generated scientific fixtures deterministic where possible.
- Tests must include at least one limiting/negative/adversarial case for decision-driving calculations.
- Do not hand-transcribe generated decision tables when they can be machine-generated and exact-compared in CI.
- Preserve raw or minimally processed data whenever redistribution rights allow it.
- If upstream data cannot legally or clearly be redistributed, store provenance and a verified retrieval procedure rather than silently copying it.
- Do not invent native CAD, measured facility performance, or experimental data.

## Literature and external evidence

Prefer primary literature, standards bodies, calibration institutes, and original datasets. For recent or changing topics, verify the current source and publication date. Record DOI or stable source identifiers where available.

When a result is sourced from a paper, distinguish what the authors actually measured from what this project infers from it.

## Pull requests

- Never commit directly to `main` for automated research work.
- Use a fresh branch for a bounded increment.
- Open a human-review PR; never enable auto-merge.
- PR bodies should include provenance, technical delta, assumptions, equations/checks, uncertainty/sensitivity, statistical independence, null explanations, corrections, unresolved risks, and the next best increment.
- If an open PR already contains a directly dependent unmerged stack, avoid duplicate/conflicting PRs; document any justified branch/PR reuse.

## Current strategic boundary

Near-term work focuses on reproducible energy/materials/process-control experiments and metrology. A longer-term open-quantum or information-processing interpretation is optional upside and must be earned by mechanism-discriminating evidence.

A useful result can be a null result, a conventional explanation, a tighter uncertainty bound, a failed model, a safer design, or a better falsifier.
