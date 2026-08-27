# R2 absolute/reference systematic uncertainty budget v3.21

## Purpose and claim boundary

v3.19/v3.20 address repeatability covariance. They cannot estimate an absolute systematic bias that is shared by every repetition of the same reference detector/source/configuration. v3.21 closes that representational gap by converting calibration-certificate, manufacturer, literature, or explicitly assumed Type-B/common terms into corrected intensity axes plus signed covariance components consumable by the unchanged v3.18 curvature engine.

This is metrology infrastructure only. It does not identify DUT recombination physics, EPC, or open-quantum transport.

## Established metrology basis

NIST TN 1297 states that recognized systematic effects should be corrected where significant and that the uncertainty of the applied correction belongs in the combined standard uncertainty. It also defines expanded uncertainty `U = k u_c`, so a quoted expanded uncertainty with known coverage factor is converted to standard uncertainty by `u = U/k`. For bounded Type-B inputs, NIST gives `u=a/sqrt(3)` for a rectangular half-width `a` and `u=a/sqrt(6)` for a triangular half-width.

Primary public sources checked 2026-08-26:

- https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-4-type-b-evaluation-standard-uncertainty
- https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-5-combined-standard-uncertainty
- https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-6-expanded-uncertainty
- https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty
- JCGM publication index, including JCGM 100:2008 and the 2026 nonlinearity amendment: https://www.bipm.org/en/committees/jc/jcgm/publications

These sources support the uncertainty methodology, not any numerical R2 performance value.

## Machine-readable model

The component metadata CSV requires:

`component_id, source_category, uncertainty_value, uncertainty_kind, coverage_factor, correction_ln_amplitude, provenance_class, provenance, version_date, validity_status, note`

The shape CSV requires:

`component_id, target_suns, shape_loading`

For component `k` and grid point `i`, the deterministic recognized log-axis correction is

`d_ki = c_k s_ki`,

where `c_k` is `correction_ln_amplitude` and `s_ki` is `shape_loading`.

The corrected calibrated intensity is

`Phi_corr,i = Phi_cal,i exp[-sum_k d_ki]`.

All correction amplitudes and uncertainty loadings are dimensionless because they are perturbations in `ln(Phi)`.

After uncertainty normalization, component `k` has standard uncertainty `u_k`. Its signed v3.18 latent loading is

`l_ki = u_k s_ki`.

The v3.18 first-order curvature uncertainty is then

`u_Delta^2 = sum_k (g^T l_k)^2`,

where `g_i = d(Delta_n_curv)/d ln(Phi_i)`.

This preserves full correlation inside each declared component. Repeating the same certificate term across 17 points never creates `sqrt(17)` independent information.

## Supported uncertainty declarations

- `standard_normal`: `u=value`.
- `expanded_normal`: `u=U/k`; `coverage_factor` is required and positive.
- `rectangular_half_width`: `u=a/sqrt(3)`.
- `triangular_half_width`: `u=a/sqrt(6)`.

The software does not infer a probability distribution from an unlabeled number.

## Provenance/validity gate

Every component requires explicit provenance class, provenance text, version/date, and validity state. Current accepted provenance classes are calibration certificate, manufacturer specification, literature, engineering assumption, and synthetic assumption. A missing provenance/version or a validity state other than `CURRENT`/`NOT_APPLICABLE` yields `INCOMPLETE`, never an implicit pass.

For real facility use, a calibration-certificate identifier and applicable configuration/range should be placed in `provenance`/`note`; v3.21 does not claim to validate certificate authenticity or scope automatically.

## Frozen synthetic verification fixture

The committed fixture is deliberately synthetic and exists only to test behavior.

Inputs, all dimensionless in `ln(Phi)`:

| Component | Synthetic declaration | Normalized 1-sigma | Correction amplitude | Shape |
|---|---:|---:|---:|---|
| responsivity scale | expanded `U=0.004`, `k=2` | 0.002 | 0.003 | common |
| detector linearity | rectangular half-width 0.0015 | 0.0008660254 | 0.0005 | linear/stretch |
| spectral shape | triangular half-width 0.004 | 0.0016329932 | 0.001 | centered quadratic |

Provenance class for all three is `synthetic_assumption`, version date `2026-08-26`. These are not NIST, facility, or vendor performance values.

The fixture uses the existing v3.18 17-point synthetic `Delta_n_curv=0.10` curve and independent 0.5 mV point-level `Voc` uncertainty.

### Nominal synthetic outputs

- recognized-axis correction changes curvature by `+0.002088789592`;
- absolute/reference systematic curvature standard uncertainty is `0.003367338539`;
- combined curvature standard uncertainty including the existing synthetic 0.5 mV `Voc` terms is `0.02267761879`;
- synthetic two-sided planning power for effect 0.10 is `0.9928506417`.

The existing v3.16 project engineering gate `|calibration curvature bias| <= 0.01` is reused as the deterministic-correction magnitude gate. This is a project gate, not a NIST requirement.

## Independent checks

### Common-scale limiting case

A perfectly common multiplicative intensity factor adds a constant to `ln(Phi)`. The derivative `dVoc/dln(Phi)` and therefore the curvature contrast must be invariant. The test sets a 1% common 1-sigma axis component and requires propagated curvature uncertainty below `1e-8`. This is a physical/algebraic limiting-case check independent of the nominal synthetic component mix.

### Nonlinear Monte Carlo

A separate standard-library Monte Carlo draws the latent systematic components, perturbs every corrected grid point through `Phi_i exp(sum_k l_ki z_k)`, and recomputes the full nonlinear v3.18 curvature estimator. Frozen seed: `20260826`; draws: `12,000`.

- first-order axis-only `u(Delta_n_curv) = 0.003367338539`;
- nonlinear Monte Carlo `u(Delta_n_curv) = 0.003400503601`;
- relative difference `0.9849%`.

Predeclared software-test tolerance: 3%. The check passes.

## Sensitivity

The synthetic spectral-shape term contributes >99.9% of the axis-systematic variance in the frozen stress fixture; the common responsivity scale is numerically negligible for the derivative curvature observable.

Doubling only the synthetic spectral-shape uncertainty gives:

- axis-systematic `u(Delta_n_curv) = 0.006734144131`;
- combined synthetic planning power `= 0.9895757637`.

The qualitative decision does not change in this synthetic fixture, but the dominant calibration investment is clear: improve intensity-dependent/spectral shape characterization before spending effort reducing a purely common scale term for this particular derivative measurand.

This dominance is model- and facility-dependent and must not be generalized without real component data.

## Statistical independence

External/common calibration components are systematic covariance terms, not independent experimental replicates. v3.21 gives no sample-size credit for repeated grid points, sweeps, pixels, or substrates. Repeatability covariance remains the separate v3.19/v3.20 program.

## Conventional/null explanations

An intensity-axis shape mode may arise from detector nonlinearity, spectral-responsivity mismatch, source-spectrum drift, range switching, temperature response, geometry, interpolation, or electronics. None is evidence about the DUT mechanism. The discriminator is independent calibration/reference characterization under the actual source/detector/configuration.

## Kill/narrow rules

Do not call the R2 curvature uncertainty budget complete if:

- a recognized calibration/reference systematic term lacks provenance or current applicability;
- a significant known correction is omitted rather than applied;
- the supplied component shape does not cover the actual intensity grid;
- deterministic correction changes `Delta_n_curv` by more than the existing 0.01 calibration-bias gate;
- nonlinear Monte Carlo and first-order propagation disagree materially at the measured uncertainty scale;
- repeatability and external/systematic components are double-counted or one is silently substituted for the other.

## Real-data handoff

For a facility campaign, populate the metadata with the actual calibration certificate/report identifiers, uncertainty convention and coverage factor, corrections, range/configuration scope, and date/version. Populate the shape table from the certificate/model/characterization used to map each component onto the 17 intensity points. The output sidecar can then be combined with empirically estimated repeatability components before v3.18 propagation.
