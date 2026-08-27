# R2 Facility Qualification CLI v3.17

## Scope and claim boundary

This increment converts the v3.16 illumination-calibration, DUT-heating, and sweep-history preregistration into an executable facility-export gate. A `PASS` qualifies the **measurement path** for the frozen v3.15 `Voc`-intensity curvature analysis. It does **not** identify H3, EPC, or open-quantum transport.

## Input contract

The CSV preserves `lot -> substrate -> pixel -> session -> sweep -> intensity -> raw reading` hierarchy and extends v3.16 with:

- `source_spectrum_id`
- `spectral_mismatch_factor`
- `spectral_mismatch_u_rel`

Missing required calibration/spectrum/temperature/precision data produce `INCOMPLETE`, never an implicit pass.

## Frozen gates

Inherited from v3.16:

- log-intensity calibration residual <= 0.5%
- propagated calibration-induced `|Delta_n_curv|` bias <= 0.01
- reference-signal anchor drift <= 0.2%
- DUT `Voc` anchor drift <= 0.5 mV
- median ascending/descending pointwise `Voc` difference <= 0.5 mV
- ascending/descending curvature difference <= 0.03
- per-sweep DUT temperature SD <= 0.25 K
- maximum DUT temperature excursion from 300 K <= 0.5 K
- point-level `Voc` SD/uncertainty <= 0.5 mV

New v3.17 spectral-risk engineering gates, to be retired or revised with real facility evidence:

- `|spectral_mismatch_factor - 1| <= 0.01`
- relative spectral-mismatch uncertainty <= 0.005
- one stable `source_spectrum_id` across a qualified sweep pair

These are project planning assumptions, not standards-derived limits.

## Calibration model

For each unique target intensity, repeated calibrated intensities are averaged. The CLI fits

`ln(Phi_cal) = a + b ln(Phi_target) + epsilon`.

A common multiplicative scale is absorbed by `a`. `b-1` is reported as log-axis gain/stretch information. The maximum `|exp(epsilon)-1|` is compared with the frozen 0.5% shape-residual gate.

The propagated curvature bias is computed by applying the measured calibrated intensity axis to the frozen synthetic v3.16/v3.15 stress curve with true `Delta_n_curv = 0.10`, then subtracting the same curve analyzed on the target axis.

`n_id = [dVoc/dln(Phi)]/(k_B T/q)` is dimensionless because both numerator and denominator are volts.

## Independent cross-check

For the limiting calibration form

`x_m = (1+a)x`, where `x=ln(Phi)`,

the local ideality and curvature scale analytically as

`Delta_n_measured = Delta_n_true/(1+a)`.

At `a=0.005` and `Delta_n_true=0.10`, the analytic bias is

`0.10/1.005 - 0.10 = -0.00049751243781`.

The independent executable calibration-bias path must agree within `1e-10`.

## Synthetic clean fixture

The committed clean fixture is explicitly synthetic. It contains 17 ascending + 17 descending points, a paired pre/post anchor, 0.3 mV point uncertainty, small temperature variation, 0.1% reference-anchor drift, 0.2 mV `Voc` anchor drift, one stable source-spectrum ID, and a small smooth calibration-axis distortion.

Frozen clean-certificate outputs include:

- calibration residual: `0.00062519535` relative
- propagated curvature bias: `-0.00128767666`
- point `Voc` SD input: `0.0003 V`
- reference-anchor drift: `0.00100100100`
- `Voc` anchor drift: `0.0002 V`
- ascending/descending median `Voc` difference: `0.0001 V`
- curvature-direction difference: approximately `1.3e-15`
- maximum temperature excursion: `0.0499995 K`
- maximum per-sweep temperature SD: `0.0360749 K`
- spectral mismatch factor deviation: `0.002`

These are software-test values, not measured facility performance.

## Adversarial synthetic faults

The test suite independently injects and requires detection of:

1. point `Voc` uncertainty = 1 mV;
2. DUT temperature = 301 K;
3. ~1% reference-anchor drift;
4. 2 mV `Voc` anchor drift;
5. 2 mV descending-sweep offset;
6. spectral-mismatch factor = 1.03;
7. smooth intensity-axis curvature large enough to violate the calibration residual gate;
8. absent source-spectrum metadata, which must return `INCOMPLETE`.

## Uncertainty and covariance

The certificate carries the maximum per-point `Voc` uncertainty, absolute propagated calibration-curvature bias, and calibration uncertainty grouped by the input `calibration_correlation_group`. Correlated calibration terms are not converted into pseudo-independent repeats.

## Validity limits

The CLI assumes the local 7-point v3.15 estimator, a 300 K normalization for the qualification calculation, paired ascending/descending sweeps, and a scalar spectral-mismatch factor supplied by the facility. It does not validate the facility's underlying spectral-mismatch derivation, detector linearity certificate, spectral irradiance measurement, or device physics.

## Release rule

- `PASS`: all required gates are evaluated and pass; v3.15 curvature analysis may proceed at the measurement-path level.
- `INCOMPLETE`: at least one required gate cannot be evaluated and none fail; do not call the measurement path qualified.
- `FAIL`: at least one gate fails; redesign/recalibrate/reacquire before confirmatory interpretation.
