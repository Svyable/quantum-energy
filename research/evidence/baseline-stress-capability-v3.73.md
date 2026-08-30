# Evidence note — v3.73 baseline stress capability

## Established metrology basis

- NIST TN 1297 distinguishes repeatability from reproducibility and recommends quantitative statements of dispersion under stated conditions rather than using vague precision labels: https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-d1-terminology
- The NIST/SEMATECH measurement-process handbook explicitly covers repeatability, reproducibility, stability, calibration and uncertainty characterization: https://www.nist.gov/publications/nistsematech-engineering-statistics-handbook-chapter-2-measurement-process
- Reese et al., *Consensus stability testing protocols for organic photovoltaic materials and devices*, Solar Energy Materials and Solar Cells 95 (2011), DOI `10.1016/j.solmat.2011.01.036`, provides the OPV ISOS research framework separating dark, light and other stress categories.

## Program evidence already established

- v3.70 created donor-free A0/A2 controls to test whether PY-IT effects can occur without D18.
- v3.71 introduced the dual-path resilience hypothesis and explicitly narrowed donor-free eC9 electrical interpretation pending architecture qualification.
- v3.72 preregistered A0/A2/B0/B2 stress tomography under thermal and operational-light stresses with fail-closed physical thresholds.

## v3.73 changed evidentiary state

v3.73 does **not** add treatment evidence. It creates a baseline-only measurement-capability gate so future A2/B2 effect margins and sample counts can be frozen using real A0/B0 lot-level repeatability rather than synthetic fixture numbers.

## Engineering assumptions

- Lot-level log-retention dispersion of A0/B0 is a useful first proxy for the scale of future four-arm interaction uncertainty.
- Future treatment-arm SD may differ; v3.73 therefore reports variance-multiplier scenarios rather than a single claimed power value.
- Five baseline lots are preferred for the first capability estimate, while three is the minimum accepted for computation.

## Synthetic/model results

The committed fixture intentionally produces `s_base ~= 0.0191624633`. Under the explicit `m=1`, `n=5` planning scenario, the approximate interaction MDE is `0.0480175688` in log units, equivalent to a ~4.9% ratio-of-ratios departure.

These values are **software verification only** and are not physical pass thresholds.

## Strong claim boundary

A narrow baseline dispersion demonstrates only that the baseline process may be measurable enough to justify a treatment experiment. It does not establish dual-path generation, PY-IT causality, useful-work improvement, durability, or any quantum mechanism.
