# Evidence map — QG0c polypentacene method envelope v3.77

## Established external computational evidence

### Excitonic topology and quantum geometry in organic semiconductors (2025)
DOI: `10.1038/s41467-025-59257-5`

- 1D inversion-protected excitonic topology is characterised by a Z2 invariant/Berry phase.
- In the polyacene regimes realised in the paper, the non-trivial excitonic Berry phase is inherited from the electronic/hole topology; the Supplementary Information reports a vanishing envelope contribution in these regimes.
- PBE/DFT places polyanthracene as trivial and polypentacene/polyheptacene as topological.
- The paper explicitly states that a cited GW treatment shifts the electronic transition to between polypentacene and polyheptacene, making N=5 method dependent.
- Quantum-geometric bound: `xi^2 >= a^2 P_exc^2 / 4`.
- Public DFT setup: Quantum Espresso, PBE, ONCV norm-conserving pseudopotentials, 80/500 Ry cutoffs, 12 chain k-points, transverse vacuum 34.3/27.52 Å, forces <0.0015 Ry/Å.
- Supplementary Information: unstrained polypentacene `a=6.89 Å`; DFT strain-driven topology change between +5% and +10%; strain model `t_i(gamma)=t_i(0) exp(-gamma C_i)`.
- Datasets for plots and first-principles input files are stated to be available upon request; they are not treated here as already possessed.

### Topologically enhanced exciton transport (2025)
DOI: `10.1038/s41467-025-66276-9`

- Public polypentacene SSH anchor: `t1=0.33 eV`, `t2=0.52 eV`.
- The trivial comparison swaps the hopping order to isolate the topological/geometric contribution while preserving the ideal SSH band dispersion.
- The paper reports enhanced free, phonon-limited and polaronic transport for its calculated topological examples; v3.77 does not independently reproduce those transport calculations.

## v3.77 derived/model results

From the public 0.33/0.52 eV anchor:

- SSH label under the stated convention: `TOPOLOGICAL_SSH`.
- Symmetric fractional hopping-order robustness radius:
  `(t2-t1)/(t2+t1)=0.22352941176470587`.
- Exact bond-swap energy-dispersion identity checked numerically on 2001 k-points.

From `a=6.89 Å` and conditional `P_exc=1`:

- `xi^2_lower = 11.868025 Å^2`.
- `xi_lower = 3.445 Å`.

From the exponential strain model and DFT transition bracket `0.05 <= gamma_c <= 0.10`:

- `ln(t2/t1)=0.4547361571149471`.
- `4.547361571149471 <= C2-C1 <= 9.094723142298942`.

## Not established

- Robust real-material topology of polypentacene across electronic-structure methods.
- A reproduced polypentacene quantum metric.
- A measured topological exciton.
- A measured or independently reproduced topological transport enhancement.
- A physical strain switching threshold for a fabricated project device.
- A dielectric tuning law for useful sink power.

## Strong conventional / alternative explanations for future transport data

1. Strain changes ordinary band dispersion, defects, aggregation, optical absorption or exciton lifetime.
2. Dielectric environment changes binding energy, energetic disorder, screening, interface electrostatics or nonradiative decay without a geometry-specific mechanism.
3. Sample morphology/packing changes dominate any apparent transport shift.
4. Inversion symmetry is sufficiently broken that the intended Z2 classification is no longer the correct experimental description.

## Required next discriminator

A same-structure, versioned PBE versus GW-level parity/topology calculation is the immediate discriminator. Do not choose a project material for the QG branch on the PBE label alone.
