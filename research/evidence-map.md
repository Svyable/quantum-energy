# Evidence Map and Claim Boundaries

## Established evidence

1. **Photosynthetic systems operate at the single-quantum level**, but the program does not assume long-lived room-temperature electronic coherence is required for efficient transport.
2. **Environment-assisted quantum transport** has experimental precedent in engineered photonic/trapped-ion systems: intermediate dephasing can outperform both near-isolation and excessive dephasing.
3. **Cavity-mediated energy transfer** between photosynthetic light-harvesting complexes has been experimentally observed, including into weak-coupling conditions.
4. **Room-temperature exciton–polariton transport** has been reported in layered perovskites, including ballistic propagation and more recent nonlinear/polaritonic device results.
5. **P3HT/C60 Fabry–Pérot photovoltaic devices** have published electrical precedent for cavity-coupled OPVs, including absorptance-normalized IQE analysis and reduced energetic-disorder metrics in tested configurations.
6. **LiF at P3HT/C60 interfaces** has conventional thickness-dependent physics: thin LiF can suppress CT recombination, while thicker LiF can suppress exciton dissociation/charge transfer. A LiF optimum is therefore not itself evidence for the program thesis.
7. **P3HT→C60 transfer across TPD spacers** has long-range/Förster precedent, providing an orthogonal non-contact energy-transfer control.
8. **Modern NFA OPVs** provide direct evidence that donor–acceptor interface structure, electron–phonon coupling, reorganization energy, charge-transfer physics, and nonradiative voltage loss are linked.
9. **Penetrated donor–acceptor interfaces** in modern OSCs have been reported with weaker EPC and lower nonradiative loss; D18/PY-IT/eC9 is the current commercial-bridge anchor.
10. **Temperature-dependent sensitive-EQE/EL and FTPS** are mature tools for separating CT energetics, disorder, injection/state-filling artifacts, and voltage-loss mechanisms.
11. **EQE_EL** is used in voltage-loss analysis through ΔVnr = -(kBT/q) ln(EQE_EL), but injection condition must be controlled because NFA systems can show carrier-density-dependent EL.
12. **OPV reproducibility and stability** depend strongly on materials batch, coating/process history, interfaces/electrodes, encapsulation, measurement method, and ageing protocol.
13. **Inline optical spectroscopy** has manufacturing precedent in OPV processing and can track thickness/optical properties/morphology-related changes.
14. **CT-state linewidth can be dominated by temperature-activated/vibrational broadening rather than static disorder.** Tvingstedt et al. (2020) observed CT EL linewidth narrowing on cooling and low-temperature saturation across several OSC systems and argued that single-temperature optical tails need not reveal a static DOS. Göhler et al. (2021) independently used temperature-dependent CT absorption/emission and reciprocity-based temperature validation and found dynamic/vibrational broadening dominated their measured systems. These are material-system precedents, not R2 results.
15. In the semi-classical Keil/Franck–Condon picture used for planning, `σ_D²(T)=λ ħω coth[ħω/(2kBT)]` and approaches the classical Marcus high-temperature result `2λkBT`. Therefore high-temperature linewidth data alone can have weak leverage for separating static from dynamic contributions.

## Engineering assumptions currently under test

- A stable weak-EL PM6:Y6 reference can keep fabrication-attributable ΔVnr scatter below 5 mV.
- A four-temperature absolute-EL/sensitive-EQE workflow can achieve ≤10 mV total equivalent ΔVnr uncertainty on the relevant weak-signal regime.
- Five independent R2 substrates are adequate for **reference qualification / fabrication-variance screening** when analyzed hierarchically; they are not assumed adequate for confirmatory H1–H4 mechanism identification.
- Witness UV-vis can become a useful low-cost process proxy rather than merely a thickness measurement.
- An interface/EPC control law can eventually migrate from laboratory spectroscopy to a scalable manufacturing proxy.
- For an R2 static-vs-dynamic CT-linewidth audit, low-temperature points near 120/150 K are experimentally feasible without changing the relevant mechanism or creating dominant condensation/injection artifacts. This is **open** and must be qualified before physical mechanism claims.

## Synthetic/model results — not experimental evidence

### v3.3 R2 mechanism-recovery study

Using the frozen v3.2 low-dimensional H1–H4 classifier and explicit synthetic planning assumptions (10 mV mechanism-driven ΔVnr effect SD, 4 mV ΔVnr noise SD, seed `20260826`, 2,000 datasets per true class):

- 5 independent substrates recovered H1/H2/H3 at 66.55% / 79.15% / 76.50%.
- 7 independent substrates recovered H1/H2/H3 at 79.75% / 86.85% / 88.65%.
- 9 independent substrates recovered H1/H2/H3 at 88.20% / 90.15% / 94.85%.
- H4 was intentionally generated as a strong alert-positive injection/state-filling artifact and was recovered at 100% in the nominal simulation; this does not establish real-world H4 sensitivity.

This synthetic negative result narrowed the claim: `N=5` is exploratory for mechanism classification.

### v3.4 low-temperature CT-broadening discriminator

A second synthetic study added a per-substrate temperature-dependent static-variance proxy using

`σ_T² = σ_S² + λ ħω coth[ħω/(2kBT)]`.

Frozen nominal assumptions include `ħω=15 meV`, `λ=150 meV`, temperatures `120/150/240/270/300/330 K`, 2 meV linewidth-noise SD, and an H1-only synthetic static-variance component correlated with the latent ΔVnr driver. These are **planning assumptions**, not measured material parameters.

Independent high-temperature check for `ħω=15 meV`: exact Keil variance exceeds classical Marcus by only 4.35/3.44/2.79/2.31% at 240/270/300/330 K, versus 16.95/10.98% at 120/150 K. This supports adding lower-temperature points if static/dynamic broadening is a target claim.

With 5,000 synthetic datasets per class at 2 meV linewidth noise:

- `N=5`: H1/H2/H3/H4 = 73.38 / 71.78 / 73.56 / 100%.
- `N=7`: 84.84 / 81.46 / 86.74 / 100%.
- `N=9`: 91.02 / 87.26 / 93.90 / 100%.

Ten additional `N=7` seeds retained H1 84.3–86.55%, H2 80.15–83.25%, H3 86.35–88.65%, H4 100% under the same synthetic generator. Thus `N=7` conditionally crosses the program's >=80% all-class synthetic recovery gate, but H2 remains near the boundary; `N=9` retains a stronger publication margin.

**Correction/narrowing:** the existing 240–330 K AT-04 grid remains appropriate for metrology and temperature-dependent voltage-loss work, but it should not be described as sufficient for strong static-vs-dynamic CT-linewidth identification.

## Core falsifiable hypotheses

### H-QT: open-system transport
A deliberately engineered finite environmental coupling can improve delivery of excitation to a designated sink relative to both very low and very high dephasing, after absorption and geometry are controlled.

### H-EPC: modern-OPV bridge
A controlled change in donor–acceptor interface population changes reorganization/EPC in a preregistered direction, predicts ΔVnr/Voc, preserves charge generation, and yields ≥5% relative stabilized-Pmax improvement across at least three lots.

### H-R2: metrology-transfer reference
A qualified weak-EL OPV transfer standard can move between sessions/facilities while keeping fabrication/reference drift below the voltage-loss signal the program seeks to measure.

### H-SoftSensor
Inline-compatible witness optical observables predict ΔVnr out of substrate, improving by ≥20% over thickness/intercept baselines and reaching ≤5 mV LOSO MAE in the pilot target.

## Novel invention concepts — not yet novelty claims

1. **Programmable open-quantum energy transport** via co-design of Hamiltonian, environment/bath, cavity connectivity, and sink.
2. **Manufacturing control targeting an EPC/reorganization-energy window** at a photovoltaic donor–acceptor interface and prospectively predicting electrical work.
3. **Latent-state soft sensor** combining cheap inline optical observables with sparse absolute quantum-loss audits to estimate interface/EPC state and drive bounded recipe corrections.
4. **Joint cavity + interface/EPC optimization** only if the modern-OPV interface program passes useful-work and durability gates.

## Explicit non-claims

- We do not claim plants implement fault-tolerant quantum computing.
- We do not claim long-lived room-temperature electronic coherence is required for photosynthetic efficiency.
- We do not claim a LiF or TPD effect alone is novel quantum transport.
- We do not claim P3HT/C60 is a commercially competitive product stack.
- We do not claim ISOS research stability procedures are IEC/UL product certification.
- We do not claim the current soft-sensor concept is patentable before a prior-art/FTO review and prospective validation.
- We do not claim a five-substrate R2 audit can confirm H1–H4 mechanisms.
- We do not claim a room-temperature/high-temperature Urbach energy or CT linewidth is a direct measurement of static energetic disorder.
- We do not claim the v3.4 synthetic `N=7` result proves seven real R2 substrates are sufficient; low-temperature feasibility and empirical linewidth uncertainty must come first.

## Source index

Primary sources used across the program include:

- Published P3HT/C60 cavity-PV work: https://pmc.ncbi.nlm.nih.gov/articles/PMC11147493/
- TPD spacer transfer precedent: https://pubmed.ncbi.nlm.nih.gov/20735062/
- LiF interface precedent: https://pmc.ncbi.nlm.nih.gov/articles/PMC5115400/
- Penetrated-interface/EPC modern OSC anchor: https://www.nature.com/articles/s41467-026-68731-7
- Temperature-dependent CT/disorder methods: https://journals.aps.org/prapplied/abstract/10.1103/PhysRevApplied.15.064009
- Temperature-dependent CT linewidth / static-vs-dynamic disorder: https://pubs.rsc.org/en/content/articlehtml/2020/mh/d0mh00385a
- Current OPV reproducibility review: https://pubs.rsc.org/en/content/articlelanding/2025/ta/d5ta05788d

Every future session should add dated source records and distinguish external evidence from internal model assumptions.
