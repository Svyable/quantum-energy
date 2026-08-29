# v3.67 — D18/PY-IT/eC9 stabilized-output evidence boundary

## Changed evidentiary state

**Claim class: established-evidence boundary / useful negative result.** The primary D18/PY-IT/eC9 anchor supports scanned J–V performance and mechanism evidence for the optimized 1:0.2:1 device, including a reported ~20 meV Voc increase, >18% efficiency, and no sacrifice in Jsc or FF. The inspected primary-article Methods specify a Keysight B2901A J–V measurement under AM1.5G, 0.041 cm² illuminated area, and about 5 ms delay per voltage point. The inspected article does not establish stabilized maximum-power tracking or a stabilized Pmax value.

Therefore the anchor **does not by itself satisfy** this repository's useful-work gate, which requires stabilized Pmax improvement with the required independent-lot hierarchy. This is not evidence that the device is unstable or that its scanned performance is wrong.

## Provenance

Primary source: Luo Y. et al., *Nature Communications* 17 (2026), DOI `10.1038/s41467-026-68731-7`, published 2026-01-26; version of record 2026-02-26. The article's data-availability statement points to Figshare DOI `10.6084/m9.figshare.29390669` and states that supporting data are in the main text and Supplementary Information, with additional data available on request.

Retrieval/audit date: 2026-08-28.

This increment does not redistribute upstream source data or code.

## Quantitative check

The only decision-driving conversion is

` t_s = t_ms / 1000 `

with `t_ms = 5 ms`, giving `t_s = 0.005 s`. Units: `ms × (1 s / 1000 ms) = s`. The executable independently recomputes the conversion with exact rational arithmetic and requires agreement within `1e-12`.

The scan delay is **not** converted into a full sweep time because the voltage sequence/number of points is not fixed sufficiently by the inspected sentence. Doing so would create false precision.

## Decision rule

The classifier deliberately separates two questions:

1. Does the source show high scanned device performance? **Yes.**
2. Does that source alone establish the project's stabilized useful-work gate? **No.**

A source-verifiable stabilized Pmax/MPPT measurement on the target chemistry can supersede or narrow this boundary. For project-level useful-work promotion, the existing ≥3-independent-lot hierarchy remains required; this increment does not invent a new physical threshold.

## Independent and negative checks

Run:

```bash
python models/d18_pyit_ec9_stabilized_output_bound_v367.py
```

Expected output includes `5 ms = 0.005000 s`, exact-arithmetic agreement, and classification as `scan_or_incomplete_output_evidence_only`.

Fixtures:

- limiting case: stabilized output + 3 independent lots becomes eligible for useful-work gate evaluation;
- negative control: arbitrarily strong scan performance without stabilized output remains incomplete;
- independence control: stabilized output on only two lots remains incomplete for the existing project gate.

The latter fixtures test logic only and are not physical measurements.

## Uncertainty, sensitivity, and validity domain

No measurement uncertainty for the approximate 5 ms delay is supplied in the inspected text, so no confidence interval is fabricated. The scientific decision is insensitive to plausible small uncertainty in that delay because the classification turns on the **type of output evidence**, not whether the delay is exactly 5 ms.

Validity domain: this is an evidence audit of the inspected primary article/main-text Methods and its data-availability statement. Absence of stabilized-output evidence there does not prove that supplementary, unpublished, requested, or later measurements do not exist.

## Conventional explanations / failure modes

At least three conventional reasons scanned and stabilized output can differ remain live:

1. transient/capacitive scan response or scan-direction/rate effects;
2. operating-point relaxation, light soaking, or degradation under sustained load;
3. ordinary device/lot variation or contact/transport variability.

This increment does not establish that any of them occurs in D18/PY-IT/eC9. It establishes that they remain unbounded by the anchor's scanned J–V evidence.

## Technical and business delta

Do not promote >18% scanned anchor efficiency to sustained useful-work evidence. The next target-chemistry campaign should acquire stabilized Pmax on the same lot/device hierarchy used for field-generation and transport/contact controls. This keeps the commercial bridge tied to sustained electrical work rather than a favorable microscopic or scan-only proxy.

## Falsifier / next physical measurement

The boundary is narrowed or retired by provenance-complete target-chemistry stabilized maximum-power traces (or an independently justified stabilized-output equivalent), with device identities, lot hierarchy, operating conditions, exclusions, raw/minimally processed data, and repeatability sufficient to evaluate the existing useful-work gate.
