# Correction — v3.32 facility-time calibration fractions

Date: 2026-08-27

## Error

The initial committed frozen-output CSV contained three hand-transcribed `calibration_fraction` values whose last digits did not exactly match the executable planner output. The largest mismatch was in the nominal scenario: committed `0.5377424090328445` versus executable `0.5377424090241829` on Python 3.12.

The total-hour values and component-hour values were unchanged and correct. The discrepancy affected only the stored derived fraction at approximately `8.7e-12` absolute in the nominal case.

## Detection

The first `r2-facility-time-budget` CI run passed the primary self-test but failed the independent frozen-output regeneration check at the predeclared `1e-12` tolerance. The failure was preserved rather than relaxing the tolerance.

## Correction

`models/fixtures/r2_facility_time_scenarios_v3_32.csv` was regenerated/recomputed from the exact component-hour totals:

- low fraction -> `0.4549763033175355`;
- nominal fraction -> `0.537742409024183`;
- high fraction -> `0.6341789052069425`.

## Downstream impact

No scientific, engineering, or commercial decision changes. Rounded percentage statements remain 45.5%, 53.8%, and 63.4%. The low/nominal/high total hours remain 2.9306 / 7.1906 / 19.9733 h.

This correction is visible because CI-detected numerical drift is part of the project's reproducibility record even when decision impact is null.
