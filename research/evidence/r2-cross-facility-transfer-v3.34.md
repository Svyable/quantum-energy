# Evidence record — R2 cross-facility transfer v3.34

Date: 2026-08-27

## Established repository evidence

- R2 is a metrology transfer standard, not a commercial product or mechanism proof.
- The current specification uses a ~5 mV scale for fabrication/reference and between-session drift screening.
- Existing merged facility/metrology protocols require frozen configuration, raw-data provenance, and explicit PASS/FAIL/INCOMPLETE handling.

## New engineering assumption

A first cross-facility screen uses `|mean facility residual| <= 5 mV` and `RMS facility residual <= 5 mV` on at least three complete qualified primary devices. This is a project screening threshold, not a standards-derived equivalence margin or calibrated confidence procedure.

## Falsifiable hypothesis

For qualified R2 primary devices measured in the frozen A→B→A sequence, the second-facility residual after interpolation of the home-facility A1/A2 measurements remains inside the 5 mV bias and RMS screens.

## Synthetic/software verification only

The committed self-test uses deterministic constructed values to verify algebra, time ordering, gate boundaries, and status behavior. No synthetic case is represented as experimental evidence.

## Experimental evidence

None added in v3.34.

## Conventional explanations retained

Calibration offset, remounting/contact geometry, spectrum mismatch, instrument response, temperature history, shipping shock, encapsulation degradation, and nonlinear ageing can all create apparent cross-facility disagreement. A1/B/A2 interpolation removes only a linear home-facility time trend.

## Kill/narrow gate

If the complete transfer packet fails either 5 mV screen, do not claim successful R2 facility transfer. If device drift is demonstrably nonlinear or transfer history changes device state, narrow the conclusion to `INCOMPLETE` for facility attribution and redesign the bracketing schedule.
