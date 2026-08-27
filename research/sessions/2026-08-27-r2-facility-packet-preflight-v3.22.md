# Session record — 2026-08-27 — R2 facility packet preflight v3.22

## Increment

Added an executable facility-handoff preflight gate before R2 measurement analysis.

## Why this increment

The open automation PRs already cover empirical repeatability covariance, prospective repeatability validation, and external/reference systematics. The missing non-overlapping failure mode was provenance/integrity at handoff: a scientifically sophisticated downstream analysis can still be invalid if the facility packet is incomplete, internally contradictory, or detached from the calibration/spectrum/linearity source bytes it claims to use.

## Technical result

The new validator requires nine evidence roles, SHA-256 + byte-count integrity for every manifested object, safe relative paths, consistent detector/source/configuration identities, core raw-CSV columns, and metadata-to-source hash binding.

Status semantics are frozen:
- missing required evidence -> `INCOMPLETE`;
- malformed/contradictory/tampered evidence -> `FAIL`;
- complete internally consistent packet -> `PASS`.

A `PASS` is explicitly not measurement qualification.

## Verification

Local Python standard-library tests passed for:
- complete synthetic packet;
- byte tamper;
- missing required source file;
- contradictory detector identity after rehashing;
- path traversal;
- source replacement after top-level manifest rehashing while metadata still binds the prior source.

No stochastic calculation is used; no random seed applies.

## Statistical independence

The preflight performs no inference and gives no sample-size credit. Lot/substrate/pixel/session/sweep/intensity hierarchy is untouched.

## Negative result preserved

A top-level file manifest alone is insufficient to protect provenance against a coordinated source-file replacement followed by manifest rehashing. v3.22 therefore also binds certificate, spectrum, and detector-linearity metadata to the corresponding source/data digest.

## Unresolved risks

- SHA-256 integrity does not authenticate an issuer or operator identity.
- The tool does not validate certificate scientific adequacy or calibration validity dates against acquisition dates.
- One detector/source/configuration population per packet is assumed.
- Real facility file naming/content may require adapters while preserving the semantic roles.
- Open covariance/systematics PRs still require human review and reconciliation.

## Next increment

Run v3.22 unchanged on the first real facility packet and preserve all missing evidence as `INCOMPLETE`; then add acquisition-date/certificate-validity and configuration-applicability checks using real metadata rather than synthetic assumptions.
