# Current Technical Specification

## Platform architecture

The current program is organized as four technical layers rather than one all-purpose device:

1. **Transport-physics layer** — excitonic/polaritonic or charge-transfer networks whose useful dynamics remain open to the environment.
2. **Environment/interface layer** — controllable vibrational, disorder, electrostatic, morphology, or cavity variables with explicit conventional null models.
3. **Sink/conversion layer** — fluorescent/energy-transfer sink for early mechanism work and charge-separation/electrical sink for useful-work tests.
4. **Measurement/control layer** — optical TMM, FTPS/sensitive EQE, absolute EL/EQE_EL, transient spectroscopy, morphology, temperature, and later inexpensive optical soft sensors.

## Research branches

### P0 — ambient transport physics
Primary material direction: layered perovskite / polaritonic transport platform. Goal: demonstrate a controlled transport effect under ambient conditions, not a commercial solar cell.

### P1 — electrical conversion benchmark
Legacy calibration stack: P3HT/C60 Fabry–Pérot photovoltaic with published cavity/electrical precedent. Purpose: validate optical, interface, sink, and mechanism-identification workflows.

### Commercial bridge — modern NFA OPV
Primary named interface/EPC system: D18 / PY-IT / eC9. PM6:Y6 serves as a modern benchmark, morphology-confound platform, and weak-EL reference architecture.

### P2 — nonlinear / quantum-information branch
Room-temperature polariton nonlinearities and future electrically driven polariton hardware remain a downstream option. They are not used to support near-term PV claims.

## Core open-system model

Baseline excitation transport model:

H = Σ_i ε_i |i><i| + Σ_ij J_ij (|i><j| + |j><i|)

with dephasing operators

L_i = sqrt(γ_i) |i><i|

plus irreversible sink trapping κ and loss Γ. Static disorder σ, dephasing γ, cavity-mediated coupling J_c, sink rate κ, and topology are explicit parameters.

### Goldilocks test
The primary qualitative prediction is non-monotonic sink delivery versus an environmental/dephasing coordinate:

η_sink(γ*) > η_sink(0)

and

η_sink(γ*) > η_sink(γ >> γ*)

A positive result is accepted only after absorption, optical-field, geometry, morphology, electrostatic, and dark-transport controls are applied.

## Modern-OPV causal model

Three-state basis: S0 / S1 / CT.

Key parameters:
- E_S1
- E_CT
- inner reorganization λ_i
- outer reorganization λ_o
- effective high-frequency mode ħΩ
- Huang–Rhys factor S = λ_i/(ħΩ)
- S1–CT electronic coupling
- radiative/nonradiative rates
- static-disorder width
- temperature

Model family comparison is mandatory: classical Marcus, one-mode MLJ, MLJ + static disorder, and more complex/multimode models only when held-out residuals justify them.

Useful-work prediction must survive model uncertainty: reduced EPC/reorganization is not assumed universally beneficial because phonon/vibronic interactions may also assist charge separation.

## Current commercial DOE

### Named arms
- B0: D18:eC9 baseline
- B1: D18:PY-IT:eC9 = 1:0.1:1
- B2: D18:PY-IT:eC9 = 1:0.2:1 published-anchor arm

### Causal chain
process/composition → penetrated-interface population → EPC/reorganization → CT kinetics/nonradiative loss → Voc → stabilized Pmax

### Gates
- Interface-population metric moves in the intended direction.
- Reorganization/EPC proxy changes in the preregistered direction.
- Model-predicted and EQE_EL-derived ΔVnr agree within a planning 20 mV window.
- EPC-mediated predicted Voc contribution ≥10 mV and correct sign.
- Charge generation ≥95% of baseline planning target.
- Stabilized Pmax ≥5% relative improvement and same sign across ≥3 independent lots.
- No unacceptable durability penalty before cavity-overlay spend.

## R2 weak-EL transfer standard

### Baseline architecture
Inverted ITO / PET-treated ZnO / PM6:Y6 / MoO3 / Ag, encapsulated.

R2 is a **metrology transfer standard**, not a commercial product and not a core invention.

### Geometry
- substrate: 25 × 25 × ~1.1 mm planning envelope
- measured aperture: 3.10 × 3.10 mm
- top-electrode window: 3.80 × 3.80 mm
- accepted minimum aperture-to-electrode residual margin: 0.10 mm on all sides
- contact pads: ≥2.5 × 3.0 mm exposed
- optical exclusion/collection zone: Ø8 mm around selected pixel
- encapsulation lid: ~18 × 18 mm planning

### Pilot topology
Current pilot recommendation: 5 independent substrates × 2 measured pixels.
- Pixel A: nominal control on every substrate.
- Pixel B: controlled thickness/registration/encapsulation perturbation.
- Five Pixel-A controls repeated in three nonconsecutive 300 K EL sessions.

### Fabrication-variance gate
fabrication σ = sqrt(σ_substrate² + σ_pixel²)

Release target:
- point estimate ≤3.5 mV ΔVnr
- upper 95% bootstrap bound <5 mV

No hero-device selection; all functional pixels are included except predefined QC failures.

## AT-04 metrology qualification

### Temperature points
240 / 270 / 300 / 330 K.

### Injection sweep
J_inj / J_sc = 0.1 / 0.25 / 0.5 / 1 / 2 / 5.

### Primary metrology acceptance
- DUT temperature accuracy ±1 K planning target
- temperature stability σ ≤0.25 K during acquisition
- radiometric repeatability CV ≤1%
- remount repeatability CV ≤2%
- dark/background ≤10% of weakest accepted signal
- spectral SNR ≥20 in the relevant weak-EL regime within the integration ceiling
- equivalent ΔVnr uncertainty ≤10 mV
- direct EQE_EL vs reciprocity-derived ΔVnr agreement ≤20 mV planning window
- between-session ΔVnr SD ≤5 mV at the primary point
- blind held-out analysis error ≤1.25× training error where applicable

No B0/B1/B2 proprietary fabrication is released until AT-04 and synthetic identifiability gates pass.

## Mechanism discrimination for R2 / soft sensor

Competing explanations:
- H1: bulk energetic disorder
- H2: thickness/optical-density confound
- H3: interface/contact recombination
- H4: CT-state filling / injection artifact
- H5: vibronic/triplet/nonradiative channel beyond static disorder

Highest-value additional audit: FTPS / sensitive EQE.

Supporting discriminator: Voc versus light intensity, using dVoc/dln(I)=n kBT/q as an empirical recombination diagnostic while explicitly avoiding a one-to-one mechanistic interpretation of ideality factor.

## Witness optical soft sensor

Acquire 350–950 nm UV-vis-NIR on a witness paired with every R2 substrate.

Frozen features:
- A_450_550
- A_600_850
- lambda_Y6_peak
- long-wave 10% edge
- ratio_Y6_PM6
- OD_750
- measured thickness_nm
- full-spectrum residual RMS

Pilot model: low-dimensional ridge/regularized regression only.

Prospective ΔVnr gate:
- leave-one-substrate-out MAE ≤5 mV
- ≥20% improvement over intercept-only baseline

If this passes prospectively, the next platform step is to test whether an inline optical proxy can estimate a latent interface/EPC state with bounded uncertainty and later support recipe correction.
