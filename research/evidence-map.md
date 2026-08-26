# Evidence Map and Claim Boundaries

## Established evidence

1. **Photosynthetic systems operate at the single-quantum level**, but the venture does not assume long-lived room-temperature electronic coherence is required for efficient transport.
2. **Environment-assisted quantum transport** has experimental precedent in engineered photonic/trapped-ion systems: intermediate dephasing can outperform both near-isolation and excessive dephasing.
3. **Cavity-mediated energy transfer** between photosynthetic light-harvesting complexes has been experimentally observed, including into weak-coupling conditions.
4. **Room-temperature exciton–polariton transport** has been reported in layered perovskites, including ballistic propagation and more recent nonlinear/polaritonic device results.
5. **P3HT/C60 Fabry–Pérot photovoltaic devices** have published electrical precedent for cavity-coupled OPVs, including absorptance-normalized IQE analysis and reduced energetic-disorder metrics in tested configurations.
6. **LiF at P3HT/C60 interfaces** has conventional thickness-dependent physics: thin LiF can suppress CT recombination, while thicker LiF can suppress exciton dissociation/charge transfer. A LiF optimum is therefore not itself evidence for the venture thesis.
7. **P3HT→C60 transfer across TPD spacers** has long-range/Förster precedent, providing an orthogonal non-contact energy-transfer control.
8. **Modern NFA OPVs** now provide direct evidence that donor–acceptor interface structure, electron–phonon coupling, reorganization energy, charge-transfer physics, and nonradiative voltage loss are linked.
9. **Penetrated donor–acceptor interfaces** in modern OSCs have been reported with weaker EPC and lower nonradiative loss; D18/PY-IT/eC9 is the current commercial-bridge anchor.
10. **Temperature-dependent sensitive-EQE/EL and FTPS** are mature tools for separating CT energetics, disorder, injection/state-filling artifacts, and voltage-loss mechanisms.
11. **EQE_EL** is used in standard voltage-loss analysis through ΔVnr = -(kBT/q) ln(EQE_EL), but injection condition must be controlled because NFA systems can show carrier-density-dependent EL.
12. **OPV reproducibility and stability** depend strongly on materials batch, coating/process history, interfaces/electrodes, encapsulation, measurement method, and ageing protocol.
13. **Inline optical spectroscopy** has manufacturing precedent in OPV processing and can track thickness/optical properties/morphology-related changes.

## Engineering assumptions currently under test

- A stable weak-EL PM6:Y6 reference can keep fabrication-attributable ΔVnr scatter below 5 mV.
- A four-temperature absolute-EL/sensitive-EQE workflow can achieve ≤10 mV total equivalent ΔVnr uncertainty on the relevant weak-signal regime.
- Five independent R2 substrates are adequate for **reference qualification / fabrication-variance screening** when analyzed hierarchically; they are no longer assumed adequate for confirmatory H1–H4 mechanism identification.
- Witness UV-vis can become a useful low-cost process proxy rather than merely a thickness measurement.
- An interface/EPC control law can eventually migrate from laboratory spectroscopy to a scalable manufacturing proxy.

## Synthetic/model results — not experimental evidence

### v3.3 R2 mechanism-recovery study

Using the frozen v3.2 low-dimensional H1–H4 classifier and explicit synthetic planning assumptions (10 mV mechanism-driven ΔVnr effect SD, 4 mV ΔVnr noise SD, seed `20260826`, 2,000 datasets per true class):

- 5 independent substrates recovered H1/H2/H3 at 66.55% / 79.15% / 76.50%.
- 7 independent substrates recovered H1/H2/H3 at 79.75% / 86.85% / 88.65%.
- 9 independent substrates recovered H1/H2/H3 at 88.20% / 90.15% / 94.85%.
- H4 was intentionally generated as a strong alert-positive injection/state-filling artifact and was recovered at 100% in the nominal simulation; this does not establish real-world H4 sensitivity.

This synthetic negative result narrows the claim: `N=5` is exploratory for mechanism classification. A confirmatory mechanism design must first demonstrate >=80% recovery for each relevant class under committed effect/noise assumptions. See `technical/r2-mechanism-recovery-v3.3.md`.

## Core falsifiable hypotheses

### H-QT: open-system transport
A deliberately engineered finite environmental coupling can improve delivery of excitation to a designated sink relative to both very low and very high dephasing, after absorption and geometry are controlled.

### H-EPC: modern-OPV bridge
A controlled change in donor–acceptor interface population changes reorganization/EPC in a preregistered direction, predicts ΔVnr/Voc, preserves charge generation, and yields ≥5% relative stabilized-Pmax improvement across at least three lots.

### H-R2: metrology-transfer reference
A qualified weak-EL OPV transfer standard can move between sessions/facilities while keeping fabrication/reference drift below the voltage-loss signal the venture seeks to measure.

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
- We do not claim a five-substrate R2 audit can confirm H1–H4 mechanisms; the current synthetic recovery study says it is exploratory under nominal assumptions.

## Source index

Primary sources used across the program include:

- Nature / Nature Communications / Nature Photonics / Communications Physics articles on photosynthetic single-photon transport, cavity-mediated energy transfer, perovskite exciton–polariton transport, polariton dynamics, modern OPV interface/EPC physics, and OPV stability.
- Published P3HT/C60 cavity-PV work: https://pmc.ncbi.nlm.nih.gov/articles/PMC11147493/
- TPD spacer transfer precedent: https://pubmed.ncbi.nlm.nih.gov/20735062/
- LiF interface precedent: https://pmc.ncbi.nlm.nih.gov/articles/PMC5115400/
- Penetrated-interface/EPC modern OSC anchor: https://www.nature.com/articles/s41467-026-68731-7
- Temperature-dependent CT/disorder methods: https://journals.aps.org/prapplied/abstract/10.1103/PhysRevApplied.15.064009
- Current OPV reproducibility review: https://pubs.rsc.org/en/content/articlelanding/2025/ta/d5ta05788d

Every future session should add dated source records and distinguish external evidence from internal model assumptions.
