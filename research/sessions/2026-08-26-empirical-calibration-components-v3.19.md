# Session record — 2026-08-26 — v3.19 empirical calibration components

## Increment

Added an empirical estimator that turns repeated reference-detector calibration sweeps into a covariance model consumable by the unchanged v3.18 uncertainty/power engine.

## Scientific delta

The uncertainty model no longer has to begin from hand-assigned common/shape/point modes. Repeated calibration data are decomposed into:

- systematic mean scale/stretch/quadratic shape;
- between-run coefficient covariance;
- pooled point residual;
- held-out predictive diagnostics.

The systematic mean shape is kept separate from repeatability covariance because a recognized systematic effect should be corrected or separately budgeted rather than automatically randomized.

## Independent checks

The deterministic synthetic fixture uses 24 calibration runs and seed `20260826`. A separate orthogonality-based closed-form coefficient calculation agrees with the normal-equation solver within `3e-15`.

Synthetic recovered values:

- mean scale `0.003267539947`;
- mean stretch `0.001534675828`;
- mean quadratic `0.002554235070`;
- adjusted between-run SDs `0.000854519239`, `0.000770682837`, `0.000517405506`;
- pooled point residual SD `0.000720322287`;
- LOSO 95% pointwise coverage `0.948529412`;
- LOSO normalized RMSE `1.04651243`.

The generator truth is explicitly synthetic: means `0.003/0.0015/0.0025`, between-run SDs `0.0010/0.0008/0.0006`, point SD `0.0007`.

The generated empirical sidecar, when fed into the unchanged v3.18 synthetic curvature fixture together with the existing 0.5 mV point-level `Voc` uncertainty, gives approximately `u(Delta n)=0.02246` and synthetic planning power `0.99366`.

## Adversarial checks

- five runs -> `INCOMPLETE`;
- systematic cubic distortion outside the frozen basis -> `INCOMPLETE`;
- mixed detector IDs -> rejected;
- non-positive adjusted covariance -> `INCOMPLETE` rather than silently clipped.

## Claim boundary

This work estimates repeatability covariance only. It cannot estimate the absolute systematic calibration error of the same reference detector from repetition, and it cannot validate R2 mechanism physics.

## Unresolved risks

- real facilities may need higher-order or wavelength-dependent calibration modes;
- residuals may be heteroscedastic rather than pooled-iid;
- multiple detector/gain regimes need separate populations or a richer hierarchical model;
- eight runs is a minimum engineering gate, not a guarantee of stable covariance estimates;
- finite-sample covariance deconvolution can be unstable near zero variance components.

## Next best increment

Specify and validate a **real reference-detector repeatability campaign**: minimum run count, day/session separation, randomized ascending/descending intensity order, detector warm-up and zero checks, source-spectrum tracking, and an acquisition export that feeds v3.19 unchanged. If a real facility can provide these repeats sooner, ingest them directly and retire the synthetic component magnitudes.
