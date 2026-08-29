# Research session — 2026-08-29 — v3.71 dual-path generation robustness

## Changed evidentiary state

The program now has an explicit, falsifiable **mechanism-redundancy hypothesis**: useful charge generation may become more resilient if interface-sensitive and spatially distributed/acceptor-domain routes respond differently to morphology/interface perturbation.

This is exploratory model logic plus cross-material evidence. No physical D18/PY-IT/eC9 redundancy is claimed.

## Primary evidence

- Hart et al., Nature Materials 2026, DOI `10.1038/s41563-026-02509-6`: delocalization, coupling, reorganization, disorder and packing control charge generation; single-domain generation is unlikely to dominate nominal low-offset heterojunction current.
- Ivanović et al., Nature Communications 2025, DOI `10.1038/s41467-025-67722-4`: simulated transient hybrid exciton–CT states can create a spatially distributed hot dissociation route; interfacial disorder can suppress it.
- Cui et al., Advanced Materials 2026, DOI `10.1002/adma.73632`: experimental stretchable-OSC precedent explicitly leveraging bulk NFA photo-charge generation for morphology robustness.

## Model

`R = (1-f_B) r_I + f_B r_B`

with exact sensitivity

`dR/df_B = r_B-r_I`.

Therefore redundancy helps only if the added route is measurably more perturbation-robust.

Synthetic fixture only: `r_I=0.5`, `r_B=0.9`; at `f_B=0.4`, `R=0.66`. Exact independent arithmetic gives `33/50`.

## Negative/control checks

- `f_B=0` returns interface-route retention.
- `f_B=1` returns distributed-route retention.
- equal route sensitivities make the route fraction irrelevant.
- a less-robust secondary route decreases total retention.
- inverse estimation fails closed when route ordering/bracketing is invalid.
- all physical thresholds remain null.

## New execution boundary for v3.70

Hart et al. report that BTP-eC9 was not included in their contact-inert single-component high-field dataset because sufficiently uniform films were not obtained for that geometry. Earlier neat eC9 device precedent uses transport layers that can participate in extraction/separation.

Therefore donor-free eC9 work needs an architecture-qualification ladder before photocurrent is interpreted as intradomain generation.

## Strong nulls

1. bulk/distributed generation exists but contributes negligibly to extracted heterojunction current;
2. apparent resilience is contact/transport or optical rather than generation redundancy;
3. perturbation affects both routes equally;
4. nonlinear recombination invalidates the two-parallel-route model;
5. normalized retention improves while absolute stabilized Pmax worsens.

## Next physical discriminator

Pair the merged v3.70 donor-free controls with one prospectively qualified perturbation and matched B0/B1/B2 measurements. Track field-generation observables, stabilized Pmax, transport/contact diagnostics, absorption/thickness and morphology before/after perturbation. Freeze physical margins only from baseline capability data.
