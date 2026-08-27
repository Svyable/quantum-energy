# Session — R2 cross-facility transfer v3.34

Date: 2026-08-27

## Increment

Added a prospective A→B→A cross-facility transfer screen for the R2 weak-EL transfer standard. The design addresses the specific confound that a one-way transfer cannot separate facility bias from elapsed-time/shipping/device drift.

## Quantitative inputs

- Measurand: `DeltaVnr`, mV; inherited R2 observable.
- Minimum complete qualified primary devices: 3; engineering minimum aligned to the existing R2 primary-device concept, not a confirmatory sample-size theorem.
- Mean-bias engineering screen: 5.0 mV; assumed/project-derived, dated 2026-08-27.
- RMS-residual engineering screen: 5.0 mV; assumed/project-derived, dated 2026-08-27.
- Software: Python standard library only; no stochastic seed, mesh, optimizer, or external package applies.
- Numerical tolerance in deterministic self-test: `1e-12` for algebraic/limiting-case equality.

## Governing model

For `t_A1 < t_B < t_A2`, define

`w=(t_B-t_A1)/(t_A2-t_A1)`,

`A_interp=(1-w)A1+w*A2`,

`r=B-A_interp`,

`bias=mean(r)`,

`RMS=sqrt(mean(r^2))`.

`w` is dimensionless. A1/B/A2/r/bias/RMS are mV. The estimator is valid only as a linear-in-time bracketing correction between A1 and A2; nonlinear drift is an unresolved model risk.

## Verification

The executable independently checks the midpoint identity `B-(A1+A2)/2`, the exact linear-drift limiting case, PASS at 3 mV residual, FAIL at 7 mV, exact 5 mV boundary behavior, INCOMPLETE with fewer than three complete devices, and FAIL for invalid time ordering.

## Uncertainty and sensitivity

No publication-grade interval is claimed. Device-level measurement uncertainty remains upstream and correlated systematic terms remain correlated. Sensitivity is discontinuous at the frozen engineering boundary by design: 5.000000 mV common residual passes; 5.000001 mV fails.

## Statistical independence

A1/B/A2 are correlated repeats on the same device. Independent device count is not multiplied by transfer legs. Hierarchy: `lot -> substrate -> device/pixel -> facility -> session -> measurement`.

## Conventional explanation / discriminator

Conventional causes include calibration offset, source spectrum, remounting/contact geometry, instrument response, temperature, shipping, degradation, and nonlinear ageing. The A-return leg discriminates a linear home-facility time trend; it does not remove nonlinear or transfer-induced state changes.

## Corrections

No prior merged result was corrected. No hidden failed calculation was encountered in this increment.

## Next increment

Execute the frozen A→B→A packet on qualified R2 primaries only after both facilities pass the prerequisite metrology/configuration gates. Preserve every device and deviation; if transfer fails, diagnose calibration versus shipping/history before any mechanism-facing multi-facility claim.
