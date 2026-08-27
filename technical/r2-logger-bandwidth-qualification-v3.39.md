# R2 v3.39 — dummy-package logger bandwidth qualification

## Status and claim class

**Engineering protocol / synthetic planning model. Not an experimental result.**

This increment converts the open v3.38 question “is a 900 s transfer-log gap defensible?” into a falsifiable dummy-package qualification. It does **not** claim that any logger, package, carrier, device, or shipping route has passed.

## Why this matters

A complete time series can still be scientifically misleading if the logger/package is too slow to resolve the environmental transient of interest. Temperature/RH sensor lag can smooth excursions; an accelerometer can attenuate short impulses. Either can preserve a false appearance of benign transport conditions. The protocol therefore separates **record completeness** from **temporal fidelity**.

## Temperature and RH model

For a controlled step with initial equilibrium `y0` and final equilibrium `y_inf`, use the first-order engineering model

`y(t) = y_inf + (y0-y_inf) exp[-(t-t0)/tau]`.

Symbols:

- `y(t)`: logger temperature [degC] or RH [%RH];
- `y0`, `y_inf`: initial/final equilibrium values in the same channel units;
- `t`, `t0`: time and commanded step time [s];
- `tau`: fitted first-order response time [s].

Dimensional check: the exponential argument `(t-t0)/tau` is dimensionless.

### Primary calculation

Normalize `r=(y-y_inf)/(y0-y_inf)`, so

`ln r = -(t-t0)/tau`.

The executable estimator fits the negative slope through the origin after endpoint normalization. Non-decaying or nonphysical normalized responses fail rather than being coerced.

### Independent calculation

For two valid points on the same exponential,

`tau_ij = -(t_j-t_i) / ln(|(y_j-y_inf)/(y_i-y_inf)|)`.

The median pairwise `tau_ij` is an independent algebraic cross-check. Synthetic exact first-order data with `tau=120 s` must return 120 s by both paths within `1e-10 s`.

### Sampling-density assumption

The provisional engineering rule is **at least 5 samples per fastest qualified time constant**, giving

`gap_max = tau_min / 5`.

The factor 5 is a **synthetic engineering assumption**, not a safety standard or measured device requirement. Its role is to replace an arbitrary fixed 900 s gap with a configuration-specific value once `tau_min` is measured. With synthetic `tau=120 s`, the derived gap is 24 s. Sensitivity is linear: synthetic `tau={60,120,300} s` gives `{12,24,60} s`; the smallest qualified `tau` governs.

At least 3 independent step runs per direction are required. Samples within one step are correlated technical observations and do not increase independent run count. Dummy placement, package geometry, carrier, logger, and reference instrument are frozen in provenance.

## Acceleration pulse screen

A slow sampled accelerometer can miss shocks even when timestamps are dense. For controlled reference pulses, compute

`R_peak = max(|a_logger|)/max(|a_reference|)`.

For decision making with supplied 1-sigma-style amplitude uncertainties, use the conservative engineering ratio

`R_lower = max(0, (A_logger-u_logger)/(A_ref+u_ref))`.

Required pulse-width groups are synthetic planning values of 10, 100, and 1000 ms, with at least 3 independent pulses per width. The provisional gate is `R_lower >= 0.90` for every group. Failure means acceleration evidence is bandwidth-incomplete at or below the failed width; it does not imply device damage.

Synthetic limiting checks: identical zero-uncertainty peaks give ratio 1.0; `0.95±0.03 g` versus `1.00±0.02 g` gives `0.92/1.02 = 0.90196078...` and passes the synthetic 0.90 screen, while `0.94±0.03 g` versus the same reference gives `0.91/1.02 = 0.89215686...` and fails.

## Uncertainty and systematics

Report fitted `tau` uncertainty from independent-run variation or a justified bootstrap. Keep common reference timing/calibration, sensor placement, package-to-dummy gradients, chamber slew, and logger quantization as separate systematic terms. Shared calibration or timebase terms must not be counted as independent repeats.

A first-order fit is a model, not a law. Multi-time-constant behavior, hysteresis, condensation, spatial gradients, nonlinear RH response, acceleration resonance, orientation dependence, clipping, and reference-instrument bandwidth are conventional counterexamples. The discriminator is residual structure plus repeated steps/pulses across direction and placement. If the first-order model is inadequate, classification is `FAIL_BANDWIDTH` or `INCOMPLETE`; do not hide inadequacy by reporting only a fitted tau.

## Frozen outcomes

- `QUALIFIED_FOR_DECLARED_BANDWIDTH`: provenance, independent-run counts, fit diagnostics, uncertainty and all pulse-width screens pass.
- `INCOMPLETE`: required evidence or independence is missing.
- `FAIL_BANDWIDTH`: temporal model/response is inadequate or a required conservative pulse screen fails.

Passing establishes only temporal-fidelity evidence for the tested dummy/package/logger configuration and perturbation range. It does not establish shipping safety, device stability, facility equivalence, electrical stability, or an open-quantum mechanism.

## Practical execution

Use dimensionally representative dummy substrates in the same carrier/package geometry intended for R2. Log the candidate logger and a calibrated faster reference simultaneously. Execute both upward and downward temperature/RH steps without exposing actual R2 primaries. For mechanical qualification, use documented controlled pulses whose reference bandwidth exceeds the tested pulse content. Preserve every run, including failures and deviations, in the raw CSV schema.
