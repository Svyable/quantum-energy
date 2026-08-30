# QG0b material-level reproduction audit v3.76

## Changed evidentiary state

v3.76 does **not** claim an independent material-level reproduction of the 2025 topological-exciton transport calculation. It advances the branch from a minimal SSH mechanism check (QG0a/v3.75) to a source-complete audit of what can and cannot presently be reproduced from public information.

The correct state is:

- `AGGREGATE_VALUES_AND_CONTROL_LOGIC_VERIFIED`
- `BLOCKED_PENDING_NUMERIC_DATA_OR_FULL_INDEPENDENT_RECOMPUTATION`
- no project physical result.

## Primary source

Joshua J. P. Thompson, Wojciech J. Jankowski, Robert-Jan Slager, Bartomeu Monserrat, **Topologically enhanced exciton transport**, *Nature Communications* 16, 11448 (2025), DOI `10.1038/s41467-025-66276-9`.

Supporting method lineage: W. J. Jankowski et al., **Excitonic topology and quantum geometry in organic semiconductors**, *Nature Communications* 16, 4661 (2025), DOI `10.1038/s41467-025-59257-5`.

## Published 300 K aggregate values

The transport paper reports the following phonon-limited exciton diffusion constants at 300 K:

| material/control | D (cm^2/s) |
|---|---:|
| polypentacene, topological | 1.76 |
| polypentacene, bond-reordered trivial counterfactual | 0.61 |
| polyheptacene, topological | 0.44 |
| polyheptacene, bond-reordered trivial counterfactual | 0.103 |

Exact arithmetic on the printed values gives:

- polypentacene: `1.76 / 0.61 = 2.885245901639344...`
- polyheptacene: `0.44 / 0.103 = 4.271844660194175...`

The authors' approximately 3x / 4.5x descriptions are rounded summaries. These ratios are **published computational evidence**, not project measurements and not independently reconstructed transport outputs.

## What the comparator actually is

The strongest causal feature of the paper is the bond-reordered SSH-style control. For polypentacene the figure caption gives approximately `t1 = 0.33 eV` and `t2 = 0.52 eV`. The trivial counterfactual swaps the hopping order.

For the two-hopping SSH spectrum,

`E(k) = +/-sqrt(t1^2 + t2^2 + 2 t1 t2 cos(k))`.

This expression is algebraically invariant under `t1 <-> t2`. Therefore a hopping-order swap can change the topological winding while leaving the idealized band dispersion unchanged. v3.76 verifies this identity numerically over a dense k grid in addition to the algebraic argument.

This comparator is a **computational counterfactual**. It is not evidence that a separately fabricated trivial polypentacene or polyheptacene sample has the reported diffusion constant.

## Transport equation reproduced at the equation level

The paper's phonon-limited diffusion calculation is of the form

`D_ph = sum_(Q,nu) <v^2_(nu,Q)> / Gamma_(nu,Q) * exp(-E_(nu,Q)/kBT) / Z`.

The squared velocity contains both conventional band and interband/geometric contributions. The practical claim in the source is not that topology removes phonon scattering. In their modeled materials the topological excitons can have stronger exciton-phonon coupling/dephasing while the geometric/group-velocity contribution is large enough to produce higher net diffusion.

Therefore the platform hypothesis must be phrased as a **multi-objective transport tradeoff**:

`net transport = geometric/band velocity benefit versus scattering/dephasing cost`.

No universal statement that topology protects transport from phonons is allowed.

## Publicly available reconstruction inputs

Public article/supplement information inspected is sufficient to identify:

- the governing diffusion and velocity equations;
- the printed 300 K aggregate diffusion values;
- the bond-reordered control logic;
- polypentacene hopping values used to illustrate the topological/trivial swap;
- DFT method lineage including Quantum ESPRESSO, PBE, norm-conserving ONCVPSP pseudopotentials, 80 Ry wavefunction cutoff, 500 Ry charge-density cutoff and 12 k-points along the chain;
- public supplementary information.

## Inputs still unresolved for an exact independent 300 K transport reproduction

The source explicitly states that plot datasets and first-principles calculation input files are available upon request. In the public material inspected, v3.76 does not yet possess:

1. the numeric plot datasets used for the reported transport curves;
2. the exact first-principles input files used for the final transport calculation;
3. the momentum-resolved `E_nu(Q)`, velocity/geometric terms and `Gamma_nu(Q)` arrays required to independently re-sum the reported Eq. 7 totals without rerunning the electronic/excitonic/phonon workflow;
4. a complete, version-pinned set of all material-specific inputs for the polyheptacene transport run;
5. explicit numerical acoustic/optical hopping-displacement coupling constants located in the inspected article text; the paper ties realistic values to earlier oligoacene work.

Missing items may ultimately be reconstructed from cited methods or supplied by the authors. Until then, exact material-level reproduction remains blocked.

## Fail-closed claim ladder

### QG0a — completed
Minimal SSH topology/quantum-metric mechanism verification. No material transport claim.

### QG0b — current v3.76 state
Verify published aggregate arithmetic, equations, control logic and public-input completeness. Status: partial reproduction/readiness audit.

### QG0c — next independent computation
Reconstruct at least one material-specific **free-exciton** band/geometry result from public source inputs and reproduce a prospectively selected figure/number without using the authors' plotted output as the computational input.

### QG0d — phonon-limited material reproduction
Reconstruct the 300 K diffusion calculation only after either:

- receiving the exact numeric/source inputs and independently recomputing the result, or
- building an independently sourced first-principles/excitonic/phonon pipeline whose inputs and convergence are sufficient to reproduce the reported quantity within a preregistered tolerance.

### QG1 — experiment
Only after QG0c/QG0d survives independent checks should this branch justify material procurement or a dedicated quantum-geometry transport experiment.

## Prospective QG0c target

Prefer polypentacene first because the source exposes an explicit hopping pair and its proximity to a topology/strain boundary makes the model easier to falsify. Freeze before calculation:

- source revision and structural input;
- electronic-structure method and convergence;
- exciton model/BSE or justified reduced-model mapping;
- target observable and tolerance;
- topology classifier;
- quantum-metric observable;
- trivial bond-reordered control;
- conventional band-dispersion comparator.

If GW versus DFT changes the topology assignment, report method dependence rather than selecting the method that preserves the desired narrative.

## Strong nulls / conventional explanations

1. The reported enhancement could be specific to the selected clean bulk counterfactual and shrink under realistic defects/interfaces.
2. Stronger exciton-phonon scattering can offset or exceed geometric velocity gain in another material.
3. A reduced SSH mapping may reproduce topology while failing quantitatively for material exciton transport.
4. Method choice (DFT versus higher-level quasiparticle corrections) can shift the predicted topological phase boundary.
5. A material with larger diffusion need not deliver more useful work unless finite lifetime, sink capture and downstream conversion also improve.

## Capital rule

No new material/instrument purchase is justified by v3.76 alone. The next spend is computational/data-access work: obtain or reconstruct the missing material-specific inputs, then attempt QG0c/QG0d under a frozen reproduction packet.
