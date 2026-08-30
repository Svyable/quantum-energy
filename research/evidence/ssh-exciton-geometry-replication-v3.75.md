# v3.75 — minimal SSH exciton quantum-geometry replication

## Status
**Synthetic/model verification. Not a material-specific reproduction. Not experimental evidence.**

## Why this increment exists
v3.74 introduced an exploratory quantum-geometry × environment branch. The next gate is to independently reproduce the mathematical core before spending effort on full DFT/BSE or fabrication.

The 2025 Nature Communications transport paper reports that topological excitons have a quantum-geometric contribution to diffusivity and gives, in the flat-band lowest-exciton limit,

`D ≈ (Delta/hbar) <g_xx>`

with a topology-derived lower bound

`D >= (Delta/hbar) a^2 P_exc^2 / 4`.

It further reports room-temperature phonon-limited diffusion values of 1.76 vs 0.61 cm^2/s for topological polypentacene vs its bond-reordered trivial counterpart, and 0.44 vs 0.103 cm^2/s for polyheptacene vs its trivial counterpart. Those published numbers are evidence from the paper; this repository has **not** independently reproduced them in v3.75.

The earlier 2025 Nature Communications topology paper identifies polyanthracene as trivial and polypentacene/polyheptacene as topological candidates in the modeled polyacene family, and reports that strain can tune the excitonic topology while dielectric screening can tune exciton spread subject to the topological bound.

## Independent minimal model
`models/ssh_exciton_geometry_replication_v375.py` implements a two-band SSH Hamiltonian

`d(k) = (t1 + t2 cos k, t2 sin k, 0)`

and computes:
1. the winding of `q(k)=t1+t2 exp(ik)` by independent phase unwrapping;
2. the band quantum metric using `g_kk = |dhat'(k)|^2/4`, evaluated from an analytic derivative rather than finite-difference eigenvector overlaps;
3. the Brillouin-zone average metric;
4. swapped-hopping pairs `(t1,t2)` and `(t2,t1)`, which preserve the SSH band-energy dispersion but change topology.

This deliberately avoids importing the authors' implementation and avoids gauge-sensitive numerical eigenvector differentiation.

## Frozen acceptance checks
- `t2>t1` has winding magnitude 1; `t1>t2` has winding 0.
- metric is non-negative.
- in lattice units `a=1`, the topological cases satisfy `<g> >= 1/4` to numerical tolerance.
- for each swapped-hopping pair, the topological case has larger average metric despite identical energy dispersion.

Passing these checks verifies only the minimal topology/metric mechanism. It does not establish the material parameters, BSE excitons, electron-phonon matrix elements, diffusion constants, or experimental realizability claimed or modeled in the papers.

## Sources
- Thompson, Jankowski, Slager & Monserrat, **Topologically enhanced exciton transport**, Nature Communications (2025), DOI 10.1038/s41467-025-66276-9.
- Jankowski et al., **Excitonic topology and quantum geometry in organic semiconductors**, Nature Communications (2025), DOI page: https://www.nature.com/articles/s41467-025-59257-5.

## Next hard gate: QG0b
Reproduce at least one material-specific published diffusion ratio from independently reconstructed parameters. Preferred target is the room-temperature phonon-limited topological/trivial ratio for polypentacene or polyheptacene. Required before claiming material-level reproduction:
- source or reconstruct the exact hopping/BSE/phonon inputs from paper + supplement;
- pin all source files and hashes where licensing permits;
- reproduce topology and exciton dispersion first;
- reproduce geometric/group-velocity contribution separately from scattering contribution;
- report absolute diffusion and ratio with numerical convergence;
- document any missing parameter that prevents exact reproduction as `INCOMPLETE`, not a fitted substitute.

## New design implication, still hypothetical
If QG0b succeeds, the program gains two potentially orthogonal knobs suggested by the source literature: **strain** for topological phase control and **dielectric environment** for exciton-spread tuning. A future environment-engineering experiment should therefore test a 2D strain × dielectric matrix rather than treating topology as a fixed material label. This is a hypothesis/design implication, not an established device result.
