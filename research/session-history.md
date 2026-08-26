# Research Session History

This file is the canonical text reconstruction of the research increments developed before the GitHub repository was connected. It preserves the key decisions, numerical gates, hypotheses, and artifact lineage so later work can continue without depending on transient chat attachments.

## Venture thesis

The program is **not** based on the claim that plants preserve long-lived room-temperature electronic coherence. The working thesis is that useful room-temperature transport can emerge in **open quantum systems** where energetic disorder, vibronic/electron–phonon coupling, dissipation, cavity/light–matter coupling, and sink geometry are co-designed.

The platform target is a **programmable ambient quantum-transport engine** whose terminal function can be either charge separation/useful electrical work or, at a later stage, nonlinear/nonclassical photonic information processing.

## Increment lineage

### v0.1 — QET-P0 prototype specification
- Defined the first decisive experiment: a non-monotonic, finite-dephasing optimum in excitation delivery to a designated sink after controlling absorption and geometry.
- Initial cavity precedent: approximately 22 nm Au / 300 nm active spacer / 22 nm Au, inspired by published photosynthetic-complex cavity work.
- Core model: single-excitation tight-binding/Lindblad network with site energies, couplings, dephasing, irreversible sink trapping, and loss.
- Key gate: an interior optimum must beat both low- and high-dephasing endpoints and reproduce across independent lots.

### v0.2 — QET-P0 model + DOE
- Converted the qualitative experiment into a parameterized DOE.
- A baseline synthetic five-site Lindblad model produced an illustrative Goldilocks curve with sink capture increasing from roughly 17.5% at zero dephasing to about 42.2% near gamma≈0.32 ps^-1, then falling at stronger dephasing.
- These were **model assumptions**, not experimental results.
- Primary mechanism experiment planning: 7 dephasing conditions × 4 replicates × 3 lots = 84 coupons, plus detuning/coupling/source–sink controls.

### v0.3 — materials downselect
- Split proof-of-physics and proof-of-electrical-work rather than forcing one material to do both.
- **P0 transport candidate:** layered PEA2PbI4 perovskite because of room-temperature ballistic bulk exciton–polariton transport evidence.
- **P1 electrical benchmark:** P3HT/C60 Fabry–Pérot OPV because a working cavity photovoltaic already provides absorptance-normalized IQE precedent.
- **P2 quantum/nonlinear branch:** quasi-2D perovskite polariton condensation / electrically driven polariton devices.

### v0.4 — P1 electrical bath DOE
- Defined a 3×3×4 factorial electrical experiment: Ag mirror 0/20/30 nm × P3HT 60/70/80 nm × four environmental/bath levels, three replicates each = 108 cells before yield reserve.
- Primary response: IQE = EQE / absorptance.
- Useful-work response: stabilized AM1.5G J–V / Pmax.
- Required controls: angle-resolved optical characterization, absorptance, dark J–V, morphology/thickness, PL/TRPL, Urbach-tail analysis.

### v0.5 — bath-control downselect
- Separated scientific calibration knobs from plausible product/manufacturing knobs.
- Temperature sweep: reversible physics control.
- Selective deuteration: orthogonal calibration/positive control for vibrational coupling, but too confounded/costly for first commercial knob.
- Polymer rigidity/Tg manipulation: secondary track.
- Ultrathin dielectric/phononic interface: primary proprietary manufacturing-track concept.

### v0.6 — LiF combinatorial coupon
- Chose LiF as a primary manufacturable perturbation and MoO3 as an electrostatic/interface control.
- Coupon concept: one substrate carrying multiple P3HT/LiF/C60 devices with LiF thickness 0/0.5/1/2/5 nm.
- Important claim boundary: a LiF electrical optimum near ~1 nm is already explainable by conventional interface/barrier physics and is **not** by itself evidence for environment-assisted quantum transport.

### v0.7 — mechanism identification
Five competing explanations were preregistered:
1. tunneling/barrier physics,
2. interface dipole / band bending,
3. morphology,
4. optical-field/cavity effects,
5. environment-assisted excited-state dynamics.

Required discriminators: absorptance-normalized IQE, TMM optical controls, Kelvin probe/UPS, AFM/GIWAXS, dark J–V/impedance, TRPL/transient absorption, stabilized Pmax, and multi-lot reproducibility.

### v0.8 — orthogonal TPD perturbation
- Added TPD as an orthogonal spacer because P3HT→C60 energy transfer across ~11 nm TPD has published long-range/Förster precedent.
- DOE: TPD 0/2/5/8/11/15 nm with resonant/detuned cavity conditions.
- Key platform test: one model should prospectively predict both LiF-dominated CT/interface behavior and TPD-separated energy-transfer behavior without unrelated post-hoc explanations.

### v0.9 — joint LiF–TPD predictive model
- TPD baseline calibrated to ~50% transfer at 11 nm.
- An 8% effective-Förster-radius cavity multiplier was used only as an **illustrative hypothesis parameter** and explicitly retired later.
- LiF null model encoded conventional recombination suppression at thin LiF and tunneling/CT-separation penalty at larger thickness.
- Joint falsification: one latent environmental-control coordinate must predict direction in both systems; optimum locations within a preregistered ±20% window.

### v1.0–v1.2 — optical TMM calibration and validation
- Retired the arbitrary 8% cavity effect; no fabrication prediction is allowed until the transfer-matrix model is calibrated against measured complex refractive index n,k and angle-resolved spectra.
- Fabrication windows anchored to published P3HT/C60 cavity hardware: Ag 20/30 nm, P3HT 60/70/80 nm, C60 20 nm, BCP 8 nm, Al 100 nm.
- 10 nm Ag excluded from primary DOE because thin-film islanding/poor quality was reported.
- Validation gates included separate TE/TM oblique incidence, layer-resolved absorption, energy conservation, measured thickness constraints, published polariton-splitting scale, and a blind holdout cavity.
- Planned angular-band RMS error gate: ≤25 nm; holdout error ≤1.25× training error.

### v1.3 — reliability / scale / data room
- Formally classified P3HT/C60 as a **mechanism-validation stack**, not the commercial product stack.
- Reliability gates: intrinsic heat, intrinsic light, combined light+heat, damp heat, thermal cycling, mechanism-retention spectroscopy, and 1 cm²→10 cm² scale transfer.
- ISOS-style procedures are used as research discipline, not as IEC product certification.
- Added FMEA for photo-oxidation, interface reactions, thickness drift, Ag morphology/cavity detuning, electrode oxidation, delamination, loss of mechanism during aging, and area nonuniformity.
- Added diligence folders for raw data, models, preregistration, fabrication, QC, reliability, IP, EHS, investor claims, and negative results.

### v1.4 — commercial migration to modern OPV
- Changed commercial bridge from generic cavity retrofit to **electron–phonon-coupling (EPC) / interface engineering** in modern non-fullerene-acceptor OPVs.
- Reason: 2026 evidence directly linked penetrated donor–acceptor interfaces to weaker EPC and reduced nonradiative voltage loss.
- Cavity coupling became a gated overlay only after interface/EPC control improves useful work and survives durability tests.

### v1.5 — named modern-material DOE
- Primary commercial bridge: D18 / PY-IT / eC9 ternary/pseudo-BHJ series, because published work reported weaker EPC at penetrated interfaces and an optimized 1:0.2:1 composition with improved Voc and >18% efficiency.
- PM6:Y6 retained as morphology-confound/benchmark system.
- Primary causal chain: process/composition → penetrated-interface population → reorganization energy/Huang–Rhys factor → CT kinetics / nonradiative loss → Voc → stabilized Pmax.
- Commercial gate: ≥5% relative stabilized-Pmax improvement across ≥3 independent lots before cavity spend.

### v1.6–v1.8 — three-state/MLJ causal model and identifiability
- Three-state S0/S1/CT model with Marcus–Levich–Jortner (MLJ) treatment.
- Parameter contract: ES1, ECT, inner/outer reorganization energies, high-frequency mode energy, Huang–Rhys factor, S1–CT coupling, transition dipoles, temperature.
- Preregistered targets included lower lambda_i/S in B2 vs B0, modeled knr reduction, model/EQE_EL ΔVnr agreement within 20 mV, ≥10 mV EPC-mediated Voc contribution, charge generation ≥95% of B0, and ≥5% stabilized-Pmax gain.
- Identifiability work added competing Marcus, MLJ, MLJ+static-disorder, and multimode models with blind holdout.
- Measurement-power planning showed that absolute EQE_EL calibration to ≤10 mV equivalent voltage uncertainty plus a four-temperature series is higher-value than early cavity hardware.

### v1.9–v2.1 — temperature-dependent absolute-EL station and uncertainty budget
- Defined a 240/270/300/330 K device-metrology system with DUT-adjacent ±1 K temperature target.
- Preferred initial strategy: external/core facility or hybrid custom carrier + core instruments; full in-house station deferred.
- Absolute EL architecture: integrating-sphere or geometry-stable collection, calibrated Si/InGaAs transfer detectors, low-noise source/measure, and NIR spectrometer/detector.
- Important injection control: measure EQE_EL across current densities around the one-sun-relevant condition because high injection can make ΔVnr appear artificially small.
- AT-04 target: total equivalent ΔVnr uncertainty ≤10 mV.

### v2.2–v2.3 — AT-04 reference qualification and sourcing
- Qualification sequence: stable bright emitter + weak OPV reference, injection sweep Jinj/Jsc = 0.1/0.25/0.5/1/2/5, four temperatures, dark/background acquisition, absolute EL, sensitive-EQE/FTPS reciprocity cross-check, session repeatability, blinded analysis, and signed go/no-go certificate.
- External routes investigated: NREL, IPVF FTPS/IQE/luminescence facilities, and EnliTech REPS/FTPS-style partner-lab route.
- Commercial rule: no B0/B1/B2 fabrication and no major metrology capex until AT-04 passes on a reference.

### v2.4–v2.9 — R2 weak-EL OPV transfer standard and reproducibility pilot
- R2 reference concept: inverted ITO / PET-treated ZnO / PM6:Y6 / MoO3 / Ag, encapsulated, non-core and intentionally not patented.
- Six-device plan: ≥3 qualified primaries, 2 witnesses, 1 destructive/backup.
- Geometry corrected after tolerance analysis: 3.10×3.10 mm measured aperture inside a 3.80×3.80 mm top electrode; minimum accepted overlap margin ≥0.10 mm.
- R2 pilot evolved from 3 substrates×3 pixels to **5 substrates×2 measured pixels** because independent substrates better identify fabrication variance than pseudo-replicated pixels.
- Critical fabrication-variance gate: point estimate ≤3.5 mV and upper 95% bound <5 mV for ΔVnr.
- Execution traveler freezes lots, solution history, coating order, witness films, mask/encapsulation factors, blind IDs, session schedule, and deviation handling.

### v3.0 — witness optical soft sensor
- Added 350–950 nm witness-film UV-vis as a low-cost inline-compatible process sensor.
- Frozen features: PM6-region integral, Y6-region integral, Y6 peak, long-wave edge, Y6/PM6 ratio, OD750, measured thickness, and full-spectrum residual score.
- Low-dimensional ridge/regularized models only; no high-capacity ML on five substrates.
- Prospective gate for ΔVnr: leave-one-substrate-out MAE ≤5 mV and ≥20% improvement over intercept-only model.
- Potential future moat: optical soft sensor → latent interface/EPC state estimate → bounded recipe correction, if prospectively validated.

### v3.1 — open-quantum mechanism discriminator
Five competing mechanisms for witness-spectrum/ΔVnr relationships:
- H1 bulk energetic disorder,
- H2 thickness/optical-density confound,
- H3 interface/contact recombination,
- H4 CT-state filling / injection artifact,
- H5 vibronic/triplet/nonradiative coupling beyond static disorder.

Highest-value additional measurement: **FTPS/sensitive EQE** on nominal R2 devices. Supporting discriminators: injection-resolved EL, Voc versus light intensity/ideality, and the existing temperature series.

The intended mechanistic ladder is:

cheap witness UV-vis → FTPS/CT-tail audit → injection-resolved EL + reciprocity → ΔVnr → useful electrical work → later closed-loop process control.

## Historical generated-artifact names

The following artifacts were generated during the pre-repository work. Their canonical technical content is being reconstructed as text/CSV under this repository because the original transient sandbox files are not currently mountable in this session:

- QET_Venture_Prototype_Spec_v0_1.docx
- QET_P0_Model_DOE_v0_2.xlsx
- QET_Materials_Downselect_v0_3.xlsx
- QET_P1_Electrical_Bath_DOE_v0_4.xlsx
- QET_Bath_Control_Downselect_v0_5.xlsx
- QET_Combinatorial_Coupon_Fab_Brief_v0_6.xlsx
- QET_Mechanism_Identification_v0_7.xlsx
- QET_Orthogonal_Perturbation_TPD_v0_8.xlsx
- QET_Joint_LiF_TPD_Predictive_Model_v0_9.xlsx
- QET_Optical_Model_Targets_v1_0.xlsx
- QET_TMM_Pipeline_v1_1.xlsx
- QET_TMM_Validation_Protocol_v1_2.xlsx
- QET_Reliability_Scale_DataRoom_v1_3.xlsx
- QET_Commercial_Migration_Interface_EPC_v1_4.xlsx
- QET_Named_Interface_EPC_DOE_v1_5.xlsx
- QET_Three_State_MLJ_Preregistration_v1_6.xlsx
- QET_MLJ_Identifiability_Design_v1_7.xlsx
- QET_Measurement_Power_VOI_v1_8.xlsx
- QET_EQEEL_Temperature_Station_Procurement_CAD_v1_9.xlsx
- QET_Vendor_Architecture_Downselect_v2_0.xlsx
- QET_AT04_Photon_Uncertainty_Budget_v2_1.xlsx
- QET_AT04_Reference_Qualification_Campaign_v2_2.xlsx
- QET_AT04_Sourcing_RFQ_v2_3.xlsx
- QET_R2_Weak_EL_OPV_Transfer_Standard_v2_4.xlsx
- QET_R2_Geometry_Encapsulation_Fixture_v2_5.xlsx
- QET_R2_Pilot_DOE_Statistical_Release_v2_6.xlsx
- QET_R2_Pilot_Power_Adaptive_Rule_v2_7.xlsx
- QET_R2_Pilot_Synthetic_Power_v2_7.csv
- QET_R2_Pilot_Raw_Template_v2_7.csv
- QET_R2_Nested_DOE_Optimization_v2_8.xlsx
- QET_R2_Nested_DOE_Simulation_v2_8.csv
- QET_R2_Execution_Traveler_Randomization_v2_9.xlsx
- QET_R2_Witness_Optical_SoftSensor_v3_0.xlsx
- QET_R2_Witness_Spectral_Features_v3_0.csv
- QET_R2_Open_Quantum_Mechanism_Discriminator_v3_1.xlsx
