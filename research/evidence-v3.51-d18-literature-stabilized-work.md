# v3.51 — D18/PY-IT/eC9 literature stabilized-work audit

Date: 2026-08-28  
Run-base `main`: `9e61f8d761cc30b5ba12eef36c9935c35591c8f5`

## Changed evidentiary state

**Claim class: derived evidence-bound / useful negative result.**

The primary D18/PY-IT/eC9 paper does **not**, on the evidence inspected here, satisfy this repository's stabilized-useful-work gate. The paper reports the optimized 1:0.2:1 device using a J–V curve and describes J–V acquisition with about 5 ms delay per voltage step. The repository gate, by contrast, requires a relative improvement in **stabilized `Pmax`** across independent fabrication lots. Therefore the literature champion result remains mechanism/champion-scan evidence and must not be promoted to project useful-work validation merely because its scan PCE is favorable.

This is intentionally narrower than saying the published efficiency improvement is unreal. It says the measurement object required by the project gate is different from the measurement object explicitly reported in the inspected primary-source text.

## Primary-source provenance

Primary article: Yongmin Luo et al., *Suppressing electron-phonon coupling and energy loss in organic solar cells by modulating donor-acceptor penetrated-interface*, Nature Communications 17 (2026), DOI `10.1038/s41467-026-68731-7`.

Stable source: <https://www.nature.com/articles/s41467-026-68731-7>

The inspected primary-source text states that:

- Fig. 5f is the J–V curve of the optimized D18-PYIT-eC9 1:0.2:1 pseudo-BHJ ternary device;
- the optimized device has about 20 meV higher `Voc`, over 18% efficiency, and no sacrifice in `Jsc` and FF;
- J–V measurements used a Keysight B2901A under AM1.5G with approximately 5 ms delay time per voltage step;
- the paper reports data DOI `10.6084/m9.figshare.29390669`.

No value in this packet is treated as a stabilized-MPP result unless an actual time-series/protocol supporting that classification is supplied.

## Governing decision model

Let

- `R` = whether the project gate requires stabilized `Pmax` evidence;
- `S` = whether the inspected evidence packet contains a stabilized-MPP trace with sufficient provenance;
- `E` = eligibility of the literature result for evaluation against the stabilized-work gate.

The fail-closed rule is

`E = (not R) OR S`.

For canonical `main`, `R = True`. For the inspected primary paper text, `S = False`. Therefore `E = False`.

An independent set-containment derivation reaches the same decision: the strong gate requires evidence tokens `{paired_power_metric, stabilized_mpp}` while the inspected literature packet supplies a scanned paired power/performance metric but not `stabilized_mpp`; the required set is therefore not a subset of the observed set.

This is Boolean evidence logic, not a physical performance model. There are no stochastic parameters, fitted material constants, or uncertainty distributions.

## Units, limiting cases, and validity domain

The decision itself is dimensionless. The reported ~5 ms value is retained only as an acquisition-setting fact; it is **not** converted into a device stabilization time, dwell requirement, or durability metric.

Limiting/control checks:

1. If the project did not require stabilized `Pmax`, the absence of stabilized MPP would not exclude the literature result on this criterion.
2. If a provenance-complete stabilized-MPP trace is later supplied, the present eligibility decision flips to permit evaluation; the result still must pass the numerical power, lot-independence, field-generation, and durability gates.
3. A high scanned PCE cannot mathematically substitute for missing time-domain stabilization evidence because it is a different evidentiary variable, not merely an uncertain value of the same variable.

Validity domain: this audit concerns only eligibility for the repository's **stabilized-useful-work** claim. It does not adjudicate the paper's spectroscopy, morphology, EPC, charge-generation, `Voc`, or scan-efficiency conclusions.

## Uncertainty and sensitivity

The dominant uncertainty is source completeness, not numerical uncertainty. The inspected main article does not expose a stabilized-MPP trace. Supplementary information, an updated public data deposit, or author-released data could contain additional evidence. The decision is therefore falsifiable and reversible if such primary-source evidence is produced.

Sensitivity to the repository's numeric 5% gain threshold is **none** for this eligibility result: while stabilized evidence is absent, changing the gain threshold cannot convert a scanned J–V result into stabilized MPP evidence. If stabilized data become available, the numeric gate then becomes relevant.

## Statistical independence

No new device observations are analyzed. The literature champion device is not counted as an independent fabrication lot, and repeated scan points are not treated as independent devices. This increment therefore does not satisfy the repository's `>=3` independent-lot requirement.

## Serious failure modes / conventional explanations

1. **Uninspected supplementary/author data may contain stabilized MPP.** This is the strongest way this negative result could be falsified. Discriminator: retrieve a primary-source stabilized MPP time series with device identity and measurement conditions, then rerun the gate.
2. **A J–V scan can agree with stabilized MPP for a well-behaved device.** Even if physically true for these devices, agreement must be demonstrated rather than assumed; otherwise scan-to-stabilized equivalence is an unsupported engineering assumption.
3. **The observed performance gain may be real but conventional.** Morphology, thickness, contacts, transport, optical absorption, or other ordinary device changes may contribute. This audit does not assign causality to EPC.

Failure mode 1 is bounded in the current increment only to the inspected primary main text and reported data citation. It remains open for supplementary/author-released material.

## Reproduction packet

Machine-readable input/decision contract:

`machine/d18-literature-stabilized-work-audit-v3.51.json`

Executable standard-library check:

```bash
python3 models/d18_literature_stabilized_work_audit_v351.py
```

Expected marker:

`D18_LITERATURE_STABILIZED_WORK_AUDIT_V3.51: PASS`

Expected classification:

`MECHANISM_OR_CHAMPION_SCAN_EVIDENCE_ONLY`

CI target versions: Python 3.12, 3.13, and 3.14.

## Corrections / superseded claims

No experimental result is corrected. This **narrows interpretation** of the literature bridge: favorable champion scan efficiency and `Voc` evidence are not stabilized-useful-work validation. Open PR #43's voltage-only bound remains complementary rather than superseded.

## Decision consequence

Do not use the paper's champion J–V/PCE result as evidence that the repository's `>=5%` stabilized-`Pmax`, `>=3`-lot gate has been met. Keep it as mechanism and scan-performance precedent. A prospective project campaign still needs full stabilized-MPP traces, contemporaneous B0 controls, independent fabrication lots, field-generation measurements, and durability evidence.

## Single best next increment

Obtain a real **B0-only stabilized-MPP baseline time series** under prospectively recorded illumination, temperature, area/contact, and tracking conditions, and use its empirical behavior to freeze stabilization/tracking rules before B1/B2 unblinding. That physical baseline is more decision-relevant than further champion-curve archaeology unless primary stabilized literature data become available.
