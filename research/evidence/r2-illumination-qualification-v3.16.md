# Evidence record — R2 illumination qualification v3.16

Date: 2026-08-26

## Established external evidence

1. IEC 60904-9:2020 classifies solar simulators by spectral distribution match, irradiance non-uniformity, and temporal instability. It was published 2020-09-18 and remains the current edition identified by IEC as of this record. Source: https://webstore.iec.ch/en/publication/28973.
2. NIST provides detector spectral-responsivity and spatial-uniformity calibration; NIST guidance notes that maximum usable photodiode power is limited by detector/electronics nonlinearity and that changed beam conditions can change measurement uncertainty. Sources accessed 2026-08-26: https://www.nist.gov/programs-projects/spectral-responsivity-measurement and https://www.nist.gov/pml/sensor-science/optical-radiation/faqs-spectral-responsivity-calibrations.
3. NREL PV calibration practice uses calibrated reference devices and spectral-mismatch correction when simulator and reference/test-device spectral responses differ. Source: https://www.nrel.gov/docs/fy17osti/66873.pdf.

These sources justify measuring linearity, drift, spectral mismatch, and reference-device traceability. They do not establish R2-specific performance.

## Engineering assumptions introduced

- Maximum relative calibration residual `<=0.5%` over 0.05–2 suns.
- Calibration-induced primary-curvature bias `|Delta_n| <=0.01`.
- Reference-intensity anchor drift `<=0.2%`.
- DUT `Voc` anchor drift `<=0.5 mV`.
- Ascending/descending curvature difference `<=0.03`.
- DUT temperature excursion `<=0.5 K`, with within-point stability `sigma <=0.25 K`.

All are open engineering gates and must be retired/revised using measured facility and R2 behavior.

## Synthetic/model result

For the frozen v3.15 17-point grid and an injected `Delta_n_curv=0.10`:

- a +2% common multiplicative intensity-scale offset produces zero curvature bias numerically, as expected analytically because it shifts `ln(Phi)` by a constant;
- a +0.5% gain/stretch of the log-intensity axis gives `Delta_n=0.09950249`, bias `-0.00049751`, agreeing with the independent analytic result `0.10/1.005`;
- a smooth quadratic log-intensity residual with 0.5% amplitude gives `Delta_n=0.09356282`, bias `-0.00643718` under this adversarial synthetic shape;
- a +0.5 K temperature-normalization error at 300 K gives a relative ideality bias of `-0.00166389`; for a 0.10 curvature this is `-0.00016639` if device physics itself is unchanged.

These are sensitivity calculations only, not measured source or device behavior.

## Falsifiable operational claim

If Q1–Q5 in `technical/r2-illumination-calibration-sweep-qualification-v3.16.md` pass on the real facility/R2 setup, the illumination-axis and sweep-history contribution is sufficiently bounded for the frozen v3.15 curvature observable to proceed to mechanism analysis. Failure narrows the experiment to metrology development until the acquisition path is redesigned.

## Conventional explanations preserved

Observed local-ideality curvature may still arise from source spectral changes, calibration nonlinearity, DUT heating, sweep kinetics/hysteresis, contacts/surface recombination, transport resistance, energetic disorder, state filling, or mixtures. Passing v3.16 only bounds the first measurement-path subset; it does not uniquely identify a recombination mechanism.
