# Research session — R2 shipping-control discriminator v3.36

Date: 2026-08-27

## Increment

Added a prospective randomized TRAVEL-versus-HOME control to separate round-trip shipping/handling state change from ordinary elapsed ageing/home-facility drift before interpreting cross-facility R2 differences.

## Why this increment

Merged v3.34 provides an A→B→A cross-facility transfer screen and merged v3.35 provides a controlled transfer carrier. Those do not independently determine whether transportation itself changes the R2 DUT. A state-changing shipment is a conventional explanation that can mimic or obscure facility disagreement.

The only open automation PR found at session start was PR #7, an alternate empirical calibration-covariance implementation. This session does not overlap that work.

## Artifacts

- `technical/data/r2_shipping_control_protocol_v3_36.json`
- `technical/data/r2_shipping_control_raw_template_v3_36.csv`
- `models/r2_shipping_control_v3_36.py`
- `technical/r2-shipping-control-v3.36.md`
- `research/evidence/r2-shipping-control-v3.36.md`
- `research/sessions/2026-08-27-r2-shipping-control-v3.36.md`
- `venture/v3.36-shipping-control-decision.md`
- `.github/workflows/r2-shipping-control.yml`

## Quantitative verification

Synthetic planning assumptions: 5 mV target effect, 3 mV common substrate-level change SD, equal arm allocation, two-sided alpha 0.05, power target 0.80.

Primary equation: `SE=sigma*sqrt(2/n)` with two-sided normal-approximation power. The standard-library implementation and an independent `statistics.NormalDist` path must agree within `1e-12` absolute power.

Frozen nominal result: six independent substrates per arm gives synthetic power `0.8229821534848882`; three per arm gives only `0.5324208639051091`. Sensitivity across assumed 2/3/4/5 mV change SD requires 3/6/11/16 substrates per arm to reach at least 80% synthetic power.

No stochastic calculation is used; random seed is not applicable. Runtime target is standard-library Python 3.12/3.13/3.14 through CI.

## Statistical hierarchy

Independent unit: substrate. Repeated pixels, injections, and sessions are technical measurements and may not be counted as additional arm-level samples. Arm randomization occurs after qualification; QC/exclusion rules freeze before arm unblinding.

## Conventional/null explanation

Shipping, handling, package shock, storage, remounting, contact change, encapsulation change, or ordinary ageing can produce an apparent facility-transfer difference. The discriminator is the randomized difference-in-changes at the same home facility.

## Safety/environment

No new material or fabrication process is introduced. Qualified primaries may travel only after the v3.35 carrier/insert is human-reviewed and physically qualified. Facility/shipping/EHS rules remain controlling.

## Corrections

No prior numerical result is corrected or superseded. The interpretation of cross-facility transfer is narrowed: v3.34 agreement/disagreement is not sufficient to rule out shipping state change unless that confound is separately controlled or bounded.

## Unresolved risks

Real R2 PRE/POST variance is unknown; normal/equal-variance planning may be optimistic; transfer environment is not yet quantitatively logged; and carrier fabrication/material compatibility still needs physical qualification.

## Single best next increment

Fabricate/qualify the v3.35 carrier on dummies, then execute a low-cost v3.36 dry run with randomized HOME/TRAVEL qualified reference substrates and raw environmental/deviation logging before spending on full A→B→A facility transfer.
