# v3.53 — D18/PY-IT/eC9 public-data reproducibility boundary

## Changed evidentiary state

**Claim class: reproducibility boundary / useful negative result.**

The inspected primary public package does not justify calling the D18/PY-IT/eC9 ternary useful-work evidence independently reproducible from public raw machine-readable data. The Nature Communications article states that all data supporting the findings are available in the main text and Supplementary Information, while additional data are available from the corresponding author on request. PMC lists the Supplementary Information as a 34.3 MB PDF. This is a narrower claim than "data absent": raw/minimally processed data may exist privately or may later be deposited.

Primary article: Luo et al., *Nature Communications* 17, 2026 (2026), DOI `10.1038/s41467-026-68731-7`, published 2026-01-26, version of record 2026-02-26. Reported data DOI: `10.6084/m9.figshare.29390669`. PMC: `PMC12946207`.

## Decision rule

Independent public raw-data reproduction eligibility requires all of:

1. public raw or minimally processed values;
2. sample/device identity sufficient to preserve hierarchy;
3. machine-readable values rather than figure-only extraction;
4. a deterministic processing path from the deposited values to the decision metric.

Observed in this run: main article and Supplementary Information PDF are publicly exposed, but the inspected public metadata did not establish the other three prerequisites. Status: `NOT_INDEPENDENTLY_REPRODUCIBLE_FROM_PUBLIC_RAW_DATA`.

This status does **not** dispute the paper's experimental findings and does not establish that raw data do not exist.

## Verification

Run:

```bash
python models/d18_public_data_reproducibility_v353.py
```

Expected markers:

```text
D18_PUBLIC_DATA_REPRODUCIBILITY_V3.53: PASS
NOT_INDEPENDENTLY_REPRODUCIBLE_FROM_PUBLIC_RAW_DATA
```

The executable uses Boolean set/prerequisite logic only; there is no stochastic model, physical threshold, measurement uncertainty, or fitted parameter. A negative fixture proves that adding only a raw-data flag while sample identity/processing remain missing stays fail-closed. A limiting positive fixture passes only when all required prerequisites are present.

## Strongest conventional explanations / failure modes

1. The corresponding author may supply complete raw/minimally processed data on request. That would revise this status and should be preserved as a visible update.
2. The Supplementary PDF may contain enough tabulated values to reconstruct some claims even if a raw device-level dataset is unavailable. That would permit a narrower reconstruction but still would not automatically establish raw-data reproduction.
3. The Figshare DOI may expose additional structured assets through an interface not successfully inspected in this run. This is why the claim is explicitly about the **inspected public package**, not universal absence.

## Consequence

Do not label the ternary field-generation, stabilized-Pmax, or lot-level useful-work literature result as `reproduced` from public raw data. The anchor remains literature evidence/motivation until a provenance-complete dataset and processing path are independently rerun.

## Falsifier / next physical discriminator

The reproducibility-boundary result is falsified by a public provenance-complete raw/minimally processed dataset with sample/device identities and a deterministic processing path sufficient to reconstruct a ternary decision metric. Programmatically, however, the highest-value next physical increment remains a blinded B0 field-generation or stabilized-MPP baseline rather than further narrative interpretation of champion figures.
