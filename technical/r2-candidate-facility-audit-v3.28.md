# R2 candidate-facility audit v3.28

Date: 2026-08-27

## Claim class and purpose

**Engineering evidence audit.** This is a prospective audit of public facility capability evidence against the merged v3.27 R2 facility contract. It is not a ranking, endorsement, vendor quote, booking confirmation, experimental result, or proof that any facility will accept the requested work.

The candidate set is intentionally small and evidence-driven: NREL Photovoltaic Device Performance Calibration Services, Fraunhofer ISE CalLab PV Cells, and Institut Photovoltaïque d'Île-de-France (IPVF). They were selected because public primary facility pages expose multiple relevant PV metrology capabilities. No score is used to convert unknowns into certainty.

## Frozen status semantics

- `PUBLICLY_SUPPORTED`: a dated primary facility page directly supports the capability class, but execution still requires configuration-specific confirmation.
- `PARTIAL_PUBLIC_SUPPORT`: related capability is public, but at least one material v3.27 requirement is not established.
- `NEEDS_CONFIRMATION`: public evidence reviewed does not establish the requested capability. This is not a negative claim that the facility lacks it.

These are pre-contact evidence states, not v3.27 scientific `PASS/FAIL/INCOMPLETE` outcomes. Actual execution remains `INCOMPLETE` until the required packet evidence exists.

## Sources reviewed

### NREL

- Primary reference cell calibration: https://www.nrel.gov/pv/pvdpc/primary-reference-cell-calibrations
- PV facilities: https://www.nrel.gov/pv/facilities.html
- Measurements and Characterization documentation: https://www.nrel.gov/docs/fy06osti/40123.pdf

Public evidence supports reference-cell traceability, spectral responsivity/QE, spectral mismatch workflows, organic-PV/electro-optical characterization, and a dedicated linearity test bed. Public pages do **not** establish willingness to execute the frozen R2 multi-session holdout, custom electrical reference-step, optical settling, or randomized 17-point protocol.

### Fraunhofer ISE CalLab PV Cells

- CalLab PV Cells: https://www.ise.fraunhofer.de/en/rd-infrastructure/accredited-labs/callab/callab-pv-cells.html
- Photonic/electronic power devices: https://www.ise.fraunhofer.de/en/business-areas/photovoltaics-materials-cells-and-modules/photonic-and-electronic-power-devices.html

Public evidence supports ISO/IEC 17025 calibration, certificate generation, 300–2000 nm spectral responsivity, experience with organic/thin-film cells, and measurements under variable spectra/intensities. The exact v3.27 linearity, repeated-session holdout, electrical-step, optical-step, and randomized-order requirements require direct confirmation.

### IPVF

- IQE Newport/Oriel: https://www.ipvf.fr/en/machines/iqe-newport-oriel/
- FTPS: https://www.ipvf.fr/machines/ftps/
- Solar simulator: https://www.ipvf.fr/en/machines/solar-simulator-oriel/
- Custom optical benches: https://www.ipvf.fr/en/machines/optical-benches/

Public evidence supports 300–1800 nm EQE/IQE with reference-diode calibration and light bias, FTPS access, and calibrated SMU-based solar-cell characterization. The published simulator range is 0.1–1.1 suns, narrower than the frozen R2 0.05–2 sun grid, so the full R2 intensity protocol is not publicly established. Custom benches may close gaps but require direct confirmation.

## Result

No candidate is classified as execution-ready from public evidence alone. That is a useful negative result: sophisticated PV characterization capability is not equivalent to satisfying the full v3.27 provenance, temporal-fidelity, prospective-holdout, spectral, and randomized-acquisition contract.

The machine-readable row-level audit is `research/data/r2_candidate_facility_audit_v3_28.csv`.

### Evidence-count summary

There are 7 capability classes per facility, 21 facility-capability rows total.

| Facility | Publicly supported | Partial public support | Needs confirmation |
|---|---:|---:|---:|
| NREL PVDPC | 3 | 1 | 3 |
| Fraunhofer ISE CalLab PV Cells | 2 | 1 | 4 |
| IPVF | 1 | 2 | 4 |

These counts are descriptive only. They are **not weighted scores** and must not be used as a procurement ranking because the unknown capabilities differ materially in scientific importance.

Independent arithmetic check: each row group sums to 7 and the three groups sum to 21. No stochastic calculation is used.

## Frozen direct-confirmation questions

Before scheduling, send the same capability questions to each candidate and preserve the dated response/source:

1. Can the facility provide the calibration certificate/report and raw responsivity metadata for the exact reference detector used in the R2 run?
2. Can it acquire wavelength-resolved source spectra at every frozen intensity and export raw spectra plus DUT/reference responsivity on declared wavelength grids?
3. Can it characterize detector/source linearity across 0.05–2 sun under the exact acquisition geometry?
4. Can it execute 30 separated reference sessions as 24 training + 6 untouched prospective holdout, preserving session/day/sweep hierarchy?
5. Can it inject a characterized ~100 mV electrical step through the exact SMU/digitizer/cabling/software path with fixed range/filter/aperture and autorange disabled?
6. Can it record repeated 0.05 ↔ 2 sun optical/DUT step transients on one qualified pixel with raw timestamps extending beyond the intended dwell?
7. Can it execute both the frozen monotonic and randomized 17-point Voc-intensity schedules on the same pixel with raw timestamped exports?
8. Can all raw files, configuration identifiers, exclusions, and provenance be returned in the v3.27 packet structure without silent preprocessing or row deletion?

Any unresolved answer remains `INCOMPLETE`; a generic statement such as “we perform PV characterization” is not sufficient evidence.

## Conventional/null explanation and discriminator

**Conventional explanation:** a candidate may appear highly capable because it performs accredited PV calibration or advanced spectroscopy, while the specific R2 custom temporal/randomization/holdout workflow is operationally unavailable.

**Discriminator:** configuration-specific written confirmation followed by a dry-run packet containing the required roles and frozen identifiers. Facility reputation or instrument ownership cannot substitute for that evidence.

## Statistical independence

This audit introduces no scientific sample-size credit. Facility pages are evidence sources, not experimental replicates. The R2 hierarchy remains `lot -> substrate -> device/pixel -> session -> sweep or step replicate -> measurement`. A multi-facility split additionally creates a facility/configuration factor that must not be pooled away without a bridge study.

## Uncertainty and sensitivity

Capability uncertainty is categorical because assigning numerical probabilities would be unsupported. Sensitivity is handled by preserving every material unknown rather than averaging it into a readiness score. A single unresolved prerequisite can keep a downstream gate `INCOMPLETE` even if all other capabilities are strong.

## Safety and shipping

This audit does not authorize sample shipment or operation. Candidate-facility EHS, shipping, electrical, optical, thermal, interlock, and sample-acceptance rules control. Organic-device encapsulation/stability requirements and any hazardous-material declarations must be resolved before shipment.

## Decision

Proceed to standardized direct confirmation; do not yet schedule the full R2 campaign. The preferred outcome is one facility that can preserve a single configuration and provenance chain. If no facility can do so, define the smallest multi-facility split and require an explicit bridge measurement before combining uncertainty components.
