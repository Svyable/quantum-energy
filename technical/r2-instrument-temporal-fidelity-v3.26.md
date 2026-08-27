# R2 instrument-chain temporal fidelity gate v3.26

## Purpose

The R2 program now has open work for randomized acquisition order and DUT/source intensity-step settling. v3.26 isolates a different conventional confound: **the electrical acquisition chain itself can add lag, timestamp error, filtering, aperture averaging, range changes, or autorange transients that manufacture or hide apparent settling**.

A v3.26 `PASS` qualifies only the declared electrical measurement configuration. It does not qualify source regulation, DUT state dynamics, or any recombination/EPC/open-quantum mechanism.

## Evidence basis

Established metrology principle, checked 2026-08-27:

- NIST pulse-calibration work determines sampler step response, corrects timebase errors, and uses deconvolution/reference waveforms to estimate impulse/step/frequency response and associated uncertainty.
- NIST high-speed pulse measurement guidance notes that accurate transition-duration/amplitude/overshoot measurements require calibration of relevant measurement-system variables.
- A 2024 NIST digitizer study explicitly evaluated different input-filter settings and aperture choice, demonstrating that filter/aperture configuration belongs in a digitizer measurement contract.

These sources support characterization of measurement-chain temporal response. They do not establish any R2 instrument performance.

## Input contract

Raw CSV hierarchy:

`electrical step -> replicate -> elapsed-time sample`.

Required fields:

`replicate_id, elapsed_s, commanded_V, measured_V, timestamp_u_s, reference_step_u_V, range_id, filter_id, aperture_s, autorange_enabled, qc_status`.

The range, digital/analog filter ID, and aperture must remain fixed. Autorange is prohibited in the qualification data because a range transition is itself a configuration change/transient.

## Primary decision rule

At elapsed time `t`, define residual

`r_j(t) = V_meas,j(t) - V_cmd(t)`.

For the replicate mean `rbar(t)`, the standard uncertainty is

`u^2(t) = u_rep^2 + u_ref^2 + [|d rbar/dt| u_t]^2`,

where:

- `u_rep` is replicate SEM [V];
- `u_ref` is standard uncertainty of the characterized reference step [V];
- `u_t` is timestamp standard uncertainty [s];
- `d rbar/dt` is the local residual slope [V/s].

Dimensional check: `(V/s)*s = V`; every term inside the variance sum has units `V^2`.

The conservative upper residual is

`R95(t) = |rbar(t)| + 1.959964 u(t)`.

The instrument qualifies at the earliest sampled time for which `R95(t)` is below the instrument allocation at that time **and all later sampled times**. Model extrapolation cannot turn an unobserved tail into `PASS`.

## Budget allocation

Open v3.25 work independently derives a total pointwise settling envelope of

`V_settle = 69.5369142 uV`

from the frozen curvature estimator and a project curvature-bias budget of 0.01.

v3.26 provisionally allocates 20% of that envelope to electrical-instrument temporal error:

`V_inst = 0.20 V_settle = 13.9073828 uV`.

The 20% split is an **engineering assumption**, not a NIST/IEC limit. It keeps instrument-chain lag from consuming most of the total settling budget while leaving 80% for source/DUT/path dynamics. If v3.25 changes during review, this dependent allocation must be recomputed.

## Independent limiting-case derivation

For a first-order acquisition path with step amplitude `A`, delay `d`, and time constant `tau`,

`|r(t)| = A exp[-(t-d)/tau]`, for `t>=d`.

Solving `|r(t)| <= V_inst` gives

`t_min = d + tau ln(A/V_inst)`.

For the deliberately synthetic limiting case `A=0.100 V`, `d=0`, the dwell sensitivity is:

- `tau=0.05 s` -> `0.363553 s`;
- `tau=0.10 s` -> `0.727107 s`;
- `tau=0.20 s` -> `1.454214 s`;
- `tau=0.50 s` -> `3.635534 s`;
- `tau=1.00 s` -> `7.271068 s`;
- `tau=2.00 s` -> `14.542135 s`.

These are synthetic planning values, not measured hardware response times.

The adversarial test uses `tau=0.2 s`, `d=0.05 s`, so the independent analytic lower bound is `1.5032424658 s`. The sampled nonparametric gate may qualify later, never earlier.

## Verification and limiting cases

The committed test suite requires:

1. the independent first-order dwell equation reproduces the frozen analytic value within `1e-12 s`;
2. an 8-replicate synthetic `tau=0.2 s` path cannot qualify earlier than the analytic bound;
3. a `tau=2 s` path fails within the frozen 3 s observation window;
4. fewer than six replicates gives `INCOMPLETE`;
5. any autorange-enabled qualification run gives `FAIL`;
6. an ideal zero-residual path qualifies at the first sample;
7. the diagnostic exponential fit recovers the injected `tau` within 2%, but the fit is never used as the PASS criterion.

Synthetic RNG seed: `20260827`. Python standard library only.

## Uncertainty and correlated terms

This gate explicitly includes repeat noise, reference-step uncertainty, and timestamp uncertainty coupled through local slope. It does **not** automatically include:

- reference generator waveform uncertainty beyond the supplied scalar term;
- correlated digitizer gain/offset uncertainty;
- cable/fixture impedance or capacitance;
- trigger-distribution skew;
- firmware buffering latency;
- source-measure compliance transitions;
- filter impulse-response uncertainty.

Any material omitted term keeps the qualification claim narrower or requires an enriched uncertainty model.

## Statistical independence

Time samples within one transient are correlated. Replicates are technical repeat units for instrument qualification, not independent substrates/devices. No `sqrt(N)` credit is transferred into DUT sample size.

## Null/conventional explanation

A slow measured intensity-step transient can be produced entirely by acquisition electronics even if source and DUT are instantaneous. Conversely, filtering can suppress a real fast overshoot and make the response look cleaner than it is. The discriminator is a characterized electrical reference step injected through the exact acquisition configuration with the DUT/source temporal physics bypassed.

## Safety and practical execution

Use a traceable/characterized low-voltage step source compatible with the instrument input range. Do not exceed SMU/digitizer input ratings or bypass protective interlocks. Lock range, aperture, filtering, sample cadence, triggering, cabling, and firmware/software version for the qualification and subsequent R2 measurement.

## Kill / narrow gates

- no fixed range/filter/aperture -> `FAIL`;
- autorange enabled -> `FAIL`;
- insufficient replicate/time coverage -> `INCOMPLETE`;
- upper residual never enters the allocated envelope within the observed window -> `FAIL`;
- uncharacterized reference-step or timestamp uncertainty -> measurement claim remains `INCOMPLETE`;
- configuration change after qualification -> requalify.

## Single best next experiment

Inject a characterized ~100 mV electrical step through the exact SMU/digitizer/cabling/software path intended for R2, with fixed range/filter/aperture and autorange disabled. Measure at least six repeated transients on a time grid extending beyond the intended DUT dwell. Run v3.26 unchanged before interpreting any slow optical-step response as DUT/source physics.
