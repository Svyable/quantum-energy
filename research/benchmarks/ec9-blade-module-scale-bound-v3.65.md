# v3.65 — eC9 blade-coated module scale-transfer benchmark

## Changed evidentiary state

**Claim class: established external experimental evidence plus project engineering bound.** A primary 2025 *Journal of Materials Chemistry C* study reports blade-coated PM6:BTP-eC9 cells at 18.1% PCE and a blade-coated 12 cm² effective-area module at 15.7% PCE using in-situ nitrogen blowing plus heating to improve film uniformity and morphology under ambient processing.

For this project, that changes one manufacturing belief: **eC9 inclusion itself is not evidence of an intrinsic inability to scale by blade coating.** The immediate falsifier for the D18/PY-IT/eC9 commercial bridge is target-chemistry process transfer — coating uniformity, drying/morphology, contacts/interconnection, charge collection, FF, stabilized Pmax, and yield — not the presence of eC9 alone.

This does **not** establish a D18:eC9 or D18:PY-IT:eC9 module result, recipe, acceptance threshold, or commercial manufacturing claim.

## Primary provenance

- Yi Jin et al., *High-efficiency blade-coated organic solar cells enabled via an in situ nitrogen-blowing and heating strategy*, **J. Mater. Chem. C** 13 (2025) 16620–16627.
- DOI: `10.1039/D5TC01245G`.
- Submitted 2025-03-22; accepted 2025-06-03; first published 2025-06-08.
- Source system used here: PM6:BTP-eC9.
- Quantities used are the primary-paper abstract summaries: 18.1% blade-coated cell PCE, 15.7% module PCE, 12 cm² module effective area.
- No upstream code or data are copied. The exact source summaries used are frozen in the companion JSON.

## Quantitative audit

Define the descriptive cell-to-module PCE retention

`R_PCE = PCE_module / PCE_cell`

and the relative drop

`D_PCE = 1 - R_PCE`.

Both are dimensionless. Using the printed source summaries,

`R_PCE = 15.7 / 18.1 = 0.8674033149...`

and

`D_PCE = 1 - 15.7/18.1 = 0.1325966851...`.

So the reported module retains **86.74%** of the reported blade-coated-cell PCE by this descriptive ratio, a **13.26% relative decrease**. This is not a statistical estimate because the abstract values are best/summary performance numbers rather than a matched hierarchical sample with a published uncertainty model.

### Reporting-resolution sensitivity

The source values are printed to one decimal place. Treating ±0.05 percentage point around each printed value as a **reporting-resolution sensitivity only**, not a confidence interval, gives

`R_PCE ∈ [15.65/18.15, 15.75/18.05] ≈ [0.8623, 0.8726]`.

The decision does not change anywhere in that narrow printed-value interval: the source still demonstrates a functional 12 cm² BTP-eC9-containing blade-coated module with substantial retained efficiency.

## Independent and negative checks

The standard-library executable uses ordinary floating-point arithmetic and independently recomputes the nominal ratio with Python `fractions.Fraction` from the printed decimal strings. Agreement tolerance is frozen at `1e-12`.

It additionally checks:

1. **limiting case:** equal cell/module PCE gives retention 1 and drop 0;
2. **negative control:** module PCE greater than cell PCE produces a negative drop rather than being clipped to an expected direction;
3. **invalid domain:** non-positive PCE values fail closed;
4. **area validity:** module effective area must be positive.

Run:

```bash
python models/ec9_blade_module_scale_bound_v365.py
```

No random numbers or non-standard packages are used.

## Interpretation and decision boundary

The useful inference is deliberately narrow. The external experiment shows that an eC9-containing OSC chemistry can be processed into a 12 cm² blade-coated module under a controlled aerodynamic/thermal drying process. Therefore, an internal assumption that “eC9 itself is fundamentally incompatible with scalable blade coating” would be too strong.

It does **not** follow that D18:eC9 or D18:PY-IT:eC9 will scale successfully. The donor, ternary composition, solvent/process window, film thickness, morphology, interface state, electrode architecture, and module geometry all change the problem.

No 86.74% retention requirement is imported into the project. A physical target-chemistry decision rule must come from the project’s own baseline data, instrument capability, manufacturing requirement, or prospective power analysis.

## Serious conventional explanations / failure modes

At least three ordinary explanations remain live:

1. **Donor/process non-transferability.** PM6 and D18 can differ in aggregation, rheology, drying kinetics, miscibility, transport, and thickness tolerance; success with PM6:BTP-eC9 does not establish D18 transfer.
2. **Hardware/process dependence.** The source result uses in-situ nitrogen blowing and heating. Uniformity may depend on that specific aerodynamic/thermal process window rather than an intrinsic chemistry advantage.
3. **Cell-to-module ratio is not mechanism-pure.** The 13.26% descriptive loss can combine coating nonuniformity, geometric/interconnection losses, sheet/contact resistance, optical effects, and device statistics. It does not isolate a microscopic scale-loss mechanism.

The first two are not bounded by this increment and require a target-chemistry prospective experiment. The third is directly bounded conceptually here by refusing to interpret the PCE ratio as a unique materials mechanism.

## Falsifier and next physical measurement

This project-level narrowing would be overturned if matched target-chemistry experiments showed that D18:eC9 or D18:PY-IT:eC9 repeatedly fails scalable coating for chemistry-specific reasons after coating uniformity, donor lot, thickness, contacts, and collection are controlled, especially if matched eC9-free controls scale successfully.

The next discriminating physical step is therefore a blinded **≥1 cm² D18:eC9 / D18:PY-IT:eC9 scale-transfer campaign** with same-lot D18 randomization, mapped thickness/uniformity, all-functional-device/yield reporting, field-generation and collection diagnostics, FF, and stabilized Pmax. That experiment should freeze its physical acceptance rules before B1/B2 unblinding rather than copy this cross-material literature ratio.
