# Session — v3.5 low-temperature reference qualification

## What changed

v3.4 proposed 120/150 K as low-temperature CT-linewidth points. This session narrows that design using PM6:Y6-specific low-temperature evidence:

- **150 K is now the primary low-temperature qualification point.**
- **120 K is conditional** and may only be used if 150 K passes survival, operating-regime, injection-heating, SNR/repeatability, and temperature-metrology gates.
- The mechanism-recovery model must be rerun with the **measured** linewidth-noise distribution and actual usable temperature grid before choosing N=7 versus N=9.

No physical R2 data were collected. This is a preregistered protocol and calculation update.

## Source provenance

### Primary literature

1. Perdigón-Toro et al., *Advanced Materials* 32, 1906763 (2020), DOI `10.1002/adma.201906763`.
   - PM6:Y6 charge generation remains unusually robust on cooling.
   - EQE changes weakly toward ~150 K and its shape is reported essentially unchanged to ~125 K.
   - A stronger decrease below ~150 K is discussed as potentially transport/recombination-related.
   - Voc(T) was approximately linear to ~100 K under the reported conditions.
2. Tvingstedt, Benduhn & Vandewal, *Materials Horizons* 7, 1888–1900 (2020), DOI `10.1039/D0MH00385A`.
   - CT EL linewidth narrowing/saturation motivates a dynamic-vibronic interpretation and low-temperature measurement.
3. Göhler et al., *Physical Review Applied* 15, 064009 (2021), DOI `10.1103/PhysRevApplied.15.064009`.
   - Temperature-dependent CT absorption/emission and reciprocity-based device-temperature validation show the need to control actual DUT temperature.

These sources are material/device precedents, not measurements of the proposed R2 transfer standard.

## Quantitative calculation

### Inputs

The linewidth sensitivity calculation intentionally reuses v3.4 **synthetic planning priors**:

- `lambda = 150 meV` — synthetic;
- `hbarOmega = 15 meV` — synthetic;
- `k_B = 0.08617333262 meV/K` — physical constant;
- temperature-error probe = `1 K` — engineering sensitivity case.

### Model

`σ_D²(T) = λ ħω coth[ħω/(2k_BT)]`.

Analytic derivative:

`dσ/dT = {λ ħω csch²(x) [ħω/(2 k_B T²)]}/{2σ}`, with `x=ħω/(2k_BT)`.

### Results

Synthetic linewidth sensitivity to a 1 K temperature error:

- 120 K: 0.1806 meV;
- 150 K: 0.1763 meV;
- 240 K: 0.1538 meV;
- 300 K: 0.1408 meV.

Under this model, ±1 K calibration error is small relative to the v3.4 synthetic 2 meV linewidth-noise assumption. The result does **not** bound errors from injection heating, transport-regime change, non-equilibrium state filling, or model misspecification.

### Independent cross-check

The analytic high-temperature expansion gives `σ² -> 2 λ k_B T`. The committed script verifies the exact one-mode variance against this independent Marcus limit at 10,000 K with relative error `<1e-4`.

The exact one-mode variance exceeds the high-T Marcus value by 10.978% at 150 K, 4.346% at 240 K, and 2.790% at 300 K. Thus 150 K retains materially more sensitivity to the dynamic model than the original 240–330 K range.

Runtime used for local recomputation during this session: Python standard library arithmetic; the committed script has no third-party package requirement.

## Engineering assumptions added

- post-cycle recovery gates: `|ΔVoc|<=10 mV`, `|ΔVnr|<=5 mV`, `|ΔPmax|<=5%`;
- normalized EQE cosine similarity `>=0.995` as an operating-regime screen;
- local Voc(T) deviation `<=20 mV`;
- injection-induced DUT heating `<=0.5 K` at the selected operating point;
- low-temperature integrated spectral SNR `>=20`;
- repeated linewidth-extraction SD `<=2 meV` to use the v3.4 nominal recovery result without changing the noise assumption.

Every threshold above is a **planning assumption**, not a published PM6:Y6 specification. Qualification data must retire or revise them.

## Statistical independence

Temperatures, injection points, and repeat spectra are repeated observations on the same device. They may reduce metrology uncertainty but do not increase the independent substrate count for mechanism recovery.

## Conventional explanations preserved

- extraction/transport changes below ~150 K;
- injection/state filling;
- contact barriers;
- Joule heating / thermal gradients;
- detector/background changes;
- multiple vibronic modes;
- dynamic broadening without dominant static disorder.

## Correction / supersession

**v3.4 scope correction:** 120 K is no longer a default mechanism-audit point. It is conditional on successful 150 K qualification and explicit operating-regime equivalence. The 240/270/300/330 K AT-04 grid remains valid for reference metrology and temperature-dependent voltage-loss work.

## Unresolved risks

- actual R2 CT/near-gap EL may be too weak at 150 K;
- PM6:Y6 device extraction can deteriorate below ~150 K even when generation remains favorable;
- a one-mode linewidth model may be inadequate;
- the added 150 K point may still be insufficient to push H1–H4 recovery to a strong publication margin;
- physical cryostat/contact/condensation behavior remains unqualified.

## Single best next increment

Create the **low-temperature reference execution package**: a concrete cryostat/sample-holder interface, DUT/stage temperature-calibration procedure, injection-power/heating sweep, dark/SNR acquisition sequence, raw-data schema, and ready-to-run analysis script that accepts measured linewidth uncertainty and automatically reruns the H1–H4 recovery decision for the actual usable temperature grid.
