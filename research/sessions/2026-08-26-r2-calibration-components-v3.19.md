# Session record — 2026-08-26 — v3.19 empirical calibration covariance

## Increment

Added an executable estimator that converts repeated reference-detector intensity sweeps into empirical covariance components consumable by the merged v3.18 curvature-uncertainty engine.

## Problem retired

v3.18 could propagate a declared covariance model but did not estimate that model from repeat calibration data. v3.19 closes that software gap for a structured first model: session common scale + within-session common/stretch/quadratic covariance + leverage-corrected point residual.

## Important correction discovered during implementation

An initial diagnostic treated correlation among post-fit residuals as evidence of physical residual covariance. That is incorrect because OLS projection itself induces residual covariance. The implementation was corrected before publication. The final estimator uses leverage correction for point residual variance and explicitly labels independence of the remaining point terms as an engineering assumption. No prior repository result is numerically superseded because the faulty diagnostic was not committed.

## Verification

Synthetic generator: Python standard library, seed `20260826`, 12 sessions, 5 sweeps/session, 17 points/sweep.

Frozen recovered values:
- session common scale SD: `0.0029110797` vs synthetic input `0.0025`;
- within common SD: `0.0015441356` vs `0.0015`;
- within stretch SD: `0.0012879367` vs `0.0012`;
- within quadratic SD: `0.0017770465` vs `0.0018`;
- median point residual SD: `0.0007906962` vs `0.0008`.

Curvature-axis uncertainty on the explicit synthetic `Delta n=0.10` reference curve:
- first-order direct/sidecar result: `0.0024486675`;
- independent 10,000-draw nonlinear Monte Carlo: `0.0024096836`.

The difference is about 1.6%, below the frozen 5% nonlinear-check tolerance.

## Statistical independence

The estimator distinguishes independent calibration sessions from sweeps and intensity points. Repeating more points or sweeps within one session does not increase the independent session count used for between-session drift.

## Conventional explanations

Any recovered calibration mode can arise from ordinary detector/source/electronics/geometry/spectral/calibration-model behavior. It is a measurement-system result, not a DUT-mechanism result.

## Unresolved risks

- real calibration residuals may require higher-order or nonstationary modes;
- session drift may include stretch/shape terms, not only common scale;
- point residuals may remain correlated after low-order removal;
- 3 sessions is only a structural software minimum;
- the estimator has not yet been tested on a real facility export.

## Single best next increment

Add held-out-session validation: estimate components on prior calibration sessions, predict the covariance of a prospectively held-out session, and reject/narrow the model when the held-out standardized residuals exceed frozen coverage/shape gates.
