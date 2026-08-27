# Evidence note — empirical R2 calibration components v3.19

## Established methodological evidence

NIST Dataplot documents a one-way random-effects ANOVA variance component for a grouping factor as

`sigma_group^2 = max(0, (MSTR - MSE)/n0)`

with the standard unbalanced-design `n0` term. This supports the v3.19 method-of-moments separation of between-session common-scale variance from within-session sweep variance.

Source: https://itl.nist.gov/div898/software/dataplot/refman1/auxillar/onewayan.htm — accessed 2026-08-26.

NIST TN 1297 describes statistical analysis of series of observations as Type A uncertainty evaluation and states that correlations are characterized by estimated covariances or correlation coefficients. Its Appendix A gives covariance-inclusive first-order propagation.

Sources:
- https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-2-classification-components-uncertainty
- https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty

Accessed 2026-08-26.

## Engineering assumptions

- Low-order calibration distortion is adequately represented initially by common, log-axis stretch, and orthogonal quadratic shape modes.
- Between-session drift is initially represented only as a common log-scale term.
- Remaining leverage-corrected point residuals are treated as independent when emitted to v3.18.
- At least 3 sessions, 2 sweeps/session, and 8 total sweeps are software minimums, not publication-grade sample-size claims.

## Falsifiable hypothesis

Repeated calibration sweeps from a stable facility configuration contain enough information to replace assumed v3.18 calibration modes with empirically estimated covariance components whose propagated curvature uncertainty remains stable on held-out sessions.

The discriminator is prospective held-out-session performance. Failure to predict held-out calibration errors means the covariance model must be expanded or the facility configuration is not stationary enough for the current representation.

## Synthetic/model result

The frozen seed-20260826 test with 12 synthetic sessions and 60 total sweeps recovers the known input component scales within preregistered tolerances. Direct covariance propagation and latent-sidecar propagation agree to numerical precision; a 10,000-draw nonlinear Monte Carlo agrees with first-order curvature uncertainty within 5%.

These are software-verification results only.

## Explicit non-claim

v3.19 does not establish real facility calibration stability, detector linearity, spectral accuracy, device physics, EPC, or open-quantum transport.
