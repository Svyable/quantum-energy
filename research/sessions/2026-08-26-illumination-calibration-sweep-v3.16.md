# Session record — v3.16 illumination calibration + sweep-history qualification

Date: 2026-08-26

## Increment

Converted the v3.15 `Voc`-intensity power design into an executable measurement-path qualification covering reference-detector calibration, intensity-axis nonlinearity, correlated uncertainty, DUT temperature, ascending/descending history, and pre/post anchor drift.

## Files added

- `models/r2_illumination_qualification_v3_16.py`
- `models/r2_illumination_qualification_v3_16.csv`
- `technical/r2-illumination-calibration-sweep-qualification-v3.16.md`
- `technical/data/r2_voc_intensity_qualification_template_v3_16.csv`
- `research/evidence/r2-illumination-qualification-v3.16.md`
- `research/sessions/2026-08-26-illumination-calibration-sweep-v3.16.md`
- `venture/v3.16-illumination-qualification-decision.md`
- `.github/workflows/r2-illumination-qualification.yml`

## External evidence added

- IEC 60904-9:2020: solar-simulator classification is based on spectral distribution match, irradiance non-uniformity, and temporal instability.
- NIST detector calibration guidance: spectral responsivity/spatial uniformity matter and detector/electronics nonlinearity limits usable power range.
- NREL PV calibration practice: calibrated reference devices and spectral-mismatch correction are required when simulator/reference/test-device spectral responses differ.

Exact URLs and access date are in the evidence record.

## Decision-driving calculation

The frozen v3.15 estimator was stressed against three intensity-axis errors using a noiseless synthetic quadratic `Voc(ln Phi)` whose local-ideality contrast is exactly 0.10.

1. Common +2% multiplicative intensity offset: exact zero curvature bias to numerical precision.
2. +0.5% log-axis gain: numerical contrast `0.09950248756`; independent analytic result `0.10/1.005` agrees within `1e-10`.
3. Smooth quadratic 0.5% log-axis residual: contrast `0.09356282035`, bias `-0.00643717965` under the frozen adversarial shape.

Dimensional check: `ln(Phi)` is dimensionless; `dVoc/dln(Phi)` and `kBT/q` are volts; `n_id` and `Delta_n_curv` are dimensionless.

Independent temperature-normalization calculation: with device physics frozen, a +0.5 K analysis-temperature error at 300 K changes inferred `n_id` by `300/300.5 - 1 = -0.00166389351`; a synthetic 0.10 curvature shifts by `-0.00016638935`.

## Sensitivity / uncertainty interpretation

A common absolute intensity scale is much less important to the derivative observable than intensity-dependent calibration curvature. Therefore the new raw schema preserves separate correlation classes: common scale, sweep/session drift, smooth nonlinearity, and point residual.

Engineering qualification gates are deliberately provisional: <=0.5% calibration residual, <=0.01 propagated calibration curvature bias, <=0.2% reference-anchor drift, <=0.5 mV DUT anchor drift, <=0.03 ascending/descending curvature difference, <=0.5 K DUT excursion, and <=0.5 mV point-level `Voc` SD. None are represented as measured facility performance or standards requirements.

## Statistical independence

Anchor repeats and repeated readings are technical repeats. They do not increase lot/substrate/device sample size. Sweep direction is blocked across independent substrates to avoid confounding acquisition order with fabrication unit.

## Conventional/null explanations

Calibration nonlinearity, source spectral changes, DUT heating, sweep history, contacts, transport resistance, energetic disorder, state filling, and carrier-density-dependent recombination remain viable explanations for curvature. Passing v3.16 only qualifies the measurement path.

## Corrections

No prior arithmetic was corrected in this session. v3.15 is narrowed operationally: its high nominal synthetic power is not usable for confirmatory interpretation until the illumination axis and sweep-history path pass v3.16.

## Unresolved risks

- real source spectral distribution may vary with intensity-setting method;
- a scalar photodiode may not track PM6:Y6-effective irradiance if spectra change;
- facility reference-detector uncertainty/covariance is not yet measured;
- R2 hysteresis may depend on dwell time and prior illumination;
- DUT-adjacent temperature may lag optical/electrical equilibration;
- the 0.5%/0.2%/0.03 gates are planning choices and need empirical retirement.

## Single best next increment

Build a **facility-ready calibration-analysis CLI** that ingests the new raw schema, estimates the log-intensity calibration model and covariance, computes spectral-mismatch flags, quantifies ascending/descending and anchor drift, and emits a signed PASS/FAIL qualification certificate plus the measured covariance inputs required by the frozen v3.15 power model. Run it first on a fully synthetic fault-injection package, then unchanged on the first real facility export.
