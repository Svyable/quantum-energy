# Evidence note — R2 facility confirmation protocol v3.29

Date: 2026-08-27

## Evidence class

This increment adds an **engineering contract / reproducibility artifact**. It does not add physical experimental evidence.

## Repository provenance

Derived from the merged main-branch `technical/data/r2_facility_capability_contract_v3_27.json`, which freezes seven required capability classes, evidence roles, configuration identifiers, execution dependencies, integrity rules, and statistical hierarchy.

Open PRs #19 and #20 were read before implementation. They prospectively audit public evidence for candidate facilities and explicitly leave unresolved custom-protocol capabilities as confirmation items. v3.29 does not rescore those candidates and does not copy their provisional facility-status conclusions into canonical mainline evidence.

## What is established by this artifact

- There is now one identical, machine-readable set of direct-confirmation questions corresponding to every v3.27 capability class.
- The response template begins every answer as `UNKNOWN`.
- Required `NO`, `UNKNOWN`, and `CONDITIONAL` responses cannot be averaged into an execution-ready label.
- A validator checks exact inheritance from the canonical v3.27 contract.

## What is not established

- No facility has answered the questionnaire.
- No partnership, schedule, quote, capability, calibration, device result, or measurement performance is claimed.
- No EPC or open-quantum mechanism is supported by this increment.

## Quantitative verification

Finite-set requirement:

`N_rows = 8 global + 2 * 7 capability = 22` response rows.

Inputs are integer counts with no units. Exact equality is required; tolerance is zero rows.

Independent check: the validator separately constructs the identifier sets `G01..G08` and `C01A..C07B` and requires the CSV template to contain each exactly once.

No stochastic method is used.

## Conventional explanation / discriminator

Publicly documented equipment does not necessarily imply support for the exact R2 protocol; unpublished custom capability can also exist. Direct written response plus a dry-run evidence packet is the discriminator.

## Negative-result preservation

A `NO` response is a useful facility-fit result and must remain visible. Missing answers remain `UNKNOWN`; they are not silently discarded or converted to a favorable status.
