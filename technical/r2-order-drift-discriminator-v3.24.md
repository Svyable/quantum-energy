# R2 acquisition-order / temporal-drift discriminator v3.24

## Purpose

The merged R2 `Voc`-intensity path uses ascending/descending sweeps and anchors, but a monotonic intensity sequence can still alias smooth time dependence into the intensity response. NIST's process-modeling handbook explicitly warns that drift cannot be separated from predictor response when the predictor is collected in increasing/decreasing time order, and emphasizes randomized run order for this reason.

Primary source checked 2026-08-27:

- NIST/SEMATECH e-Handbook, run-order plots and drift: https://itl.nist.gov/div898/handbook/pmd/section4/pmd443.htm
- NIST/SEMATECH e-Handbook, completely randomized designs: https://www.itl.nist.gov/div898/handbook/toolaids/pff/pri.pdf

These sources support experiment-design logic only. They do not establish that R2 actually has temporal drift or any device mechanism.

## Claim classes

**Established experiment-design evidence:** randomized order enables time-order residual diagnostics and reduces confounding between a predictor and time trend.

**Engineering assumptions:** four complete randomized blocks are an acceptable first drift-discrimination design; smooth within-block drift is adequately represented by block-specific linear + quadratic time terms; residual SD <=0.5 mV and propagated drift-model curvature uncertainty <=0.01 are provisional project gates.

**Falsifiable hypothesis:** after randomizing the 17 intensity settings, a low-order time model can separate smooth temporal conditioning/drift from the frozen intensity-curvature observable with <=0.01 standard uncertainty contribution and <=0.5 mV unexplained point residual SD.

**Synthetic/model results:** all numerical results below are software-verification values, not R2 measurements.

## Acquisition design

Use the frozen 17-point 0.05–2 sun grid in four complete blocks (68 measurements). The committed schedule uses seed `20260827` and two independently shuffled permutations; each is paired with its exact reverse.

This pairing gives every intensity exactly the same mean acquisition rank across the four blocks:

`mean(rank_i) = 8` for ranks 0...16.

Therefore a purely linear run-order term is exactly balanced in the block average. The four-block design is not perfectly balanced for all higher moments; the analysis estimates quadratic drift explicitly rather than assuming cancellation.

The schedule is in `models/fixtures/r2_order_schedule_v3_24.csv`.

Randomization never overrides instrument warm-up, interlocks, source settling, safe slew limits, or a preregistered dwell requirement. Actual elapsed time is recorded and used; sequence index alone is not substituted for time.

## Measurement model

For block `b`, intensity setting `i`, and normalized within-block elapsed time `tau_bi`:

`Voc_bi = alpha_i + delta_b + l_b tau_bi + q_b (tau_bi^2 - mean_b(tau^2)) + epsilon_bi`.

Definitions:

- `Voc_bi`: measured open-circuit voltage [V].
- `alpha_i`: intensity-specific voltage effect [V].
- `delta_b`: block intercept [V].
- `l_b`: block-specific linear temporal term [V per dimensionless tau].
- `q_b`: block-specific quadratic temporal term [V per tau^2].
- `tau`: dimensionless elapsed-time coordinate scaled to approximately [-1,1] inside each block.
- `epsilon`: residual [V].

The design uses all 17 intensity fixed effects, three nonbaseline block intercepts, and two temporal coefficients per block. With four blocks this gives 28 fitted coefficients from 68 observations and 40 residual degrees of freedom.

The drift-adjusted `alpha_i` values are fed into the same frozen 7-point local-quadratic curvature estimator used by the R2 stack.

## Curvature equation and units

`n_id(Phi) = [dVoc/d ln(Phi)] / (k_B T/q)`

and

`Delta_n_curv = n_id(~1 sun) - n_id(~0.1 sun)`.

`ln(Phi)` and `n_id` are dimensionless. `dVoc/dln(Phi)` and `kBT/q` are volts, so `Delta_n_curv` is dimensionless.

Because the local polynomial derivative is linear in the fitted `alpha_i`, the OLS covariance of the intensity effects propagates exactly at first order:

`u_Delta^2 = w^T Cov(alpha) w`,

where `w` is the frozen curvature weight vector.

## Independent limiting-case derivation

The frozen intensity grid is geometric, so acquisition rank in a monotonic sweep is affine in `x = ln(Phi)`.

A purely linear time drift is therefore linear in `x` and changes the local slope but not the slope difference. Synthetic 2 mV peak-to-peak linear drift gives curvature bias `-8.33e-17`, numerical zero.

For a monotonic quadratic drift

`V_drift = A tau^2`,

with `tau` spanning -1 to +1 and `A = V_pp,quad/2`, differentiation gives the independent analytic curvature alias

`Delta_n_alias = 8 A (x_H - x_L) / [(x_max - x_min)^2 (kBT/q)]`.

For `V_pp,quad = 0.001 V`, the analytic result is

`Delta_n_alias = 0.0262150929257`.

The independent numerical frozen-curvature implementation gives

`0.0262150929257`,

agreement within `1e-12`.

## Synthetic stress fixture

Inputs:

- 17 points, 0.05–2 sun geometric grid;
- explicitly synthetic true `Delta_n_curv = 0.10`;
- four frozen randomized blocks;
- 2 mV peak-to-peak linear temporal drift;
- 1 mV peak-to-peak quadratic temporal drift;
- point `Voc` noise SD = 0.2 mV;
- Python standard library;
- schedule seed `20260827`.

One deterministic noise realization gives:

- randomized-model curvature `0.0925735107`;
- error vs synthetic truth `-0.0074264893`;
- propagated `u(Delta_n_curv) = 0.0049249476`;
- residual SD `0.18597 mV`;
- status `PASS` under the provisional v3.24 gates.

In the noise-free limiting case, the randomized model recovers the synthetic curvature with absolute error `2.36e-16`.

## Sensitivity to nonlinear time drift

With the 2 mV linear term held fixed, monotonic-sweep curvature alias is:

| quadratic peak-to-peak drift | monotonic curvature bias |
| ---: | ---: |
| 0 mV | ~0 |
| 0.25 mV | 0.00655377 |
| 0.50 mV | 0.01310755 |
| 1.00 mV | 0.02621509 |
| 2.00 mV | 0.05243019 |

Thus only 0.5 mV peak-to-peak quadratic temporal structure exceeds the existing project `|curvature bias| <= 0.01` planning scale in this synthetic limiting case.

The frozen randomized model removes every row of this noise-free sensitivity table to numerical precision; see `models/fixtures/r2_order_sensitivity_v3_24.csv`.

## Stochastic numerical check

A separate test fixes the acquisition schedule and varies only independent 0.2 mV Gaussian point noise across 400 synthetic experiments (`noise seed = 700000 + replicate`).

Results:

- nominal `estimate +/- 1.96 u` coverage: `0.9325`;
- 95th percentile absolute curvature error: `0.0106171`.

This is a useful negative result: the simple finite-sample Gaussian OLS interval should **not** be advertised as a calibrated 95% confidence interval from this 400-run software check. v3.24 therefore reports the propagated 1-sigma standard uncertainty and uses it as an engineering gate; it does not promote the 1.96 multiplier to a publication confidence claim.

## Gates

A v3.24 randomized block analysis requires:

- >=4 complete randomized blocks;
- exactly one observation per frozen target intensity per block after preregistered QC exclusions;
- actual elapsed time inside every block;
- drift-model `u(Delta_n_curv) <= 0.01`;
- residual SD <=0.5 mV.

These numerical limits are engineering assumptions pending real facility evidence; they are not NIST requirements.

A pass means only that smooth within-block acquisition-order drift is bounded under the declared model. It does not validate calibration, spectral mismatch, temperature stability, contact physics, recombination mechanism, EPC, or open-quantum transport.

## Statistical independence

The 68 measurements are technical repeats on one DUT state. They are not 68 independent devices, substrates, or fabrication replicates. No `sqrt(68)` device-level evidence credit is allowed. The controlling hierarchy remains lot -> substrate -> pixel -> session -> block -> intensity observation.

## Conventional explanations / discriminator

Ordinary explanations for temporal structure include source settling, thermal conditioning, photodoping/light soaking, contact equilibration, trap filling, instrument autoranging, detector/electronics drift, and irreversible degradation. v3.24 is intentionally agnostic about which is responsible.

The discriminator is acquisition order: if apparent curvature changes materially after randomized-order time adjustment, the monotonic-sweep mechanism interpretation must be narrowed to an acquisition-time confound until the temporal physics is separately characterized.

## Validity limits

The model only removes smooth block-specific linear/quadratic time behavior. Step changes, long-memory state dependence, intensity-history interactions, irreversible degradation, and time constants comparable to settling/dwell intervals can violate it. Those cases require an explicit dynamical protocol rather than adding higher polynomial degree post hoc.

## Best next experiment

On a qualified R2 pixel, acquire the four frozen randomized blocks under the same source, temperature, spectral, dwell, and calibration conditions as the monotonic v3.17 sweep. Compare the drift-adjusted curvature and uncertainty with the monotonic result before mechanism interpretation.
