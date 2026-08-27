# Research session — R2 facility time budget v3.32

Date: 2026-08-27

## Why this increment

The merged program already defines facility capabilities, evidence roles, direct-confirmation questions, dry-run packet semantics, calibration repeatability, temporal-fidelity, settling, spectral, and randomized-order requirements. The uncovered deployment gap is a reproducible translation from those protocols into instrument/handling hours for a facility quote or scheduling discussion.

No open automation PR contained a facility-time planner. Open PR #7 was reviewed and is superseded calibration-analysis provenance; canonical calibration authority remains the merged implementation recorded by v3.31.

## What changed

Added:

- `models/r2_facility_time_planner_v3_32.py`
- `models/fixtures/r2_facility_time_scenarios_v3_32.csv`
- `technical/data/r2_facility_time_input_template_v3_32.csv`
- `technical/r2-facility-time-budget-v3.32.md`
- `research/evidence/r2-facility-time-budget-v3.32.md`
- `research/sessions/2026-08-27-r2-facility-time-budget-v3.32.md`
- `venture/v3.32-facility-time-quote-decision.md`
- `.github/workflows/r2-facility-time-budget.yml`

## Claim classes

**Established repository evidence:** merged protocols contain the structural acquisition counts cited in the technical note.

**Engineering assumptions:** all low/nominal/high seconds-per-operation values and the 34-point monotonic scheduler placeholder.

**Synthetic/model result:** low/nominal/high total modeled burden = 2.9306 / 7.1906 / 19.9733 h; reference-repeatability share = 45.5 / 53.8 / 63.4%.

**Falsifiable hypothesis:** a real facility can populate the same timing template under one frozen configuration and execute every required v3.27 role without silently dropping prerequisites.

**Experimental result:** none.

**Novel invention concept:** none.

## Verification

The planner derives time from explicit count × duration equations. Dimensional analysis yields seconds term-by-term and hours after conversion.

Independent structural checks:

- 30×4×17 = 2040 calibration grid records;
- 30×4×4 = 480 calibration auxiliary records;
- 4×17 = 68 randomized-order observations;
- 2×6×10 = 120 optical settling observations.

The self-test freezes scenario totals to 1e-12 h, verifies strict low < nominal < high ordering, and requires calibration to exceed 50% of nominal modeled burden. CI separately recomputes totals from the CSV without calling the planner.

No stochastic code is used, so seed/convergence checks do not apply.

## Negative/useful boundary

Calibration does **not** dominate the low synthetic scenario: its share is 45.5%. Therefore the repo should not claim that repeatability necessarily dominates every facility schedule. The narrower decision is that repeatability dominates the nominal/high examples and is sufficiently multiplied by protocol counts that it deserves an explicit quote line item.

## Statistical integrity

Measurement counts are scheduling multipliers, not independent scientific sample sizes. Existing hierarchy and prospective holdout rules are unchanged.

## Unresolved risks

- facility timing values are not yet measured or quoted;
- qualified settling dwell may exceed the example values;
- spectral/integration timing may depend strongly on SNR and hardware;
- warm-up, stabilization, queueing, staffing, shipping, troubleshooting, and EHS/legal overhead are incomplete unless explicitly supplied;
- a failed gate can require repetition or redesign and is not represented as a universal contingency percentage;
- real facility responses may reveal missing timing categories requiring a versioned schema extension.

## Next increment

Obtain one dated facility response using the frozen confirmation protocol plus v3.32 timing template, replace synthetic timing assumptions with facility-provided values, and regenerate the model unchanged before scheduling or comparing service cost.
