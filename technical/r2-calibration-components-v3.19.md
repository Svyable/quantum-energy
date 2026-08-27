# R2 empirical calibration-component estimator v3.19

## Purpose

v3.18 can propagate correlated intensity-axis uncertainty through the frozen 17-point `Voc`-intensity curvature observable, but its component loadings were still declared inputs. v3.19 adds a facility-neutral estimator that derives those loadings from **repeated reference-detector calibration sweeps** before the device sweep is interpreted.

This is metrology infrastructure. It does not identify a recombination mechanism, EPC, or open-quantum transport.

## Input hierarchy

Each calibration row must carry:

`session_id, sweep_id, sequence_index, target_suns, calibrated_suns, qc_status`

The estimator requires at least 8 PASS sweeps, at least 3 sessions, at least 2 PASS sweeps per session, and a common target-intensity grid with at least 7 points. These are engineering minimums for software operation, not a claim that 3 sessions are sufficient for a publication-grade facility covariance estimate.

The hierarchy is preserved as session -> calibration sweep -> intensity point. Repeated intensity points are not independent calibration sessions.

## Measurement model

For target intensity `Phi_i` and calibrated intensity `Phi_hat_si` in sweep `s`, define the dimensionless log-axis error

`e_si = ln(Phi_hat_si / Phi_i)`.

Let

`x_i = ln(Phi_i)`,

`z_i = (x_i - mean(x)) / max_j |x_j - mean(x)|`,

and construct `q_i` by orthogonalizing `z_i^2` against the constant and `z` basis on the frozen grid.

Each sweep is fit as

`e_si = a_s + b_s z_i + c_s q_i + r_si`.

Interpretation:

- `a_s`: common log-scale offset;
- `b_s`: log-axis stretch/gain mode;
- `c_s`: smooth quadratic shape mode;
- `r_si`: remaining point residual.

All terms are dimensionless because they operate in `ln(Phi)`.

## Session drift

The session-level common-scale component is estimated from the fitted `a_s` values with a one-way random-effects ANOVA moment estimator.

For `J` sessions, `N` sweeps, session sizes `n_j`, between-session mean square `MSB`, and within-session mean square `MSW`,

`n0 = [N - sum_j(n_j^2)/N] / (J - 1)`

and

`sigma_session^2 = max(0, (MSB - MSW) / n0)`.

This matches the random-effects variance-component form documented by NIST Dataplot. The `max(0, ...)` truncation is a method-of-moments boundary, not evidence that true between-session variance is exactly zero when the unconstrained estimate is negative.

## Within-session smooth covariance

After subtracting each session's coefficient mean, v3.19 forms the pooled 3x3 covariance of `(a,b,c)` across sweeps. A Cholesky factor `L` satisfies

`C_within = L L^T`.

The three columns of `L` are mapped back through `[1, z_i, q_i]` to produce signed, perfectly correlated latent loadings compatible with the v3.18 component sidecar. This preserves covariance among common, stretch, and quadratic within-session modes instead of forcing them independent.

## Point residual

OLS fitting suppresses residual variance according to point leverage. With orthogonal basis `[1,z,q]`, leverage is

`h_i = 1/n + z_i^2 / sum(z^2) + q_i^2 / sum(q^2)`.

The point residual standard deviation is therefore estimated as

`u_point,i = SD_s(r_si) / sqrt(1 - h_i)`.

v3.19 then treats those remaining point terms as independent in the generated sidecar. **That diagonal residual assumption is an explicit engineering assumption.** Real facility data must challenge it; coherent higher-order residual structure would require another correlated component rather than being hidden inside the point term.

## Synthetic verification

The committed adversarial test uses Python standard-library RNG seed `20260826` and an explicitly synthetic 12-session x 5-sweep/session x 17-point calibration campaign. Data-generating standard deviations are:

- session common scale: `0.0025` in `ln(Phi)`;
- within-session common: `0.0015`;
- within-session stretch: `0.0012`;
- within-session quadratic: `0.0018`;
- independent point residual: `0.0008`.

The within-session coefficient generator includes correlations `rho(a,b)=0.4`, `rho(a,c)=0.1`, and `rho(b,c)=-0.2`.

On the frozen seed, the estimator returns:

- session scale SD `0.00291108`;
- within common SD `0.00154414`;
- stretch SD `0.00128794`;
- quadratic SD `0.00177705`;
- median leverage-corrected point SD `0.000790696`.

These are synthetic recovery values, not measured facility performance.

## Independent checks

1. **Known-input recovery:** estimated synthetic standard deviations must remain within frozen tolerances of their generator values (30% for within-session modes, 40% for the noisier session variance component, 20% for median point residual).
2. **Covariance factorization:** `L L^T` must reconstruct the pooled coefficient covariance to absolute error <= `1e-15`.
3. **Independent algebraic propagation:** curvature-axis variance is computed directly as `B^T C B + sum_i(g_i u_i)^2` and separately through the emitted latent-component projections. They must agree within `1e-12` absolute uncertainty.
4. **Nonlinear Monte Carlo:** 10,000 draws from the fitted component model are propagated through the full v3.18 nonlinear curvature estimator. For the frozen synthetic case, linear `u(Delta n)=0.00244867` and Monte Carlo `u(Delta n)=0.00240968`, a difference of about 1.6%, inside the preregistered 5% check.
5. **Limiting case:** a perfectly common intensity scale remains nearly invisible to derivative curvature; v3.18 already freezes that negative control.

## Sensitivity and decision meaning

The synthetic recovery tolerance is intentionally wider for between-session variance because variance components are noisy at small session counts. Increasing repeated sweeps inside one session does not substitute for more independent sessions when estimating session drift. The estimator therefore reports `n_sessions` and `n_pass_sweeps` separately.

The v3.18 power decision should use components produced from calibration data acquired under the same detector/source/configuration regime as the DUT measurement. Reusing an old covariance estimate after source, detector, geometry, software, or calibration-chain changes is out of scope.

## Null / conventional explanations

A smooth calibration mode can arise from detector nonlinearity, source regulation, range switching, spectral mismatch, interpolation/calibration-model error, thermal drift, geometry, or ordinary electronics. Finding a nonzero smooth covariance mode is not quantum-mechanism evidence. The discriminator is calibration/reference data acquired independently of DUT physics.

## Kill / narrow gates

Do not generate a v3.18 sidecar if the calibration repeat campaign fails structural requirements. Narrow or redesign the covariance model if real residuals show repeatable higher-order structure, heteroscedasticity not captured by the point terms, nonstationarity across sessions, or a source/detector configuration change.

## Provenance

- NIST Dataplot ONE WAY ANOVA documents the random-effects variance-component estimator `max(0,(MSTR-MSE)/n0)` and the unbalanced `n0` expression.
- NIST TN 1297 classifies statistical series-of-observation uncertainty as Type A and represents correlations using estimated covariances/correlation coefficients; Appendix A gives the covariance-inclusive first-order propagation law.

Accessed 2026-08-26 America/Chicago. External sources are methodological support only; all v3.19 numerical results are synthetic.
