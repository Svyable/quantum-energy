# Evidence note — weak-EL public data interoperability v3.12

## FAIR Guiding Principles

Wilkinson et al., *Scientific Data* 3, 160018 (2016), DOI `10.1038/sdata.2016.18`.

Program use:
- machine-actionable metadata should describe data and the workflows needed to reuse them;
- provenance and explicit data-usage terms support reusability;
- FAIR principles guide implementation but are not themselves a file-format standard.

Source: https://doi.org/10.1038/sdata.2016.18

## NIST Technical Note 1297

Taylor and Kuyatt, *Guidelines for Evaluating and Expressing the Uncertainty of NIST Measurement Results*.

Program use:
- standard uncertainty is expressed as an estimated standard deviation;
- correlated components require covariance/correlation treatment;
- recognized systematic effects should be corrected or explicitly accounted for;
- measurand definition and units must remain explicit.

Source: https://www.nist.gov/pml/nist-technical-note-1297

## Internal synthetic check

The v3.12 2-nm fixture is deliberately constructed so the correct bin-density transform returns `6e10 photons/s`, whereas omitting the bin-width conversion returns `1.2e11 photons/s`. The exactly 2x discrepancy is synthetic/unit-test evidence only.

## Claim boundary

The new schema is project-specific. Do not describe it as an established community standard. Its value must be tested by asking real facilities to export data without custom hand editing.
