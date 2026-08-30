# Session — QG0c polypentacene method envelope v3.77

Date: 2026-08-30
Base main SHA: `25b9742f33ad86543069bb62ce551772249f4629`

## Intended changed evidentiary state

Move from QG0b's aggregate transport-readiness audit to the narrowest material-specific free-exciton/topology statement reproducible from public inputs, while making method dependence impossible to hide.

## What changed

1. Froze public polypentacene anchors `t1=0.33 eV`, `t2=0.52 eV`, `a=6.89 Å`.
2. Derived a 22.3529411765% symmetric hopping-order robustness radius for the SSH classification.
3. Derived the conditional topological spread bound `xi>=3.445 Å`.
4. Combined the source strain model with the +5% to +10% DFT transition bracket to infer `4.54736 <= C2-C1 <= 9.09472`.
5. Elevated the PBE/GW classification discrepancy to a blocking method-dependence gate.
6. Added the design hypothesis of a future two-knob control surface: strain for discrete topology switching, dielectric screening for continuous quantum-geometry tuning.

## Agent Replication Packet

Claim class: external computational evidence + derived/model bounds.

Executable:

`python models/qg0c_polypentacene_method_envelope_v377.py --check-expected`

Expected key output:

- `QG0c polypentacene control-envelope v3.77: PASS`
- `ssh_classification=TOPOLOGICAL_SSH`
- `ordering_margin_fraction=0.223529411765`
- `xi_lower_bound_A=3.445000000000`
- `C2_minus_C1_bracket=4.547361571149,9.094723142299`
- `material_topology_claim=METHOD_DEPENDENT_NOT_ROBUST`
- `physical_result=NONE_EXTERNAL_COMPUTATIONAL_EVIDENCE_ONLY`

Negative claim test:

`python models/qg0c_polypentacene_method_envelope_v377.py --assert-robust-material-topology`

Expected: non-zero exit status and explicit rejection because the DFT/GW method disagreement is unresolved.

Independent checks:

- exact algebraic recomputation of `(0.52-0.33)/(0.52+0.33)`;
- exact `6.89/2` spread-length lower bound;
- independent `ln(0.52/0.33)/gamma` strain-sensitivity bracket;
- 2001-point numerical verification that the ideal SSH energy dispersion is invariant under hopping swap.

## Strongest falsifier

A converged, same-structure GW-level calculation that places the N=5 system in the trivial regime while PBE places it topological means the material label is method dependent. This is currently the state of the published evidence and therefore blocks promotion.

## Strongest conventional explanations for any later experiment

- ordinary strain-induced band-dispersion/lifetime changes;
- morphology/packing or defect changes;
- dielectric-screening effects unrelated to quantum geometry;
- inversion-symmetry breaking invalidating the intended quantised invariant.

## Corrections / scope

The 22.35% value is not a physical tolerance on strain, chemistry or method choice. It is only the symmetric fractional perturbation radius of the two fitted SSH numbers under a fixed two-parameter model.

The `xi>=3.445 Å` result is a conditional lower bound from the published topology relation. It is not a measured or independently reproduced exciton radius.

## Next physical/computational discriminator

Use one hash-pinned relaxed polypentacene structure and run PBE and GW-level electronic calculations on the identical geometry. Compare inversion eigenvalues at Gamma/X, fitted hoppings and topology before solving the excitonic Wannier equation. Do not progress to phonon-limited QG0d if the discrete topology label remains method sensitive without an experimentally justified method choice.
