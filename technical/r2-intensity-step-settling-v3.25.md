# R2 v3.25 — intensity-step settling qualification

## Status and claim boundary

This is a **prospective engineering/metrology protocol**. It does not contain real R2 settling data and does not establish any recombination, EPC, open-quantum, or device-performance claim.

The purpose is narrower: before the v3.24 randomized-order `Voc`-intensity discriminator is used, qualify a dwell time after intensity changes such that unresolved step transients are bounded relative to the already frozen curvature-bias scale.

## Why this increment exists

IEC TR 63228:2019 identifies transient response to external stimulus and instability with time as measurement challenges for emerging PV technologies including OPV. NIST measurement terminology defines response/settling time by entry into and continued residence within specified limits around the final steady value. These references support the measurement principle; they do not imply that R2 has any particular response time.

Sources checked 2026-08-27:
- IEC TR 63228:2019: https://webstore.iec.ch/en/publication/64040
- NIST Technical Note 1551 glossary, response-time definition: https://www.nist.gov/document/nist-tn-1551pdf
- NIST step-response/transient-measurement precedent: https://www.nist.gov/publications/characterizing-transient-measurements-use-step-response-and-convolution-integral

## Frozen measurand and voltage envelope

The R2 curvature observable remains

`n_id(Phi) = [dVoc/d ln(Phi)] / (k_B T/q)`

and

`Delta_n_curv = n_id(~1 sun) - n_id(~0.1 sun)`.

For the frozen 17-point geometric grid from 0.05 to 2 sun and the frozen 7-point local quadratic derivative, let `w_i` be the linear weights that map point-level voltage errors to curvature error:

`delta Delta_n_curv = sum_i w_i delta V_i`.

The executable calculates

`||w||_1 = 143.8085097637075 V^-1`.

An independent analytic derivation exists because the grid is equally spaced in `x=ln(Phi)`. For a symmetric 7-point quadratic derivative, the slope weights are

`j / (28 h)`, `j=-3,-2,-1,0,1,2,3`,

where

`h = ln(2/0.05)/16`.

The low- and high-intensity derivative windows are disjoint, so

`||w||_1 = 2 sum(|j|) / [28 h (k_B T/q)] = 6/[7 h (k_B T/q)]`.

At `T=300 K`, this independently gives the same `143.8085097637075 V^-1` to the frozen `1e-10` tolerance.

The inherited project curvature-bias budget is

`B_curv = 0.01` dimensionless.

A conservative pointwise settling envelope is therefore

`V_settle = B_curv / ||w||_1 = 6.953691416753467e-05 V = 69.5369 uV`.

Dimensional check: dimensionless divided by `V^-1` gives volts.

This is a project-derived engineering tolerance, not an IEC/NIST limit.

## Acquisition protocol

Before randomized-order curvature acquisition, collect repeated transients for the intensity jumps most likely to stress settling. Minimum initial qualification:

- at least 6 independent **step replicates** per step class;
- both large-step directions, nominally `0.05 -> 2 sun` and `2 -> 0.05 sun`;
- elapsed-time samples spanning the unresolved transient and a visibly late plateau;
- recommended planning grid: `0.25, 0.5, 1, 2, 4, 8, 16, 24, 32, 48 s`;
- identical source, detector, range/gain, contact, temperature, spectral, and DUT configuration to the intended R2 measurement;
- preserve every acquired row except preregistered QC failures.

If facility constraints require a different time grid, the exact elapsed times must be exported; the analysis does not assume uniform sampling.

The statistical hierarchy is

`lot -> substrate -> pixel -> session -> step class -> step replicate -> elapsed-time sample`.

Elapsed-time samples within one transient are not independent devices or independent calibration sessions.

## Primary nonparametric gate

For each step class and elapsed time, pool the replicate `Voc` observations. The final plateau is the mean of all replicate observations at the last three elapsed-time points.

For each time `t`, calculate

`D(t) = |mean[V(t)] - V_plateau| + 1.959964 * u_diff(t)`,

where `u_diff` is the standard uncertainty of the difference formed from the replicate SEM at `t` and the plateau SEM.

The qualified dwell is the earliest sampled time `t*` such that

`D(t) <= V_settle`

for `t` and **every later sampled time**.

This is deliberately stricter than declaring the first crossing to be settled.

A late-window trend guard also requires the absolute fitted voltage change across the final three time points to be no more than `0.5 V_settle`. A long unresolved tail therefore cannot qualify solely because the last points happen to be close together under noise.

If the data do not demonstrate settlement inside the measurement window, the result is `FAIL`; the tool does not extrapolate a passing dwell from an assumed exponential model.

## Diagnostic exponential model and independent check

A single-exponential time constant is reported only as a diagnostic. It does not control `PASS`.

For a true first-order transient

`|delta V(t)| = |Delta V| exp(-t/tau)`,

the analytic minimum dwell for the same voltage envelope is

`t_min = tau ln(|Delta V|/V_settle)`.

For the deliberately conservative synthetic step amplitude

`|Delta V| = (k_B T/q) ln(2/0.05) = 0.0953649108583 V`

at `T=300 K`, the planning sensitivity is:

| tau (s) | analytic minimum dwell (s) |
|---:|---:|
| 0.5 | 3.6118 |
| 1 | 7.2236 |
| 2 | 14.4472 |
| 5 | 36.1180 |
| 10 | 72.2361 |

These are synthetic limiting-case calculations, not measured response times.

The conservative 0.0954 V amplitude corresponds to an `n=1` idealized `Voc` difference across the full 0.05–2 sun span and is used only for sensitivity. Real step amplitudes are measured, not assumed.

## Limiting cases and adversarial checks

The committed test suite enforces:

1. numerical curvature-weight L1 norm agrees with the separate geometric-grid analytic derivation within `1e-10`;
2. the `tau=2 s` first-order synthetic limiting case cannot qualify earlier than the independent analytic `14.4472 s` dwell;
3. fewer than 6 step replicates returns `INCOMPLETE`;
4. a deliberately injected slow 80 s tail returns `FAIL` inside the frozen 48 s observation window;
5. adding a constant voltage offset to every transient sample leaves the qualified dwell unchanged.

The last test is a sign/normalization check: settling depends on transient deviation from the plateau, not absolute `Voc` level.

## Uncertainty and sensitivity

The principal uncertainty is empirical replicate scatter at each elapsed time plus uncertainty of the late plateau mean. These enter the 95% upper envelope directly.

Systematic terms that do not average away include:
- source switching latency;
- timestamp alignment error;
- detector/SMU bandwidth and autorange behavior;
- temperature evolution;
- spectral changes during/after a step;
- DUT photodoping, trapping, degradation, or hysteresis;
- contact/electronics relaxation.

The tool therefore does not interpret a fitted `tau` as a material constant. It qualifies the **whole declared acquisition path**.

The sensitivity table `models/fixtures/r2_settling_sensitivity_v3_25.csv` shows that required dwell scales linearly with `tau` under the first-order limiting model. A factor-of-two error in the dominant time constant therefore changes dwell by a factor of two; this is why v3.25 uses observed envelope settlement rather than extrapolation as the primary gate.

## Null and conventional explanations

A measured transient can be produced by ordinary source regulation, lamp/LED heating, detector response, SMU filtering/autorange, device capacitance, trap filling, photodoping, contact equilibration, thermal evolution, or irreversible degradation. None of these is quantum-mechanism evidence.

The immediate discriminator is **history dependence under controlled repeated steps**. If step transients do not settle within a practical acquisition window, the randomized-order experiment must be redesigned around the observed dynamics rather than interpreted as a static `Voc(Phi)` curve.

## Exclusions / QC

Permitted exclusions must be frozen before analysis and limited to acquisition failures such as:
- missing or invalid timestamp;
- source/interlock fault;
- detector/SMU overrange or saturation;
- recorded configuration mismatch;
- missing required replicate/timepoint;
- explicit instrument interruption.

Large or slow transients, unfavorable late drift, or failure to settle are **not** exclusion reasons.

## Safety / environmental considerations

No new fabrication chemistry is introduced. Qualification must remain within device/source safe operating limits. Large randomized illumination steps must respect facility optical/electrical interlocks, source slew limitations, thermal limits, and degradation constraints. If the stress step itself damages the device, that is a failed/invalid qualification design and must be recorded, not hidden.

## Release gate

Do not use v3.24 randomized-order data as confirmatory curvature evidence unless:

- every required step class is `PASS` under v3.25;
- the randomized-order dwell is at least the maximum qualified dwell across required classes;
- the exact source/configuration matches the settling qualification;
- no later drift/spectral/temperature gate invalidates the qualification.

If a real facility requires dwell longer than practical, narrow the experiment to a dynamic/history-dependent measurement problem and characterize the time response before mechanism inference.
