# Session v3.13 — external `Voc`–intensity benchmark

## What changed

Added an executable regression benchmark using a real public 2026 PM6:Y12 light-intensity dataset rather than another synthetic-only test. The purpose is to validate the arithmetic and interpretation limits of the R2 H3 `Voc`-versus-light-intensity discriminator.

## Evidence added

- Wang et al., *Advanced Materials* 2026, DOI `10.1002/adma.202523681`.
- Supporting open dataset, Zenodo DOI `10.5281/zenodo.20525023`.
- Exact benchmark CSV MD5: `b430562c7fc5bbc6858553911efb8cc1`.

## Calculation

For a locally linear `Voc` response to light intensity `Phi`:

`n_id = (dVoc/d ln Phi)/(k_B T/q)`.

The implementation uses `k_B = 8.617333262e-5 eV/K`, `T=300 K`, and volts/electron-volt numerical consistency for a single electronic charge.

The frozen primary intensity window is `0.1–1 sun`.

Primary OLS result from the public 45% PM6 data:

- `n_id = 1.054131426`
- regression SE `= 0.009775690`
- `Voc` RMSE `= 0.488 mV`
- mean source-file local `n_id` over the same points `= 1.042550354`

Independent two-endpoint slope over the same window gives `n_id = 1.047852257`; `|Delta n| = 0.00628`, inside the frozen `<0.08` sanity tolerance.

## Sensitivity / negative result

Changing only the intensity window changes the global fitted ideality materially:

- `0.05–0.5 sun`: `n=1.10091`
- `0.1–1 sun`: `n=1.05413`
- `0.2–1 sun`: `n=1.02797`
- `0.5–2 sun`: `n=0.91093`

The ~0.19 range is a useful negative result: **the R2 program must not select an intensity window after seeing which ideality factor best supports a mechanism story.** The window and local-curvature treatment must be frozen prospectively.

## Assumptions

- `T=300 K` is used for this room-temperature benchmark.
- Standard OLS residual SE is descriptive; the upstream data do not provide a complete covariance/measurement-uncertainty model for these plotted points.
- The global fit is an empirical diagnostic rather than a unique physical ideality parameter where the curve is visibly non-linear.

## Conventional explanations retained

A change in fitted ideality can reflect surface/contact recombination, energetic disorder, traps, transport limitations, injection/state filling, or fit-window curvature. Therefore this benchmark strengthens arithmetic reliability but narrows mechanism claims.

## Files changed

- `models/voc_intensity_realdata_benchmark.py`
- `models/voc_intensity_realdata_expected_v3_13.csv`
- `.github/workflows/voc-intensity-realdata.yml`
- `technical/voc-intensity-realdata-benchmark-v3.13.md`
- `research/evidence/voc-intensity-realdata-v3.13.md`
- this session record

## Corrections / supersessions

No prior numerical result is corrected. The interpretation is narrowed: a single fitted ideality factor should not be treated as a mechanism label without a frozen window and independent discriminators.

## Unresolved risks

- external Zenodo availability can make CI transiently fail;
- upstream license metadata is not explicit on the record page, so the repository does not redistribute the source CSV;
- the current benchmark is PM6:Y12, not R2 PM6:Y6;
- full experimental point covariance is unavailable;
- ideality factor is not uniquely mechanistic.

## Single best next increment

Use the same public dataset to benchmark the **local ideality / curvature extraction** itself against the source-provided local `n_id` series, then freeze a regularized derivative method and noise sensitivity before R2 data collection. That is more informative than relying on one global slope.
