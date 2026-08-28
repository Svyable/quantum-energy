# Evidence record — v3.44 AT-04 uncertainty budget

## Established/project-canonical inputs

- AT-04 currently carries an internal planning target of `<=10 mV` equivalent `DeltaV_nr` uncertainty in `technical/current-specification.md`.
- The project uses `DeltaV_nr = -(k_B T/q) ln(EQE_EL)` for direct EQE_EL-derived nonradiative voltage-loss analysis.
- `k_B/q = 8.617333262e-5 V/K` is derived from exact SI constants.

## Synthetic/model results — not experimental evidence

The v3.44 fixture uses `T=300 K`, `u(T)=1 K`, `EQE_EL=1e-6`, 10% relative EQE uncertainty, and 4/3/2 mV equivalent radiometric/repeatability/background terms. These numbers are synthetic planning assumptions chosen only to exercise the budget machinery.

It produces `DeltaV_nr=357.1585759879732 mV` and a zero-correlation combined standard uncertainty of `6.091027601721118 mV`. Correlating the synthetic 4 mV radiometric and 2 mV background terms at `rho=-0.5,0,+0.5` yields `5.3944987945988565`, `6.091027601721118`, and `6.71569931168218 mV` respectively.

## Claim boundary

None of the values above demonstrates AT-04 or R2 measurement performance. The only supported engineering conclusion is that the repository now has an executable calculation path capable of representing component uncertainty and simple covariance sensitivity.

A future experimental PASS requires measured/provenance-backed components, correlation review, no-double-counting review, an appropriate propagation model, and the combined budget meeting the internal target.

## Conventional explanations preserved

Calibration-scale drift, background subtraction, DUT-temperature error, injection mismatch, shared calibration covariance, session drift, and weak-signal non-Gaussianity remain ordinary explanations for apparent voltage-loss differences. These must be bounded before a mechanism-facing result can be promoted.
