# v3.52 — D18/PY-IT/eC9 ternary field-generation evidence gap

**Claim class:** established-evidence boundary / literature audit.  
**Run base:** `9e61f8d761cc30b5ba12eef36c9935c35591c8f5` on `main`.  
**Audit date:** 2026-08-28.

## Changed evidentiary state

The D18/PY-IT/eC9 primary anchor paper is **not sufficient, from the primary article text inspected in this run, to satisfy the repository's field-dependent-generation requirement for a strong useful-work claim on the ternary arm**.

This is a narrowing, not a contradiction of the paper. The paper provides strong motivation for the commercial bridge and reports a ternary photovoltaic result, while its charge-generation mechanism measurements discussed in the main text are PP-TAS/PPP-TAS studies of the PA/SMA binary-system series. The repository's v3.45 gate is more specific: it requires a prospective field-dependent-generation measurement such as TDCF, bias-dependent PL, or an independently justified equivalent on the useful-work arm.

The correct audit state is `INCOMPLETE`, **not `ABSENT`**. Supplementary Information, the cited Figshare record, or author-held data could contain additional evidence that was not independently established here.

## Primary-source provenance

Luo et al., *Suppressing electron-phonon coupling and energy loss in organic solar cells by modulating donor-acceptor penetrated-interface*, **Nature Communications 17, 2026 (2026)**. DOI: `10.1038/s41467-026-68731-7`.

- published: 2026-01-26;
- version of record: 2026-02-26;
- data DOI cited by the article: `10.6084/m9.figshare.29390669`;
- article license: CC BY-NC-ND 4.0 as stated by the publisher.

No source figure or upstream dataset is copied here. The committed packet records provenance and an independent claim-to-evidence audit.

## What the article text establishes

### Binary-system charge-generation evidence

The article's section **“Charge generation dynamics with the effects of P-interface”** reports pump-probe and pump-push-probe transient absorption spectroscopy. Figure 4 and associated text analyze hole-transfer kinetics and bound charge-transfer-exciton separation for the PA and SMA systems across donor–acceptor ratios. This is meaningful charge-generation/mechanism evidence for those studied systems.

It is not automatically a measurement of **field dependence under device operating bias**, and it is not automatically evidence on the D18/PY-IT/eC9 ternary useful-work arm.

### Ternary electrical evidence

The article reports an optimized D18/PY-IT/eC9 pseudo-bulk-heterojunction device at 1:0.2:1. The main text states approximately **20 meV higher `Voc`**, **over 18% efficiency**, and **no sacrifice in `Jsc` or FF**; Figure 5f is identified as a J–V curve.

The `~20 meV` value is **literature-derived and approximate**. No uncertainty is supplied in the inspected main-text sentence, and this repository does not use it as a physical threshold.

### Named field-dependent methods

Search of the inspected primary article text returned no occurrence of `TDCF` or `bias-dependent PL`. This supports only the narrow statement that the main article text does not establish the repository's named field-generation discriminator by those methods. It does **not** prove that qualifying data are absent from every supplementary or author-controlled source.

## Fail-closed decision rule

For this evidence audit only,

```text
eligible_for_field_robustness_claim
    = ternary_specific
      AND field_dependent
      AND provenance_complete
```

The three inputs are Boolean evidence-eligibility conditions, not physical material variables. The current audited values are all `false`, therefore the state is `INCOMPLETE`.

This rule has no units and introduces no physical acceptance threshold.

## Independent / negative checks

The standard-library executable performs three controls:

1. the committed observed state must evaluate `INCOMPLETE`;
2. a negative fixture with ternary specificity and provenance but **no field dependence** must remain `INCOMPLETE`;
3. a limiting logic fixture with all three prerequisites true must evaluate `PASS`.

It also asserts that the approximate 20 meV literature value retains `uncertainty=null` and cannot be promoted to a project acceptance threshold.

Reproduce with:

```bash
python models/d18_ternary_field_evidence_audit_v3_52.py --check
```

Expected output:

```json
{"eligible_for_field_robustness_claim": false, "status": "INCOMPLETE"}
```

Runtime: standard-library Python; CI exercises Python 3.12, 3.13, and 3.14.

## Two strongest conventional explanations / failure modes

1. **Uninspected-source explanation.** A qualifying ternary field-dependent-generation dataset may exist in Supplementary Information, the cited Figshare record, or author-held data. **Discriminator:** identify and inspect the exact primary dataset/revision and rerun this audit.
2. **Kinetics-versus-field explanation.** Fast PP/PPP-TAS charge-transfer or CTE-separation kinetics may coexist with field-dependent free-charge-generation loss under operating bias. **Discriminator:** prospectively freeze and execute TDCF and/or bias-dependent PL on the actual B0/B1/B2 device arms.

A third conventional possibility remains live: any later FF or stabilized-power change can arise from morphology, thickness, contacts, mobility, or recombination rather than the proposed EPC/interface causal path. Those controls remain mandatory even if the field-generation gate passes.

## Statistical independence and uncertainty

No new experimental sample is analyzed, so this increment does not create an experimental confidence interval or sample-size claim. It preserves the project hierarchy `lot -> substrate -> device/pixel -> session -> measurement` for the next physical test.

The principal uncertainty is **source completeness**, not numerical precision. Therefore the result is deliberately `INCOMPLETE` rather than a claim of nonexistence.

## Falsifier and next physical discriminator

This audit is falsified/narrowed by a provenance-complete primary-source D18/PY-IT/eC9 ternary dataset that directly measures field-dependent free-charge generation under defined conditions.

If no such source is identified, the next physical step is a blinded B0 baseline followed by B1/B2 TDCF and/or bias-dependent PL under prospectively frozen bias, fluence, timing, temperature, thickness/morphology, and contact controls. No physical pass margin should be invented before B0 repeatability and instrument capability are measured.
