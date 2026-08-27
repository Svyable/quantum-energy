# R2 Covariance-Aware Curvature Uncertainty and Power Gate v3.18

## Purpose

v3.17 qualifies whether the facility path is structurally usable. v3.18 answers the next question: **given the declared correlation structure of the measurement uncertainties, what is the standard uncertainty of the frozen local-ideality curvature observable, and what does that do to the v3.15 planning-power decision?**

Passing this model does not identify H3, EPC, or open-quantum transport. It only quantifies the uncertainty of the declared curvature measurement model.

## Frozen measurand

The local ideality estimate is

\[
n_{id}(\Phi)=\frac{dV_{OC}/d\ln\Phi}{k_B T/q},
\]

and the frozen curvature contrast is

\[
\Delta n_{curv}=n_{id}(\sim1\;sun)-n_{id}(\sim0.1\;sun).
\]

The 7-point local quadratic estimator from v3.14 remains primary. Anchor row identities are selected from the preregistered target-intensity grid; calibrated intensities provide the fitted x-axis.

## Covariance law

For a local measurement model `y=f(x)`, first-order propagation uses

\[
u_y^2 = g^T C g,
\]

where `g` is the sensitivity vector and `C` is the covariance matrix of the input quantities.

The implementation represents covariance through latent components. For component `k`,

\[
\delta x_i = l_{ik} z_k,\qquad z_k\sim N(0,1),
\]

so

\[
u_y^2 = \sum_k (g^T l_k)^2.
\]

This form makes correlation explicit and prevents the same systematic component from being divided by `sqrt(N)` merely because it appears on many rows.

For `Voc`, sensitivity weights are analytic because the local quadratic estimator is linear in `Voc`. For calibrated intensity, the code evaluates `d(Delta n_curv)/d ln(Phi_i)` by centered finite difference at `eps=1e-6` and checks convergence in the adversarial test suite.

## v3.17 compatibility and v3.18 sidecar

Without a sidecar:
- each `calibration_correlation_group` in the v3.17 CSV is interpreted as one perfectly correlated latent component;
- its per-row loading is `calibration_relative_u_1sigma`;
- each `source_spectrum_id` is interpreted as one correlated spectral-mismatch component with per-row loading `spectral_mismatch_u_rel`;
- `voc_u_V` is treated as independent point uncertainty.

This is useful but incomplete. One scalar uncertainty plus one group label per row cannot simultaneously represent, for example, a common calibration scale, a smooth shape mode, and a point residual.

The optional v3.18 component sidecar therefore allows multiple components per row:

`(sweep_id, sequence_index, variable, component_id, loading_1sigma, unit, note)`.

Rows sharing a `component_id` are perfectly correlated through one latent variable and may have different or signed loadings. This can represent common scale, gain/stretch, quadratic shape, session drift, detector stitching modes, or independent point terms.

## Independent verification

Synthetic checks use the exact frozen 17-point 0.05–2 sun grid and an explicitly synthetic `Delta n_curv=0.10` curve.

### Common intensity scale

A 0.5% perfectly common multiplicative intensity uncertainty gives propagated curvature uncertainty of approximately

`2.15e-12`

in the synthetic limiting case: a constant shift of `ln(Phi)` does not change a derivative-based curvature observable.

This is a useful check against naive RSS, which would incorrectly assign a large uncertainty to the same common scale repeated 17 times.

### Independent point-axis uncertainty

If the same 0.5% 1-sigma magnitude is instead independent at every intensity point, the propagated curvature standard uncertainty is

`0.005524884`.

### Smooth quadratic shape mode

A correlated quadratic log-axis mode with maximum 0.5% loading gives first-order

`u(Delta n_curv) = 0.006438705`.

An independent 12,000-draw Monte Carlo propagation gives approximately

`0.006434494`.

The relative difference is below 0.1%, supporting the local linearization for this stress case.

### v3.15 point-Voc cross-check

For independent 0.5 mV point-level `Voc` uncertainty and no axis uncertainty, v3.18 recovers

`u(Delta n_curv) = 0.0224200905`

and two-sided alpha=0.05 planning power for an explicitly synthetic 0.10 effect of

`0.993795964`.

These reproduce the v3.15 analytic result through a different implementation path.

### Combined frozen stress fixture

The committed v3.18 fixture combines:
- independent 0.5 mV `Voc` uncertainty at each point;
- one correlated quadratic axis mode with maximum 0.5% loading.

It gives

`u(Delta n_curv) = 0.02332632385`

and planning power

`0.9900183826`.

These are synthetic software-verification values, not facility measurements.

## Statistical independence

Ascending/descending sweeps, anchor revisits, repeated readings, and repeated calibration rows are technical repeats. v3.18 reports each sweep separately and feeds the **worst sweep** uncertainty into the power interface. It deliberately gives no `sqrt(N)` power credit for multiple sweep directions.

Independent substrate count remains a separate level in the lot -> substrate -> pixel -> session -> sweep -> intensity hierarchy.

## Current publication boundary

The BIPM/JCGM GUM requires significant correlations to be included in uncertainty propagation. JCGM 101 provides Monte Carlo propagation for cases where propagation of distributions is more appropriate. The 2026 GUM Amendment 1 explicitly addresses nonlinearity in measurement models. v3.18 therefore uses first-order covariance propagation as the primary transparent calculation and an independent Monte Carlo check for a nonlinear stress mode.

The sidecar is a model of declared covariance, not proof that the declaration is physically correct. Real facility characterization must determine the actual components and loadings.

## Stop / narrow rules

Do not call the R2 curvature measurement confirmatory if:
- required covariance components are unknown or knowingly omitted;
- the first-order result and Monte Carlo propagation disagree materially under the measured uncertainty scale;
- the uncertainty model requires correlation forms the sidecar cannot represent;
- the resulting worst-sweep planning power is below the preregistered decision threshold;
- sweep hysteresis, temperature, spectral mismatch, or other v3.17 gates fail.

## Next experiment

The next best evidence is still a real facility export. Once one is available, run v3.17 and v3.18 unchanged, then replace the synthetic covariance modes with experimentally supported components from reference-detector repeats, source-spectrum measurements, calibration residuals, and repeated `Voc` observations.
