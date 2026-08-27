# Evidence note — R2 absolute/reference systematics v3.21

## Established evidence

Checked 2026-08-26.

1. NIST TN 1297 section 4 treats calibration reports, manufacturer specifications, previous data, and other relevant information as legitimate inputs to Type-B uncertainty evaluation. A quoted uncertainty stated as a multiple of a standard deviation is converted by dividing by that multiplier. For symmetric bounded inputs, rectangular and triangular models give standard uncertainties `a/sqrt(3)` and `a/sqrt(6)` respectively.
   - https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-4-type-b-evaluation-standard-uncertainty
2. NIST TN 1297 section 5 states that recognized significant systematic effects should be corrected and that the uncertainty of the applied correction belongs in the combined standard uncertainty; covariance is included as appropriate.
   - https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-5-combined-standard-uncertainty
3. NIST TN 1297 section 6 defines expanded uncertainty `U = k u_c`.
   - https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-6-expanded-uncertainty
4. The BIPM/JCGM publication index currently lists JCGM 100:2008, JCGM 101:2008, and JCGM 100:2008/Amd.1:2026 on nonlinearity in measurement models.
   - https://www.bipm.org/en/committees/jc/jcgm/publications

These sources support the metrology method only. They do not establish any R2 detector accuracy, OPV performance, EPC effect, or quantum-mechanism claim.

## Engineering assumptions

- The facility can express each material external systematic as a signed loading across the frozen intensity grid.
- A component ID represents one perfectly correlated latent uncertainty source; different component IDs are independent unless a richer decomposition is supplied.
- The existing v3.16 `|Delta_n_curv calibration bias| <= 0.01` project gate is reused for the magnitude of recognized deterministic correction.
- `CURRENT`/`NOT_APPLICABLE` validity states are manually asserted metadata; software does not authenticate calibration certificates.

## Synthetic/model result

The committed v3.21 stress fixture is not measured data. It uses synthetic common-scale, stretch/nonlinearity, and quadratic spectral-shape components to verify normalization, correction, covariance propagation, limiting cases, sensitivity, and nonlinear Monte Carlo agreement.

Nominal synthetic axis-systematic `u(Delta_n_curv)=0.003367338539`; independent 12,000-draw nonlinear Monte Carlo gives `0.003400503601`, a 0.9849% difference inside the frozen 3% software-check tolerance.

## Negative/useful result

For the derivative-based curvature measurand, a perfectly common multiplicative intensity-scale uncertainty cancels to numerical precision. In the frozen stress fixture the intensity-dependent spectral-shape component contributes >99.9% of axis-systematic variance. This is a synthetic sensitivity result, not a statement about any real facility.

## Falsifiable hypothesis

A real facility's externally supported calibration/reference components, when mapped onto the actual 17-point grid and combined with empirical repeatability covariance, will produce a complete uncertainty budget whose nonlinear propagation agrees with first-order propagation within a preregistered tolerance and whose recognized deterministic correction remains within the existing 0.01 curvature-bias gate.

## Conventional explanations / discriminator

Calibration-axis shape can be caused by ordinary detector nonlinearity, spectral responsivity, source-spectrum drift, range switching, temperature, geometry, interpolation, or electronics. Independent reference characterization under the actual measurement configuration distinguishes these measurement-system effects from DUT physics.

## Evidence level

v3.21 is **cross-checked software/metrology infrastructure on synthetic inputs**. No real calibration certificate or facility dataset has yet been propagated through it.
