# R2 v3.36 — shipping/handling state-change discriminator

## Status and claim boundary

This is an **engineering experiment specification plus synthetic sample-size planning result**. It introduces no measured R2 shipping stability, facility equivalence, device-performance result, EPC result, or open-quantum result.

The principal conventional explanation addressed here is simple: an apparent A-versus-B facility difference can be caused by shipping, handling, remounting, storage, encapsulation/contact change, or elapsed ageing. The discriminator is a contemporaneous randomized **TRAVEL versus HOME** control measured at the same qualified home facility before and after the transfer interval.

## Design

Qualified independent R2 substrates are randomized after qualification to two arms:

- `TRAVEL`: PRE measurement at facility A, frozen v3.35 carrier/packing, intended A→B→A transfer or representative dry run, POST measurement at facility A.
- `HOME`: PRE measurement at facility A, logged storage for the same elapsed interval, matched remount/measurement sequence without shipment, POST measurement at facility A.

The experimental unit is the **substrate**. Pixels, repeat injections, and repeated sessions remain technical measurements and do not increase arm-level sample size.

Primary observable: `delta_vnr_mV` at a frozen qualified facility-A configuration, temperature, injection condition, calibration lineage, analysis commit, and QC policy.

## Estimator and units

For substrate `i`, define the PRE-to-POST change

`d_i = ΔVnr_POST,i - ΔVnr_PRE,i`.

The shipping-control estimate is

`Δ_ship = mean(d_i | TRAVEL) - mean(d_i | HOME)`.

Every term has units of mV. Positive `Δ_ship` means the travel cohort worsened in nonradiative voltage loss relative to the contemporaneous home cohort.

With independent substrate-level changes and sample standard deviations `s_T` and `s_H`, the engineering standard error is

`SE = sqrt(s_T²/n_T + s_H²/n_H)`.

Dimensional check: each variance term is mV² divided by a dimensionless count; the square root is mV.

The 5 mV practical-effect scale is an **engineering planning scale** inherited from the program's R2 transfer/fabrication precision targets. It is not a standard, universal equivalence margin, or experimentally established shipping tolerance.

## Known limiting cases

1. If every TRAVEL and HOME substrate changes by the same amount, `Δ_ship=0`, even if all devices age substantially. This is the intended cancellation of common elapsed-time drift.
2. If every TRAVEL substrate changes by +5 mV and every HOME substrate changes by 0 mV, `Δ_ship=+5 mV`.
3. Swapping arm labels changes the estimator sign but not magnitude.
4. Additional pixels or repeated sessions on one substrate can reduce measurement noise but cannot increase `n_T` or `n_H`.

These limiting cases are executable tests in `models/r2_shipping_control_v3_36.py`.

## Synthetic sample-size planning

### Inputs

All values in this subsection are **synthetic planning assumptions**, not measured R2 variability:

| input | value | unit | uncertainty/status | provenance |
|---|---:|---|---|---|
| target detectable effect `|δ|` | 5.0 | mV | engineering planning scale | internal R2 precision target |
| substrate change SD `σ` | 3.0 nominal | mV | synthetic; sensitivity 2–5 mV | v3.36 assumption |
| two-sided `α` | 0.05 | dimensionless | fixed planning choice | v3.36 assumption |
| target power | 0.80 | dimensionless | fixed planning choice | v3.36 assumption |
| arm allocation | equal `n` | substrates/arm | design assumption | v3.36 |

No stochastic simulation is used; seed is not applicable.

### Governing approximation

For equal arm size `n` and common substrate-level change SD `σ`, the standard error under the planning model is

`SE = σ sqrt(2/n)`.

Let `z = |δ|/SE` and `zcrit = Φ⁻¹(1-α/2)`. The two-sided normal-approximation power is

`power = 1 - Φ(zcrit-z) + Φ(-zcrit-z)`.

This is a planning approximation, not a claim that real R2 change distributions are Gaussian or homoscedastic.

### Nominal result and independent check

For `δ=5 mV`, `σ=3 mV`, `n=6/arm`, `α=0.05`:

- `SE = 3*sqrt(2/6) = 1.7320508075688772 mV`;
- power = `0.8229821534848882`.

The primary code path uses `math.erf` with a frozen standard-normal critical value. An independent code path uses `statistics.NormalDist().inv_cdf()` and `NormalDist.cdf()`. Agreement tolerance is `1e-12` absolute power and is tested in CI.

### Sensitivity

Minimum equal arm size achieving at least 80% synthetic power for a 5 mV effect:

| assumed `σ_change` | minimum `n` per arm |
|---:|---:|
| 2 mV | 3 |
| 3 mV | 6 |
| 4 mV | 11 |
| 5 mV | 16 |

The scientific/engineering decision is **sensitive** to the unknown substrate-level change variance. Therefore six per arm is not frozen as a universal requirement; it is the nominal design under `σ=3 mV` and must be revisited once real PRE/POST variance exists.

Useful negative result: at `σ=3 mV`, only three substrates per arm gives synthetic power `0.5324208639051091`; a very small transfer screen can therefore miss a practically material 5 mV shipping effect under the nominal model.

## Uncertainty and systematic terms

The arm-level SE captures only independent substrate-to-substrate change variability represented by the sample variances. It does **not** automatically cover:

- calibration drift between PRE and POST;
- common temperature error;
- correlated lot effects;
- differences in elapsed time between arms;
- unequal handling/remount burden;
- analyst/QC selection bias;
- carrier revision changes;
- non-Gaussian degradation tails;
- a shipping effect that interacts with initial device state.

These remain separate systematic/model risks. The HOME arm is specifically intended to absorb common elapsed-time and home-facility drift, but it does not make every systematic disappear.

## QC, exclusions, and hierarchy

Freeze QC/exclusion rules before arm unblinding. Allowed exclusions are limited to predefined acquisition failure, identity/provenance mismatch, invalidating visible damage/unsafe state, missing PRE/POST primary outcome, or frozen configuration mismatch.

Large adverse changes, shipping excursions, or results that worsen `Δ_ship` are **not** exclusion reasons. Preserve all functional substrates.

Hierarchy remains `lot -> substrate -> device/pixel -> session -> measurement`. Statistical arm size is the number of independent substrates, not the number of pixels, injections, timestamps, or repeated sessions.

## Decision semantics

`PASS_SCREEN` means the complete engineering screen does not reveal a material adverse shipping effect under its frozen assumptions. It is **not proof of equivalence**.

`FAIL_SCREEN` is a useful negative result: diagnose packaging, carrier, storage, handling, contact, encapsulation, and shipping exposure before pooling cross-facility data.

`INCOMPLETE` means required data/provenance/configuration evidence is missing; missing evidence never becomes PASS.

## Safety and environmental considerations

Use the reviewed v3.35 carrier/insert before qualified primaries travel. Facility and carrier EHS/handling constraints remain controlling. Randomization never justifies unsafe shipment. Preserve damaged samples and adverse exposure records when safe; do not erase them to improve transfer statistics.

## Source provenance

Internal sources read from `main` on 2026-08-27:

- `README.md`
- `OPEN_SCIENCE.md`
- `CONTRIBUTING.md`
- `research/CALCULATION_VERIFICATION.md`
- `research/session-history.md`
- `research/evidence-map.md`
- `technical/current-specification.md`
- `venture/business-plan.md`
- `automation/hourly-loop.md`
- merged v3.34 cross-facility transfer artifacts
- merged v3.35 transfer-fixture artifacts

No new external empirical performance source is required for this increment; all new numerical variability assumptions are explicitly synthetic/planning values.

## Falsifiable hypothesis and kill/narrow rule

**Hypothesis:** after qualification and under the frozen transfer configuration, the TRAVEL cohort does not show a practically material PRE-to-POST increase in `ΔVnr` relative to contemporaneous HOME controls.

**Kill/narrow:** if the shipping-control effect is adverse or uncertain enough to matter, do not interpret an A/B cross-facility discrepancy as facility metrology transfer until shipping/handling state change is repaired or bounded prospectively.
