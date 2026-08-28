# v3.54 — External field-generation FF-loss benchmark

## Changed evidentiary state

**Claim class: literature-derived real-data/model benchmark.**

The commercial-bridge program now has one quantitative external benchmark for how large a fill-factor penalty associated with field-dependent free-charge generation can be in a low-voltage-loss organic solar cell. Zhang et al. report for PTO2:Y1 a measured `FF = 0.27` and a reconstructed `FF = 0.58` expected if the device were limited only by transport and bimolecular recombination. In the same discussion they report `eta_int = 0.06` and `beta = 0.09 V^-1` for PTO2:Y1 in their field-dependent-generation model.

This benchmark **does not** assert that D18/PY-IT/eC9 has the same mechanism, parameters, or penalty. Its decision value is narrower: a material system exists in the primary literature where the gap between measured FF and a transport/bimolecular-only reconstruction is much larger than the project's 5% useful-work target. Therefore field-dependent-generation measurements remain a prerequisite before a small voltage-loss gain can be promoted to useful-work evidence.

Primary source: H. Zhang et al., “Overcoming the fill-factor limit of organic solar cells,” *Nature Photonics* (version of record 2026-06-19), DOI `10.1038/s41566-026-01946-8`.

## Quantitative benchmark

Inputs, exactly as used:

| Symbol | Value | Unit | Uncertainty/tolerance | Provenance |
|---|---:|---|---|---|
| `FF_meas` | 0.27 | 1 | physical uncertainty not stated in inspected scalar passage; ±0.005 used only as two-decimal reporting-resolution half-width | literature-derived measured result |
| `FF_tr` | 0.58 | 1 | physical uncertainty not stated in inspected scalar passage; ±0.005 used only as two-decimal reporting-resolution half-width | literature-derived reconstructed model result |
| `eta_int` | 0.06 | 1 | not stated here | literature-derived fitted/experimental parameter; context only |
| `beta` | 0.09 | V^-1 | not stated here | literature-derived fitted parameter; context only |

Governing equations:

`R_FF = FF_meas / FF_tr`

`D_FF = FF_tr - FF_meas`

`d_FF = 1 - R_FF`

where `R_FF` is measured-FF retention relative to the transport/bimolecular-only reconstruction, `D_FF` is the absolute FF deficit, and `d_FF` is the relative deficit. All three are dimensionless because FF is dimensionless.

Result:

- `R_FF = 0.4655172413793104`
- `D_FF = 0.31` absolute FF
- `d_FF = 0.5344827586206896`, i.e. a 53.45% relative FF deficit versus the reported transport/bimolecular-only reconstruction.

These are arithmetic transformations of published values, not new device measurements.

## Reporting-resolution sensitivity

The source values are printed to two decimals. Treating only their unknown last-digit rounding as intervals—**not** as measurement uncertainty—gives:

- `FF_meas in [0.265, 0.275)`
- `FF_tr in [0.575, 0.585)`
- `R_FF in [0.452991..., 0.478261...)`
- `D_FF in (0.30, 0.32]` up to endpoint convention.

The qualitative decision does not change anywhere in this reporting-resolution interval: measured FF remains below half of the transport/bimolecular-only reconstructed FF.

## Independent and negative checks

The executable packet computes the primary ratio directly and cross-checks it through the numerically distinct identity

`R_FF = exp(log(FF_meas) - log(FF_tr))`.

The frozen agreement tolerance is `1e-12`.

Limiting case: if `FF_meas = FF_tr`, then `R_FF = 1` and both deficits are zero.

Negative/control case: if `FF_meas > FF_tr`, the absolute deficit must become negative. The self-test uses `0.60` versus `0.58` and requires that sign reversal.

Runtime target: standard-library Python 3.12, 3.13, and 3.14 in CI. No random sampling is used, so no stochastic seed applies.

## Validity domain and conventional explanations

This scalar benchmark does **not** independently reproduce Zhang et al.'s full TDCF/device model. Two serious conventional/model explanations remain live:

1. The `0.58` reconstructed FF depends on the authors' transport/recombination model and fitted inputs; model misspecification could change the decomposition.
2. The measured `0.27` FF can contain contact, series/shunt resistance, morphology, optical, or other device losses in addition to field-dependent generation. The paper uses TDCF and modelling to argue field-dependent generation is dominant for PTO2:Y1, but that causal attribution is not re-established by this arithmetic packet.

The current increment directly bounds neither explanation; instead it prevents transfer of the PTO2:Y1 magnitude to D18/PY-IT/eC9. The discriminator for the project remains a prospective D18/PY-IT/eC9 field-dependent-generation measurement (preferably TDCF plus bias-dependent PL) under frozen conditions, alongside stabilized FF/Pmax and conventional controls.

## Falsification / correction rule

Revise or retire this benchmark if the primary source is corrected, if a source-version mismatch is found, or if the cited `0.58` quantity is shown not to be the transport/bimolecular-only reconstructed FF described in the main text. Do not reinterpret the reporting-resolution interval as a physical confidence interval.

## Reproduction

```bash
python models/d18_field_generation_external_benchmark_v354.py
```

Machine-readable inputs and frozen outputs are in `models/inputs/d18_field_generation_external_benchmark_v354.json`.
