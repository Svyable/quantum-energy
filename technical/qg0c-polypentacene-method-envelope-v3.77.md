# QG0c — polypentacene method-dependence and control envelope v3.77

## Changed evidentiary state

QG0b established that the published material-level transport totals cannot yet be independently reproduced from the currently resolved numerical packet. QG0c moves one layer upstream and asks a narrower question:

> What material-specific free-exciton/topology statements can be reproduced or bounded from the public polypentacene inputs **before** a full first-principles + excitonic recomputation?

Answer: several useful derived controls can be verified, but a robust material-topology claim is blocked by method dependence.

## Primary sources

1. W. J. Jankowski et al., *Excitonic topology and quantum geometry in organic semiconductors*, Nature Communications 16, 4661 (2025), DOI `10.1038/s41467-025-59257-5`.
2. J. J. P. Thompson et al., *Topologically enhanced exciton transport*, Nature Communications 16, 11448 (2025), DOI `10.1038/s41467-025-66276-9`.

The 2025 topology paper specifies the PBE/Quantum Espresso setup: 80 Ry wavefunction cutoff, 500 Ry charge-density cutoff, 12 k-points along the chain, ONCV/PBE norm-conserving pseudopotentials, 34.3 Å and 27.52 Å transverse vacuum, and force relaxation below 0.0015 Ry/Å. Its Supplementary Information gives the unstrained polypentacene chain lattice parameter `a=6.89 Å`, describes a DFT topological-to-trivial transition between +5% and +10% tensile strain, and gives the exponential strain model `t_i(gamma)=t_i(0) exp(-gamma C_i)`.

The 2025 transport paper publicly states an extracted polypentacene SSH anchor `t1=0.33 eV`, `t2=0.52 eV`.

## Material-method conflict

At PBE/DFT level, the topology paper places unstrained polypentacene (N=5) in the topological electronic/excitonic regime. The same paper explicitly reports that a cited many-body GW treatment shifts the electronic transition to occur between N=5 and N=7. Therefore the topology assignment of N=5 is **method dependent**.

This is not a minor numerical uncertainty. It changes the discrete topological label. Consequently:

`material_topology_claim = METHOD_DEPENDENT_NOT_ROBUST`

until a versioned same-structure comparison resolves the discrepancy.

## Public SSH classification

For the public transport-paper anchor,

- `t1 = 0.33 eV`
- `t2 = 0.52 eV`

and the SSH classification is topological because `t2>t1`.

The bond-reordered control swaps the values. The ideal SSH dispersion

`E(k)=sqrt(t1^2+t2^2+2 t1 t2 cos(k))`

is exactly invariant under `t1 <-> t2`, so this control changes the SSH topology label without changing the ideal band-energy dispersion.

## Ordering robustness radius

Suppose both fitted hoppings can suffer an adversarial symmetric fractional perturbation `r`:

`t2 -> t2(1-r)` and `t1 -> t1(1+r)`.

The topological ordering is guaranteed only while

`t2(1-r) > t1(1+r)`.

Solving gives

`r < (t2-t1)/(t2+t1)`.

For 0.33/0.52 eV:

`r_order = 0.22352941176470587` (~22.35%).

This is a **parameter-ordering algebraic radius**, not an uncertainty estimate and not protection against changing the electronic-structure method. The PBE/GW disagreement demonstrates why the distinction matters.

## Quantum-geometric lower bound

For a 1D inversion-protected topological exciton,

`xi^2 >= a^2 P_exc^2 / 4`.

Using `a=6.89 Å` and the public SSH/PBE topological label `P_exc=1`:

- `xi^2 >= 11.868025 Å^2`
- `xi >= 3.445 Å`

This is a topological lower bound on the centre-of-mass Wannier spread under the model assumptions. It is **not** a reproduced material quantum metric or measured exciton radius.

For `P_exc=0`, the topology supplies no nonzero lower bound. It does not imply `xi=0`.

## New derived strain constraint

The Supplementary Information models strain by

`t_i(gamma)=t_i(0) exp(-gamma C_i)`.

For the public topological anchor `t2>t1`, a tensile crossover at `gamma_c` requires

`t1 exp(-gamma_c C1) = t2 exp(-gamma_c C2)`

and therefore

`C2-C1 = ln(t2/t1)/gamma_c`.

The source places the DFT crossover between +5% and +10% tensile strain. With `ln(0.52/0.33)=0.4547361571`, this implies the derived bracket

`4.5473615711 <= C2-C1 <= 9.0947231423`.

The bracket is conditional on the exponential model, the public t1/t2 anchor and the reported DFT crossover interval. It is not a fitted experimental strain coefficient.

## Dual-control hypothesis: digital topology + analog geometry

The source literature suggests two qualitatively different control knobs:

1. **Strain:** can cross the topological phase boundary, acting as a candidate discrete topology switch.
2. **Dielectric environment:** can continuously alter the exciton quantum geometry/spread while the topological lower bound remains in force.

This motivates a future `strain x dielectric x sink` experiment in which topology is treated as the discrete state variable and quantum geometry as an analog tuning variable. This is a project design hypothesis only.

## QG0c falsifiers / blockers

A robust material-topology promotion fails if any of the following hold:

1. Same-structure PBE and GW-level workflows disagree on inversion parity/topology after convergence.
2. The fitted `t1,t2` ordering is not stable to the predeclared fitting/model-selection uncertainty.
3. Excitonic Wannier/BSE calculation yields a different `P_exc` than the inherited single-particle picture.
4. Breaking inversion symmetry removes quantisation of the stated invariant under the actual experimental perturbation.
5. A dielectric/strain change improves transport through ordinary band dispersion, lifetime, morphology, defects or optical effects without the predeclared geometry discriminator.

## QG0c -> QG0d promotion gate

Before phonon-limited transport reproduction:

- freeze one structural coordinate file and hash;
- run converged PBE and GW-level electronic calculations on that same structure;
- report inversion eigenvalues at Gamma/X and fitted SSH parameters with fitting uncertainty;
- solve the lowest excitonic band with versioned interaction/screening inputs;
- compute `P_exc`, Berry phase and quantum metric by two independent numerical paths;
- retain the method disagreement publicly if it persists;
- only then introduce exciton-phonon scattering and attempt the 300 K diffusion values.

No physical experiment or project-material claim is created by v3.77.
