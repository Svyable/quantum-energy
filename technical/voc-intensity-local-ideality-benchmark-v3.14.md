# v3.14 — Local ideality / curvature benchmark on real PM6:Y12 data

## Scope

This increment benchmarks a **local** `Voc`-versus-light-intensity derivative against the source-provided local ideality-factor series in the public Wang et al. PM6:Y12 dataset. It narrows the v3.13 conclusion that one global slope is fit-window dependent.

This is an estimator benchmark on one published material system. It is **not** evidence that ideality factor uniquely identifies an R2 recombination mechanism.

## External evidence and provenance

Primary article: Wang et al., *Rethinking Charge Transport and Recombination in Donor-Diluted Organic Solar Cells*, Advanced Materials (2026), DOI `10.1002/adma.202523681`.

Public dataset: Zenodo record `10.5281/zenodo.20525023`, published June 2026. Exact source file: `Figure S3 + Figure S16a.csv`, upstream MD5 `b430562c7fc5bbc6858553911efb8cc1`.

The paper states that recombination ideality factors are determined from light-intensity- and temperature-dependent suns-`Voc` measurements and uses them as an empirical input to its density-of-states / recombination analysis. The same paper reports ideality factors below unity in the higher-donor devices near high illumination and discusses surface recombination as a possible contributor. Therefore curvature and illumination window are physical information, not nuisance detail.

## Governing relation and dimensions

For intensity `Phi`,

`n_id(Phi) = [d Voc / d ln(Phi)] / (k_B T / q)`.

Because `ln(Phi)` is dimensionless, `dVoc/dln(Phi)` has units volts. `k_B T/q` is volts, so `n_id` is dimensionless.

The implementation uses `k_B = 8.617333262e-5 eV/K` and `T = 300 K`, so `k_B T/q = 0.025851999786 V` in the eV-per-charge convention.

## Frozen estimator

Primary estimator: **7-point local quadratic regression in `x = ln(Phi)`**.

For each evaluation point `x_i`, fit the nearest seven source points to

`Voc(x) = a + b (x-x_i) + c (x-x_i)^2`

by ordinary least squares. Then

`n_id(x_i) = b / (k_B T/q)`.

A 9-point local quadratic is reported as a smoothing sensitivity analysis. The 7-point estimate is primary because it gives materially lower zero-noise bias than 5-point fits while remaining more local than the 9-point fit.

No high-order spline or high-capacity smoother is permitted for the R2 pilot unless preregistered on an independent dataset.

## Real-data benchmark

Operational benchmark window: **0.05–2 suns**, chosen to cover the neighborhood around the v3.13 0.1–1 sun primary operating region while retaining curvature above one sun. There are 16 source points in this window for the 45% PM6 series.

Using the source-provided local `n_id` series as the external benchmark:

- 7-point local quadratic: MAE ≈ **0.00394**, RMSE ≈ **0.00682**, maximum absolute difference ≈ **0.02339**, Pearson `r ≈ 0.99866`.
- 9-point sensitivity: MAE ≈ **0.00679**, RMSE ≈ **0.00889**.

The source local series decreases from roughly 1.16 near 0.055 sun toward roughly 0.83 near 1.97 suns. The local estimator preserves that curvature; therefore R2 should not collapse an injection sweep to one post-hoc global ideality number.

These values are derived from public experimental plot data. They validate arithmetic/estimator behavior only; the source file does not provide a full covariance matrix for these plotted points.

## Synthetic noise sensitivity

Because the source plot-data file does not provide `Voc` measurement uncertainty, noise injection is explicitly **synthetic planning analysis**.

Frozen stress case: independent Gaussian `Voc` noise `sigma = 0.5 mV`, seed `20260826`, 5,000 repetitions.

Approximate operating results from the independent planning calculation:

- 7-point estimator: median MAE ≈ **0.0157** in `n_id`; 95th-percentile MAE ≈ **0.0263**.
- 9-point estimator: median MAE ≈ **0.0122**; 95th-percentile MAE ≈ **0.0204**.

The 9-point method is more noise-robust but less local. Therefore the publication rule is: report the 7-point primary curve and the 9-point curve as a smoothing sensitivity. A physical conclusion that changes between them is conditional, not robust.

## Independent checks

1. The local quadratic is solved with an explicit 3×3 Gaussian-elimination normal-equation implementation rather than NumPy/SciPy fitting routines.
2. v3.13's global OLS and independent two-endpoint slope remain separate calculation paths for the average slope over a chosen interval.
3. Dimensional analysis gives a dimensionless `n_id`.
4. Constant/linear limiting case: for exactly linear `Voc` versus `ln(Phi)`, any admissible local quadratic window must recover the same slope (up to floating-point error).
5. The source file's raw `Voc` column and local-`n_id` `Voc` column must agree within 5 µV before the benchmark runs.
6. Source bytes must match the Zenodo-published MD5 before parsing.

## Statistical independence

Intensity points in one device/series are **not** independent fabrication replicates. This benchmark tests a derivative estimator on one published 45% PM6 intensity series only. It makes no inference about R2 substrate count or mechanism prevalence.

## Conventional / null explanations preserved

A local `n_id` curve can reflect surface/contact recombination, bulk trap/disorder behavior, transport resistance, carrier-density-dependent recombination, state filling, or combinations of these. Agreement with the published local series does not identify which mechanism is correct.

For R2, local ideality is an H3/H4 discriminator only when interpreted jointly with FTPS/sensitive EQE, injection-resolved EL, temperature dependence, and contact/transport controls.

## R2 preregistration change

For the R2 `Voc`-intensity audit:

- acquire at least enough log-spaced intensity points to support a 7-point local fit over the intended 0.05–2 sun range;
- freeze the intensity grid before unblinding;
- primary curve = 7-point local quadratic;
- sensitivity curve = 9-point local quadratic where enough points exist;
- preserve and publish the full `Voc(Phi)` curve;
- report the previously frozen global 0.1–1 sun slope only as a summary, not the sole mechanism statistic;
- if 7- and 9-point interpretations disagree materially, mark the mechanism conclusion conditional and acquire more precise / denser data rather than choosing the preferred curve post hoc.

## Claim classification

**Established evidence:** real PM6:Y12 `Voc(Phi)` data are curved; the source publication uses light-intensity-dependent ideality analysis and discusses non-unique recombination regimes.

**Engineering assumption:** 7-point local quadratic smoothing is an appropriate bias/locality compromise for the planned R2 intensity grid.

**Synthetic/model result:** the 0.5 mV noise stress results are not measurements.

**Falsifiable hypothesis:** local curvature plus FTPS/EL/contact controls will improve H1–H4 discrimination compared with one global slope.

**Novel invention concept:** none in this increment.

## Publication gate

The local-ideality method may be called **cross-checked on this public dataset** only if the executable benchmark downloads the exact MD5-pinned file and meets all of:

- 7-point source-series MAE `< 0.006`;
- 7-point RMSE `< 0.010`;
- Pearson correlation `> 0.995`;
- 9-point sensitivity MAE `< 0.010`;
- under the explicitly synthetic 0.5 mV stress, 95th-percentile MAE `< 0.035` (7-point) and `< 0.030` (9-point).

Passing this gate does not confer mechanism validity.