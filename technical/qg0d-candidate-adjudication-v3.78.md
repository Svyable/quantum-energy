# QG0d-prep — candidate pivot and same-structure topology gate v3.78

## Objective

Choose the next material for a **same-structure PBE/GW topology adjudication** while preserving the N=5 method disagreement as a control. Do not introduce exciton-phonon transport reproduction until the discrete topology classification is stable enough to justify it.

## Evidence boundary

This increment uses published computational outputs and derived arithmetic. It contains no project material calculation and no physical measurement.

The central distinction is:

> `cross-study label agreement != same-structure method consensus`

N=7 polyheptacene is promoted only to **first adjudication target**, not to validated topological material status inside this project.

## Candidate table

| candidate | PBE label reported in 2025 topology work | cited GW-side label implied by transition | project role |
| --- | --- | --- | --- |
| N=5 polypentacene | topological | trivial | method-sensitivity control |
| N=7 polyheptacene | topological | topological | primary same-structure adjudication candidate |

The GW labels above are inherited from the source statement that the GW chain-length transition occurs between N=5 and N=7. They are not our own GW calculation.

## Transport reach arithmetic

The transport paper gives external 300 K calculations:

- N5 topological: `D5 = 1.76 cm^2/s`
- N5 trivial control: `D5,triv = 0.61 cm^2/s`
- N7 topological: `D7 = 0.44 cm^2/s`
- N7 trivial control: `D7,triv = 0.103 cm^2/s`

The relative diffusion enhancement is

`R_D = D_top / D_triv`.

From the printed values:

- `R_D,N5 = 176/61 = 2.885245901639...`
- `R_D,N7 = 440/103 = 4.271844660194...`

If lifetime is unchanged within a topological/trivial pair, diffusion length scales as

`L_D proportional sqrt(D tau)`,

so the relative reach amplification is

`R_L = sqrt(R_D)`.

This gives:

- N5: `R_L = 1.698601160261...`
- N7: `R_L = 2.066844130600...`

However, absolute transport reverses the superficial ranking. If N5 and N7 have equal lifetimes,

`L_D,N7 / L_D,N5 = sqrt(0.44/1.76) = 0.5`.

To match N5's absolute topological diffusion length, N7 needs

`D7 tau7 = D5 tau5`,

therefore

`tau7/tau5 = D5/D7 = 1.76/0.44 = 4`.

This 4x factor is an arithmetic consequence of the published D values under the simple diffusion-length model. It is **not** a prediction that N7 actually has or lacks that lifetime.

## Why D*tau outranks relative enhancement

A high topological/trivial ratio can be scientifically interesting yet fail an energy-collection objective if absolute diffusion length remains short. Therefore the next decision variables are ordered as:

1. topology classification stability across methods;
2. absolute `D` and `tau` separately;
3. `D*tau` / diffusion length;
4. irreversible sink-capture probability;
5. only then relative geometric/topological enhancement as a platform descriptor.

This prevents selecting a candidate merely because the denominator of a relative comparison is small.

## Same-structure adjudication contract

Before calling N7 method-robust, require one coordinate file with one SHA-256 hash to feed both method branches.

### Frozen PBE anchor to reproduce

From the 2025 topology paper:

- Quantum ESPRESSO family;
- PBE;
- 80 Ry wavefunction cutoff;
- 500 Ry charge-density cutoff;
- 12 k-points along the chain;
- ONCV/PBE norm-conserving pseudopotential family;
- internal-coordinate relaxation to forces below 0.0015 Ry/Å.

Exact executable versions and pseudopotential file hashes must still be pinned.

### GW branch

The GW workflow is not yet fully specified by a versioned local input packet. Before running it, freeze:

- code/version;
- starting mean-field state;
- pseudopotential files/hashes;
- dielectric and self-energy settings;
- empty-band convergence;
- k-grid convergence;
- frequency treatment;
- Coulomb truncation / 1D periodic treatment;
- self-consistency choice;
- numerical tolerances.

### Required observables

For each material and method:

- structure SHA-256;
- band gap and convergence table;
- inversion eigenvalues at Gamma and X or an equivalent occupied-manifold invariant;
- Berry/Zak phase with convention recorded;
- Wannier centre or equivalent topological marker;
- SSH t1/t2 only if the low-energy fit is adequate;
- fit residuals/covariance;
- topology label plus stability to convergence/fitting choices.

At least two independent topological markers must agree before promotion.

## Prospective decision rule

### PROMOTE_N7_TO_QG0D_TRANSPORT_REPRODUCTION

Only if converged PBE and GW-level calculations on the identical hashed N7 structure both classify the state as topological, the independent invariant paths agree, and the decision is stable to frozen convergence/fit uncertainty.

### RETAIN_METHOD_DEPENDENCE

If PBE/GW disagree on the same hash, or parity and Berry/Wannier diagnostics disagree.

### KILL_OR_PIVOT_POLYACENE_QG_BRANCH

If the converged higher-level method makes N7 trivial, or the topology label can be preserved only by discretionary numerical choices near the transition.

### INCOMPLETE

If structures, code revisions, pseudopotentials, convergence results or independent invariants are missing.

## Negative controls

The executable must reject:

1. an assertion that the existing cross-study N7 labels already establish same-structure consensus;
2. an assertion that N5 has robust topology while the published PBE/GW conflict remains.

## Next discriminator after topology

If N7 passes the same-structure gate, acquire/reconstruct its exciton lifetime alongside diffusion. The 4x lifetime-compensation arithmetic makes this a direct falsifier of whether N7's larger relative geometric leverage can overcome its lower absolute published D.

No fabrication or instrument purchase is justified by v3.78 alone.
