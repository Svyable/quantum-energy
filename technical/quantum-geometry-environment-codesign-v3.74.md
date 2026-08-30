# Quantum geometry × environment co-design v3.74

## Status

**Exploratory synthetic/model branch.** No project material is claimed to host topological excitons. The purpose is to ask whether a verified quantum-geometric transport enhancement would create useful finite-lifetime sink-capture headroom, and how much environment/disorder penalty it could tolerate before that headroom vanishes.

## Why this branch is ambitious but relevant

The current platform thesis co-designs Hamiltonian, environment/bath, and sink. Recent exciton-topology work adds a potentially independent transport-control axis: **quantum geometry**.

Thompson et al. (Nature Communications 2025, DOI `10.1038/s41467-025-66276-9`) predict that topological excitons can have enhanced transport in free, phonon-limited, and polaronic regimes. In their cited organic polyacene examples, transport can increase by up to approximately four-fold. Their theory attributes part of the enhancement to the exciton quantum metric and proposes non-uniform electric-field gradients as a direct probe of geometric transport contributions.

This does not imply that topology is immune to disorder or that every topological material has higher transport. The cited paper explicitly discusses exciton-phonon scattering and assumes sufficiently clean bulk systems for key calculations.

## Geometric lower bound

In the cited one-dimensional inversion-symmetric framework,

`xi^2 >= a^2 P_exc^2 / 4`,

where `xi` is exciton centre-of-mass spread, `a` is lattice parameter, and `P_exc` is the excitonic topological invariant.

For `P_exc=1`, topology imposes a non-zero lower bound on the spread. For `P_exc=0`, that lower bound vanishes; this **does not** mean a trivial exciton has zero size.

## Energy-collection translation

The literature result is a transport result, not directly an energy-collection result. v3.74 adds the simplest irreversible-sink model that connects diffusion to capture.

Consider one-dimensional diffusion with coefficient `D`, an absorbing sink a distance `L` away, and an independent exponential exciton lifetime `tau`.

Let `u(L)` be the probability of reaching the sink before recombination. The backward equation is

`D u'' - tau^-1 u = 0`,

with

- `u(0)=1` at the absorbing sink;
- `u(infinity)=0`.

The physically bounded solution is

`P_capture = exp[-L/sqrt(D tau)]`.

Define the reference diffusion length scale

`ell_0 = sqrt(D0 tau)`

and dimensionless sink distance

`x = L/ell_0`.

For an effective diffusion gain

`G_eff = D_candidate/D_reference`,

we obtain

`P(G_eff)=exp[-x/sqrt(G_eff)]`.

The capture gain is therefore

`P(G_eff)/P(1)=exp[x(1-1/sqrt(G_eff))]`.

This calculation does not require or imply long-lived electronic coherence. It only asks what a measured diffusion change would do in a finite-lifetime first-passage problem.

## Frozen synthetic sensitivity

The committed table uses

- `x = 0.5, 1, 2, 3`;
- `G = 1, 1.5, 2, 4`.

The 4× point is included because it lies within the cited polyacene calculation results. It is not assigned to any project material.

### Headline synthetic case

At `x=2`:

- reference capture: `exp(-2) = 0.1353353`;
- 4×-diffusion capture: `exp(-1) = 0.3678794`;
- capture gain: `e = 2.7182818`.

At `x=3`, the same 4× diffusion sensitivity changes capture from ~0.0498 to ~0.2231, a ~4.48× ratio. This illustrates an important design fact: transport improvements matter most when the system is already diffusion-limited.

## Environment/disorder robustness budget

An intrinsic geometric gain is useful only if it survives the actual environment.

Let

- `G_intrinsic` = candidate/reference diffusion ratio before an additional environment penalty;
- `r_candidate` = retained fraction of candidate diffusion under the perturbation;
- `r_reference` = retained fraction for the reference;
- `rho = r_candidate/r_reference`.

Then

`G_eff = G_intrinsic * rho`.

The candidate retains a diffusion advantage only when

`G_intrinsic * rho > 1`.

Therefore the break-even relative retention is

`rho_break_even = 1/G_intrinsic`.

For the synthetic 4× case, `rho_break_even=0.25`: the candidate can suffer substantially more fractional degradation than the reference and still retain a net diffusion advantage. This is a mathematical robustness budget, not evidence that a real topological material actually has such robustness.

## Independent verification

The model is checked two ways.

### 1. Backward-equation solution

Direct solution of the diffusion-with-killing boundary-value problem gives

`P_capture=exp[-L/sqrt(D tau)]`.

### 2. Brownian first-passage Monte Carlo

For Brownian motion with variance `2Dt`, the exact first-passage time to a boundary a distance `L` away can be sampled as

`T_hit = L^2/(2 D Z^2)`, with `Z ~ Normal(0,1)`.

An independent loss time is sampled as

`T_loss ~ Exponential(1/tau)`.

The Monte Carlo estimator counts `T_hit < T_loss`.

With 100,000 draws and frozen seeds, the headline case gives approximately:

- baseline: `0.13162` versus analytic `0.135335`;
- 4× candidate: `0.36939` versus analytic `0.367879`.

The CI tolerance is ±0.008 absolute.

## Proposed QG-ENAQT branch

The ambitious hypothesis is:

> **Quantum geometry can provide intrinsic exciton-transport headroom while environment engineering determines how much of that headroom survives to an irreversible sink.**

This is complementary to ENAQT rather than a replacement. Topology/quantum geometry changes the state-space and transport geometry; bath/dephasing/disorder controls determine scattering, localization, and robustness.

### QG0 — reproduction

- reproduce v3.74;
- independently reproduce or benchmark at least one published topological-exciton transport result before synthesis claims;
- preserve trivial and non-topological alternatives.

### QG1 — transport measurement

Compare a serious candidate/control pair using exciton-diffusion imaging. Measure lifetime separately so higher `D` is not confused with longer `tau`.

### QG2 — quantum-metric discriminator

Apply a calibrated non-uniform electric-field gradient and test the differential transport response predicted for topological versus trivial excitons.

Critical controls:
- exciton dissociation;
- free-carrier drift;
- electroabsorption;
- heating;
- dielectric changes;
- field-induced morphology or trap effects.

### QG3 — environment map

Vary temperature, dielectric environment, and controlled disorder/dephasing. The key quantity is not merely `D_top/D_trivial` at one condition but whether the advantage persists over an experimentally useful environment window.

### QG4 — sink capture

Add a controlled quencher or electrical sink at known distance and compare measured sink capture with the first-passage prediction using independently measured `D` and `tau`.

A strong result requires the sink measurement to agree prospectively, not merely a larger diffusion coefficient.

### QG5 — programmable routing, only after QG1–QG4

A separate 2026 PRL demonstrates all-optical exciton steering through engineered potential landscapes in monolayer MoS2. That different platform provides precedent for a future **reconfigurable exciton router**: geometry supplies passive transport headroom; optical/electric potential landscapes route excitons among sinks.

This is a future architecture concept, not a present project claim.

## Major nulls / kill rules

Narrow or kill the branch if:

1. matched controls remove the apparent diffusion advantage after lifetime, morphology, defects, and crystal quality are separated;
2. a non-uniform-field response is explained by dissociation/free carriers rather than exciton quantum geometry;
3. interfaces/defects erase the bulk advantage on the sink length scale;
4. `rho <= 1/G_intrinsic` over the relevant environment window;
5. improved `D` fails to improve irreversible sink capture;
6. the candidate requires impractical synthesis, stability, toxicity, or processing conditions relative to the achievable energy benefit.

## Claim boundary

This increment establishes a **decision model and experimental ladder**, not a topological-material discovery. The program should not call this a quantum-energy breakthrough until a candidate's topology/geometry, transport advantage, environmental robustness, and sink benefit are all measured prospectively.
