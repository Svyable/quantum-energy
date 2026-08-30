# Research session — QG0d candidate adjudication v3.78

Date: 2026-08-30

## Intended evidentiary change

Convert the v3.77 N=5 method-dependence blocker into a prospective candidate-selection and same-structure adjudication protocol without claiming that the method conflict is already resolved.

## Main SHA at start

`84364e5db3cc79ed31681f563d7b8c851a3c0ee5`

No open pull requests were found during preflight.

## Sources checked

### Jankowski et al. 2025

DOI `10.1038/s41467-025-59257-5`.

The article reports PBE/DFT N=3 trivial and N=5/N=7 topological electronic states. It also states that the referenced GW chain-length transition occurs between N=5 and N=7, rather than between N=3 and N=5. The Methods give the PBE numerical anchors used in the prospective protocol.

Supplementary Data 1 is publicly linked as a TXT file. The current web reader exposed the exact media.springernature.com endpoint but rejected the octet-stream content type; a second direct network attempt in the local execution environment also failed. Therefore the structural SHA-256 remains unresolved in v3.78. This is an access/tooling limitation, not evidence that the file is absent.

### Thompson et al. 2025

DOI `10.1038/s41467-025-66276-9`.

External 300 K calculated diffusion constants used as frozen literature inputs:

- N5 topological 1.76 cm^2/s; trivial bond-reordered 0.61 cm^2/s;
- N7 topological 0.44 cm^2/s; trivial bond-reordered 0.103 cm^2/s.

The article attributes the larger N7 relative enhancement to a larger percentage geometric contribution to excitonic group velocity associated with flatter exciton bands.

## Independent calculations

Printed-value ratios are kept as exact rational arithmetic for software verification:

- N5: `176/61 = 2.885245901639...`;
- N7: `440/103 = 4.271844660194...`.

For conventional diffusion reach `L_D proportional sqrt(D tau)`:

- N5 topological/trivial equal-lifetime reach amplification: `sqrt(176/61) = 1.698601160261...`;
- N7: `sqrt(440/103) = 2.066844130600...`;
- N7/N5 absolute topological reach at equal lifetime: `sqrt(0.44/1.76) = 0.5`;
- lifetime compensation for equal absolute reach: `tau7/tau5 = 1.76/0.44 = 4`.

These are arithmetic consequences of printed external numbers. No uncertainty is inferred from their decimal presentation.

## Changed decision

N7 polyheptacene becomes the **primary same-structure topology-adjudication candidate** because it has cross-study PBE/GW topological label agreement.

N5 polypentacene remains the **method-sensitivity control** because its published labels conflict.

No same-structure method consensus is claimed for either material.

## New prospective protocol

`research/protocols/qg0d-same-structure-adjudication-v3.78.json` freezes the requirement that both PBE and GW branches use one identical structural file hash. It requires independent parity/inversion and Berry/Zak/Wannier markers, convergence tables, and fit covariance before promotion.

## Serious failure modes

1. **Cross-study agreement is an artifact of differing structures/settings.** Direct test: identical SHA-256 structure and controlled convergence across methods.
2. **Relative enhancement hides poor absolute collection reach.** Direct bound: N7 has one-quarter of the printed N5 topological D, so lifetime must be measured/reconstructed; equal-reach compensation is 4x under the simple diffusion-length model.
3. SSH reduction may fail to represent the relevant first-principles bands near the transition. Retain parity/Berry classification as primary when fit adequacy is poor.
4. Even method-robust electronic topology may not produce a useful excitonic/sink advantage once screening, lifetime, defects and phonons are included.

## Negative controls

The v3.78 executable must fail if asked to assert:

- same-structure method consensus from the frozen cross-study fixture;
- robust N5 topology while the published PBE/GW conflict remains.

## Physical result

`NONE_EXTERNAL_COMPUTATIONAL_EVIDENCE_ONLY`

## Next best increment

Retrieve/version Supplementary Data 1 (or reconstruct a fully independent structure with its own provenance), hash it, and execute the same-geometry N7 PBE/GW adjudication. Do not start phonon-limited diffusion reproduction until that gate passes.
