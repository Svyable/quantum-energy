# 2026-08-27 — v3.43 open-licensing release gate

## Increment

Converted the repository's acknowledged licensing gap into a machine-readable, CI-checked release-governance contract. This does not apply licenses yet; it defines the human-review decision surface and prevents automation from silently treating a public repository as formally licensed.

## Inputs read

Current main-branch `README.md`, `OPEN_SCIENCE.md`, `CONTRIBUTING.md`, `research/CALCULATION_VERIFICATION.md`, `research/session-history.md`, `research/evidence-map.md`, `technical/current-specification.md`, `venture/business-plan.md`, `automation/hourly-loop.md`, plus open automation PR #33.

PR #33 concerns agent/public discoverability and explicitly leaves software/data/hardware licensing unresolved, so v3.43 is non-overlapping.

## External sources checked

- Creative Commons official 4.0/application guidance, checked 2026-08-27.
- CERN OHL v2 variants at the Open Hardware Repository, checked 2026-08-27.
- SPDX license-list reference, checked 2026-08-27.

## Verification

The primary validator requires exactly the four proposed artifact classes and exact recommended identifiers. It also requires `effective_date=null` and all six release-gate Booleans to remain false.

The CI workflow independently reparses the manifest instead of importing the validator and checks the same class mapping plus `all(gates.values()) is False`.

No stochastic methods, meshes, fits, measured quantities, or experimental samples are involved. Software checks use exact equality.

## Claim discipline

- Established evidence: official license families/identifiers and current repository license-gap statements.
- Engineering assumptions/recommendations: the proposed four-way license split.
- Experimental results: none.
- Synthetic/model results: none.
- Patent/FTO/legal conclusions: none.

## Conventional/null explanation

Public download/fork capability can be mistaken for a reuse grant. The discriminator is explicit license application plus provenance/rightsholder review.

## Unresolved risks

Third-party rights, mixed-artifact files, contributor/inbound rights, data/database rights, patent/FTO, trademarks, privacy, export control, and exact attribution/noticing remain unresolved. Human/legal review may change any recommendation.

## Next increment

Create a path-level third-party and inbound-rights inventory, then—only after human approval—commit the approved canonical license texts and notices in a separate PR and change release-gate state explicitly.
