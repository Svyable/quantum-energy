# R2 Illumination Calibration and Sweep-History Qualification v3.16

## Scope and claim boundary

This protocol qualifies the **measurement axis and sweep history** for the frozen v3.15 `Voc`-versus-light-intensity curvature experiment. Passing this protocol means the 0.05–2 sun illumination axis, DUT thermal state, and sweep-history behavior are sufficiently controlled for the preregistered local-ideality analysis. It does **not** establish H3, EPC, open-quantum transport, or any causal recombination mechanism.

## External evidence / standards context

- IEC 60904-9:2020 classifies PV solar simulators using spectral distribution match, test-plane irradiance non-uniformity, and temporal instability. The standard is used here as metrology context; this protocol does not claim IEC certification. Source: IEC 60904-9:2020, published 2020-09-18, https://webstore.iec.ch/en/publication/28973.
- NIST spectral-responsivity calibration services explicitly characterize photodetector spectral responsivity and spatial uniformity, and NIST notes that detector/electronics nonlinearity sets the upper usable optical-power range. Sources: https://www.nist.gov/programs-projects/spectral-responsivity-measurement and https://www.nist.gov/pml/sensor-science/optical-radiation/faqs-spectral-responsivity-calibrations (accessed 2026-08-26).
- NREL PV calibration practice uses calibrated reference devices and spectral-mismatch correction when simulator spectrum and device responsivities differ. Source: NREL photovoltaic calibrations, https://www.nrel.gov/docs/fy17osti/66873.pdf.

These sources support the need for traceable responsivity, linearity, spatial/temporal control, and spectral-mismatch awareness. They do not supply the project-specific numerical gates below; those are engineering assumptions to be retired or revised with measured facility performance.

## Frozen R2 acquisition grid

The v3.15 grid remains unchanged:

- 17 geometrically spaced levels from 0.05 to 2.0 nominal suns;
- ratio `1.259298684` between adjacent levels;
- primary local quadratic window: 7 points in `ln(Phi)`;
- mandatory sensitivity window: 9 points;
- primary curvature contrast: `Delta_n_curv = n_id(~1 sun) - n_id(~0.1 sun)`.

No intensity points, smoothing windows, or primary anchors may be changed after R2 response data are unblinded.

## Reference-detector calibration model

For each requested intensity level `j`, record dark-subtracted reference-detector signal

`S_j = S_raw,j - S_dark,j`.

The relative calibrated intensity is

`Phi_j / Phi_ref = (S_j / S_ref) * C_j`,

where `C_j` contains any wavelength/spectral-response or facility-specific correction required by the calibrated reference path. If the source spectrum changes with commanded intensity, `C_j` is not assumed constant.

All relative uncertainties must be tagged as one of:

1. **absolute/common scale** — shared multiplicative term;
2. **session/sweep drift** — correlated within a sweep or session;
3. **smooth nonlinearity** — intensity-dependent correlated term;
4. **point residual** — remaining point-specific component.

Do not RSS all four terms as if independent.

## Why nonlinearity matters more than common scale

Let `x = ln(Phi_true)` and `x_m = x + delta(x)` be the analyzed log-intensity axis. For a constant multiplicative calibration error, `delta` is constant and

`dVoc/dx_m = dVoc/dx`,

so the local ideality derivative is invariant to that common scale shift.

For a local log-axis gain error `x_m=(1+a)x+c`,

`n_measured = n_true/(1+a)`.

The committed v3.16 synthetic calculation independently verifies this analytic result.

For the frozen synthetic `Delta_n_curv=0.10` planning effect:

- +2% common intensity scale: curvature bias `0` to numerical precision;
- +0.5% log-axis gain: curvature bias `-0.0004975`;
- smooth quadratic log-axis residual with 0.5% amplitude across the full range: curvature bias `-0.006437`.

The final case is intentionally adversarial and model-dependent. It demonstrates that smooth calibration curvature can masquerade as physical ideality curvature even when absolute scale is unimportant.

## Qualification gates

These are preregistered **engineering gates**, not standards-derived acceptance limits.

### Q1 — reference-chain linearity / nonlinearity

Over the 17 commanded levels, after dark subtraction and normalization:

- fit `ln(S_j/S_ref)` versus the commanded/log-calibrated intensity coordinate using a predeclared low-order calibration model;
- maximum absolute residual in relative intensity must be `<=0.5%` over 0.05–2 suns;
- residuals must not show a monotonic or quadratic structure that produces `|Delta_n_curv calibration bias| >0.01` when propagated through the frozen v3.15 estimator.

If either condition fails, the intensity axis is not qualified for confirmatory curvature work.

### Q2 — repeatability and drift

At minimum, repeat reference-detector anchors near 0.1 and 1.0 sun before and after every device sweep.

- pre/post calibrated-intensity drift at either anchor: `<=0.2%` planning gate;
- pre/post `Voc` anchor drift on the DUT: `<=0.5 mV` planning gate;
- any systematic monotonic drift with acquisition order is retained and modeled, not averaged away.

Anchor repeats are technical repeats and do not increase independent substrate count.

### Q3 — ascending / descending history

Across independent substrates, block sweep direction so both ascending and descending sweeps are represented.

For a qualification subset on the same stable pixel:

- pointwise ascending-versus-descending `Voc` difference after time alignment: median absolute difference `<=0.5 mV`;
- difference in the primary `Delta_n_curv` between directions: `<=0.03`.

If the curvature-direction difference exceeds 0.03, the result is classified as sweep-history-sensitive and cannot be used as a confirmatory recombination discriminator without a new kinetic protocol.

### Q4 — DUT temperature

Record DUT-adjacent temperature for every intensity level.

- temperature stability during an accepted point: `sigma <=0.25 K`;
- maximum excursion relative to the preregistered 300 K target: `<=0.5 K` during the primary sweep unless the analysis explicitly uses measured point temperatures;
- any reproducible temperature-versus-intensity structure is a physical confound to be tested, not merely a normalization correction.

For a fixed measured `Voc` slope, using 300.5 K instead of 300 K changes inferred ideality by `300/300.5 - 1 = -0.1664%`; for a synthetic curvature of 0.10 this normalization-only bias is `-0.0001664`. This small arithmetic effect does **not** bound temperature-driven changes in the device's recombination physics.

### Q5 — point-level `Voc` precision

The v3.15 confirmatory gate remains `<=0.5 mV` SD for the point estimate under the actual acquisition protocol. Repeated raw readings may estimate technical noise but are not independent fabrication samples.

## Spectral mismatch / source-state control

Because simulator spectrum may change with source command or attenuation method, record the illumination configuration at every point. If the source uses lamp-current changes, LED-channel redistribution, filters, or ND wheels that change spectrum, measure or bound the spectral change and compute a device/reference mismatch correction where feasible.

A reference detector with a different spectral responsivity from PM6:Y6 can report a stable total signal while the effective excitation of the DUT changes. Therefore a scalar reference-current calibration alone is insufficient if source spectrum varies materially with intensity.

## Raw-data contract

Use `technical/data/r2_voc_intensity_qualification_template_v3_16.csv` and preserve:

`lot -> substrate -> pixel -> session -> sweep -> intensity -> raw reading`.

Required fields include commanded and calibrated intensity, reference-detector raw/dark signal, detector identity, one-sigma calibration uncertainty, correlation group, DUT temperature and uncertainty, `Voc` and uncertainty, sweep direction/order, anchor pairing, QC status, and deviations.

## Exclusions and QC

Predefine hardware-invalid states before analysis: detector saturation/nonlinearity, source unlock, missing dark/reference data, failed temperature logging, open/short device, or documented contact interruption. A point is not excluded merely because it creates curvature or disagrees with the preferred mechanism.

All functional samples remain reported. Failed qualification points remain in the raw dataset with QC status and reason.

## Independent checks

The executable model `models/r2_illumination_qualification_v3_16.py` performs:

1. noiseless local-quadratic limiting-case recovery;
2. exact invariance to a common multiplicative intensity scale;
3. analytic versus numerical agreement for a constant log-axis gain error;
4. adversarial smooth calibration-curvature sensitivity;
5. independent analytic temperature-normalization sensitivity.

The generated CSV is frozen and CI must regenerate it exactly on supported Python versions.

## Decision rule

The R2 `Voc`-intensity mechanism observable remains **exploratory** unless Q1–Q5 pass prospectively. If calibration curvature, sweep-history, or DUT heating fail their gates, the remedy is to redesign acquisition/calibration before interpreting H1–H4—not to add post-hoc smoothing or select a favorable sweep direction.
