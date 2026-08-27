# Research session — R2 facility handoff v3.27

Date: 2026-08-27

## Session objective

Convert the fragmented open R2 metrology qualification stack into one machine-readable and human-readable facility execution contract so external labs and research agents can determine whether the full experiment is actually executable before scientific acquisition begins.

## Prior work checked

Read the canonical main-branch governance, verification, evidence, technical, venture, and automation files required by `automation/hourly-loop.md`. Also inspected the open automation PR set #6–#14 before acting.

Overlap audit:

- #6/#7: empirical calibration covariance;
- #8: prospective repeatability holdout;
- #9: external/reference systematics;
- #10: facility packet integrity;
- #11: wavelength-resolved spectral mismatch;
- #12: randomized acquisition-order drift;
- #13: optical/DUT settling;
- #14: electrical acquisition-chain temporal fidelity.

v3.27 does not replace any of those methods. It integrates their facility-facing prerequisites and gate ordering.

## Artifacts added

- `technical/data/r2_facility_capability_contract_v3_27.json`
- `technical/r2-facility-handoff-v3.27.md`
- `tools/validate_r2_facility_capability_v3_27.py`
- `research/evidence/r2-facility-handoff-v3.27.md`
- `research/sessions/2026-08-27-r2-facility-handoff-v3.27.md`
- `venture/v3.27-facility-partner-gate.md`
- `.github/workflows/r2-facility-capability-contract.yml`

## Main result

The complete facility requirement is now represented as a dependency graph rather than prose scattered across multiple open PRs. Required capability classes, evidence roles, frozen configuration identifiers, data-integrity requirements, status semantics, and statistical hierarchy are machine-readable.

## Verification

The standard-library validator independently checks structural invariants rather than trusting the JSON by inspection:

- required capability set exists;
- every capability's evidence role is declared in the packet role set;
- status semantics contain exactly PASS/FAIL/INCOMPLETE;
- FAIL preserves negative results;
- INCOMPLETE prohibits implicit zero uncertainty/PASS;
- statistical hierarchy is preserved verbatim;
- gate-dependency graph is acyclic;
- dependencies precede dependent gates in execution order;
- mandatory non-claims remain present;
- SHA-256/raw-vs-processed/exclusion-retention rules remain enabled.

No stochastic computation is introduced; no seed applies.

## Negative / null result retained

A facility matching the capability contract does not provide any evidence that R2 has unusual device physics. The contract can succeed operationally while the eventual experiment returns a null mechanism result.

## Corrections / superseded claims

No prior numerical result is corrected. Interpretation is tightened: the R2 metrology stack should not be called facility-ready merely because each individual method exists. Facility readiness now requires satisfying the integrated v3.27 evidence/dependency contract.

## Unresolved risks

- real facilities may expose undocumented configuration dependencies absent from v3.27;
- capability claims inferred from public websites can be stale or ambiguous and require direct confirmation;
- multi-facility execution can break configuration/provenance continuity unless explicitly bridged;
- open PRs #6–#14 still require human review and integration before any complete execution release;
- repository licensing remains unresolved for formal reuse terms.

## Single best next increment

Prospectively score at least three real candidate facilities against the v3.27 contract using dated public sources plus explicit `NEEDS_CONFIRMATION` fields. Do not rank facilities from marketing language alone; resolve every decision-critical unknown before selection or split the workflow with an explicit provenance bridge.
