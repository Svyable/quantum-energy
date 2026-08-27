# Evidence note — R2 prospective reference-repeatability campaign v3.20

## Established methodological evidence

NIST Dataplot documents the one-way random-effects variance component

`variance_between = max(0, (MSTR - MSE) / n0)`

with `n0` equal to the group sample size in the balanced case. This supports the planning variance-component calculation used to size the calibration campaign.

Source: https://itl.nist.gov/div898/software/dataplot/refman1/auxillar/onewayan.htm — checked 2026-08-26 America/Chicago.

NIST TN 1297 states that combined standard uncertainty incorporates individual standard uncertainties and covariances as appropriate, and its Appendix A treats changes across observers, instruments, samples, laboratories, and measurement times as potential input quantities in a measurement process.

Sources:
- https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-5-combined-standard-uncertainty
- https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty

Checked 2026-08-26 America/Chicago.

## Program context

Two open automation PRs (#6 and #7) currently contain overlapping v3.19 empirical calibration-covariance estimators. This v3.20 increment does not choose between or duplicate them. It freezes the prospective acquisition/holdout design that either implementation can consume after human review reconciles the estimator path.

## Engineering assumptions

- 24 training sessions are the initial covariance-fitting population.
- 6 additional sessions are kept prospectively untouched until the estimator, model form, QC rules, and holdout score are frozen.
- Four sweeps/session are used, with two ascending and two descending sweeps.
- Training spans six day blocks; holdout spans two later day blocks.
- A 30% 90th-percentile absolute relative error in session-SD estimation is the planning precision gate.
- The session-count sensitivity model assumes balanced Gaussian random effects. Real facility non-Gaussianity/nonstationarity is a reason to narrow or redesign, not to force the model.

These are project design choices, not metrology-standard requirements.

## Synthetic planning result

Python standard library, seed `20260826`, 20,000 simulated campaigns per design cell.

For 24 sessions and four sweeps/session:
- within/between SD ratio 0.75 -> p90 absolute relative error of estimated between-session SD `0.27918`;
- ratio 1.00 -> `0.31115`.

For 30 sessions at ratio 1.00 -> `0.27457`.

The mean estimated **variance** remains within about 0.3% of the normalized truth for the 24-session ratio-0.75 cell (`0.99714`) and within about 0.2% for ratio 1.00 (`1.00148`). This agrees with the independent expected-mean-squares derivation that the unconstrained ANOVA moment estimator targets the between-session variance.

These are synthetic operating characteristics only.

## Falsifiable hypothesis

A low-order empirical calibration covariance model fitted on sessions 1–24 will predict the untouched sessions 25–30 under the same frozen facility configuration well enough to pass preregistered holdout diagnostics without refitting.

The discriminator is prospective performance on those six sessions. Failure is evidence that the covariance model, facility stationarity assumption, or configuration lock is inadequate.

## Explicit non-claims

- The 24+6 design is not experimental evidence of facility stability.
- The model does not establish absolute detector accuracy.
- Passing calibration validation does not identify a DUT recombination mechanism, EPC, or open-quantum transport.
- More sweeps or intensity points do not substitute for additional independent sessions/day blocks.
