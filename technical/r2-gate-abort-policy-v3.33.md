# R2 Gate Abort and Evidence-Salvage Policy v3.33

## Purpose

This specification turns the merged v3.27 R2 facility dependency graph into an explicit stop/continue/salvage policy. It answers a practical question that the capability contract did not fully encode: **after a prerequisite FAIL or INCOMPLETE result, which downstream work must stop, which independent branch may continue, and which negative evidence remains useful?**

This is an engineering execution policy. It is not experimental evidence of R2 performance, EPC, open-quantum transport, or commercial PV performance.

## Source provenance

Canonical input: `technical/data/r2_facility_capability_contract_v3_27.json`, reviewed from `main` on 2026-08-27. The dependency-controlled gates and prerequisite sets are copied exactly and checked programmatically. The policy adds explicit graph nodes for `packet_preflight` and the already-declared `reference_repeatability_freeze` execution stage, plus `BLOCKED` semantics and evidence-salvage rules.

Open PR #24 was read before this increment. It models facility time and quote planning. v3.33 intentionally does not add timing, rates, vendor quotes, or expected failure probabilities. Open PR #7 is overlapping historical calibration work and is not used as a second analysis authority.

## Status semantics

- `PASS`: evidence is complete and the frozen gate criteria pass.
- `FAIL`: evidence is sufficient to test, but a frozen criterion is violated. Preserve the result.
- `INCOMPLETE`: material evidence or provenance is absent. Missing evidence may not be treated as zero uncertainty or PASS.
- `BLOCKED`: the gate must not execute because at least one declared prerequisite is not `PASS`.

Governing logical model for gate `g` with prerequisite set `D_g`:

`RUN(g) = AND[d in D_g] I(status_d = PASS)`.

`I(.)` is a dimensionless indicator. The expression is Boolean; no physical unit conversion applies. A prerequisite `FAIL` and a prerequisite `INCOMPLETE` both make `RUN(g)=false`, but their scientific meanings remain distinct.

## Dependency policy

Ten explicit stages are represented in `technical/data/r2_gate_abort_policy_v3_33.json`:

1. packet preflight;
2. instrument temporal fidelity;
3. optical/DUT settling;
4. spectral-shape gate;
5. reference-repeatability training;
6. reference-repeatability freeze;
7. prospective repeatability holdout;
8. monotonic Voc-intensity acquisition;
9. randomized-order Voc-intensity acquisition;
10. combined uncertainty propagation.

The v3.27 dependency-controlled prerequisite sets are unchanged. The v3.27 `execution_order` already contains `reference_repeatability_freeze`; v3.33 makes that stage an explicit graph node depending on training so the holdout dependency is fully closed rather than dangling.

Monotonic Voc-intensity acquisition is blocked unless instrument temporal fidelity, optical/DUT settling, and spectral-shape qualification all pass. A complete combined uncertainty result is blocked unless prospective repeatability holdout, spectral-shape qualification, and randomized-order acquisition all pass.

## Evidence salvage instead of all-or-nothing shutdown

A failed prerequisite blocks its dependents, **not every independent branch**. Examples:

- If optical/DUT settling fails after packet preflight and instrument fidelity pass, spectral characterization and reference-repeatability work may continue. Monotonic/randomized Voc-intensity work is blocked.
- If spectral-shape qualification fails, instrument temporal characterization and repeatability work may continue. Voc-intensity mechanism-facing acquisition is blocked.
- If the repeatability freeze cannot be accepted, the prospective holdout remains untouched and blocked rather than being consumed during model tuning.
- If prospective repeatability holdout fails, the untouched holdout remains a useful negative validation result. Complete combined uncertainty qualification is blocked rather than repaired post hoc by switching estimator branches.

Raw/minimally processed evidence collected before the stop remains publishable with its true status and provenance. Remediation/rerun is a new session/configuration record; it never erases the earlier failure.

## Independent verification

Executable validator: `models/r2_gate_abort_policy_v3_33.py`.

Checks:

1. exact equality between v3.27 dependency sets and v3.33 policy dependencies;
2. explicit closure of the v3.27 repeatability-freeze execution stage;
3. acyclic dependency graph/topological order;
4. exhaustive local truth tables for every dependency-controlled stage and every `PASS/FAIL/INCOMPLETE` combination;
5. adversarial branch-salvage cases for optical-settling and spectral-shape failures;
6. incomplete freeze blocks prospective holdout;
7. failed prospective holdout blocks complete uncertainty propagation;
8. every stage carries a nonempty salvage record;
9. explicit non-claim boundary is retained.

The exhaustive local enumeration contains exactly **81 prerequisite-status combinations**: the exact sum of `3^k` across the nine non-root stages, where `k` is each stage's prerequisite count. This is a discrete structural count, not a statistical sample size.

There are no stochastic inputs, package dependencies, mesh settings, or Monte Carlo seeds. Python standard library only. Equality checks are exact.

## Calculation / dimensional / limiting-case audit

The decision-driving quantitative claims are structural only: 10 explicit stages and 81 local prerequisite truth-table cases. They are exact discrete counts, not measurements and not uncertain physical quantities.

Known limiting cases:

- no dependencies -> root stage is runnable subject to its own evidence/QC;
- all dependencies PASS -> dependent stage is runnable;
- any one dependency FAIL -> dependent stage is blocked;
- any one dependency INCOMPLETE -> dependent stage is blocked;
- failure on an unrelated branch does not block a stage whose own dependencies still pass.

These cases are independently exercised by explicit adversarial assertions in the validator rather than inferred from the documentation prose.

## Uncertainty and sensitivity

No probability of gate failure is assigned because no real facility campaign supports one. Therefore v3.33 does **not** compute expected cost, expected time, or probability of success.

Sensitivity is logical rather than probabilistic: changing any prerequisite from PASS to FAIL/INCOMPLETE flips dependent execution from runnable to blocked; changing an unrelated branch status does not. This is the intended design property.

## Statistical independence

Gate outcomes are not experimental replicates. Measurements retain the hierarchy:

`lot -> substrate -> device/pixel -> session -> sweep or step replicate -> measurement`.

Continuing an independent evidence branch after another branch fails does not increase device-level sample size or mechanism evidence.

## Conventional/null explanation

A blocked R2 mechanism-facing acquisition can arise entirely from ordinary metrology failure: calibration provenance, electronics response, source/DUT settling, spectral mismatch, or repeatability transfer. Blocking later acquisition is therefore not evidence of exotic DUT dynamics.

The discriminator is remediation followed by the same frozen prerequisite test under a new, fully recorded configuration/session.

## Safety/environmental boundary

The policy is subordinate to facility EHS, optical/electrical interlocks, source duty limits, instrument ratings, thermal limits, and device-handling rules. A branch marked runnable by this graph may still be prohibited by safety or equipment constraints.

## Kill/narrow rule

If a prerequisite required for mechanism-facing Voc-intensity interpretation is FAIL or INCOMPLETE, do not collect/interpret the dependent result as if qualification succeeded. Preserve diagnostic data, repair the conventional measurement problem, and rerun prospectively under a new recorded session/configuration.
