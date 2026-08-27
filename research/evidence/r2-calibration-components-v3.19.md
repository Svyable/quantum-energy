# Evidence note — empirical calibration components v3.19

## Established metrology basis

JCGM 100:2008 section 5.2 states that significant correlations between input quantities must be included. Section 5.2.5 further notes that covariances can be evaluated experimentally when feasible and that common influences can be introduced as explicit independent input quantities.

- BIPM JCGM 100: https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf

NIST TN 1297 states that recognized systematic effects that significantly influence a result should be corrected, or otherwise appropriately included in the uncertainty evaluation, and that combined uncertainty uses covariance where appropriate.

- NIST TN 1297 section 5: https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-5-combined-standard-uncertainty

JCGM 101 provides Monte Carlo propagation as a separate route for nonlinear measurement models.

- https://www.bipm.org/en/doi/10.59161/jcgm101-2008

## Established program facts

- v3.16 showed common intensity scale and intensity-axis shape have very different effects on the derivative curvature observable.
- v3.17 preserved calibration correlation-group metadata.
- v3.18 converted explicit signed covariance components into propagated `Delta n_curv` standard uncertainty and planning power.

## Engineering assumptions

- A scale/stretch/quadratic basis is an adequate first low-order model for repeated calibration sweeps only if held-out and residual diagnostics pass.
- At least eight independent calibration runs are required before the empirical model can return PASS.
- The current LOSO/residual thresholds are project gates, not standards-derived limits.
- The deconvolution `C_between = C_observed - sigma_res^2 (X^T X)^-1` assumes the pooled point residual model is appropriate.

## Hypothesis

Repeated reference-detector sweeps can estimate enough of the facility's run-to-run covariance structure to replace hand-assigned calibration repeatability modes in the v3.18 power calculation.

## Important non-identifiability

Absolute systematic calibration bias of the reference detector is not identifiable from repeated measurements with that same detector. It must remain a separate externally supported calibration/Type-B term.

## Claim boundary

The v3.19 synthetic results validate the decomposition software and its falsification checks only. They do not establish any real facility uncertainty, R2 performance, recombination mechanism, EPC effect, or open-quantum transport phenomenon.
