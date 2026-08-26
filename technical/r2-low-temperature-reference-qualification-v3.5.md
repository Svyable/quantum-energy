# v3.5 — Low-temperature R2/reference feasibility qualification

## Decision this increment

**150 K is the primary low-temperature CT-linewidth qualification point. 120 K is conditional, not automatic.**

This narrows v3.4. The reason is material-system evidence rather than model preference: published PM6:Y6 measurements show efficient/free-charge generation remains unusually robust on cooling and the EQE spectral shape is essentially unchanged to roughly 125 K, but a steeper EQE loss appears below roughly 150 K and was attributed to extraction/recombination complications. Therefore 120 K may cross into a different device operating regime even if it provides more linewidth leverage.

No R2 low-temperature measurement exists yet. Every numerical acceptance threshold below is an **engineering planning gate** unless explicitly sourced.

## Evidence anchors

### Established evidence

1. Perdigón-Toro et al., *Advanced Materials* 32, 1906763 (2020), DOI `10.1002/adma.201906763`: PM6:Y6 TDCF/EQE/Voc measurements found a very small charge-generation activation energy; EQE changed only weakly on cooling toward ~150 K, the spectral shape was essentially unaffected down to ~125 K, and the stronger decrease below ~150 K was discussed as a possible transport/recombination issue. Voc remained approximately linear with temperature down to ~100 K under the reported conditions.
2. Tvingstedt, Benduhn & Vandewal, *Materials Horizons* 7, 1888–1900 (2020), DOI `10.1039/D0MH00385A`: CT EL linewidth narrowing and low-temperature saturation motivate explicit vibronic/dynamic broadening models rather than interpreting a room-temperature tail as static DOS.
3. Göhler et al., *Physical Review Applied* 15, 064009 (2021), DOI `10.1103/PhysRevApplied.15.064009`: temperature-dependent CT absorption/emission and reciprocity-based temperature validation show that actual device temperature and dynamic broadening must be controlled.

These papers are precedents from published devices/material systems; none is an R2 result.

## Governing planning model

The v3.4 one-mode linewidth planning relation is retained only as a sensitivity model:

`σ_D²(T) = λ ħω coth[ħω / (2 k_B T)]`

with optional static contribution

`σ_T²(T) = σ_S² + σ_D²(T)`.

Symbols:
- `σ_D`: dynamic/vibronic linewidth standard deviation, meV;
- `σ_S`: static-disorder standard deviation, meV;
- `λ`: reorganization-energy parameter, meV;
- `ħω`: effective vibrational-mode energy, meV;
- `k_B`: Boltzmann constant, `0.08617333262 meV/K`;
- `T`: device temperature, K.

Dimensional check: `λ ħω` has units meV² and `coth(...)` is dimensionless, so `σ²` has units meV².

### Independent high-temperature check

For `x = ħω/(2k_BT) << 1`, `coth(x) = 1/x + x/3 + ...`, hence

`σ_D² ≈ 2 λ k_B T + λ(ħω)²/(6 k_B T) + ...`.

The first term is the classical Marcus high-temperature variance. The committed script verifies convergence to this limit at 10,000 K to relative error `<1e-4`.

## Temperature-error sensitivity

Using the **synthetic v3.4 planning priors** `λ=150 meV`, `ħω=15 meV`, the analytic derivative is

`dσ/dT = [1/(2σ)] d(σ²)/dT`

with

`d(σ²)/dT = λ ħω csch²(x) [ħω/(2 k_B T²)]`.

Committed outputs show:

| T | synthetic σ_D | dσ/dT | bias from 1 K temperature error |
|---:|---:|---:|---:|
| 120 K | 60.233 meV | 0.1806 meV/K | 0.1806 meV |
| 150 K | 65.601 meV | 0.1763 meV/K | 0.1763 meV |
| 240 K | 80.462 meV | 0.1538 meV/K | 0.1538 meV |
| 300 K | 89.286 meV | 0.1408 meV/K | 0.1408 meV |

Thus, **under this synthetic model**, ±1 K sensor error contributes far less than the v3.4 assumed 2 meV linewidth-extraction noise. This does not make temperature control unimportant: Joule heating or a change of transport regime can bias the physics itself rather than merely shift the fitted linewidth.

## Qualification article

Use a **non-proprietary R2/reference device**, not D18/PY-IT/eC9, and a bright optical transfer reference. No proprietary-material conclusion is allowed from this qualification.

Experimental hierarchy must remain:

`reference batch → substrate/device → pixel → temperature → injection point → repeat acquisition`.

Temperatures and injections are repeated observations, not independent fabrication samples.

## Frozen feasibility sequence

### LT-0 — room-temperature baseline

At 300 K acquire:
- J–V / Voc;
- photovoltaic EQE or sensitive EQE where available;
- absolute/injection-resolved EL at `Jinj/Jsc = 0.1, 0.25, 0.5, 1, 2, 5`;
- CT/near-gap spectral region used for linewidth analysis;
- DUT-adjacent and stage temperatures.

### LT-1 — 150 K primary qualification

Cool in the dark under controlled atmosphere/vacuum. After thermal equilibration, repeat the locked measurements. 150 K is the first low-temperature point because published PM6:Y6 evidence supports broadly preserved charge-generation behavior in this neighborhood while lower temperatures carry more extraction risk.

### LT-2 — 120 K conditional qualification

Proceed to 120 K **only if LT-1 passes all critical operating-regime and metrology gates**. A 120 K failure does not invalidate the entire low-temperature discriminator; it retires 120 K for this reference/process and leaves 150 K as the low-temperature anchor.

### LT-3 — return-to-300 K recovery

Warm to 300 K and repeat the baseline. This distinguishes reversible low-temperature behavior from device degradation/contact rearrangement.

## Critical gates

Thresholds are engineering assumptions to be retired by the qualification dataset.

### Q-LT1: device survival / reversibility

After return to 300 K:
- `|ΔVoc| <= 10 mV`;
- `|ΔVnr| <= 5 mV` where qualified absolute-EL/reciprocity data exist;
- `|ΔPmax| <= 5%` relative to pre-cycle baseline.

Failure: do not use this device/reference for mechanism classification.

### Q-LT2: operating-regime equivalence

At 150 K, and separately at 120 K if attempted:
- normalized photovoltaic-EQE spectral shape must not show a new qualitative band/edge;
- preregistered shape metric: cosine similarity of normalized EQE over the common valid wavelength/energy window `>=0.995`;
- no discontinuity in Voc(T) larger than `20 mV` relative to a local smooth/linear trend defined without the test point;
- injection-resolved EL must retain a stable spectral family around the primary operating point; material spectral-shape evolution between `0.5–2 × Jsc` triggers an H4/non-equilibrium flag.

The numeric thresholds are planning assumptions. Failure means the low-temperature point is **not comparable enough for confirmatory static-vs-dynamic inference**, even if spectra are measurable.

### Q-LT3: Joule-heating / injection control

For every injection point record electrical power `P = I V` and DUT/stage temperature difference.

Fit the empirical effective thermal resistance in the locally linear regime:

`R_th,eff = d(T_DUT - T_stage)/dP`  [K/W].

Primary 0.5–2 × Jsc analysis window passes only if measured injection-induced DUT heating is `<=0.5 K` at the selected operating point. If not, lower injection, improve thermal coupling, or use reciprocity/sensitive-EQE as primary evidence.

No assumed `R_th` value is permitted in the final analysis.

### Q-LT4: CT spectral SNR and repeatability

At the low-temperature point:
- background/dark contribution `<=10%` of weakest accepted signal;
- integrated spectral SNR `>=20` in the preregistered CT/near-gap fit region;
- three repeat linewidth extractions on the same mounted device must have SD `<=2 meV` to remain compatible with the v3.4 nominal recovery simulation.

If empirical SD exceeds 2 meV, rerun the committed mechanism-recovery simulation with the measured noise distribution before choosing N=7 or N=9. Do not loosen the gate post hoc.

### Q-LT5: temperature metrology

- DUT-adjacent absolute temperature error target `<=1 K`;
- acquisition stability SD `<=0.25 K`;
- stage and DUT sensor streams retained;
- any electrical-power-correlated temperature rise is reported separately from sensor calibration uncertainty.

### Q-LT6: model adequacy

Do not force the one-mode model.

Compare at minimum:
1. classical Marcus high-T form;
2. one-mode Keil/Franck–Condon planning form;
3. static-plus-dynamic form;
4. a more flexible/multimode alternative only if residual structure justifies the extra parameters.

Use leave-one-temperature-out prediction and residual inspection. The one-mode model may remain the synthetic power generator only if it does not materially underperform a justified alternative. If it fails, update the generator and rerun H1–H4 recovery before physical mechanism claims.

## Why 150 K is now primary

Under the frozen synthetic `15 meV` mode prior, the exact Keil variance exceeds the classical high-temperature Marcus approximation by:
- 150 K: **10.98%**;
- 240 K: **4.35%**;
- 300 K: **2.79%**.

So 150 K provides materially more model leverage than the original 240–330 K grid without immediately forcing the experiment into the riskier <150 K region documented in PM6:Y6. 120 K provides still more leverage (16.95%) but is now conditional on an empirical equivalence test.

## Conventional explanations / counterexamples

A low-temperature linewidth change is not automatically static-disorder evidence. Plausible alternatives include:
- dynamic/vibronic broadening;
- a transition into transport/extraction-limited behavior;
- injection/state filling;
- contact barriers changing with temperature;
- Joule heating and DUT/stage thermal gradients;
- detector/background changes;
- multiple vibrational modes causing an apparent intercept.

The qualification protocol exists to distinguish measurement feasibility from mechanism inference.

## Decision table

- **150 K passes, 120 K passes:** rerun v3.4 recovery using empirical linewidth-noise and actual temperature grid; choose N=7 or N=9 only after that result.
- **150 K passes, 120 K fails:** retire 120 K; use 150 K plus higher-temperature points and rerun recovery.
- **150 K fails operating-regime equivalence:** do not use low-temperature linewidth as the confirmatory H1 discriminator on R2; seek another observable/material/reference.
- **Spectra fail SNR/repeatability:** improve detector/integration/calibration before increasing substrate count.
- **One-mode model fails held-out prediction:** update the physical generator before sample-size decisions.

## Publication boundary

Passing this protocol establishes **measurement feasibility and operating-regime comparability for the reference**. It does not establish static disorder, EPC, open-quantum transport, or a power advantage.
