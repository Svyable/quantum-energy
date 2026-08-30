# QG0d-prep candidate adjudication evidence — v3.78

## Changed evidentiary state

v3.77 established that the N=5 polypentacene topology label is method dependent across the published PBE and cited GW treatments. v3.78 does **not** resolve that discrepancy. Instead, it uses the published chain-length transition locations to choose the next same-structure adjudication target without pretending that cross-study agreement is same-structure validation.

## Primary sources

1. W. J. Jankowski et al., *Excitonic topology and quantum geometry in organic semiconductors*, Nature Communications 16, 4661 (2025), DOI `10.1038/s41467-025-59257-5`.
2. J. J. P. Thompson et al., *Topologically enhanced exciton transport*, Nature Communications 16, 11448 (2025), DOI `10.1038/s41467-025-66276-9`.
3. D. Romanin, M. Calandra, A. W. Chin, *Excitonic switching across a Z2 topological phase transition: From Mott-Wannier to Frenkel excitons in organic materials*, Physical Review B 106, 155122 (2022), DOI `10.1103/PhysRevB.106.155122`.

## Published topology sequence

Jankowski et al. report at their PBE/DFT level:

- N=3 polyanthracene: trivial electronic topology;
- N=5 polypentacene: topological electronic topology;
- N=7 polyheptacene: topological electronic topology.

The same article states that repeating the chain-length analysis with a many-body GW treatment moves the trivial-to-topological transition to between N=5 and N=7. Therefore, at the level of the published cross-study labels:

- N=5: `PBE=TOPOLOGICAL`, `GW=TRIVIAL` -> `CROSS_STUDY_METHOD_CONFLICT`;
- N=7: `PBE=TOPOLOGICAL`, `GW=TOPOLOGICAL` -> `CROSS_STUDY_LABEL_AGREEMENT_TOPOLOGICAL`.

This does **not** establish a same-structure method consensus for N=7. The structures, code versions, pseudopotentials, convergence axes and exact GW workflow have not yet been frozen to an identical input packet inside this project.

## Published 300 K transport values

Thompson et al. report the following room-temperature diffusion constants from their external computation:

| material | topological D (cm^2/s) | bond-reordered trivial D (cm^2/s) |
| --- | ---: | ---: |
| polypentacene (N=5) | 1.76 | 0.61 |
| polyheptacene (N=7) | 0.44 | 0.103 |

The article attributes the larger relative enhancement for N=7 primarily to a larger percentage geometric contribution to excitonic group velocity associated with flatter exciton bands. These are **external computational values**, not project measurements.

## Independent arithmetic

Using the printed decimal values as exact frozen software inputs only:

- N=5 relative diffusion ratio: `1.76/0.61 = 176/61 = 2.885245901639...`
- N=7 relative diffusion ratio: `0.44/0.103 = 440/103 = 4.271844660194...`

For diffusion length/reach under the conventional relation `L_D proportional sqrt(D tau)`:

- within N=5, equal lifetime between topological/trivial controls gives a reach ratio `sqrt(176/61) = 1.698601160261...`;
- within N=7, equal lifetime gives `sqrt(440/103) = 2.066844130600...`.

For the absolute topological candidates, if N=5 and N=7 had equal lifetime:

`L_D,N7 / L_D,N5 = sqrt(0.44/1.76) = 0.5`.

Therefore N=7 would need

`tau_N7 / tau_N5 = 1.76/0.44 = 4`

to match the N=5 topological diffusion length under this simple relation.

No uncertainty bars are reconstructed from the printed values. Exact rational arithmetic is a check on transcription/calculation, **not physical precision**.

## Decision consequence

For the next same-structure topology adjudication only:

- **primary candidate:** N=7 polyheptacene;
- **method-sensitivity control:** N=5 polypentacene.

Reason: N=7 is the unique member of this N=5/N=7 pair with published cross-study topological label agreement. This is a topology-certainty gate, not a claim that N=7 is the better energy material.

For useful transport, the next objective is `D*tau` and eventually sink capture, not the topological/trivial D ratio alone.

## Conventional / failure explanations retained

1. The N=7 cross-study agreement may disappear when both methods are run on the identical hashed structure and identical dimensional treatment.
2. A larger relative topological/trivial ratio can coexist with poorer absolute transport because the N=7 exciton bands are flatter.
3. Lifetime may differ strongly between N=5 and N=7, invalidating any equal-lifetime reach comparison.
4. Morphology, defects, vibronic structure, dimensionality and environment may dominate a future experimental transport result before quantum geometry is distinguishable.
5. An SSH fit may be inadequate even if a parity/Berry invariant is stable.

## Current status

`N7_cross_study_label = AGREEMENT_TOPOLOGICAL`

`N7_same_structure_method_consensus = NOT_ESTABLISHED`

`N5_role = METHOD_SENSITIVITY_CONTROL`

`physical_result = NONE_EXTERNAL_COMPUTATIONAL_EVIDENCE_ONLY`
