# v3.55 — PTO2:Y1 field-generation scale benchmark

## Changed evidentiary state

**Established external evidence:** Zhang et al. (Nature Photonics, 2026; DOI `10.1038/s41566-026-01946-8`) report, for their PTO2:Y1 example, `eta_int = 0.06` and `beta = 0.09 V^-1` in the analytical field-dependent free-charge-generation parameterization

`JG(V) = JAbs * eta_int * [1 + (1/eta_int - 1) * beta * |V - Voc|]`.

**This repository's derived benchmark:** the corresponding normalized generation slope is

`S = (1/eta_int - 1) * beta = 1.41 V^-1`.

Thus, within that reported parameterization, a point `0.5 V` away from `Voc` has

`JG(V)/JG(Voc) = 1 + S*0.5 = 1.705`.

This is a real external material-system benchmark. It is **not** a D18/PY-IT/eC9 measurement, not a physical acceptance threshold, and not an independent reproduction of the paper's causal attribution.

## Why this changes a decision

The magnitude makes field-generation measurements decision-relevant rather than optional: in at least one low-voltage-loss OSC example, the paper's fitted free-charge-generation term changes strongly over an operating-voltage-scale interval. Therefore a D18/PY-IT/eC9 arm cannot be promoted from lower voltage loss to useful-work evidence without directly bounding field-dependent generation under frozen conditions.

The benchmark does **not** justify using `1.41 V^-1`, `70.5%`, or any fraction thereof as a D18 gate. The prospective D18 margin still must come from its own B0 repeatability, instrument capability, literature precedent appropriate to that material, and/or prospective power analysis.

## Verification

Inputs and provenance are frozen in `research/benchmarks/pto2-y1-field-generation-v3.55.json`.

Run:

```bash
python models/pto2_y1_field_generation_v355.py
```

Expected nominal outputs:

- `S = 1.41 V^-1`
- `JG(Voc +/- 0.5 V)/JG(Voc) = 1.705`

Independent arithmetic uses

`[eta_int + (1-eta_int)*beta*|dV|] / eta_int`,

which must agree with the primary normalized expression within `1e-12`.

Limiting/negative checks:

- `|V-Voc| = 0` gives ratio `1`.
- `eta_int = 1` gives zero field-dependent geminate term.
- `beta = 0` gives ratio `1` at all tested bias offsets.
- reversing the sign of `V-Voc` leaves the result unchanged because the source model uses an absolute voltage difference.

Dimensional analysis: `(1/eta_int - 1)` is dimensionless; `beta` is `V^-1`; therefore `S` is `V^-1`, and `S|V-Voc|` is dimensionless as required.

## Uncertainty and sensitivity

The paper values are quoted to two decimal places in the inspected main text and no physical uncertainty is assigned here. A **reporting-resolution sensitivity only** takes half-unit intervals `[0.055,0.065]` for `eta_int` and `[0.085,0.095] V^-1` for `beta`. The resulting slope range is `1.2226923–1.6322727 V^-1`. This is not a confidence interval and must not be described as measurement uncertainty.

The qualitative decision does not change across that reporting-resolution range: the field-generation term remains large enough to warrant direct prospective measurement before a useful-work claim.

## Statistical independence

This benchmark contains no new project measurements and therefore no independent D18 fabrication replicates. It must not be counted as a lot, substrate, device, session, or measurement in project statistics.

## Serious conventional explanations / failure modes

1. `eta_int` and `beta` are source-model parameters inferred from TDCF/device analysis; other loss mechanisms or model misspecification can affect their interpretation. The current increment does not prove that field-dependent generation alone causes the entire PTO2:Y1 FF deficit.
2. PTO2:Y1 may be a poor quantitative analogue for D18:eC9 or D18:PY-IT:eC9 because energetic offsets, morphology, contacts, mobilities, recombination, and CT-state properties differ.

The first is bounded here by making only a model-parameter scale claim and preserving the source equation. The second requires the already-prioritized prospective B0 D18 field-generation experiment.

## Falsifier and next physical discriminator

Supersede this benchmark if source correction or a provenance-complete reconstruction shows the quoted equation/parameters were misread. The next physical discriminator is a blinded, provenance-complete D18:eC9 B0 TDCF plus bias-dependent-PL baseline, preserving `lot -> substrate -> device -> session -> measurement`, from which a D18-specific noninferiority margin can be frozen before B1/B2 unblinding.
