# R2 Facility Candidate Audit v3.28

## Purpose and claim class

This increment prospectively applies the merged v3.27 facility capability contract to three real organizations using only dated, public evidence available on 2026-08-27.

**Classification:** prospective public-evidence audit / engineering decision support. It is not a facility certification, measurement result, vendor quote, partnership statement, or evidence for an EPC/open-quantum mechanism.

The audited candidates are:

- National Laboratory of the Rockies PV Device Performance Calibration Services (`NLR_PVDPC`, public pages at `nrel.gov`);
- Institut Photovoltaïque d'Île-de-France (`IPVF`);
- Fraunhofer ISE CalLab PV Cells (`FRAUNHOFER_ISE_CALLAB`).

Candidate inclusion means only that public evidence indicated plausible relevance to the R2 metrology stack.

## Frozen method

The governing capability set is imported unchanged from `technical/data/r2_facility_capability_contract_v3_27.json`:

1. `reference_detector_traceability`;
2. `spectral_characterization`;
3. `linearity_characterization`;
4. `repeatability_campaign`;
5. `electrical_step_characterization`;
6. `optical_step_characterization`;
7. `voc_intensity_acquisition`.

Each candidate-capability pair is assigned exactly one status:

- `KNOWN_AVAILABLE`: the reviewed public source explicitly documents the material capability closely enough to support the v3.27 capability class;
- `NEEDS_CONFIRMATION`: public evidence is absent, incomplete, too generic, or does not establish the exact R2 configuration/provenance contract;
- `UNAVAILABLE`: a reviewed authoritative source explicitly rules the capability out.

Absence of public evidence is **not** `UNAVAILABLE`, and institutional reputation is never promoted to `KNOWN_AVAILABLE`.

## Quantitative summary

For candidate `c`, define publicly evidenced coverage

`f_c = K_c / C`,

where:

- `K_c` = number of v3.27 capabilities marked `KNOWN_AVAILABLE` for candidate `c`;
- `C = 7` = frozen number of required capability classes.

Both quantities are counts, so `f_c` is dimensionless. This is an evidence-completeness diagnostic, **not** a performance score or probability that a facility can execute R2.

Frozen result from the committed matrix:

| Candidate | KNOWN_AVAILABLE | NEEDS_CONFIRMATION | Public-evidence fraction |
|---|---:|---:|---:|
| NLR_PVDPC | 2 | 5 | 2/7 = 0.2857 |
| IPVF | 1 | 6 | 1/7 = 0.1429 |
| FRAUNHOFER_ISE_CALLAB | 2 | 5 | 2/7 = 0.2857 |

Across all three candidates, the union of capabilities explicitly confirmed by reviewed public evidence contains only two classes: reference-detector traceability and spectral characterization. Therefore public web evidence alone does not establish a complete R2 execution path at any candidate or even across this three-candidate set.

## Independent check

The primary calculation path is `tools/score_r2_facility_candidates_v3_28.py`, which imports the seven capability IDs directly from v3.27, checks exactly one row per candidate/capability, validates status vocabulary and dated HTTPS provenance, recomputes counts/fractions, and compares the result byte-semantically against the frozen JSON summary.

An independent arithmetic check uses the CSV matrix directly:

- NLR has two `KNOWN_AVAILABLE` rows: traceability and spectral characterization;
- IPVF has one: spectral characterization;
- Fraunhofer ISE has two: traceability and spectral characterization.

Thus the manually counted `K=(2,1,2)` and union-known count `2` agree with the executable summary exactly. Predeclared tolerance is exact integer equality; no floating-point scientific tolerance is required beyond representing the rational fractions.

## Limiting cases and semantic checks

Known limiting cases:

- if every row for a candidate were `KNOWN_AVAILABLE`, `f=1`;
- if none were, `f=0`;
- converting a `NEEDS_CONFIRMATION` row into `UNAVAILABLE` does not change `K` but materially changes partner strategy;
- converting one unresolved row to `KNOWN_AVAILABLE` increases `f` by exactly `1/7`.

The validator deliberately fails if the frozen summary claims a complete publicly confirmed candidate, if any candidate has zero unresolved capabilities, or if public-known union covers all seven capabilities. Those adversarial checks prevent optimistic interpretation of the current matrix.

## Uncertainty and sensitivity

The dominant uncertainty is **epistemic**, not sampling noise: public webpages do not necessarily enumerate custom measurement services, current scheduling, configuration flexibility, or willingness to execute a prospective research protocol.

No Gaussian confidence interval is appropriate for `f_c`. The uncertainty is represented directly by `NEEDS_CONFIRMATION`.

Sensitivity to unresolved items is simple and decision-relevant:

- NLR and Fraunhofer each require five status resolutions before a single-site full-stack execution can be confirmed;
- IPVF requires six;
- even combining all currently `KNOWN_AVAILABLE` rows leaves five of seven capability classes unresolved.

Therefore the decision **does not change** under any one-at-a-time optimistic status resolution: direct confirmation remains mandatory.

## Evidence provenance

Sources checked 2026-08-27 and recorded row-by-row in the CSV include:

### NLR / nrel.gov

- Primary Reference Cell Calibrations: `https://www.nrel.gov/pv/pvdpc/primary-reference-cell-calibrations`
- PV facilities: `https://www.nrel.gov/pv/facilities.html`
- PV work-with-us / partnership access: `https://www.nrel.gov/pv/work-with-us.html`
- NREL measurements/characterization technical material: `https://www.nrel.gov/docs/fy06osti/40123.pdf`

Public evidence supports traceable reference calibration and spectral-responsivity capability. Custom R2 repeatability, electrical-step, optical-step, linearity, and exact randomized `Voc` acquisition remain confirmation items.

### IPVF

- IQE Newport/Oriel system: `https://www.ipvf.fr/en/machines/iqe-newport-oriel/`
- Solar Simulator Newport/Oriel: `https://www.ipvf.fr/en/machines/solar-simulator-oriel/`

Public evidence supports wavelength-resolved EQE/IQE capability. The solar-simulator page documents `Voc`, a 4-wire source meter, and tunable illumination, but the published range is 0.1–1.1 suns rather than the frozen 0.05–2 sun R2 grid, so exact `Voc`-intensity execution remains `NEEDS_CONFIRMATION`. Reference-diode calibration is not treated as equivalent to the full v3.27 certificate/provenance contract.

### Fraunhofer ISE

- CalLab PV Cells: `https://www.ise.fraunhofer.de/en/rd-infrastructure/accredited-labs/callab/callab-pv-cells.html`
- Organic photovoltaics characterization: `https://www.ise.fraunhofer.de/en/business-areas/photovoltaics-materials-cells-and-modules/organic-photovoltaics.html`

Public evidence supports ISO/IEC 17025 calibration/certificates, spectral-responsivity measurement including organic/thin-film technologies, and broad OPV electro-optical characterization. The exact prospective R2 campaign and temporal-step/configuration requirements remain confirmation items.

## Conventional/null explanation

A candidate may actually possess every unresolved capability but omit it from public webpages. Conversely, a page may describe an instrument without guaranteeing that the exact R2 configuration, uncertainty, scheduling, raw-export, or prospective-freeze requirements can be offered.

The discriminator is a written capability confirmation against the exact v3.27 fields followed by a small preflight packet—not reputation, publication record, or equipment-brand inference.

## Statistical independence

This audit contains no device-level statistical inference. Candidate organizations are not experimental replicates, webpage entries are not observations of physical performance, and multiple pages from one organization do not increase statistical sample size.

The downstream experimental hierarchy remains `lot -> substrate -> device/pixel -> session -> sweep_or_step_replicate -> measurement`.

## Exclusion rule

No candidate was removed because of unfavorable coverage. A candidate may be removed from a later operational shortlist only if a dated authoritative response explicitly marks a decision-critical capability unavailable or a safety/provenance constraint incompatible.

## Safety/environmental boundary

This audit introduces no new fabrication or exposure. Any later execution remains subject to facility optical/electrical interlocks, source-duty limits, instrument ratings, thermal constraints, material-handling SOPs, shipping/import controls, and waste requirements.

## Decision

**Do not select a facility based on public evidence alone.** Send the same frozen capability-confirmation packet to all three candidates, focusing on the five capability classes not publicly confirmed anywhere in the audited set: linearity characterization, prospective repeatability campaign, electrical-step characterization, optical-step characterization, and exact `Voc`-intensity acquisition.

This preserves a fair, falsifiable partner-selection process and avoids converting web discoverability into imagined laboratory capability.

## Single best next increment

Create and send a versioned, identical confirmation questionnaire derived mechanically from v3.27, with yes/no/conditional responses, configuration limits, raw-export fields, uncertainty/provenance deliverables, scheduling constraints, and a source document/upload field. Score only returned evidence; do not alter requirements after seeing which facility responds favorably.
