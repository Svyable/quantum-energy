# Evidence note — R2 acquisition-order drift discriminator v3.24

Date: 2026-08-27

## Established evidence

NIST's process-modeling guidance states that run-order residual plots are useful for detecting drift only when the data were collected in randomized or otherwise non-monotonic predictor order; when predictor level increases/decreases with time, drift can be inseparable from the predictor-response relationship. NIST's experiment-design guidance likewise defines randomization as random determination of run sequence.

Sources checked 2026-08-27:

- https://itl.nist.gov/div898/handbook/pmd/section4/pmd443.htm
- https://www.itl.nist.gov/div898/handbook/toolaids/pff/pri.pdf

These sources support the experimental-design principle, not any claim that R2 exhibits drift.

## Engineering assumptions

- Four complete randomized 17-point blocks are an adequate first-order discriminator.
- Separate linear + quadratic within-block time terms are sufficient to represent smooth short-run conditioning for the gate.
- `u(Delta_n_curv) <= 0.01` and residual SD `<=0.5 mV` are provisional project limits.
- Randomization is performed only after satisfying facility settling/interlock/safety constraints.

## Falsifiable hypothesis

A real R2 `Voc`-intensity curvature signal will remain materially unchanged after randomized acquisition order and explicit smooth time-drift adjustment. Failure indicates that acquisition history/time is a conventional confound requiring characterization before mechanism inference.

## Synthetic/model results — not experimental evidence

Frozen software stress case:

- true synthetic curvature `0.10`;
- 17 points from 0.05 to 2 sun;
- four randomized blocks, seed `20260827`;
- 2 mV peak-to-peak linear time drift;
- 1 mV peak-to-peak quadratic time drift;
- 0.2 mV independent point noise.

Results:

- monotonic quadratic-drift alias: `0.0262150929257`;
- independent analytic alias: `0.0262150929257`;
- noise-free randomized corrected bias: `2.36e-16`;
- one noisy frozen realization: curvature `0.0925735107`, bias `-0.0074264893`, `u=0.0049249476`, residual SD `0.18597 mV`.

Sensitivity shows a 0.5 mV peak-to-peak quadratic drift already produces monotonic curvature bias `0.01310755`, above the existing 0.01 curvature-bias planning scale.

A 400-replicate fixed-design noise study gives nominal `+/-1.96u` coverage `0.9325` and p95 absolute curvature error `0.0106171`. This undercoverage is retained as a negative result; the software does not claim a calibrated 95% confidence interval.

## Independent check

For a geometric intensity grid, monotonic acquisition rank is affine in `x=ln(Phi)`. Purely linear drift is therefore linear in `x` and cannot create a slope difference; the numerical bias is `-8.33e-17`.

For `V_drift=A tau^2`, the separate analytic derivation gives

`Delta_n_alias = 8 A (x_H-x_L) / [(x_max-x_min)^2 (kBT/q)]`.

At 1 mV peak-to-peak quadratic drift (`A=0.5 mV`) this equals `0.0262150929257`, matching the numerical frozen-curvature implementation within `1e-12`.

## Conventional explanations preserved

Temporal dependence may reflect ordinary source settling, temperature evolution, photodoping/light soaking, trap filling, contact equilibration, autoranging/electronics drift, or degradation. A randomized-order discrepancy is evidence of an acquisition-time confound, not evidence for a quantum mechanism.

## Claim boundary

v3.24 can elevate only the statement that a declared smooth time-order model has been tested and bounded. It cannot establish recombination mechanism, electron–phonon coupling, open-quantum transport, or useful-energy improvement.
