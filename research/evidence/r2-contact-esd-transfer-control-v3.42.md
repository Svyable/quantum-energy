# Evidence record — R2 contact-state / ESD transfer control v3.42

Date: 2026-08-27

## Evidence class

This increment adds an **engineering protocol and synthetic software arithmetic fixture**. It adds no experimental R2 result, vendor specification, ESD-immunity claim, facility-equivalence claim, or quantum-mechanism evidence.

## Internal provenance

Canonical `main` sources read before work: `README.md`, `OPEN_SCIENCE.md`, `CONTRIBUTING.md`, `research/CALCULATION_VERIFICATION.md`, `research/session-history.md`, `research/evidence-map.md`, `technical/current-specification.md`, `venture/business-plan.md`, and `automation/hourly-loop.md`.

Open automation PR #33 was also reviewed and concerns public-agent discoverability, not transfer contact/ESD controls; v3.42 therefore does not duplicate it.

The need for this increment comes from conventional explanations already preserved by the transfer program: remounting/contact changes, particles, ESD/EOS, fixture differences, temperature mismatch, and package/handling damage can mimic or contaminate cross-session or cross-facility changes.

## New falsifiable discriminator

For each qualified transferred primary, preserve a matched PRE/POST dark-I–V fingerprint using an identical prospectively frozen configuration and an independently documented ESD-sentinel/handling record. If the electrical state changes beyond a declared limit or a frozen sentinel/QC rule fails, cross-facility interpretation is narrowed/blocked pending diagnosis.

A clean result bounds this conventional explanation only to the sensitivity and applicability of the frozen electrical/sentinel measurements.

## Quantitative fixture provenance

All fixture values in `machine/r2-contact-esd-control-v3.42.json` are **synthetic software-test inputs**, created 2026-08-27 for arithmetic verification. They are not literature values and are not measured R2 values.

Synthetic inputs:

- `I_pre = [1,0,4] nA`
- `I_post = [1,2,3] nA`
- `u_pre = u_post = 0.5 nA`
- `rho=0`

Derived fixture outputs:

- `RMS_shift = sqrt(5/3) nA = 1.2909944487358057 nA`
- `u_delta = sqrt(0.5^2+0.5^2) nA = 0.7071067811865476 nA`
- `Z_max = 2/0.7071067811865476 = 2.8284271247461903`

Independent limiting-case checks use the covariance identity for `Var(POST-PRE)` and zero-change behavior.

## Uncertainty and sensitivity

Decision sensitivity is dominated by measurement uncertainty, PRE/POST covariance, contact geometry, probe configuration, temperature, and the eventual acceptance limits. v3.42 deliberately leaves probe conditions and limits unset (`null`) until their provenance is available. Unknown correlation defaults to `rho=-1` for the uncertainty calculation, while both physical RMS shift and standardized shift are retained so a conservative uncertainty assumption cannot by itself erase a large physical change.

## Statistical independence

Voltage points and repeated sweeps are technical observations, not independent devices. The substrate remains the independent experimental unit. ESD-sentinel samples add no substrate-level sample size.

## Negative-result policy

A large POST shift, sentinel event, or visual/electrical failure remains in the public record. It is not an exclusion unless a prospectively frozen rule already applies. `INCOMPLETE` is also a useful result when thresholds, configuration, covariance provenance, or sentinel interpretation are missing.

## External-source status

No new external quantitative threshold or standards-derived acceptance criterion is introduced in v3.42. This is intentional: ESD/contact thresholds are configuration-specific and must not be fabricated from generic assumptions.
