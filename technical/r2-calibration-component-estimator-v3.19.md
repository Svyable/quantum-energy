# R2 Empirical Calibration-Component Estimator v3.19

## Purpose

v3.18 can propagate a covariance model through the frozen R2 local-ideality curvature metric. v3.19 estimates that covariance model from repeated reference-detector calibration sweeps instead of assigning shape/drift modes by assumption.

The estimator works on repeated calibration runs over one shared target-intensity grid and one reference detector. It decomposes

`e_si = ln(Phi_cal,si / Phi_target,i)`

into a low-order calibration-shape basis plus residuals.

Passing v3.19 means the declared repeatability covariance is empirically estimable and passes held-out checks. It does **not** estimate the absolute systematic calibration uncertainty of the reference detector, and it does not identify any device mechanism.

## Basis and model

Let `z_i` be centered, normalized `ln(Phi_target)` and let `q_i` be an orthogonalized normalized quadratic basis. For calibration run `s`,

`e_si = a_s + b_s z_i + c_s q_i + epsilon_si`.

Interpretation:
- `a_s`: run-level scale / common-mode offset;
- `b_s`: run-level log-axis stretch;
- `c_s`: run-level smooth quadratic shape;
- `epsilon_si`: point residual after the frozen smooth basis.

The mean coefficients `(mean a, mean b, mean c)` are treated as an estimated **systematic mean calibration shape**. Following ordinary metrology practice, recognized systematic effects should be corrected when practical or separately budgeted; they are not automatically converted into random repeatability uncertainty.

Between-run coefficient covariance is estimated from the fitted coefficients after subtracting the coefficient-estimation variance contributed by the pooled point residual:

`C_between = C_observed(beta) - sigma_res^2 (X^T X)^-1`.

The adjusted 3x3 covariance must be positive definite. Its Cholesky factor is converted into signed v3.18 sidecar loadings so coefficient correlations are preserved instead of discarded.

## Point residual

The pooled residual standard deviation uses

`sigma_res = sqrt(SSE / [N_runs * (N_points - 3)])`.

The v3.19 sidecar represents this as one independent point component per intensity. That is allowed only while residual diagnostics do not show material unexplained smooth structure or serial correlation.

## Model-adequacy checks

The current engineering checks are:

- at least **8 independent calibration runs**;
- one reference-detector ID across the modeled run population;
- identical target-intensity grid across runs;
- adjusted coefficient covariance must be positive definite;
- leave-one-run-out 95% predictive coverage >= 0.80;
- leave-one-run-out normalized RMSE between 0.6 and 1.5;
- maximum observed coefficient correlation <= 0.80;
- RMS of the mean residual shape <= 0.5 times pooled point-residual SD;
- absolute pooled residual lag-1 correlation <= 0.40.

These thresholds are **project engineering gates**, not JCGM/NIST requirements. Real facility data may motivate tightening, replacing, or expanding the basis before physical interpretation.

## Independent synthetic verification

The deterministic software fixture uses 24 synthetic calibration runs on the frozen 17-point grid with seed `20260826` and known generator values:

- systematic mean scale = 0.003;
- systematic mean stretch = 0.0015;
- systematic mean quadratic = 0.0025;
- between-run SDs = 0.0010 / 0.0008 / 0.0006;
- independent point residual SD = 0.0007.

The recovered finite-sample values are:

- mean scale `0.003267539947`;
- mean stretch `0.001534675828`;
- mean quadratic `0.002554235070`;
- adjusted SD scale `0.000854519239`;
- adjusted SD stretch `0.000770682837`;
- adjusted SD quadratic `0.000517405506`;
- pooled residual SD `0.000720322287`.

These are synthetic verification results, not measurements.

An independent coefficient calculation exploits the orthogonality of the frozen basis and agrees with the 3x3 normal-equation solver to better than `3e-15` in the synthetic fixture.

Held-out validation gives:

- LOSO nominal 95% pointwise coverage `0.948529412`;
- LOSO normalized RMSE `1.04651243`.

The pointwise coverage statistic is diagnostic, not an independent-binomial experiment, because points within a held-out calibration run are correlated.

## Adversarial checks

The test suite requires:

1. only five calibration runs -> `INCOMPLETE`;
2. a systematic cubic log-axis distortion outside the frozen basis -> `INCOMPLETE` through the mean-residual-shape gate;
3. mixed reference-detector IDs -> rejected rather than pooled;
4. synthetic finite-sample coefficient estimates remain within a broad factor-of-1.5 recovery band around the generator parameters.

## Integration with v3.18

v3.19 emits a signed component sidecar for the unchanged v3.18 covariance engine.

On the frozen synthetic `Delta n_curv=0.10` fixture, combining the empirically estimated calibration repeatability with the existing independent 0.5 mV `Voc` terms gives approximately:

- `u(Delta n_curv) ~= 0.02246`;
- planning power for the synthetic 0.10 effect `~= 0.99366`.

Again, these are software operating characteristics only.

## Identifiability boundary

Repeated sweeps can estimate repeatability and drift/shape variability. They **cannot determine absolute reference-detector calibration bias from repetition alone**. Absolute detector calibration, spectral responsivity uncertainty, and other common Type-B/systematic terms require external calibration evidence and must remain separate inputs to the uncertainty budget.

## Publication rule

Do not publish a facility-derived covariance sidecar as an empirical uncertainty model unless:

- the calibration runs are archived with provenance;
- the model passes the frozen or explicitly revised adequacy checks;
- systematic mean shape is corrected or separately budgeted;
- the absolute reference-detector systematic terms are declared separately;
- v3.18 accepts the emitted sidecar without analysis changes after unblinding.
