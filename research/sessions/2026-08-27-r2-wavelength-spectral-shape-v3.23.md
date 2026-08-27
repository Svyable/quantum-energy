# Session record — 2026-08-27 — R2 wavelength-resolved spectral-shape gate v3.23

## Increment selected

Added an executable wavelength-resolved spectral mismatch/source-shape gate for the R2 `Voc`-intensity curvature path.

## Why this increment

Open automation PRs already cover empirical repeatability covariance (#6/#7), a prospective repeatability campaign (#8), external/Type-B systematics (#9), and facility-packet integrity (#10). Creating another estimator, campaign, uncertainty budget, or packet validator would duplicate open work.

The uncovered risk is intensity-dependent spectral shape: v3.17 carries a scalar spectral mismatch field, but a source whose spectrum changes with attenuation can distort the effective DUT `ln(Phi)` axis even when broadband reference signal is stable.

## External sources

Checked 2026-08-27:

- IEC 60904-7:2019: https://webstore.iec.ch/en/publication/26502
- NIST PV spectral mismatch equation/reference-cell responsivity paper: https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=915586
- NIST SRI 6014 calibrated PV reference cell: https://www.nist.gov/sri/standard-reference-instruments/sri-6014-calibrated-reference-photovoltaic-cell
- NIST PV characterization laboratory: https://www.nist.gov/laboratories/tools-instruments/photovoltaic-characterization-laboratory
- IEC TR 63228:2019 emerging-PV measurement challenges: https://webstore.iec.ch/en/publication/64040

## Calculation and checks

Primary model:

`M_s = (int E_s R_t / int E_s R_r) (int E_0 R_r / int E_0 R_t)`.

Effective DUT axis:

`Phi_eff = Phi_ref M_s`.

Synthetic 17-point stress fixture, 400–900 nm / 10 nm grid:

- max `|M-1| = 0.003180480548`;
- synthetic `Delta_n=0.10` curvature bias `= +0.001215076355`;
- first-order spectral `u(Delta_n) = 1.739868419e-05`.

Independent nonlinear check:

- Python standard library RNG;
- seed `20260827`;
- 12,000 draws;
- nonlinear `u(Delta_n)=1.737721670e-05`;
- first-order vs MC relative difference `0.1234%`, below frozen 3% tolerance.

Hard limiting cases:

- source spectra differing only by scalar intensity -> `M=1`;
- identical reference/DUT responsivity -> `M=1`;
- common source radiometric-scale uncertainty -> zero mismatch/curvature contribution to numerical precision.

Sensitivity:

- nominal and 2x deterministic spectral-shape stress pass;
- 4x stress gives max `|M-1|=0.0104400` and fails the provisional 1% mismatch gate.

## Claim class

- standards/NIST mismatch methodology: established evidence;
- 1% SMM, 0.01 bias, 0.01 spectral-u limits: engineering assumptions/project gates;
- synthetic fixture outputs: synthetic/model/software-verification results;
- real R2 spectrum stability: open falsifiable hypothesis;
- no experimental R2 result is introduced.

## Negative/null result value

The implementation explicitly demonstrates that absolute broadband source scale can be irrelevant to mismatch while wavelength-dependent shape matters. This prevents effort from being misallocated toward headline broadband stability if the actual curvature risk is spectral shape.

## Statistical independence

Wavelength bins are numerical quadrature points, not independent samples. Intensity spectra within a source sweep are correlated measurement states. No sample-size claim is made.

## Files

- `models/r2_spectral_shape_gate_v3_23.py`
- `models/r2_spectral_shape_gate_test_v3_23.py`
- `models/r2_spectral_shape_fixture_generator_v3_23.py`
- `models/fixtures/r2_spectral_expected_v3_23.csv`
- `technical/r2-wavelength-spectral-shape-gate-v3.23.md`
- `research/evidence/r2-wavelength-spectral-shape-v3.23.md`
- `research/sessions/2026-08-27-r2-wavelength-spectral-shape-v3.23.md`
- `venture/v3.23-spectral-shape-decision.md`
- `.github/workflows/r2-spectral-shape-gate.yml`

## Corrections / superseded claims

No merged arithmetic is corrected. Interpretation is narrowed: a scalar `spectral_mismatch_factor` is not by itself sufficient evidence that mismatch is invariant across the entire intensity sweep. Wavelength-resolved source spectra plus responsivities are required for the stronger statement.

## Unresolved risks

- no real facility source spectra or R2 spectral responsivity have been ingested;
- exact-grid requirement may require an explicit facility resampling/uncertainty procedure later;
- wavelength-correlated spectroradiometer calibration uncertainty must be supplied by a real facility rather than inferred;
- DUT responsivity may itself depend on intensity, temperature, bias, or history;
- attenuation optics may introduce angle/polarization dependence not represented here;
- open PRs #6–#10 remain under human review and must eventually be reconciled with this gate.

## Single best next increment

Acquire wavelength-resolved source spectra at every frozen R2 intensity point under the actual `Voc` acquisition configuration and pair them with traceable reference-detector responsivity plus measured R2 EQE/spectral responsivity. Run v3.23 before inspecting curvature.