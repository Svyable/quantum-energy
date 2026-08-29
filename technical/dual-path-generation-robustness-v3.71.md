# Dual-path charge-generation robustness v3.71

## Status

**Exploratory synthetic/model result plus prospective hypothesis.**

This increment asks whether a photovoltaic material can gain **graceful degradation** from two charge-generation routes that respond differently to morphology/interface perturbation:

1. an interface-sensitive route;
2. a more spatially distributed or acceptor-domain route.

It does **not** claim that D18/PY-IT/eC9 already has a large donor-independent photocurrent fraction, or that route redundancy is quantum fault tolerance.

## Why this idea is worth testing

Three primary results now point in the same design direction without proving the same mechanism.

### Hart et al., Nature Materials 2026

Hart et al. combine single-component NFA experiments and a delocalized-state model. They identify exciton binding, reorganization energy, energetic disorder, electronic coupling, packing motif and state delocalization as important charge-generation variables. Their model predicts that the same molecular properties that improve charge generation in neat NFA domains also tend to help low-offset heterojunctions.

Crucially, they also conclude that single-domain charge generation is **unlikely to drive the nominal photocurrent** in low-offset heterojunctions. v3.71 therefore treats donor-independent generation as a possible resilience contribution under perturbation, not as an assumed dominant B1/B2 current source.

DOI: `10.1038/s41563-026-02509-6`.

### Ivanović et al., Nature Communications 2025

Non-adiabatic molecular-dynamics simulations of an idealized donor/acceptor heterojunction show a transition from a cold interfacial dissociation route to a more efficient hot route as electronic coupling or dielectric constant rises. Transiently delocalized hybrid exciton–CT states can proceed toward charge separation several nanometres from the nominal interface, while an inserted interfacial defect suppresses the hot pathway in the tested model.

This is computational evidence in a6T/PDI, not evidence for D18/PY-IT/eC9, but it shows that the physically relevant generation topology need not be confined to one atomically sharp interface.

DOI: `10.1038/s41467-025-67722-4`.

### Cui et al., Advanced Materials 2026

Cui et al. explicitly exploit bulk NFA photo-charge generation as a route to reduced morphology sensitivity in a stretchable OSC. Their AQx-2F-based system retained more than 80% of initial PCE at 90% tensile strain and after 1000 stretch/release cycles at 30% strain. The authors attribute part of the robustness strategy to a bulk photo-charge-generation pathway with weaker dependence on blend morphology.

This is the strongest direct experimental precedent for the **robustness concept**, but it is a different material/device architecture and cannot be quantitatively transferred to D18/PY-IT/eC9.

DOI: `10.1002/adma.73632`.

## First falsification model

Let

- `G_I0` = nominal generation/output contribution of an interface-sensitive route;
- `G_B0` = nominal contribution of a more distributed/bulk-like route;
- `r_I` = fraction of interface-route output retained after a perturbation;
- `r_B` = fraction of distributed-route output retained after the same perturbation.

The baseline and perturbed outputs are

`G0 = G_I0 + G_B0`

and

`Gs = r_I G_I0 + r_B G_B0`.

Define the baseline fractional distributed contribution

`f_B = G_B0 / G0`.

Then total retention is

`R = Gs/G0 = (1-f_B) r_I + f_B r_B`.

All factors in the retention equation are dimensionless.

The exact sensitivity is

`dR/df_B = r_B - r_I`.

Therefore, **if and only if the secondary route is actually more perturbation-robust (`r_B > r_I`)**, increasing its contribution increases total retention in this first-order parallel-channel model.

If the secondary route is less robust, it makes retention worse. Route redundancy is not intrinsically beneficial.

## Synthetic fixture

Software-test values only:

- `r_I = 0.50`
- `r_B = 0.90`

The frozen sweep gives:

| f_B | total retention R |
|---:|---:|
| 0.0 | 0.50 |
| 0.1 | 0.54 |
| 0.2 | 0.58 |
| 0.3 | 0.62 |
| 0.4 | 0.66 |
| 0.5 | 0.70 |
| 0.6 | 0.74 |

At `f_B=0.40`, exact rational arithmetic gives

`R = (3/5)(1/2) + (2/5)(9/10) = 33/50 = 0.66`.

The 0.50/0.90 route-retention values and the entire `f_B` sweep are synthetic semantics checks. They are not physical expectations or thresholds.

## Inverse bound

If independent measurements establish `r_B > r_I`, then the linear model can be algebraically inverted:

`f_B = (R-r_I)/(r_B-r_I)`.

This is useful only if:

- the two-route approximation is adequate;
- `r_I` and `r_B` are independently bounded rather than fitted to the same output;
- measured `R` lies between them;
- optical, transport and recombination changes have been separately controlled.

Otherwise the inverse is not identifiable and the executable fails closed.

## Why this can create new product value

The current platform largely treats morphology/interface stability as something that must preserve one favored microscopic pathway. v3.71 adds a different strategy: **design multiple physically distinct generation pathways so a local failure does not eliminate the sink output.**

This is analogous to engineering redundancy, not quantum-error correction. If experimentally validated, the useful controller could optimize both nominal output and response to perturbations such as:

- morphology drift during thermal/light ageing;
- interfacial disorder;
- coating non-uniformity;
- strain/flexing in future mechanically compliant products;
- thickness/scale-transfer variation.

A device with high normalized retention but poor absolute Pmax is not a success. Absolute stabilized useful work remains the final sink metric.

## Prospective D18/PY-IT/eC9 test

v3.70 already introduced donor-free acceptor-domain controls A0/A1/A2. v3.71 adds a second dimension: **matched perturbation response**.

A future experiment should acquire, before and after one prospectively defined perturbation:

- A0/A1/A2 donor-free field-generation observables where a physically valid architecture is available;
- B0/B1/B2 TDCF or bias-dependent PL/IQE;
- stabilized Pmax, Voc, Jsc and FF;
- absorption/thickness normalization;
- pseudo-FF/FF or another predeclared transport/contact diagnostic;
- morphology/packing witness such as GIWAXS when available;
- full material-lot -> fabrication-lot -> substrate -> device -> session hierarchy.

The perturbation should be selected to alter interface/morphology state without introducing an uncontrolled catastrophic failure. Its physical severity and acceptance margins must be frozen from B0/A0 capability data, not from the synthetic v3.71 model.

Candidate perturbation families include the already-preregistered thermal/light durability stresses and, for a separate flexible-material branch, controlled mechanical deformation. The experiment need not use strain simply because the Cui et al. precedent does.

## Interpretation ladder

A route-redundancy claim is strengthened if all of the following occur prospectively:

1. a donor-free A-arm shows independently validated generation capability;
2. that capability is demonstrably less sensitive to the selected perturbation than the interface-sensitive comparator;
3. the corresponding B-arm retains field generation and stabilized useful work better than an interface-only explanation predicts;
4. absorption, thickness, transport/contact and morphology controls cannot explain the difference alone;
5. the direction reproduces across independent fabrication lots.

The result remains **mixed/conventional materials physics** unless an additional experiment specifically establishes a quantum-mechanical mechanism. Robustness alone is not a quantum signature.

## Strong nulls

1. The distributed route exists spectroscopically but contributes negligibly to extracted heterojunction current.
2. Apparent robustness is caused by better contacts, mobility or optical absorption rather than generation redundancy.
3. The perturbation changes both routes equally, so no redundancy advantage exists.
4. Recombination/transport interactions make the linear parallel-channel model invalid.
5. Better normalized retention comes with worse absolute stabilized Pmax.

Any of these is a useful negative result.

## Reproduction

```bash
python models/dual_path_generation_robustness_v371.py --check-expected
```

The executable checks endpoint limits, exact rational arithmetic, analytic versus finite-difference sensitivity, inverse recovery, equal-route behavior, a deliberately worse secondary route, invalid inverse use, and that no synthetic value has been populated as a physical acceptance threshold.
