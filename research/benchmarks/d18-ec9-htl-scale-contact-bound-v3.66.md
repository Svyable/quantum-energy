# v3.66 — D18/BTP-eC9 HTL scale/contact confound bound

## Changed evidentiary state

**Established external evidence:** Li et al. (2026) report D18/BTP-eC9 devices using either pristine PEDOT:PSS or a beta-CuI-DPA/PEDOT:PSS (`beta-P`) hole-transport layer, including 1 cm^2 devices. Table 1 reports a materially different large-area penalty depending on HTL.

**Project inference:** contact/interlayer state is therefore a decision-relevant conventional explanation for apparent composition/interface gains during D18-family scale transfer. B0/B1/B2 useful-work attribution must hold contacts/interlayers fixed (or factorially randomize them) and audit contact/transport behavior. This does **not** show that the project's EPC hypothesis is false; it removes permission to infer EPC causality from PCE/FF changes without bounding contact effects.

## Primary source / version

Yanxun Li, Weichao Zhang, et al., *Topology-Engineered Coordination Polymers for Enhanced Hole Transport in Organic Solar Cells*, **Angewandte Chemie International Edition** 65 (2026) e9811085. DOI `10.1002/anie.9811085`; Version of Record online 2026-05-26; PMCID `PMC13383085`. Values below are printed Table 1 values. No upstream code is copied.

## Inputs and claim classes

All numerical inputs are **literature-derived experimental summaries**, not measurements by this project. Machine-readable values and provenance are frozen in `d18-ec9-htl-scale-contact-bound-v3.66.json`.

For D18/BTP-eC9:

| HTL | area class | Voc (V) | Jsc (mA cm^-2) | FF (%) | PCE (%) |
|---|---:|---:|---:|---:|---:|
| PEDOT:PSS | source small-area | 0.868 | 26.72 | 75.71 | 17.55 |
| PEDOT:PSS | 1 cm^2 | 0.860 | 25.77 | 67.92 | 15.06 |
| beta-P | source small-area | 0.877 | 27.41 | 77.45 | 18.62 |
| beta-P | 1 cm^2 | 0.869 | 26.36 | 73.37 | 16.82 |

The source describes beta-P as improving PEDOT:PSS stacking, longitudinal conductivity and work function; it also reports active-layer/interfacial changes. Consequently this comparison is **not mechanism-pure**.

## Governing arithmetic and dimensional audit

For each HTL, define dimensionless scale retention

`R_s = PCE_large / PCE_small`

and scale drop `D_s = 1 - R_s`. Define the large-area relative PCE gain from changing HTL as

`G_HTL = PCE_betaP,large / PCE_PEDOT,large - 1`.

All ratios use the same PCE units, so they are dimensionless. The FF comparison is an absolute percentage-point difference.

Reproduced values:

- PEDOT:PSS scale retention: `15.06/17.55 = 0.8581196581` (**85.81%**), scale drop **14.19%**.
- beta-P scale retention: `16.82/18.62 = 0.9033297530` (**90.33%**), scale drop **9.67%**.
- HTL-associated scale-retention difference: **4.521 percentage points**.
- At 1 cm^2, beta-P vs PEDOT:PSS: PCE **+11.69% relative**, FF **+5.45 percentage points**, Voc **+9 mV**, Jsc **+2.29% relative**.

These are descriptive source-table comparisons. They are neither confidence intervals nor a causal decomposition of PCE.

## Independent check and controls

`python models/d18_ec9_htl_scale_contact_bound_v366.py`

uses standard-library floating-point arithmetic and independently checks all ratio arithmetic with exact `fractions.Fraction` values at absolute tolerance `1e-12`.

Frozen controls:

1. **Limiting case:** identical small/large PCE produces `R_s=1`, zero retention advantage and zero HTL gain.
2. **Negative control:** an alternate HTL that worsens large-area PCE must produce negative advantage/gain; code may not clamp it to a favorable result.
3. **Domain control:** non-positive PCE inputs fail closed.

## Uncertainty / sensitivity

The source Table 1 does not provide formal uncertainty intervals for these champion values, so none are invented. A last-printed-digit perturbation (half-unit in the final reported decimal place) is only a reporting-resolution sensitivity, not a statistical interval. The decision is not based on a precise threshold: a multi-percentage-point FF/scale-retention difference remains large compared with final-digit rounding.

Statistical independence is unresolved for these specific champion comparisons; the source also reports device statistics elsewhere, but the four table entries used here are not treated as independent lot-level observations. No p-value or population effect is inferred.

## Serious conventional explanations / failure modes

1. **Contact/interlayer extraction and series-resistance effects.** The authors directly report altered longitudinal conductivity/work function; these can change FF and large-area loss without any change to the project's proposed active-layer EPC mechanism. This failure mode is directly bounded by the present counterexample: changing HTL is associated with a 5.45-point large-area FF difference in target-near D18/BTP-eC9 chemistry.
2. **HTL-induced active-layer morphology/interfacial changes.** The HTL can alter surface energy and molecular organization, so the observed difference is not purely electrical contact resistance.
3. **Champion-device / area confounding.** Small and 1 cm^2 values are not a paired hierarchical scale experiment; substrate/lot/device sampling may contribute.
4. **BTP-eC9 vs eC9 naming/architecture transfer.** This source is D18/BTP-eC9 PMHJ and is not the exact D18:PY-IT:eC9 B0/B1/B2 stack.

## Decision and falsifier

**Decision change:** for B0/B1/B2, contact/interlayer identity and processing become a frozen causal-control variable, and direct collection/contact diagnostics remain co-primary with field-generation, DeltaVnr/Voc, FF and stabilized Pmax. An interface arm that improves FF/Pmax while contact diagnostics also move cannot be assigned to EPC alone.

**Falsifier of this conventional explanation:** prospectively randomize B0/B1/B2 within identical contact/interlayer lots and show the useful-work effect across independent material lots while pseudo-FF/FF, contact resistance or another preregistered transport/contact diagnostic demonstrates that contact state is unchanged within empirical uncertainty. If the effect disappears after this control, narrow the mechanism claim.

## Validity boundary

This increment is a **real-data benchmark / conventional counterexample**, not stabilized-Pmax evidence, not a project device result, not a physical acceptance threshold, and not proof that beta-P should be used in the project. The transferable result is the control requirement, not the material recipe.
