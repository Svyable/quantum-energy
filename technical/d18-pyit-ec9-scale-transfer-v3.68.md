# v3.68 — Prospective >=1 cm² D18/PY-IT/eC9 scale-transfer protocol

## Claim class and changed evidentiary state

**Claim class:** prospective experiment protocol.

This increment does not claim a measured scale-up result. It changes the program from relying on small-area or cross-material scale precedents to a fail-closed, target-chemistry test of whether the D18/PY-IT/eC9 useful-work effect survives at **>=1 cm²**.

The existing project useful-work rule remains unchanged: a candidate arm must show **>=5% relative stabilized-Pmax improvement with the same sign across >=3 independent fabrication lots**. No new physical acceptance margin is invented for scale retention, field generation, transport/collection, thickness uniformity, or yield.

## Why this is the next decision-relevant falsifier

Open automation PRs #59–#61 address HTL/contact confounding and the distinction between scanned and stabilized output. They do not provide a target-chemistry >=1 cm² prospective execution contract. The anti-drift decision is therefore to move toward the physical scale-transfer experiment rather than add another retrospective benchmark or metrology refinement.

A favorable small-area DeltaVnr/Voc or scanned-PCE result is not enough. At >=1 cm², ordinary coating nonuniformity, drying history, sheet/contact resistance, active-area definition, defects, and interconnect/current-crowding effects can erase useful electrical work without falsifying the microscopic EPC/interface hypothesis.

## Experimental hierarchy and randomization

Preserve:

`material_lot -> fabrication_lot -> substrate -> device -> session -> measurement`

For strong useful-work inference, the independent unit is the **fabrication lot**, not repeated devices or repeated readings.

Within each fabrication lot:

- use the same D18 material lot across compared blinded arms;
- use the same HTL and electrode lots across compared arms;
- randomize blinded active-layer arms across substrate positions;
- include contemporaneous small-area references and >=1 cm² devices;
- preserve all functional devices unless a prospectively frozen QC rule excludes them;
- record failures and yield rather than replacing failed devices with hero devices.

The existing useful-work gate requires >=3 independent fabrication lots. The number of devices per lot remains **unfrozen** until real B0 variance/process-capability data support a prospective power calculation; repeats are not allowed to masquerade as independent lots.

## Primary sink metric

Use stabilized maximum-power density under frozen illumination and temperature conditions.

For fabrication lot `l`:

`G_l = Pmax_density_arm,large,l / Pmax_density_B0,large,l - 1`

where:

- `Pmax_density_arm,large,l` = lot-level candidate-arm stabilized maximum-power density for the >=1 cm² class;
- `Pmax_density_B0,large,l` = contemporaneous B0 stabilized maximum-power density;
- `G_l` is dimensionless.

Project useful-work promotion requires:

1. >=3 independent fabrication lots;
2. `G_l > 0` in every qualifying lot;
3. mean `G_l >= 0.05`;
4. field-generation and transport/collection controls do not fail their separately frozen B0-derived margins;
5. contact/HTL/material-lot provenance is comparable.

This is the existing project gate, not a new v3.68 threshold.

## Scale-retention descriptor

For a matched arm and fabrication lot:

`R_scale,l = Pmax_density_large,l / Pmax_density_small,l`

`R_scale` is dimensionless. It is descriptive until real B0 scale-transfer data and process capability justify a prospective physical margin.

**Current physical acceptance threshold: null.**

A missing threshold is `INCOMPLETE`, not a zero-loss assumption and not PASS.

## Required co-primary controls

Acquire on mapped devices/lots, or a prospectively justified paired subset:

- stabilized Pmax density;
- illuminated J–V;
- TDCF or a predeclared field-generation equivalent;
- bias-dependent PL or another orthogonal field-generation control;
- pseudo-FF/FF or another predeclared transport/collection equivalent;
- measured active area;
- thickness and spatial-uniformity maps;
- functional-device yield;
- temperature and irradiance records;
- D18, HTL and electrode lot provenance.

A favorable voltage-loss result with worse field robustness, collection, or stabilized useful work remains mechanism science rather than platform validation.

## Fail-closed decision states

`PASS` is available only when the existing >=5%/three-lot stabilized useful-work gate passes at >=1 cm² and the separately frozen B0-derived control margins also pass.

`FAIL` includes a complete dataset where large-area stabilized useful work misses the existing project gate, where the direction reverses in any qualifying lot, or where a frozen field-generation/collection control fails.

`INCOMPLETE` includes missing stabilized Pmax, missing active-area provenance, fewer than three independent fabrication lots, missing contact/material provenance, or still-unfrozen B0-derived physical margins.

## Synthetic software fixture — not a device prediction

For code verification only:

- B0 large-area power density: `[10.0, 10.0, 10.0]` arbitrary units;
- positive candidate fixture: `[10.6, 10.6, 10.6]` -> mean relative gain `0.06` -> software PASS;
- adversarial candidate fixture: `[10.6, 10.4, 9.9]` -> one lot reverses sign -> software FAIL.

These values are arbitrary arithmetic fixtures. They are not expected D18/PY-IT/eC9 performance, uncertainty, or material constants.

Independent verification uses exact rational arithmetic: `10.6/10.0 - 1 = 106/100 - 1 = 3/50 = 0.06`, compared with the floating-point path at absolute tolerance `1e-12`.

Limiting cases:

- equal candidate and B0 power density -> zero gain;
- equal large- and small-area power density -> `R_scale = 1`;
- only two independent fabrication lots -> `INCOMPLETE`, regardless of favorable device repeats;
- non-positive Pmax density -> invalid input.

## Uncertainty and sensitivity

No new physical uncertainty model is imposed before B0 scale data exist. Real execution must separate:

- device/session repeatability;
- lot-to-lot variance;
- active-area uncertainty;
- irradiance and temperature uncertainty;
- correlated calibration/systematic terms;
- spatial coating/thickness nonuniformity;
- contact/interlayer lot effects.

If first-order propagation is inadequate for ratios near a decision boundary, use bootstrap, Monte Carlo, or interval propagation at the lot level, preserving correlated terms.

## Strong conventional explanations / failure modes

1. **Coating/drying nonuniformity:** a target arm can look favorable at small area but lose power at >=1 cm² because composition/thickness/morphology vary spatially. Direct discriminator: thickness/uniformity maps plus randomized positions and same-lot small-area references.
2. **Contact/current-collection loss:** sheet/contact resistance can lower large-area FF/Pmax without changing active-layer EPC. Direct discriminator: frozen HTL/electrode lots plus pseudo-FF/FF or another preregistered collection diagnostic.
3. **Material-lot variation:** D18 molecular-weight/batch variation can dominate apparent arm effects. Direct discriminator: same-D18-lot randomization within fabrication lot and explicit material provenance.
4. **Field-generation penalty:** a lower DeltaVnr arm can still lose FF under operating field. Direct discriminator: TDCF plus bias-dependent PL or equivalent.

## Falsifier

The useful-work scale-transfer claim is falsified if a complete blinded >=1 cm² campaign shows that a candidate arm does not maintain the existing >=5% relative stabilized-Pmax improvement across >=3 independent fabrication lots, reverses sign in any qualifying lot, or fails a prospectively frozen B0-derived field-generation/collection margin.

## Reproduction

```bash
python models/d18_pyit_ec9_scale_transfer_v368.py
```

Expected software-fixture output includes:

- `pass_mean_gain=0.060000000000`
- a negative gain in the adversarial fixture;
- `checks=PASS`

Runtime: Python standard library. CI matrix: Python 3.12, 3.13, 3.14.
