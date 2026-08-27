# Research session — R2 facility candidate audit v3.28

Date: 2026-08-27

## Increment

Applied the merged v3.27 machine-readable R2 facility contract prospectively to three real candidate organizations using dated public evidence only. The goal was to turn a generic partner-search recommendation into a reproducible, source-linked capability matrix while preserving uncertainty rather than guessing missing services.

## Inputs

Canonical requirements: `technical/data/r2_facility_capability_contract_v3_27.json`.

Candidate evidence was collected from official NLR/nrel.gov, IPVF, and Fraunhofer ISE pages listed in `research/evidence/r2-facility-candidate-audit-v3.28.md` and row-by-row in the CSV matrix.

## Result classification

Engineering decision support / public-evidence audit. No measurement or partnership result.

## Quantitative result

Seven frozen capability classes were scored categorically.

- NLR_PVDPC: 2 `KNOWN_AVAILABLE`, 5 `NEEDS_CONFIRMATION`.
- IPVF: 1 `KNOWN_AVAILABLE`, 6 `NEEDS_CONFIRMATION`.
- FRAUNHOFER_ISE_CALLAB: 2 `KNOWN_AVAILABLE`, 5 `NEEDS_CONFIRMATION`.
- Union of publicly confirmed capabilities across all three: 2/7.

The fractions are evidence-completeness counts, not probabilities or quality rankings.

## Independent verification

`tools/score_r2_facility_candidates_v3_28.py` imports the v3.27 capability IDs, validates the 21-row matrix, recomputes the frozen JSON summary, and enforces adversarial semantics. A separate manual count of CSV statuses gives the same integer totals exactly.

## Uncertainty / sensitivity

Uncertainty is epistemic and represented as `NEEDS_CONFIRMATION`. No Gaussian uncertainty model is justified. Resolving any one currently unknown capability optimistically cannot make any candidate complete; direct confirmation remains required.

## Null explanation

Public webpages can omit custom services, while listed instruments may not support the exact requested protocol. Direct written confirmation and a small preflight packet are the discriminator.

## Negative result

No candidate should be selected as a complete R2 partner from public evidence alone. Five decision-critical capability classes remain unconfirmed everywhere in the audited set.

## Statistical integrity

No physical samples were analyzed. Facilities are not experimental replicates, and multiple webpages from one organization do not create statistical sample size.

## Corrections

No prior merged numerical result was corrected. v3.28 narrows partner-search language: public relevance is insufficient for execution qualification.

## Next increment

Generate a frozen, identical capability-confirmation questionnaire directly from the v3.27 contract, including configuration limits, evidence uploads, uncertainty/provenance requirements, scheduling constraints, and explicit yes/no/conditional responses. Returned evidence—not reputation—should control the partner decision.
