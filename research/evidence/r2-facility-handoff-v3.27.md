# Evidence record — R2 facility handoff v3.27

Date: 2026-08-27

## Classification

**Engineering contract / integration specification.** No new experimental result is introduced.

## Established internal evidence

The repository's open R2 work already separates multiple conventional metrology risks into dedicated gates: empirical calibration covariance, prospective calibration holdout, external/reference systematic uncertainty, facility-packet integrity, spectral mismatch, acquisition-order drift, optical/DUT settling, and electrical-chain temporal fidelity.

The current main-branch open-science and verification rules require explicit claim classes, uncertainty, prospective validation where practical, preserved negative results, immutable/raw provenance, and experimental hierarchy.

## New engineering assumption

A single machine-readable facility capability/evidence contract will reduce integration ambiguity when external laboratories or autonomous research agents evaluate whether a facility can execute the R2 measurement stack.

Consequence if wrong: the contract may appear complete while still omitting a material facility-specific dependency. Any such omission should produce a visible contract revision rather than retroactive reinterpretation of the original version.

## Falsifiable operational hypothesis

A prospective candidate-facility audit can use the v3.27 contract to classify each required capability from dated evidence and identify missing/uncertain capabilities before experimental scheduling, without silently strengthening scientific claims.

## Quantitative/calculation audit

v3.27 adds no new decision-driving physical magnitude, estimated performance, vendor quote, or sample-size claim. The decision-driving object is a directed dependency graph and a finite set of required evidence roles.

Independent structural check: the committed standard-library validator verifies the graph is acyclic, verifies every dependency precedes its dependent gate in the frozen execution order, and verifies capability evidence roles resolve to declared packet roles.

Dimensional analysis: not applicable to the logical dependency graph. The only physical unit in the frozen configuration fields is `aperture_s`, explicitly seconds.

Uncertainty: capability availability itself is not represented numerically. Prospective facility scoring must preserve `NEEDS_CONFIRMATION` rather than assign a probability without evidence.

## Statistical independence

No sample-size credit is introduced. The existing hierarchy remains `lot -> substrate -> device/pixel -> session -> sweep or step replicate -> measurement` and is checked verbatim by the validator.

## Conventional/null explanation

A facility can satisfy every capability and still observe no R2 mechanism effect. Conversely, a missing facility capability can prevent inference even if the underlying device physics is interesting. The handoff contract is measurement-system infrastructure, not mechanism evidence.

## Negative-result policy

`FAIL` remains visible and `INCOMPLETE` cannot be converted to zero uncertainty or PASS. A failed prospective holdout cannot become tuning data and then be relabeled validation.

## Sources/provenance

No new external scientific claim was necessary for this increment. Provenance is the current canonical repository plus open automation PRs #6–#14, whose scopes were inspected before implementation. Issue #15 is the partner-handoff integration target.

## Reproduction

Run:

`python tools/validate_r2_facility_capability_v3_27.py`

Expected result:

`PASS: v3.27 facility capability contract is structurally consistent`

Python standard library only; no stochastic seed applies.
