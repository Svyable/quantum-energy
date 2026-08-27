# Session record — 2026-08-27 — R2 acquisition-order drift discriminator v3.24

## Increment

Added a randomized-order `Voc`-intensity acquisition and analysis gate to distinguish frozen curvature from smooth within-sweep temporal drift/conditioning.

## Why this increment

Open PRs already cover empirical calibration covariance (#6/#7), prospective calibration holdout (#8), absolute/reference systematic uncertainty (#9), facility packet integrity (#10), and wavelength-resolved spectral mismatch (#11). None directly break the confounding between DUT intensity and acquisition time in the DUT `Voc`-intensity sweep.

## Established evidence used

NIST process-modeling guidance warns that drift cannot be separated from a predictor-response relation when predictor order is monotonically tied to time, and emphasizes randomized order for drift diagnostics. No external source is used to claim that R2 actually has drift.

## Engineering design

- four complete 17-point randomized blocks (68 observations);
- fixed seed `20260827`;
- two shuffled permutations, each paired with its exact reverse;
- actual `elapsed_s` recorded and modeled;
- intensity fixed effects plus separate block intercept, linear-time, and quadratic-time terms;
- drift-adjusted intensity effects feed the frozen local-ideality curvature estimator.

Provisional project gates:

- `u(Delta_n_curv) <= 0.01`;
- residual SD `<=0.5 mV`;
- >=4 complete blocks on the identical grid.

## Decision-driving synthetic checks

All values below are software/synthetic, not R2 measurements.

Stress inputs:

- true synthetic curvature `0.10`;
- 2 mV peak-to-peak linear time drift;
- 1 mV peak-to-peak quadratic time drift;
- 0.2 mV independent point noise.

Results:

- monotonic same-drift curvature alias `0.0262150929257`;
- analytic independent derivation `0.0262150929257`;
- pure linear-drift limiting-case bias `-8.33e-17`;
- randomized noise-free corrected bias `2.36e-16`;
- frozen noisy realization: curvature `0.0925735107`, bias `-0.0074264893`, `u=0.0049249476`, residual SD `0.000185969 V`.

Sensitivity:

- 0.25 mV quadratic p-p -> monotonic bias `0.00655377`;
- 0.50 mV -> `0.01310755`;
- 1.00 mV -> `0.02621509`;
- 2.00 mV -> `0.05243019`.

Thus a sub-millivolt smooth temporal effect is large enough to cross the current 0.01 curvature-bias planning scale.

## Independent numerical / statistical check

A separate test derives the monotonic quadratic alias analytically from the geometric grid and compares it with the frozen numerical estimator at tolerance `1e-12`.

A fixed-design 400-replicate Gaussian-noise check uses seeds `700000...700399`:

- nominal `+/-1.96u` coverage `0.9325`;
- p95 absolute curvature error `0.01061705`.

The undercoverage is preserved as a negative result. The implementation reports 1-sigma propagated uncertainty and does not call `1.96u` a calibrated 95% confidence interval.

## Statistical independence

The 68 observations are technical repeats within one measurement session/pixel. They do not increase substrate/device sample size. Experimental hierarchy becomes `lot -> substrate -> pixel -> session -> randomized block -> intensity observation` for this diagnostic.

## Conventional/null explanations

Source settling, DUT temperature evolution, photodoping/light soaking, trap filling, contact equilibration, autoranging/electronics drift, and degradation can all create temporal structure. The randomized protocol is a discriminator for time-order confounding, not a mechanism classifier.

## Corrections / superseded claims

No merged arithmetic is corrected. Interpretation is narrowed: ascending/descending agreement alone is not sufficient to exclude nonlinear acquisition-time drift as a curvature confound. Confirmatory curvature should include a randomized-order discriminator or an equivalent independently justified temporal model.

## Files

- `models/r2_order_drift_v3_24.py`
- `models/r2_order_drift_test_v3_24.py`
- `models/fixtures/r2_order_schedule_v3_24.csv`
- `models/fixtures/r2_order_sensitivity_v3_24.csv`
- `technical/r2-order-drift-discriminator-v3.24.md`
- `research/evidence/r2-order-drift-v3.24.md`
- `research/sessions/2026-08-27-r2-order-drift-v3.24.md`
- `venture/v3.24-order-drift-decision.md`
- `.github/workflows/r2-order-drift.yml`
- canonical `research/evidence-map.md` and `technical/current-specification.md` updates.

## Unresolved risks

- real R2 time dependence may be non-polynomial or intensity-history dependent;
- randomized jumps may need facility-specific settling times and could themselves perturb device state;
- point errors may be heteroscedastic/correlated;
- four blocks are an engineering minimum, not a publication sample-size theorem;
- the nominal OLS 95% interval is not yet calibrated prospectively;
- open PRs #6–#11 remain to be reconciled by human review.

## Single best next increment

Execute the frozen four-block randomized schedule on the first qualified R2 pixel immediately after a standard v3.17 ascending/descending measurement, using identical source/calibration/temperature/dwell conditions. Compare monotonic and drift-adjusted curvature before any mechanism interpretation.
