# Research session — 2026-08-30 — v3.74 quantum-geometry sink headroom

## Bounded increment

Open a new exploratory branch: **QG-ENAQT — quantum geometry × environment co-design**.

The goal is not to claim a new material. It is to determine whether a verified quantum-geometric diffusion enhancement would materially improve irreversible exciton sink capture before recombination, and how much environment/disorder penalty could erase that advantage.

## New external evidence

Primary sources:

- Thompson et al., Nature Communications 16, 11448 (2025), DOI `10.1038/s41467-025-66276-9` — topological excitons predicted to enhance transport across free, phonon-limited, and polaronic regimes; up to ~4× in cited polyacene examples; non-uniform field gradients proposed as quantum-metric probes.
- Jankowski et al., Nature Communications 16, 4661 (2025), DOI `10.1038/s41467-025-59257-5` — excitonic topology/quantum geometry framework.
- Yu et al., Physical Review Letters 136, 246901 (2026), DOI `10.1103/sslb-bpc9` — complementary all-optical exciton steering in MoS2, relevant only to a future programmable-routing extension.

## Governing calculation

For 1D diffusion coefficient `D`, exponential lifetime `tau`, and an absorbing sink distance `L` away, solve

`D u'' - tau^-1 u = 0`

with `u(0)=1`, `u(infinity)=0`.

Result:

`P_capture = exp[-L/sqrt(D tau)]`.

Set

`x=L/sqrt(D0 tau)`

and

`G_eff=D_candidate/D_reference`.

Then

`P(G_eff)=exp[-x/sqrt(G_eff)]`.

## Frozen synthetic result

At `x=2`:

- reference `G=1`: `P=0.1353352832`;
- candidate `G=4`: `P=0.3678794412`;
- capture gain = `2.7182818285`.

This is a dimensionless sensitivity result. The 4× point is included because it lies within the cited polyacene theoretical result range; it is not assigned to a project material.

## Environment robustness condition

Let `rho=r_candidate/r_reference` be relative retained diffusion under a perturbation. Then

`G_eff=G_intrinsic*rho`.

The candidate keeps a diffusion advantage only if

`G_intrinsic*rho>1`.

For the synthetic 4× case, break-even `rho=0.25`.

## Independent numerical verification

100,000-draw exact Brownian first-passage Monte Carlo with frozen seeds:

- baseline estimate ~`0.13162` vs analytic `0.135335`;
- 4× candidate estimate ~`0.36939` vs analytic `0.367879`.

CI tolerance is ±0.008 absolute.

## Major validity limits

- no material topology is computed here;
- no exciton-phonon or interface calculation is reproduced;
- first-passage geometry is 1D and single-sink;
- `D` and `tau` are assumed independently measurable;
- topology can be overwhelmed by defects/interfaces;
- a larger diffusion coefficient is not useful-work evidence unless sink delivery improves.

## Falsification ladder

1. independently reproduce a published topological-exciton transport benchmark;
2. measure candidate/control diffusion and lifetime separately;
3. test non-uniform-field response with free-carrier/dissociation controls;
4. map environment/disorder robustness;
5. add a controlled irreversible sink and prospectively predict capture from measured `D` and `tau`.

## Changed evidentiary state

The program now has a mathematically explicit route from **quantum geometry → transport headroom → finite-lifetime sink capture**, plus a break-even environment penalty. This is a new hypothesis branch, not a new physical claim.

## Single best next increment

Reproduce one material-specific result from Thompson et al. or an equivalent open topological-exciton model using an independent implementation. Do not synthesize or fabricate a QG candidate until at least one material-level transport calculation has been independently reproduced and a credible matched control is identified.
