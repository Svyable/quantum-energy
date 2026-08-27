# Session record — 2026-08-26 — R2 prospective reference-repeatability campaign v3.20

## Increment

Preregistered a facility-neutral calibration repeatability campaign designed to prospectively validate the empirical covariance model rather than continue retrospective/synthetic fitting.

## Non-duplication decision

Open automation PRs #6 and #7 both implement overlapping v3.19 empirical calibration-covariance estimators. This run intentionally does not add a third estimator. It creates the shared next-step acquisition and holdout protocol instead.

## Frozen hierarchy and partition

`campaign -> day block -> session -> sweep -> intensity point`

- 24 training sessions across 6 day blocks;
- 6 prospective holdout sessions across 2 later day blocks;
- 4 sweeps/session;
- 2 ascending + 2 descending sweeps/session;
- 17 grid points/sweep;
- total 30 sessions, 120 sweeps, 2,040 grid-point measurements before dark/anchor rows.

The estimator/model hash, covariance basis, QC/exclusions, and holdout scoring rule must be frozen after session 24 and before acquisition of session 25.

## Quantitative planning

Model:

`y_sj = mu + A_s + e_sj`

with `A_s ~ N(0,sigma_between^2)` and `e_sj ~ N(0,sigma_within^2)`.

Balanced variance-component estimator:

`hat(sigma_between^2) = max(0, (MS_between-MS_within)/m)`, `m=4`.

Known expected-mean-squares cross-check:

`E[MS_between]=sigma_within^2+m*sigma_between^2`; `E[MS_within]=sigma_within^2`.

The simulation normalizes `sigma_between=1`, sweeps within/between SD ratio from 0.25 to 1.5, and uses seed `20260826`, 20,000 campaigns/cell.

Decision-driving synthetic outputs:
- 24 sessions, ratio 0.75: p90 absolute relative SD error `0.27918`;
- 24 sessions, ratio 1.0: `0.31115`;
- 30 sessions, ratio 1.0: `0.27457`.

Thus 24 training sessions meet the frozen 30% p90 planning-error gate only conditionally when within-session variability is not too large relative to between-session variability. This is a design result, not measured facility precision.

## Independent verification

The method-of-moments variance estimator has the correct algebraic expectation before nonnegative truncation. The Monte Carlo mean estimated variance / true variance for the 24-session cells is `0.99714` at ratio 0.75 and `1.00148` at ratio 1.0, consistent with the analytic target.

## Raw-data requirements

Added a CSV schema carrying partition/day/session/sweep hierarchy, sweep direction, row type, target/calibrated intensity, detector/source IDs, source-spectrum hash, gain/geometry state, temperatures, raw signal/dark, QC/exclusion code, and deviation note.

## Conventional explanations preserved

Any apparent session covariance can arise from source regulation, detector nonlinearity, spectral drift, range switching, thermal state, geometry, electronics, operator setup, or calibration-model error. Passing the campaign only supports a measurement-repeatability model; it does not establish DUT mechanism physics.

## Negative-result rule

If the six held-out sessions fail the frozen score, they remain the failed prospective test. They cannot be reused as tuning data and then called a new validation set. Redesign requires another untouched holdout.

## Unresolved risks

- both v3.19 estimator PRs remain open and need human reconciliation;
- the Gaussian balanced random-effects planning model may understate heavy tails/nonstationarity;
- day-block effects may require a richer hierarchy than session-only covariance;
- absolute reference-detector systematic uncertainty remains external;
- facility-specific warm-up/interlock/SOP constraints may require schedule adaptation before the campaign begins, which must be frozen before acquisition.

## Single best next increment

Human-review/reconcile the v3.19 estimator implementation, freeze a single held-out scoring rule, then execute sessions 1–24 at a cooperating facility and commit the freeze record before collecting sessions 25–30.
