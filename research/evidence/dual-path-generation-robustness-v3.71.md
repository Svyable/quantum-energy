# Evidence note — v3.71 dual-path generation robustness

## Established external evidence

Hart et al., *Nature Materials* 25, 1209–1218 (2026), DOI `10.1038/s41563-026-02509-6`, report that single-component NFA charge generation depends on exciton binding, reorganization energy, energetic disorder, electronic coupling, packing and state delocalization. Their model also predicts that the same material properties tend to help low-offset heterojunction generation, while cautioning that single-domain generation is unlikely to dominate nominal low-offset heterojunction photocurrent.

Ivanović et al., *Nature Communications* 16, 11560 (2025), DOI `10.1038/s41467-025-67722-4`, simulate an idealized donor/acceptor interface and find that stronger electronic coupling or dielectric screening can favor transiently delocalized hybrid exciton–CT states and a more spatially distributed hot-dissociation pathway. An interfacial defect suppresses that pathway in their model. This is computational evidence in a different material system, not D18/PY-IT/eC9 evidence.

Cui et al., *Advanced Materials* 38, e73632 (2026), DOI `10.1002/adma.73632`, explicitly use bulk NFA photo-charge generation as part of a stretchable-OSC robustness strategy. Their cited device retains more than 80% of initial PCE at 90% tensile strain and after 1000 stretch/release cycles at 30% strain. These values belong only to that material/device system and are not project thresholds.

## New project hypothesis

A material/device can be more resilient if useful charge generation is shared between physically distinct routes whose sensitivities to a chosen perturbation are not perfectly correlated.

This is **mechanism redundancy**, not quantum error correction and not yet an experimental result.

## Important eC9 architecture boundary

Hart et al. attempted contact-selective single-component NFA devices designed to minimize exciton dissociation at the electrodes. Their Methods state that BTP-eC9 and C8-ITIC were not included in the single-component high-field dataset because sufficiently uniform films could not be obtained for that measurement geometry.

Therefore the v3.70 donor-free A0/A1/A2 concept remains a useful causal falsifier, but the cited 2026 study does **not** establish a ready-to-use contact-inert BTP-eC9 high-field architecture.

Earlier work by Mahadevan et al., *Materials Horizons* (2023), DOI `10.1039/D2MH01411D`, reports neat-NFA devices including an eC-9 comparison using selective transport layers. That provides useful feasibility precedent, but transport-layer-assisted extraction/separation remains a conventional explanation and must not be silently labelled purely intradomain generation.

### Execution consequence

Future eC9 donor-free work should use an architecture-qualification ladder:

1. neat-film optical measurements to test intrinsic exciton/charge signatures without making electrical extraction claims;
2. contact-inert/selective photodiode only after film-integrity and leakage qualification;
3. transport-assisted neat-NFA device as a positive operational control, explicitly labelled as potentially contact-assisted;
4. never equate donor-free photocurrent with purely intradomain charge generation without an independent discriminator.

This narrows execution; it does not correct a measured project result.

## Strong conventional alternatives

- contact selectivity/extraction rather than generation redundancy;
- morphology/packing and optical absorption changes;
- transport/mobility changes;
- recombination suppression rather than a new generation path;
- field redistribution from changed dielectric/thickness;
- geometry/mechanical changes in stretchable systems.

The v3.71 model is useful only if these are measured or bounded prospectively.
