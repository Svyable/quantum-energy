# Weak-EL Facility Export Standard v1.0 (v3.12)

## Status

**Open publication/data infrastructure.** This project-specific format defines the minimum machine-readable package a laboratory should export for weak absolute-electroluminescence measurements used by R2 / AT-04. It is intentionally plain JSON + CSV. It is not a community standard, instrument certification, or evidence that a facility reaches the program's <=10 mV `DeltaVnr` target.

## v3.7 dimensional correction

The historical v3.7 synthetic harness represented `N_lambda` as a wavelength spectral density but generated expected detector counts from `N_lambda * eta(lambda) * t` without an explicit spectral-bin width. Dimensionally, a density in `photons s^-1 nm^-1` must be multiplied by `Delta lambda` before it becomes a per-bin photon rate.

The frozen v3.7 default uses `Delta lambda = 1 nm`, so its published/default numerical recovery values are unchanged. The correction narrows the validity domain: v3.7 must not be generalized to non-1-nm or real facility grids without an explicit bin-width treatment.

The v1.0 physical path is:

`r_net,i = (C_sample,i - C_background,i) / t_i`  [count s^-1]

`Phi_i = r_net,i * K_i`  [emitted photons s^-1 bin^-1]

`phi_lambda,i = Phi_i / Delta lambda_i`  [emitted photons s^-1 nm^-1]

`Phi_total = sum_i(phi_lambda,i * Delta lambda_i) = sum_i Phi_i`  [photons s^-1]

`R_e = I/q`  [electrons s^-1]

`EQE_EL = Phi_total/R_e`

`DeltaV_nr = -(k_B T/q) ln(EQE_EL)`.

`K_i` is the calibrated number of emitted photons represented by one background-subtracted detector count in channel `i`, including the calibrated collection/detection chain.

### Background convention

`background_counts` is acquired with device emission suppressed/blocked while retaining detector dark and optical stray/background under the same integration condition. Therefore the signal calculation is `sample_counts - background_counts`.

`dark_counts` is a separate QC diagnostic and is **not subtracted a second time**. A facility using a different native convention must transform to this convention and document the transformation.

## Required package

- `manifest.json`
- `measurements.csv`
- `spectra.csv`
- `wavelength_calibration.csv`
- `radiometric_calibration.csv`
- `linearity.csv`
- recommended `README.md`

The JSON Schema is `schemas/weak_el_facility_export_v1.schema.json`. The executable validator is `tools/validate_weak_el_export.py`.

## Required fields

`measurements.csv`: `measurement_id`, `device_id`, `session_id`, `timestamp_utc`, `temperature_K`, `temperature_standard_uncertainty_K`, `injection_current_A`, `injection_current_standard_uncertainty_A`, `active_area_m2`.

`spectra.csv`: `measurement_id`, `replicate_id`, `detector_channel`, `integration_time_s`, `sample_counts`, `background_counts`, `dark_counts`.

`wavelength_calibration.csv`: `detector_channel`, `wavelength_nm`, `wavelength_standard_uncertainty_nm`, `bin_width_nm`. `bin_width_nm` is mandatory; centers alone are not enough for a unit-safe density transform, especially on nonuniform grids.

`radiometric_calibration.csv`: `detector_channel`, `emitted_photons_per_count`, `relative_standard_uncertainty`, `correlation_group`. Correlation groups are mandatory so wavelength-channel scale errors are not silently treated as independent.

`linearity.csv`: `count_rate_cps`, `relative_response`, `relative_standard_uncertainty`. Every accepted sample acquisition must lie inside the manifest's declared calibrated count-rate interval.

`manifest.json` records schema/version, package ID, open-science status, reuse-license expression/URI, UTC creation time, facility/instrument/software IDs, exact count/calibration conventions, valid linearity range, uncertainty convention, and SHA-256 for each required payload.

`NOASSERTION` is allowed only for software fixtures; a public experimental package is not publication-ready until reuse rights are explicit.

## Validator gates

The standard-library validator enforces required files/columns; SHA-256 integrity; unique IDs/calibrations; positive times/bin widths/radiometric factors/areas/current/temperature; matching calibration channel sets; linearity coverage; exactly one calibrated channel per measurement/replicate; spectral-density/bin conservation; `0 < EQE_EL <= 1`; and deterministic `DeltaVnr` using exact SI `k_B` and `q`.

The committed synthetic fixture intentionally uses **2 nm bins**. Correct density integration conserves photon rate. The historical no-bin-width pattern is wrong by exactly 2x and is retained as a deliberate negative control.

## Uncertainty

The format records standard uncertainties and correlation groups but does not pretend a generic parser can construct a facility's full covariance model. Publication-grade data must provide enough information to reconstruct Type A repeatability, Type B calibration terms, correlated absolute-radiometric scale, wavelength uncertainty where relevant, current and temperature uncertainty, background/dark/linearity contributions, geometry corrections, and covariance or a justified approximation.

This follows NIST TN 1297's principle that correlated components require covariance treatment rather than naive independent RSS.

## Open-data rationale

The package is designed to be machine-actionable: typed metadata, explicit units, file roles, hashes, provenance, reuse terms, and a reconstructable raw-count-to-measurand path. This is aligned with the FAIR principles' emphasis on metadata, provenance, interoperability, and reuse, but v1.0 does **not** claim full FAIR compliance or community-standard status.

## Claim classes

**Established:** calibration provenance and uncertainty accounting are necessary for absolute measurement; correlated uncertainty terms require covariance treatment; rich machine-readable metadata and provenance improve reuse.

**Engineering assumptions:** JSON + CSV is sufficient for the first collaboration round; one stationary wavelength/radiometric calibration per package is adequate for v1.0.

**Falsifiable hypothesis:** a facility can export a conforming package such that the unchanged validator reconstructs absolute photon rate, `EQE_EL`, and `DeltaVnr` without facility-specific hand edits.

**Novel invention:** none. This is intentionally open interoperability infrastructure.

## Publication gate

A real package may replace synthetic facility/noise assumptions only if the validator passes unchanged, reuse rights are explicit, calibration/linearity cover every accepted measurement, the full uncertainty/covariance statement is supplied, repeated-reference data quantify empirical repeatability, and the existing reciprocity/injection claim boundaries remain satisfied.

## Next test

Request v1.0 from one real facility and run the validator **unchanged**. If the facility cannot represent its actual calibration without hand preprocessing, revise the schema before interpreting device physics.
