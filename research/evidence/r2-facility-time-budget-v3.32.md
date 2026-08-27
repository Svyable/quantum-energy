# Evidence note — R2 facility time budget v3.32

Date: 2026-08-27

## Evidence class

This increment contains **engineering planning assumptions and deterministic model outputs only**. It adds no experimental device result, facility capability confirmation, vendor quote, facility throughput measurement, electron–phonon coupling evidence, open-quantum mechanism evidence, or commercial PV performance claim.

## Repository provenance

Decision-driving structural counts were taken from merged project artifacts:

- `technical/r2-reference-repeatability-campaign-v3.20.md`: 30 sessions, 4 sweeps/session, 17 grid points/sweep, 4 auxiliary acquisitions/sweep.
- `technical/r2-order-drift-discriminator-v3.24.md`: 4 randomized blocks × 17 intensity settings = 68 observations.
- `technical/r2-intensity-step-settling-v3.25.md`: two large-step directions, at least 6 step replicates/direction, recommended 10-point elapsed-time planning grid.
- `technical/r2-instrument-temporal-fidelity-v3.26.md`: at least 6 electrical-step replicates; elapsed-time sampling remains configuration dependent.
- `technical/data/r2_facility_capability_contract_v3_27.json`: required capability/evidence contract and execution dependency graph.
- `technical/r2-facility-confirmation-protocol-v3.29.md`: direct facility confirmation remains required.
- `technical/r2-facility-dryrun-packet-v3.30.md`: structural packet success is not scientific success.
- `machine/analysis-registry.json`: canonical merged v3.19 calibration estimator authority.

Open PR #7 was read and is not used as a second canonical analysis path.

## Synthetic timing inputs

All seconds-per-operation values in `technical/data/r2_facility_time_input_template_v3_32.csv` are synthetic planning assumptions created 2026-08-27 for sensitivity analysis. They have zero vendor/facility provenance and must be replaced when real facility information is obtained.

The example monotonic point count of 34 is likewise a scheduler assumption representing two 17-point passes; it is not asserted as a new canonical acquisition requirement.

## Deterministic model outputs

The low/nominal/high synthetic planning totals are 2.9306 / 7.1906 / 19.9733 hours. These are not confidence intervals or commitments.

Reference-repeatability campaign share is 45.5 / 53.8 / 63.4% respectively. Thus the statement that calibration dominates the burden is conditional: it holds in nominal/high scenarios but not in the low scenario.

## Independent checks

- record counts are independently derived from protocol hierarchy factors;
- primary planner self-test freezes expected total hours to `1e-12 h`;
- CI recomputes totals with a separate inline implementation;
- units reduce to seconds for each additive term, then hours after division by 3600;
- no stochastic process is used.

## Conventional explanation / claim boundary

Facility time burden is ordinary metrology/logistics burden. It cannot be used as evidence for unusual or quantum device physics. A fast quote may instead signal omitted prerequisites; a slow quote may reflect proper traceability/stabilization. Completeness against v3.27 is the discriminator.
