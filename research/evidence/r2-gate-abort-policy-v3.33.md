# Evidence record — R2 gate abort/salvage policy v3.33

Date: 2026-08-27

## Classification

- Established repository evidence: merged v3.27 declares the R2 capability set, execution order, gate dependencies, PASS/FAIL/INCOMPLETE semantics, raw/processed separation, and statistical hierarchy.
- Engineering assumption/policy: only gates whose declared prerequisites are PASS may execute; failure blocks dependents but not unrelated branches.
- Falsifiable hypothesis: applying this policy to a real facility handoff will prevent downstream mechanism-facing acquisition from proceeding across unresolved prerequisite failures while still preserving useful independent calibration/metrology evidence.
- Synthetic/model result: none.
- Experimental result: none.
- Novel invention concept: none.

## Provenance

Primary internal source: `technical/data/r2_facility_capability_contract_v3_27.json` on current `main`, read 2026-08-27. Governance sources read before acting: `README.md`, `OPEN_SCIENCE.md`, `CONTRIBUTING.md`, `research/CALCULATION_VERIFICATION.md`, `research/session-history.md`, `research/evidence-map.md`, `technical/current-specification.md`, `venture/business-plan.md`, `automation/hourly-loop.md`.

Open automation PRs read before acting: #24 (facility time budget) and #7 (older overlapping calibration estimator). This increment does not duplicate either. It introduces no external factual claim requiring a new web citation.

## Verification

`models/r2_gate_abort_policy_v3_33.py` checks exact dependency agreement against v3.27, DAG acyclicity, exhaustive local prerequisite status combinations, explicit adversarial independent-branch cases, and preserved claim boundaries. Standard-library Python only; no stochastic method.

## Useful negative result

A failure in one qualification branch should not be treated as a reason either to (a) continue all downstream work regardless, or (b) discard every other independent evidence branch. The policy formalizes the narrower response: block only dependency descendants, keep independent branches available when their own prerequisites pass, and preserve failed/incomplete results publicly.

## Unresolved evidence gap

No real facility run has yet exercised the stop/continue/salvage policy. Real operations may reveal additional dependencies (for example shared mounting, thermal history, or source configuration) that must be versioned explicitly rather than inferred ad hoc.
