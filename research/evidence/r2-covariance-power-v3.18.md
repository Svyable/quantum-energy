# Evidence note — covariance-aware R2 uncertainty v3.18

## Established metrology basis

- JCGM 100:2008, section 5.2, states that significant correlations between input quantities must be accounted for in combined uncertainty. For correlated inputs, the combined variance includes covariance terms rather than an independence-only RSS.
  - BIPM: https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf
- JCGM 101:2008 covers propagation of probability distributions using Monte Carlo methods.
  - BIPM: https://www.bipm.org/en/doi/10.59161/jcgm101-2008
- The BIPM JCGM publication list includes JCGM 100:2008/Amd.1:2026 on nonlinearity in measurement models.
  - https://www.bipm.org/en/committees/jc/jcgm/publications
- NIST TN 1297 likewise describes combined standard uncertainty using individual standard uncertainties and covariances as appropriate.
  - https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-5-combined-standard-uncertainty

## Established program facts

- v3.15 froze the 17-point 0.05–2 sun local-ideality curvature observable and showed 0.5 mV point-level `Voc` noise implies `u(Delta n)=0.0224200905` and synthetic planning power `0.993795964` for a 0.10 effect.
- v3.16 identified calibration-axis shape, not common intensity scale alone, as the relevant systematic for derivative curvature.
- v3.17 preserved calibration uncertainty groups but only summarized them; it did not yet propagate their covariance into `Delta n_curv`.

## Engineering assumptions

- v3.18 treats rows sharing a component ID as perfectly correlated through one latent standard-normal component.
- First-order finite-difference propagation is assumed adequate only when verified against Monte Carlo at the relevant uncertainty magnitude.
- The explicit synthetic stress modes (0.5% common, independent, and quadratic axis uncertainty; 0.5 mV `Voc`) are verification scenarios, not measured facility uncertainties.

## Hypothesis

A covariance-aware model will materially improve the integrity of the power decision by preventing common-mode uncertainties from being double-counted while preserving shape/nonlinearity components that actually affect the derivative observable.

## Novel/open implementation concept

The component sidecar is an open, facility-neutral way to encode measurement-error modes as signed loadings on shared latent components. It is not claimed as novel IP.

## Claim boundary

This increment validates uncertainty propagation software and representation. It does not validate any real facility covariance, detector physics, recombination mechanism, EPC effect, or energy-conversion performance.
