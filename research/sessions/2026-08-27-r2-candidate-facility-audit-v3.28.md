# Session — R2 candidate-facility audit v3.28

Date: 2026-08-27

## Increment

Prospectively audited three real candidate facilities against the merged v3.27 machine-readable R2 facility capability contract using dated primary public facility evidence. The audit intentionally preserves unknowns instead of inferring custom capability from general laboratory reputation.

## Result

No candidate is execution-ready from public evidence alone. NREL PVDPC has 3 publicly supported, 1 partial, and 3 needs-confirmation capability rows; Fraunhofer ISE CalLab PV Cells has 2/1/4; IPVF has 1/2/4. Counts are descriptive, unweighted, and not a facility ranking.

The principal useful negative result is that accredited calibration, spectral-response instrumentation, or advanced PV characterization does not by itself establish the frozen temporal-fidelity, prospective-holdout, custom intensity-step, randomized-order, raw-export, and provenance requirements.

## Verification

`tools/validate_r2_candidate_facility_audit_v3_28.py` checks 21 unique facility-capability rows, exact coverage of all seven v3.27 capability classes for each candidate, frozen status vocabulary, dated HTTPS evidence, nonempty unresolved questions, expected count totals, and preservation of at least one `NEEDS_CONFIRMATION` item for every candidate.

Independent arithmetic: 7 capabilities × 3 facilities = 21 rows; each facility's category counts sum independently to 7. No stochastic model or physical decision-driving magnitude is introduced.

## Claim boundary

This session creates an engineering evidence audit only. It does not claim that any facility will accept the work, that its public pages are complete, that any candidate lacks an undocumented capability, or that any R2 physical/mechanism result has been obtained.

## Conventional explanation / discriminator

A prestigious or accredited lab can still be unsuitable for this exact experiment because the custom temporal/randomization/holdout workflow may not be operationally supported. The discriminator is configuration-specific written confirmation plus a dry-run evidence packet, not reputation.

## Next increment

Send the frozen direct-confirmation questions to candidate facilities (or otherwise obtain dated written responses), then update only evidence states supported by those responses. If no single facility can execute the complete chain, design a minimal multi-facility bridge study before pooling uncertainty components.
