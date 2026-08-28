# Research session — v3.40 transfer-sensor representativeness

Date: 2026-08-27

## Increment

Added a prospective dummy-package test that bounds whether the environmental logger used for R2 transfer actually represents the dummy/device location. This is deliberately downstream of v3.39 temporal-bandwidth qualification and upstream of any qualified-primary travel.

## Why this increment

The current program had already recognized package-to-dummy gradients as an unresolved systematic. A time-complete and bandwidth-qualified logger can still produce misleading transfer evidence if its placement sees materially different conditions from the device plane. That conventional explanation must be bounded before cross-facility disagreement is interpreted scientifically.

## Quantitative model

For each paired logger/reference observation:

`e_i = y_ref,i - y_logger,i`

and

`u_e,i = sqrt(u_ref,i^2 + u_logger,i^2 - 2 rho_i u_ref,i u_logger,i)`.

The conservative channel statistic is

`E_channel = max_i(|e_i| + u_e,i)`.

All quantities retain the channel unit; `rho` is dimensionless. If correlation is undeclared, the decision gate uses `rho=-1`, giving the worst-case `u_e=u_ref+u_logger` for fixed nonnegative component uncertainties.

No physical acceptance threshold is invented. Temperature/RH thresholds are null by default and must be declared prospectively with provenance. Missing thresholds produce `INCOMPLETE`.

## Verification

Synthetic arithmetic fixtures only:

- with `|e|max=0.6`, `u_ref=u_logger=0.1`, unknown correlation -> `rho=-1`, `E=0.8`;
- with `|e|max=0.9` under the same uncertainties, `E=1.1`;
- equal 0.1 uncertainties with `rho=+1` give the common-mode limiting case `u_e=0`;
- monotonic sensitivity across `rho=-1,0,+1` is checked.

Predeclared arithmetic tolerance: `1e-12` channel units. Deterministic standard-library code; no stochastic seed.

## Independence / exclusions

Require at least 3 separately executed controlled runs per channel and transient direction. Samples within one transient are correlated technical observations and do not increase independent sample count. All functional runs remain in the record unless a frozen QC rule excludes them with reason.

## Conventional explanations retained

Package thermal/RH gradients, airflow shielding, sensor contact/self-heating, chamber spatial nonuniformity, calibration offset/drift, timing mismatch, multi-time-constant package response, and reference-sensor perturbation remain valid conventional causes of disagreement.

## Negative result preserved

A v3.39 bandwidth qualification does not establish spatial representativeness. Temporal fidelity and placement representativeness are separate gates.

## Files added

- `machine/r2_transfer_representativeness_v3_40.json`
- `research/templates/r2_transfer_representativeness_raw_v3_40.csv`
- `models/r2_transfer_representativeness_v3_40.py`
- `technical/r2-transfer-sensor-representativeness-v3.40.md`
- `research/evidence/r2-transfer-sensor-representativeness-v3.40.md`
- `research/sessions/2026-08-27-transfer-sensor-representativeness-v3.40.md`
- `venture/v3.40-transfer-representativeness-gate.md`
- `.github/workflows/r2-transfer-representativeness.yml`

## Unresolved risks

Threshold provenance is still absent; reference-sensor placement may perturb the package; real package response may depend on orientation, airflow, route, carrier loading, or transient amplitude; calibration covariance may not be captured by a scalar rho; ESD, light exposure, particles, and mechanical contact changes remain separate transfer confounds.

## Best next increment

Execute v3.39 and v3.40 together on one dimensionally representative dummy package against calibrated faster/device-adjacent references. Preserve all raw runs and use the measured bandwidth and placement-gradient evidence to freeze the transfer logger configuration before any qualified R2 primary travels.
