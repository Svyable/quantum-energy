# Session v3.14 — local ideality / curvature benchmark

## What changed

Extended v3.13 from a window-dependent global ideality slope to a preregistered local derivative method benchmarked against the source-provided local `n_id` series in the same public PM6:Y12 dataset.

## Evidence provenance

- Article: Wang et al., Advanced Materials (2026), DOI `10.1002/adma.202523681`.
- Dataset: Zenodo `10.5281/zenodo.20525023`.
- File: `Figure S3 + Figure S16a.csv`.
- Upstream MD5: `b430562c7fc5bbc6858553911efb8cc1`.

The upstream CSV is not redistributed here because the Zenodo record page exposes no explicit dataset reuse license. The committed code downloads and hash-verifies it.

## Quantitative result

On the 45% PM6 source series over 0.05–2 suns, the 7-point local quadratic derivative in `ln(Phi)` gives approximately:

- MAE `0.00394` in `n_id`;
- RMSE `0.00682`;
- maximum absolute difference `0.02339`;
- Pearson `r=0.99866` versus the source-provided local series.

The 9-point sensitivity fit gives MAE about `0.00679` and RMSE about `0.00889`.

A synthetic `0.5 mV` Gaussian `Voc`-noise stress (5,000 repetitions, seed `20260826`) gives planning 95th-percentile MAE near `0.026` for the 7-point fit and `0.020` for the 9-point fit. These are simulation results, not experimental uncertainty estimates.

## Calculation audit

Equation:

`n_id = [dVoc/dln(Phi)]/(kBT/q)`.

Units: volts divided by volts, therefore dimensionless.

Primary implementation uses an explicit local quadratic and an independent 3×3 Gaussian-elimination solver. The existing v3.13 global OLS and two-endpoint calculations remain independent average-slope checks rather than the local estimator itself.

Limiting case: an exactly linear `Voc` versus `ln(Phi)` must return a constant derivative for every admissible local window.

## Statistical integrity

One published intensity series is not a set of independent fabrication replicates. The benchmark validates estimator behavior only and does not alter the R2 substrate-count gate.

## Conventional explanations

Local ideality curvature can arise from surface/contact recombination, bulk disorder/traps, transport resistance, carrier-density-dependent recombination, state filling, or mixed regimes. It is not a unique H3 label.

## Program consequence

R2 must publish the full `Voc(Phi)` curve. The 7-point local quadratic becomes the primary curvature estimator, with 9-point smoothing sensitivity. The previously frozen 0.1–1 sun global slope remains a summary statistic only.

## Corrections / superseded claims

No arithmetic from v3.13 is corrected. Its interpretation is narrowed further: a single global ideality number is not the primary mechanism observable when real curvature is present.

## Unresolved risks

- source covariance / per-point `Voc` uncertainty is unavailable;
- PM6:Y12 is not the R2 PM6:Y6 reference;
- the optimum smoothing window may change with R2 point density and noise;
- local ideality remains mechanistically non-unique;
- network CI depends on upstream Zenodo availability.

## Single best next increment

Design the **actual R2 intensity grid and power calculation**: choose log-spaced illumination points and replicate structure so 7-point local `n_id` and its 9-point sensitivity can resolve a preregistered curvature magnitude under empirically plausible `Voc` noise, while minimizing illumination/heating time and preserving the lot→substrate→pixel→session hierarchy.