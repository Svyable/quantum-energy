# QG0b material reproduction evidence ledger v3.76

## Evidence class

This file records **external computational evidence and a project reproducibility audit**. It contains no project experimental result.

## Primary source

Thompson, J. J. P.; Jankowski, W. J.; Slager, R.-J.; Monserrat, B. **Topologically enhanced exciton transport.** *Nature Communications* 16, 11448 (2025). DOI `10.1038/s41467-025-66276-9`.

### Established from the source

- The authors calculate free, phonon-limited and polaronic exciton transport in topological organic-polymer models/material mappings.
- Their phonon-limited diffusion expression thermally weights squared excitonic velocities divided by exciton-phonon scattering/dephasing rates.
- The squared velocity includes a geometric/interband quantum-metric contribution.
- The paper constructs bond-reordered trivial counterparts so the SSH hopping ordering changes while the idealized two-hopping dispersion is unchanged.
- Printed 300 K phonon-limited diffusion constants are 1.76 versus 0.61 cm^2/s for polypentacene and 0.44 versus 0.103 cm^2/s for polyheptacene.
- The paper attributes the larger relative polyheptacene enhancement to the larger percentage geometric contribution to excitonic group velocity associated with the flatter exciton band.
- Topological excitons in the modeled systems can also experience stronger exciton-phonon scattering/dephasing. Net diffusion enhancement is therefore material-dependent, not a universal topological protection rule.
- Defects/interfaces are outside the demonstrated clean-bulk calculation.

### Data/code availability boundary

The article states that plot datasets are available upon request and that first-principles calculation input files are available upon request. Public supplementary information exists, but v3.76 does not yet possess all numeric transport-run inputs required to independently reconstruct the reported 300 K totals.

## Supporting source

Jankowski, W. J. et al. **Excitonic topology and quantum geometry in organic semiconductors.** *Nature Communications* 16, 4661 (2025). DOI `10.1038/s41467-025-59257-5`.

### Established from the supporting source

- Quantum ESPRESSO/PBE/norm-conserving ONCVPSP workflow is documented with 80 Ry wavefunction cutoff, 500 Ry charge cutoff and 12 k-points along the polymer chain.
- The predicted topological phase boundary is method-sensitive: DFT and GW-level treatment do not place the transition at exactly the same oligomer/polymer length.
- Strain can tune the topology in the model family, especially near the polypentacene boundary.
- Dielectric screening changes exciton spatial extent, motivating a future strain x dielectric-environment experiment only after material-level reproduction.

## Project arithmetic audit

From the printed aggregate values only:

- `1.76 / 0.61 = 2.885245901639344...`
- `0.44 / 0.103 = 4.271844660194175...`

This confirms that the source's approximately 3x and 4.5x descriptions are rounded. Recomputing a ratio from printed outputs is **not** independent reproduction of the underlying transport simulation.

## Project control-logic audit

For an SSH two-hopping dispersion,

`E(k)^2 = t1^2 + t2^2 + 2 t1 t2 cos(k)`.

The expression is exactly symmetric under `t1 <-> t2`. v3.76 verifies this separately by numerical grid evaluation using the paper-caption polypentacene pair `t1=0.33 eV`, `t2=0.52 eV`.

This verifies the mathematical control logic. It does not verify the material mapping, exciton BSE, electron/exciton-phonon coupling, or final diffusion calculation.

## Missing-input register

Status `BLOCKED_PENDING_NUMERIC_DATA_OR_FULL_INDEPENDENT_RECOMPUTATION` remains mandatory until one of two paths succeeds.

### Path A — source-data reproduction

Obtain versioned copies of:

- numeric plot data;
- final first-principles calculation input files;
- momentum-resolved exciton energies and velocity/geometric terms;
- momentum-resolved scattering/dephasing rates or raw quantities sufficient to recompute them;
- exact structural/model input corresponding to the reported polypentacene/polyheptacene transport curves.

Then recompute the reported aggregate diffusion values with independent code.

### Path B — from-scratch reproduction

Independently reconstruct the entire material calculation from public/cited methodology with explicit convergence, versioned structures, pseudopotentials, exciton solver, phonon coupling and transport integration. This is scientifically stronger but substantially more expensive.

## Falsifiers

The QG branch should be narrowed if:

1. a source-data recomputation cannot reproduce the paper within a prospectively frozen numerical tolerance;
2. a from-scratch calculation changes the topology assignment or removes the transport advantage under well-converged higher-level treatment;
3. realistic disorder/interfaces erase the candidate advantage;
4. increased scattering outweighs geometric/group-velocity gain;
5. improved diffusion fails to improve finite-lifetime sink delivery or useful conversion.

## Publication wording guard

Allowed after v3.76:

> We independently verified the printed transport ratios and the SSH bond-swap spectral-control identity, and audited the public inputs required for full reproduction.

Not allowed after v3.76:

> We reproduced the reported polypentacene/polyheptacene 300 K topological exciton diffusion calculation.
