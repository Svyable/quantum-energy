# v3.13 — real-data `Voc`–light-intensity regression benchmark

## Purpose

Replace one synthetic-only component of the R2 H3 discriminator with a public experimental regression benchmark.

The benchmark uses the 45% PM6 series in `Figure S3 + Figure S16a.csv` from the open Zenodo dataset supporting Wang et al., *Rethinking Charge Transport and Recombination in Donor-Diluted Organic Solar Cells* (Advanced Materials, 2026; DOI `10.1002/adma.202523681`; dataset DOI `10.5281/zenodo.20525023`). The source dataset states that it includes light-intensity-dependent measurements and provides all figure data as CSV. The exact source file has Zenodo-published MD5 `b430562c7fc5bbc6858553911efb8cc1`.

The upstream dataset is not vendored into this repository. The executable benchmark downloads the exact file and refuses to run if its MD5 changes.

## Governing relation

For an approximately linear region of `Voc` versus logarithmic light intensity,

`dVoc / d ln(Phi) = n_id k_B T / q`.

Because `k_B` is represented in eV/K, `k_B T` has the same numerical value in volts as `k_B T / q` when one electron charge is implicit in the eV-to-V conversion. Therefore

`n_id = slope / (k_B T)`

with `slope` in V per natural-log unit and `k_B = 8.617333262e-5 eV/K`.

The benchmark uses `T = 300 K`, consistent with the paper's room-temperature analysis. This is an external-data arithmetic benchmark, not a claim that a single global ideality factor is a unique physical mechanism.

## Results

For the preregistered `0.1–1 sun` window, ordinary least squares on the public 45% PM6 data gives:

- `n_fit = 1.054131426`
- standard error from linear-regression residuals: `0.009775690`
- `Voc` fit RMSE: `0.488 mV`
- mean of the source file's local `n_id` values over the same included points: `1.042550354`
- difference: `+0.011581072`

An independent two-endpoint calculation over the same window gives `n = 1.047852257`, differing from the OLS result by `0.00628`. The two calculations are not expected to be identical because the real curve is measurably non-linear.

## Sensitivity to the fit window

The inferred global `n_id` is not invariant to the chosen intensity interval:

| intensity window (suns) | points | global `n_id` |
|---|---:|---:|
| 0.03–2.0 | 18 | 1.05717 |
| 0.05–0.5 | 10 | 1.10091 |
| 0.1–1.0 | 10 | 1.05413 |
| 0.2–1.0 | 7 | 1.02797 |
| 0.1–2.0 | 13 | 1.01309 |
| 0.5–2.0 | 6 | 0.91093 |

This is a decision-driving negative result for interpretation: **a single global ideality factor can shift by ~0.19 across plausible intensity windows in this real NFA dataset**. The R2 H3 audit must therefore freeze its light-intensity window before unblinding and retain the local/curvature information rather than selecting a favorable slope post hoc.

## Conventional explanations / claim boundary

The source paper itself discusses ideality factors below unity near high donor fractions and attributes the high-intensity behavior to surface recombination. More generally, ideality factor in OSCs can be affected by energetic disorder, traps, transport, surface/contact recombination, and the intensity window. Therefore:

- this benchmark validates our extraction arithmetic and demonstrates real window dependence;
- it does **not** validate H3 as the unique explanation for an R2 `DeltaVnr` change;
- an R2 H3 interpretation still requires the frozen FTPS/EL/injection controls and comparison to H1/H2/H4.

## Verification

`models/voc_intensity_realdata_benchmark.py` performs:

1. exact URL download;
2. upstream MD5 verification;
3. structure-based identification of the two `45% PM6` column groups;
4. consistency check between the raw-`Voc` and source local-`n_id` `Voc` columns;
5. closed-form OLS rather than a black-box fitting package;
6. comparison to frozen expected outputs;
7. independent endpoint-slope sanity check.

CI runs this benchmark on every PR. The source file is external and may be temporarily unavailable; an upstream network outage is a CI infrastructure failure, not a scientific failure.

## Open-science status

**Established evidence:** the public dataset, its source-file checksum, and the underlying light-intensity measurements.

**Reproduced calculation:** the committed OLS ideality extraction once CI downloads the checksum-matched source and reproduces the frozen outputs.

**Cross-check:** independent endpoint slope agrees within the predeclared `|Delta n| < 0.08` tolerance.

**Not established:** any R2 interface-recombination mechanism, EPC mechanism, or energy-conversion improvement.
