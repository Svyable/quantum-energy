# R2 facility instrument-time budget v3.32

## Purpose and claim boundary

This increment converts the merged R2 metrology protocols into a **parametric facility instrument-time planner** for scheduling, RFQ scoping, and partner discussions.

It does **not** contain a vendor quote, measured facility throughput, a commitment from any laboratory, or a scientific result. Every seconds-per-operation value in the frozen scenario CSV is an explicit **synthetic planning assumption** and must be replaced by a facility's actual configuration-dependent timing before contracting or scheduling.

The output is intended to answer a narrow operational question: given the already frozen protocol counts and an explicit set of timing assumptions, how much instrument/handling time is implied, and which protocol block dominates that burden?

## Provenance

Canonical merged inputs checked 2026-08-27:

- `technical/r2-reference-repeatability-campaign-v3.20.md`
- `technical/r2-order-drift-discriminator-v3.24.md`
- `technical/r2-intensity-step-settling-v3.25.md`
- `technical/r2-instrument-temporal-fidelity-v3.26.md`
- `technical/data/r2_facility_capability_contract_v3_27.json`
- `technical/r2-facility-confirmation-protocol-v3.29.md`
- `technical/r2-facility-dryrun-packet-v3.30.md`
- `machine/analysis-registry.json`

Open automation PR #7 was also reviewed. It is superseded-analysis provenance and does not change the facility-time calculation. No overlapping open facility-time planner was found.

## Frozen structural inputs

These counts come from merged protocols rather than timing assumptions:

### Reference repeatability v3.20

- 30 sessions = 24 training + 6 untouched prospective holdout sessions;
- 4 sweeps/session;
- 17 grid points/sweep;
- 4 auxiliary acquisitions/sweep: pre-dark, pre-anchor, post-anchor, post-dark.

Therefore:

`N_grid = 30 * 4 * 17 = 2040`

`N_aux = 30 * 4 * 4 = 480`

and total calibration records before session-level overhead are

`N_cal = 2520`.

These records are technical measurements. They are not 2520 independent sessions.

### Instrument temporal fidelity v3.26

Minimum repeated electrical reference steps:

`N_inst_rep = 6`.

The number of elapsed-time samples per replicate is not standards-derived or fixed by v3.26, so v3.32 keeps it as an explicit planning input.

### Optical/DUT settling v3.25

Minimum initial qualification uses:

- 2 large-step directions;
- 6 replicates/direction;
- the recommended 10-point elapsed-time planning grid.

Thus the nominal structural sample count is

`N_opt = 2 * 6 * 10 = 120` elapsed-time observations.

If a facility uses a different time grid, the input must be changed rather than silently retaining 120.

### Randomized-order acquisition v3.24

The frozen design is

`N_rand = 4 blocks * 17 intensities = 68` voltage observations.

The input template also contains `monotonic_points`, set to 34 in all three example scenarios as an explicit planning assumption representing two 17-point monotonic passes. This value is **not** promoted to a merged protocol requirement by v3.32; a real facility plan must replace it if the executed monotonic sequence differs.

## Governing time model

All quantities below are seconds unless otherwise stated.

Let:

- `t_g` = acquisition time per calibration grid point;
- `t_a` = acquisition time per calibration auxiliary point;
- `t_sess` = non-point session overhead;
- `n_it` = electrical-step samples/replicate;
- `t_it` = electrical-step acquisition time/sample;
- `t_ir` = electrical-step replicate overhead;
- `t_ot` = optical-step acquisition time/sample;
- `t_or` = optical-step replicate overhead;
- `N_m` = monotonic Voc points;
- `N_r` = randomized Voc points;
- `t_v` = voltage read time/point;
- `t_d` = qualified settling dwell applied before each randomized observation in this conservative scheduler;
- `N_spec` = source spectral intensity states;
- `t_spec` = time/spectral state;
- `t_spec0` = spectral setup overhead;
- `t_lin` = detector/source linearity characterization allocation;
- `t_admin` = packet/configuration/provenance administration allocation.

The component times are:

`T_cal = 2040 t_g + 480 t_a + 30 t_sess`

`T_inst = 6 (n_it t_it + t_ir)`

`T_opt = 12 (10 t_ot + t_or)`

`T_voc = N_m t_v + N_r (t_v + t_d)`

`T_spec = t_spec0 + N_spec t_spec`

and

`T_total = T_cal + T_inst + T_opt + T_voc + T_spec + t_lin + t_admin`.

Dimensional check: every multiplicative count is dimensionless and every term has units seconds. Division by 3600 converts seconds to hours.

## Frozen synthetic planning scenarios

Input: `technical/data/r2_facility_time_input_template_v3_32.csv`.

Output: `models/fixtures/r2_facility_time_scenarios_v3_32.csv`.

The three scenarios are deliberately broad stress cases, not confidence intervals:

| scenario | total planning time | reference-repeatability share |
| --- | ---: | ---: |
| low | 2.9306 h | 45.5% |
| nominal | 7.1906 h | 53.8% |
| high | 19.9733 h | 63.4% |

These totals exclude facility queueing, staff availability, sample shipping, temperature stabilization not represented by the supplied timing fields, reruns after failures, troubleshooting, safety review, contract/legal work, and any measurement block not explicitly parameterized. They therefore must not be described as a complete project-duration estimate.

### Decision implication

Across this intentionally broad timing sweep, the reference-repeatability campaign grows from 45.5% to 63.4% of modeled burden and exceeds half of the nominal total. The operational decision is therefore stable for the nominal/high planning cases: facility discussions should quote the repeatability campaign explicitly rather than burying it inside a generic measurement-day request.

The low scenario is a useful counterexample: under aggressive per-point timing assumptions, calibration falls below half of total modeled burden. Therefore v3.32 does **not** claim that repeatability must dominate every real facility schedule.

## Independent verification

Primary implementation:

`models/r2_facility_time_planner_v3_32.py`.

Independent count derivations are hard-coded separately in the self-test rather than read back from the calculator's intermediate values:

- `30 * 4 * 17 = 2040` grid records;
- `30 * 4 * (2 + 2) = 480` auxiliary records;
- `4 * 17 = 68` randomized measurements;
- `2 * 6 * 10 = 120` optical-step observations.

The self-test requires the frozen low/nominal/high total hours to agree with the independently precomputed CSV values within `1e-12 h`, requires strict scenario ordering, and checks that the repeatability share exceeds 50% in the nominal scenario.

CI additionally recomputes the same totals from CSV using a separate inline Python implementation that does not call the primary planner.

No randomness is used, so seed/convergence/Monte Carlo checks do not apply.

## Uncertainty and sensitivity

The v3.32 output is a deterministic function of uncertain planning inputs. It is therefore an engineering sensitivity envelope, not a probabilistic uncertainty interval.

Material correlated/systematic scheduling terms include:

- facility warm-up and stabilization policy;
- source switching and qualified dwell;
- spectrometer integration/averaging requirements;
- manual sample mounting/remounting;
- calibration-certificate review and configuration freeze;
- failed QC requiring a repeat session;
- facility operating-hour restrictions and staff coverage;
- equipment-sharing/queue delays.

These terms should be represented explicitly when a candidate facility responds. They must not be folded into an unexplained contingency percentage if they are known.

The largest modeled sensitivity is per-point/per-session timing in the 30-session calibration campaign because it is multiplied across 2520 records plus 30 session overheads.

## Statistical independence

Time burden and evidence count are separate concepts. The 2040 calibration grid points, 480 auxiliary records, 120 settling samples, and 68 randomized observations do not increase independent device or session sample size merely because they consume instrument time.

The inherited hierarchy remains:

`lot -> substrate -> device/pixel -> session -> sweep or step replicate -> measurement`.

For a future multi-facility transfer study, facility/configuration must be an explicit grouping level.

## Conventional/null explanation

A long or expensive campaign can arise entirely from ordinary metrology requirements—stabilization, repeatability, traceability, spectral characterization, or export/provenance overhead. High time burden is not evidence that the underlying device physics is complex or quantum.

Conversely, a very fast quoted campaign may simply omit a prerequisite. The discriminator is role-by-role mapping against the v3.27 contract and unchanged execution dependencies, not headline instrument hours.

## Kill / narrow rules

- If a quote omits a required v3.27 capability or packet role, mark the facility plan `INCOMPLETE` regardless of low price/time.
- If a facility changes the 24+6 prospective split, do not call the result a v3.20 prospective holdout.
- If a facility cannot preserve the qualified settling dwell in randomized acquisition, do not call the v3.24 result confirmatory.
- If real timing differs materially from a frozen scenario, replace the planning row and regenerate outputs; do not defend the old estimate.
- Do not use v3.32 hours as a vendor quote, committed schedule, or scientific evidence.

## Safety and environmental considerations

Shortening the schedule is never a reason to bypass optical/electrical interlocks, source-duty limits, temperature limits, instrument ratings, required warm-up, or safe handling. The planner intentionally treats safety-controlled delays as facility inputs rather than optimization targets.

## Single best next increment

Send the v3.29 confirmation package together with this v3.32 input template to the first responding facility and request its configuration-specific timing values for every row. Commit the returned timing assumptions with dated provenance, regenerate the quote model unchanged, and compare candidate facilities on **complete protocol hours**, not on partial service-line prices.
