# 2026-08-27 — R2 facility confirmation protocol v3.29

## Increment

Created a frozen direct-confirmation questionnaire and machine-readable response template for prospective R2 facility partners.

## Why this increment

Merged v3.27 defines the integrated facility capability contract. Open PRs #19/#20 perform candidate public-evidence audits and both preserve unresolved custom-protocol questions. The next non-duplicative step is therefore to freeze the direct-confirmation interface before any candidate response is seen.

## Claim discipline

- Established evidence: merged v3.27 capability/evidence contract exists on main.
- Engineering assumption: standardized direct confirmation reduces ambiguity and selection bias.
- Falsifiable hypothesis: at least one candidate or explicit multi-facility bridge can meet the unchanged contract.
- Synthetic/model result: none.
- Experimental result: none.
- Novel invention concept: none.

## Calculation audit

Decision-driving finite-set count:

`N = 8 + 2*7 = 22` required response rows.

Units: counts are dimensionless.

Independent path: construct exact expected ID sets (`G01..G08`, `C01A..C07B`) and require one-to-one equality with CSV rows rather than only checking the numeric length.

Tolerance: exact equality; no stochastic seed or numerical convergence is applicable.

## Uncertainty / sensitivity

Capability uncertainty is epistemic and represented by `UNKNOWN`/`CONDITIONAL`; no unsupported probability is assigned. One required `NO` can make a capability unavailable; one unresolved required item prevents confirmation. The decision is intentionally non-compensatory.

## Statistical independence

No experimental inference is performed. Facility responses do not increase device sample size. Downstream hierarchy remains lot -> substrate -> device/pixel -> session -> sweep or step replicate -> measurement.

## Null / conventional explanation

A facility can own relevant instruments without being able to satisfy exact timing, range, raw-export, prospective-holdout, provenance, or EHS requirements. Conversely, a capability omitted from a webpage may exist. Written confirmation plus a dry-run packet is the discriminator.

## Files added

- `technical/data/r2_facility_confirmation_questionnaire_v3_29.json`
- `technical/data/r2_facility_confirmation_response_template_v3_29.csv`
- `tools/validate_r2_facility_confirmation_v3_29.py`
- `technical/r2-facility-confirmation-protocol-v3.29.md`
- `research/evidence/r2-facility-confirmation-v3.29.md`
- `research/sessions/2026-08-27-r2-facility-confirmation-v3.29.md`
- `venture/v3.29-facility-confirmation-decision.md`
- `.github/workflows/r2-facility-confirmation.yml`

## Corrections

No prior scientific result is corrected. The facility-selection process is narrowed: public evidence is triage only; execution readiness requires direct confirmation and dry-run evidence.

## Single best next increment

Send the identical questionnaire unchanged to the audited candidates, commit dated responses, mechanically classify them, and require a dry-run v3.27 evidence packet before scheduling full acquisition.
