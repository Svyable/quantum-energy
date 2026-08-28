# Evidence note v3.45 — field-dependent Ex→CT generation and the Voc–FF trade-off

## Claim class

This note contains **established external evidence** plus an explicitly labeled **project inference**. The v3.45 numerical sweep is a separate synthetic/model result.

## Primary evidence: Nature Photonics 2026

Zhang et al., *Overcoming the fill-factor limit of organic solar cells*, Nature Photonics (published 19 June 2026), DOI `10.1038/s41566-026-01946-8`.

The article reports:

- a persistent Voc–FF trade-off associated with field-dependent free-charge generation;
- TDCF evidence that free-charge generation varies with bias in four representative OSC systems;
- bias-dependent PL evidence supporting a field-sensitive Ex→CT bottleneck;
- a Marcus-theory treatment with first- and second-order Stark energy shifts;
- an approximate interfacial CT separation of 3.5 nm and internal field of `1e7 V/m`, giving an approximate 35 meV first-order shift;
- second-order shifts estimated at only ~0.0035–0.035 meV for the cited polarizability range;
- a proof-of-concept ternary PM6:L8-BO:Y18-C3 system with FF 81.1%, voltage loss 0.516 V and PCE 20.1%, while the corresponding PM6:Y18-C3 binary had lower voltage loss (0.502 V) but FF 68.8%;
- the optimal blend's reported acceptor exciton lifetime increased to 870 ps from 690 ps in Y18-C3.

Those are results of the cited systems, not results of this repository.

## Existing project anchor: Nature Communications 2026

Luo et al., *Suppressing electron-phonon coupling and energy loss in organic solar cells by modulating donor-acceptor penetrated-interface*, Nature Communications 17, 2026 (2026), DOI `10.1038/s41467-026-68731-7`.

This remains the basis for investigating penetrated interfaces, EPC/reorganization and non-radiative voltage loss in the D18/PY-IT/eC9 commercial bridge.

## Project inference / narrowing

Taken together, the two papers motivate a stricter causal chain:

`interface/process -> EPC/reorganization + energetic offset -> Ex/CT kinetics and field sensitivity -> non-radiative voltage loss + FF -> stabilized Pmax`

rather than treating reduced EPC/reorganization as a monotonically beneficial endpoint.

This is a **program inference**, not a claim that the two papers studied the same material system or that field-dependent generation is already present in D18/PY-IT/eC9.

## Reproducibility software lineage

The Nature Photonics article links `https://github.com/HuotianZhang/DriftFusionOPV_FieldDependent`.

At commit `d5e805ec69359f36be6e1da17a401ed8d64721a3`:

- `functions/kDis_stark.m` exposes a Marcus/Stark rate sweep;
- `functions/marcus_equation_stark.m` visibly computes a quadratic polarizability Stark term.

The main paper separately estimates a dominant ~35 meV first-order dipole shift and states its Fig. 4g simulation is based on the first-order Stark effect.

Therefore the exact code/data lineage for the paper's first-order Fig. 4g–i result should be resolved before anyone describes the current public MATLAB head as a byte-for-byte reproduction of that figure. This note does **not** call the upstream code wrong and does not copy it.

## Conventional explanations retained

A measured FF or field-dependence change can arise from morphology, transport, non-geminate recombination, contacts, series/shunt resistance, energetic disorder, exciton lifetime/diffusion, electrostatics or optical generation. Field dependence is a discriminator to add, not a unique quantum/EPC signature.
