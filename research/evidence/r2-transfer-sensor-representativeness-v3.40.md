# Evidence record — R2 transfer-sensor representativeness v3.40

Date: 2026-08-27

## Evidence class

This increment is an **engineering protocol with synthetic software fixtures**. No real logger, dummy, carrier, package, device, facility, or shipping route is claimed to pass.

## Established internal dependencies

- v3.38 requires transfer environmental logging but explicitly leaves device-local representativeness unresolved.
- v3.39 qualifies temporal response/bandwidth and explicitly lists package-to-dummy gradients and sensor placement as remaining systematic risks.
- The repository calculation protocol requires correlated/systematic uncertainty to be treated separately from repeatability and forbids converting technical repeats into independent experimental samples.

## New falsifiable engineering claim

For a fixed tested package geometry, paired logger/reference measurements can bound the logger-to-dummy-location disagreement using

`E_channel = max_i(|y_ref,i-y_logger,i| + u_e,i)`

with

`u_e,i = sqrt(u_ref,i^2 + u_logger,i^2 - 2 rho_i u_ref,i u_logger,i)`.

A prospective engineering threshold is required before the result can be classified as qualified. No threshold is inferred from the data and no safe shipping limit is supplied by this increment.

## Independent/limiting checks

For equal uncertainties of 0.1 channel units:

- `rho=-1` gives `u_e=0.2`, independently from the algebraic identity `sqrt((u_ref+u_logger)^2)`;
- `rho=+1` gives zero for equal perfectly common-mode uncertainties;
- the synthetic pass fixture yields `0.6+0.2=0.8`;
- the synthetic fail fixture yields `0.9+0.2=1.1`.

Software tolerance: `1e-12` channel units for these exact fixtures.

## Uncertainty and sensitivity

Correlation is a decision-driving systematic. If it is not justified, the qualification gate uses `rho=-1`, which maximizes difference uncertainty for fixed nonnegative component uncertainties. Sensitivity is required at `rho=-1,0,+1` where meaningful.

No stochastic seed is required because the v3.40 validator is deterministic. Runtime target is Python standard library on Python 3.12–3.14.

## Statistical independence

The required minimum is 3 separately executed controlled runs per channel and transient direction. Samples within a run are correlated technical observations. This protocol does not increase substrate sample size and does not create experimental evidence about R2 device performance.

## Conventional/null explanations

Ordinary package physics can create disagreement: thermal/RH gradients, airflow shielding, sensor contact/self-heating, calibration offset, time misalignment, chamber nonuniformity, and multi-time-constant response. A disagreement is not evidence of a novel device mechanism.

## Claim narrowing

A v3.39 bandwidth pass alone is insufficient to say that a transfer logger represents the device-local environment. The logger can be temporally faithful and spatially unrepresentative. v3.40 makes that negative boundary explicit and testable.
