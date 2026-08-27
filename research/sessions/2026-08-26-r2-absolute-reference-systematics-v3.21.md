# Session record — 2026-08-26 — v3.21 absolute/reference systematics

## Increment

Added a machine-readable absolute/reference systematic uncertainty budget that complements the open repeatability/covariance work without duplicating it.

## Why this increment

The open v3.19/v3.20 work correctly states that repeated sweeps cannot identify an absolute systematic calibration bias shared by every repetition. v3.21 turns that unresolved caveat into an executable interface: recognized corrections are applied on the log-intensity axis and their remaining standard uncertainties are emitted as signed v3.18 covariance components.

## Inputs and provenance

External methodology was checked against NIST TN 1297 sections 4–6 and Appendix A plus the current BIPM/JCGM publication index. All numerical component magnitudes used for software verification are explicitly synthetic assumptions dated 2026-08-26.

## Governing model

For component `k` and intensity point `i`:

`ln(Phi_corr,i) = ln(Phi_cal,i) - sum_k c_k s_ki`

and

`l_ki = u_k s_ki`.

The unchanged v3.18 engine propagates

`u_Delta^2 = sum_k (g^T l_k)^2`.

The model is dimensionless on the intensity axis. Correlated component rows are never treated as independent replicates.

## Synthetic verification values

Fixture declarations:

- synthetic common responsivity scale: expanded `U=0.004`, `k=2`, correction amplitude `0.003`;
- synthetic linear/stretch term: rectangular half-width `0.0015`, correction `0.0005`;
- synthetic quadratic spectral-shape term: triangular half-width `0.004`, correction `0.001`.

Normalized standard uncertainties are `0.002`, `0.000866025404`, and `0.001632993162` respectively.

On the frozen v3.18 synthetic 17-point curve:

- deterministic correction delta in curvature: `+0.002088789592`;
- axis-systematic `u(Delta_n_curv)`: `0.003367338539`;
- combined with existing synthetic 0.5 mV point `Voc`: `0.02267761879`;
- synthetic planning power for an explicitly assumed 0.10 effect: `0.9928506417`.

## Independent checks

- A 1% perfectly common intensity-scale uncertainty must cancel for a derivative curvature observable; test requires output below `1e-8`.
- Independent nonlinear Monte Carlo: 12,000 latent-component draws, seed `20260826`, gives axis `u=0.003400503601` versus first-order `0.003367338539`; relative difference `0.9849%`, below a frozen 3% tolerance.
- Distribution normalization checks explicitly recover `U/k`, `a/sqrt(3)`, and `a/sqrt(6)`.

## Sensitivity / useful negative result

The synthetic quadratic spectral-shape term contributes >99.9% of axis-systematic variance; the common-scale term is negligible for this derivative measurand. Doubling only the spectral-shape uncertainty raises axis `u` to `0.006734144131` while synthetic planning power remains `0.9895757637`.

This does not imply a real facility has the same dominance ordering. It does show that a generic push for lower absolute scale uncertainty can have low value if intensity-dependent shape is the true limiting systematic.

## Correction history

No merged result was numerically corrected. v3.21 narrows an interpretation: repeatability covariance and external/Type-B systematic uncertainty are separate evidence classes and must not be substituted for one another.

## Statistical independence

Certificate/common terms are systematic covariance components, not independent samples. The DUT hierarchy remains lot -> substrate -> pixel -> session -> sweep -> intensity; v3.21 changes none of those sample counts.

## Null/conventional explanation

Detector nonlinearity, spectral mismatch, source drift, temperature response, geometry, interpolation, and electronics can all create smooth calibration-axis structure. The budget therefore supports metrology quality only, not DUT mechanism identification.

## Files

- `models/r2_absolute_systematic_budget_v3_21.py`
- `models/r2_absolute_systematic_budget_test_v3_21.py`
- `models/fixtures/r2_absolute_systematic_components_v3_21.csv`
- `models/fixtures/r2_absolute_systematic_shapes_v3_21.csv`
- `technical/r2-absolute-reference-systematics-v3.21.md`
- `research/evidence/r2-absolute-reference-systematics-v3.21.md`
- `research/sessions/2026-08-26-r2-absolute-reference-systematics-v3.21.md`
- `venture/v3.21-absolute-systematic-decision.md`
- `.github/workflows/r2-absolute-systematics.yml`

## Unresolved risks

- no actual facility calibration certificate/report has been mapped into component shapes;
- certificate scope/validity is metadata and is not cryptographically or semantically authenticated;
- component independence between different IDs is an assumption unless a richer covariance factorization is supplied;
- real spectral mismatch may require wavelength-resolved modeling rather than a scalar grid-shape component;
- v3.19/v3.20 repeatability work remains open and must eventually be combined without double counting.

## Single best next increment

Obtain one real reference-detector calibration certificate/report plus the facility source-spectrum/linearity characterization, map every applicable correction and uncertainty component to the 17-point grid, and run v3.21 together with the selected empirical repeatability model. Preserve any missing component as `INCOMPLETE` rather than inventing a value.
