# Session v3.8 — Published ΔVnr regression benchmark

## What changed

Added an external regression test for the core `EQE_EL → ΔVnr` calculation using five published PM6:NFA device points that report both measured `EQE_EL` and non-radiative voltage loss.

This increment is intentionally narrower than the planned real-facility ingestion because no native facility calibration/reference package is currently available in the repository. Instead of inventing one, the run retires a more basic software risk first: whether our canonical loss equation, sign, unit convention and implementation reproduce an independent published benchmark.

## Evidence provenance

Primary source:

Li et al., Nature Communications 13, 3113 (2022)
https://www.nature.com/articles/s41467-022-30225-7

The paper reports exact text values for five devices:

- PM6:Y6: `EQE_EL=6.2e-5`, non-radiative loss `0.250 V`
- PM6:BO-4F: `1.3e-4`, `0.231 V`
- PM6:BO-4Cl: `1.4e-4`, `0.229 V`
- PM6:BO-5Cl: `1.02e-3`, `0.178 V`
- PM6:BO-6Cl: `7.2e-4`, `0.187 V`

## Governing equation and unit audit

`ΔVnr = -(k_B T/q) ln(EQE_EL)`.

`EQE_EL` must be dimensionless. With `k_B` represented as `8.617333262145e-5 eV/K`, `k_B T` in eV is numerically equal to `k_B T/q` in V for a single elementary charge.

Sign/limits:

- `EQE_EL=1 → ΔVnr=0`
- lower `EQE_EL → larger positive ΔVnr`

## Quantitative result

At 300 K, the committed direct calculation differs from the five rounded published voltage-loss values by only:

- +0.464 mV
- +0.323 mV
- +0.407 mV
- +0.067 mV
- +0.072 mV

Maximum absolute discrepancy: **0.464 mV**.

Independent algebraic inversion of the same published pairs gives implied temperatures of **299.44–299.89 K**.

This agreement is consistent with the published values being evaluated at nominal room temperature and validates the equation/unit implementation against an external dataset.

## Deliberate failure test

Treating an already fractional `EQE_EL` as though it needed multiplication by 100 causes an error of approximately **−118.6 to −119.0 mV**.

This is several times larger than the 10–20 mV EPC-bridge signal of interest, so percent/fraction normalization is now a hard regression test.

## Uncertainty / sensitivity

For fixed `EQE_EL`, `∂ΔVnr/∂T = -(k_B/q)ln(EQE_EL)`.

Across the five benchmark devices, a 1 K temperature change shifts ΔVnr by about **0.594–0.835 mV/K**. This supports retaining DUT-adjacent temperature measurement as a correlated systematic in AT-04.

For small relative `EQE_EL` uncertainty `u_r`, first-order propagation is `u(ΔVnr)≈(k_BT/q)u_r`; at 300 K, 1% relative `EQE_EL` uncertainty contributes about **0.259 mV** before correlated radiometric/systematic errors.

## Independent checks performed

1. Direct five-point 300 K evaluation.
2. Independent inverse-temperature algebraic check.
3. Sign and limiting-case checks.
4. Deliberate percent/fraction error injection.
5. Temperature and relative-EQE sensitivity derivations.

A separate local arithmetic recomputation was used to prepare the frozen CSV. The committed script is designed to regenerate the same CSV and fail if maximum benchmark error exceeds 1 mV or if implied temperature leaves 298–302 K.

## Claim classification

- **Established evidence:** published `EQE_EL` and voltage-loss values.
- **Reproduced calculation:** direct equation evaluation matches rounded published values within 0.464 mV.
- **Cross-checked:** independent algebraic inversion returns ~300 K for every point.
- **Not experimental reproduction:** no source raw detector data were remeasured or reanalyzed.
- **No mechanism claim:** this says nothing about EPC, disorder, R2, or facility performance.

## Correction / supersession

No prior numerical result is corrected. This run adds an external benchmark that future ΔVnr pipelines must pass.

## Files added

- `models/delta_vnr_literature_benchmark.py`
- `models/delta_vnr_literature_benchmark_v3_8.csv`
- `technical/delta-vnr-literature-regression-v3.8.md`
- `research/evidence/delta-vnr-literature-benchmark-v3.8.md`
- this session record

## Unresolved risks

- The source table values are rounded and do not provide the raw absolute-EL uncertainty budget.
- The source measurement injection condition is not a substitute for the program's AT-04 injection sweep.
- Real facility data can still fail through detector nonlinearity, background drift, spectral truncation, calibration correlation, or non-equilibrium injection even though this equation benchmark passes.

## Single best next increment

Obtain or ingest one real facility/native reference package (wavelength calibration, radiometric response, dark/background, linearity data, and repeated weak-EL reference spectra) and require the frozen v3.7 raw-spectrum harness **plus this v3.8 ΔVnr regression** to pass unchanged before replacing synthetic linewidth uncertainty with empirical uncertainty.
