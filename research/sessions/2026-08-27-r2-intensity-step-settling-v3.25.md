# Session record — 2026-08-27 — R2 v3.25 intensity-step settling qualification

## Increment

Added a prospective step-response qualification that must pass before randomized intensity order can be treated as a static `Voc(Phi)` measurement.

## Why now

Open PR #12 correctly randomizes intensity order to discriminate nonlinear temporal drift, but it also identifies a remaining conventional confound: intensity jumps can perturb the DUT/source/instrument state. v3.25 resolves that gap without duplicating the open calibration-covariance, holdout, systematic, packet-integrity, spectral-shape, or order-drift PRs.

## Quantitative derivation

Frozen curvature sensitivity satisfies

`delta Delta_n_curv = sum_i w_i delta V_i`.

The numerical 17-point implementation gives

`||w||_1 = 143.8085097637075 V^-1`.

An independent closed-form derivation for the equally spaced log-intensity grid gives

`||w||_1 = 6/[7 h (kBT/q)]`, `h=ln(40)/16`,

which agrees within `1e-10`.

Using the existing project curvature-bias budget `0.01` gives a conservative settling voltage envelope

`V_settle = 0.01 / ||w||_1 = 69.536914 microvolt`.

For an explicitly synthetic first-order transient with full-span `n=1` 300 K step amplitude `0.0953649108583 V`,

`t_min = tau ln(DeltaV/V_settle)`.

Sensitivity:
- tau=0.5 s -> 3.6118 s;
- tau=1 s -> 7.2236 s;
- tau=2 s -> 14.4472 s;
- tau=5 s -> 36.1180 s;
- tau=10 s -> 72.2361 s.

These are planning values only, not measured R2 dynamics.

## Primary analysis choice

The PASS gate is deliberately nonparametric. For each elapsed time, the repeated-step mean is compared with the late plateau and expanded by a 95% normal uncertainty envelope. The dwell is the first sampled time for which **all subsequent points** remain inside the voltage limit. A final-window slope guard rejects unresolved tails.

The single-exponential fit is diagnostic only. It cannot extrapolate a failed observation window into a pass.

## Independent / adversarial checks

The committed test suite requires:
- numerical and analytic curvature sensitivity agreement;
- a synthetic tau=2 s step cannot qualify before the analytic 14.4472 s limiting dwell;
- five step replicates -> `INCOMPLETE`;
- an injected 80 s slow tail -> `FAIL` inside the 48 s window;
- constant absolute `Voc` offset leaves dwell unchanged.

## Statistical independence

Elapsed-time points are repeated observations within a transient, not independent devices. Step replicates are the repeat units for the settling estimate. This does not increase independent substrate count for any R2 mechanism claim.

## Null explanations

Ordinary source regulation, detector bandwidth, SMU filtering/autorange, device capacitance, traps/photodoping, thermal evolution, contacts, spectral changes, and degradation remain live explanations for any transient.

## Safety

No new material or fabrication step. Large illumination jumps must stay within source interlocks, thermal limits, safe slew/dwell constraints, and DUT degradation limits. Randomization or qualification never overrides facility SOP.

## Corrections / superseded interpretation

No merged numerical result is corrected. Interpretation is narrowed: randomized acquisition order is not sufficient by itself if the randomization induces unresolved step transients. v3.24 should be considered confirmatory only after settling is qualified under the same acquisition configuration.

## Unresolved risks

- real response may be multi-timescale, nonstationary, or direction/history dependent;
- the plateau estimator can be biased if the acquisition window is too short;
- timestamp latency and instrument filtering need explicit real-facility provenance;
- the 69.5 microvolt envelope is conservative and may demand more repeat averaging than practical;
- a calibrated finite-sample confidence procedure for the envelope is not yet established.

## Single best next increment

At the first cooperating facility, collect repeated large-step transients under the exact intended R2 configuration and run v3.25 unchanged. If a practical dwell passes, use at least that dwell in the v3.24 randomized schedule. If it does not, characterize the dynamic state model before interpreting randomized curvature.
