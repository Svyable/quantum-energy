# Evidence record — R2 transfer environment v3.38

Date: 2026-08-27

## Evidence/source provenance

No new external physical-performance claim is introduced. The protocol is derived from the repository's merged R2 transfer-standard, randomized HOME/TRAVEL shipping-control, cross-facility A→B→A, and transfer-carrier requirements. `main` at session start was commit `9f7e35801a834fb436d49b3eaaa1d94d66abc3cd`.

The numerical 900 s maximum logging gap is a **synthetic planning assumption** for data completeness only. It has no vendor, standards, material-reliability, or experimental provenance and is not a safe-exposure threshold.

## New falsifiable statement

A cross-facility or shipping-state interpretation is better constrained when the transfer record has: (1) immutable package/carrier/substrate/logger provenance; (2) UTC-bracketed temperature/RH/acceleration observations; (3) declared measurement uncertainty; and (4) no unobserved gap larger than the frozen completeness rule. This is an engineering data-integrity proposition, not evidence that the R2 device is stable under any particular exposure.

## Conventional explanation retained

Transport can change the device through temperature, humidity, mechanical shock, remounting/contact changes, particles, light exposure, time-dependent ageing, or package interactions. This ledger directly observes only temperature, RH and sampled acceleration; the other explanations remain live.

## Negative-result rule

An incomplete log is a useful negative result: it prevents later analysts from claiming that shipping exposure was controlled when it was not. An exposure beyond a subsequently documented material/package limit is also preserved and should trigger diagnosis rather than exclusion of the affected substrate after outcomes are known.

## Claim boundary

`LOG_COMPLETE` is not “shipping qualified.” `WITHIN_DECLARED_LIMITS` is only as defensible as the provenance and applicability of those declared limits. Neither status supports a quantum-mechanism claim, device-stability claim, vendor-capability claim, or facility-equivalence claim.
