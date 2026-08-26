# v3.8 — Published EQE_EL → ΔVnr regression benchmark

## Purpose

Before ingesting any real facility data, verify the program's core non-radiative voltage-loss calculation against an independent published dataset containing both measured `EQE_EL` and reported non-radiative voltage loss.

This is a **calculation/regression benchmark**, not a reproduction of the source experiment.

## Primary source

Li et al., *Asymmetric electron acceptor enables highly luminescent organic solar cells with certified efficiency over 18%*, Nature Communications 13, 3113 (2022):

https://www.nature.com/articles/s41467-022-30225-7

The paper reports the following measured `EQE_EL` values and corresponding non-radiative voltage losses for five PM6:NFA devices:

| Device | Published EQE_EL (fraction) | Published ΔVnr (V) |
|---|---:|---:|
| PM6:Y6 | 6.2e-5 | 0.250 |
| PM6:BO-4F | 1.3e-4 | 0.231 |
| PM6:BO-4Cl | 1.4e-4 | 0.229 |
| PM6:BO-5Cl | 1.02e-3 | 0.178 |
| PM6:BO-6Cl | 7.2e-4 | 0.187 |

These values are external experimental evidence reported by the authors. The calculations below are ours.

## Governing relation

For external electroluminescence quantum efficiency expressed as a **dimensionless fraction**,

`ΔVnr = -(k_B T / q) ln(EQE_EL)`.

Using `k_B = 8.617333262145e-5 eV/K`, the numerical value `k_B T` in eV is equal to `k_B T/q` in volts for one elementary charge.

### Dimensions

- `EQE_EL`: dimensionless.
- `ln(EQE_EL)`: dimensionless.
- `k_B T/q`: volts.
- Therefore `ΔVnr`: volts.

### Sign and limiting cases

- `0 < EQE_EL <= 1`.
- `ln(EQE_EL) <= 0`, hence `ΔVnr >= 0`.
- `EQE_EL = 1` gives `ΔVnr = 0`.
- Lower `EQE_EL` must give larger `ΔVnr` at fixed temperature.

## 300 K recomputation

The committed implementation is `models/delta_vnr_literature_benchmark.py` and the frozen output is `models/delta_vnr_literature_benchmark_v3_8.csv`.

At 300 K:

| Device | Calculated ΔVnr (V) | Published (V) | Error (mV) | Implied T from published pair (K) |
|---|---:|---:|---:|---:|
| PM6:Y6 | 0.250463899 | 0.250 | +0.464 | 299.444 |
| PM6:BO-4F | 0.231323076 | 0.231 | +0.323 | 299.581 |
| PM6:BO-4Cl | 0.229407237 | 0.229 | +0.407 | 299.467 |
| PM6:BO-5Cl | 0.178067350 | 0.178 | +0.067 | 299.887 |
| PM6:BO-6Cl | 0.187071775 | 0.187 | +0.072 | 299.885 |

Maximum absolute discrepancy is **0.464 mV**, well inside the preregistered 1 mV literature-rounding benchmark. The independently inverted temperatures span **299.44–299.89 K**, strongly consistent with a nominal 300 K evaluation and providing a separate algebraic cross-check.

The sub-millivolt discrepancies are consistent with rounding of the published EQE_EL and voltage-loss values; they are not evidence that the underlying measurements had sub-millivolt uncertainty.

## Deliberate unit-failure control

A common catastrophic error is to take an EQE_EL already expressed as a fraction and multiply it by 100 as though converting from percent to fraction.

Applying that deliberately incorrect transformation shifts the recomputed voltage loss by approximately **−118.6 to −119.0 mV** across all five benchmark devices.

This is much larger than the 10–20 mV effect scale targeted by the EPC bridge. The regression test therefore freezes a hard rule:

> `EQE_EL` must enter every ΔVnr calculation as a dimensionless fraction, with the source representation and conversion recorded explicitly.

## Independent checks

1. **Direct equation evaluation** at 300 K against five independent published device points.
2. **Inverse algebraic check**: solve each published `(EQE_EL, ΔVnr)` pair for temperature. All imply ~300 K.
3. **Limiting cases**: `EQE_EL=1 → ΔVnr=0`; decreasing EQE_EL increases loss.
4. **Unit-failure control**: the percent/fraction mistake creates an ~119 mV bias and must fail loudly.

## Uncertainty and sensitivity

For fixed `EQE_EL`,

`∂ΔVnr/∂T = -(k_B/q) ln(EQE_EL)`.

For the benchmark range, a ±1 K temperature error contributes approximately 0.59–0.84 mV of ΔVnr shift. Thus the existing ±1 K DUT-temperature gate remains appropriate relative to the 10 mV total AT-04 target, but temperature is a correlated systematic and must not be silently combined as independent pixel noise.

For small relative EQE_EL uncertainty `u_r`, first-order propagation gives

`u(ΔVnr) ≈ (k_B T/q) u_r`.

At 300 K, 1% relative EQE_EL uncertainty corresponds to approximately 0.259 mV of voltage-loss uncertainty before correlated calibration terms.

## Publication / claim boundary

**Established evidence:** the source paper reports the five EQE_EL and non-radiative-loss pairs above.

**Reproduced calculation:** our direct 300 K calculation matches the rounded published losses within 0.464 mV.

**Cross-check:** algebraic inversion of each pair independently returns 299.44–299.89 K.

**Not established:** this benchmark does not validate our detector chain, R2 reference, injection protocol, or EPC mechanism. It validates the equation/unit convention and the implementation against published values.

## Program consequence

The ΔVnr equation/unit implementation is no longer merely internally self-consistent; it has a public external regression benchmark. Every future AT-04 or B0/B1/B2 analysis should run this benchmark before processing new data. A failure blocks publication and mechanism interpretation until resolved.
