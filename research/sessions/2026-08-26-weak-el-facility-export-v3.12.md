# Session v3.12 — weak-EL facility export standard and unit correction

**Date:** 2026-08-26

## What changed

This increment defines the first facility-neutral public export package for weak absolute electroluminescence and adds an executable validator plus a synthetic 2-nm-bin fixture.

While auditing units, the v3.7 synthetic raw-spectrum harness was found to omit an explicit wavelength-bin width in its count-generation/inversion dimensional model. Because its frozen default grid is 1 nm, its published/default numerical values do not change; the validity claim is narrowed and arbitrary-bin/facility ingestion is superseded by v3.12.

## Governing equations

For channel `i`:

`r_net,i = (C_sample,i - C_background,i)/t_i`

`Phi_i = r_net,i K_i`

`phi_lambda,i = Phi_i/Delta lambda_i`

`Phi_total = sum_i phi_lambda,i Delta lambda_i`

`EQE_EL = Phi_total/(I/q)`

`DeltaVnr = -(k_B T/q) ln(EQE_EL)`.

## Independent calculation

Synthetic M001 is hand-constructed from 10 s integration, sample counts 1100/2100/3100, backgrounds 100/100/100, `K=1e8 photons/count`, 2 nm bins, `I=1e-4 A`, and `T=300 K`.

Independent exact-SI arithmetic gives:

- total emitted photon rate = `6.0e10 photons/s`;
- `EQE_EL = 9.613059803999998e-05`;
- `DeltaVnr = 0.23912590245957163 V`.

The validator is required to recover those values. Correct density integration conserves photon rate; the deliberately wrong no-bin-width path is exactly 2x on this fixture. A separate tamper test alters one count without updating the manifest and must fail SHA-256 verification.

## Uncertainty and correlations

No real facility precision is claimed. Per-channel radiometric standard uncertainties are tagged with a mandatory correlation group so common absolute-scale uncertainty cannot be incorrectly reduced by independent RSS across wavelength channels. A real publication package must provide its complete covariance/uncertainty model.

## Statistical hierarchy

The format preserves device, session, measurement, and replicate IDs. Repeated spectra are not reinterpreted as independent devices/substrates.

## Conventional/null explanations retained

A structurally valid facility package does not establish detector linearity beyond the calibrated range, reciprocity/quasi-equilibrium, CT-model validity, absence of injection/state-filling artifacts, EPC/static-disorder causality, or energy-conversion performance.

## Correction / supersession

The frozen v3.7 default 1-nm synthetic outputs remain numerically reproduced. Its dimensional count model is superseded for non-1-nm and real facility data. See `research/corrections/2026-08-26-v3.12-spectral-bin-width.md`.

## Single best next increment

Obtain one real weak-EL facility package in v1.0 and run the validator **unchanged**. If the facility calibration cannot be represented faithfully, revise the schema before interpreting physical data.
