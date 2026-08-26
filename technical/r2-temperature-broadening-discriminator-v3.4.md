# v3.4 — Low-temperature CT-broadening discriminator

## Status

**Synthetic/model planning result. No R2 devices have been fabricated or measured.**

This increment tests the v3.3 proposal to add an orthogonal temperature-dependent CT-linewidth observable before increasing sample count blindly.

## Established evidence and source provenance

- Tvingstedt, Benduhn, Vandewal, *Materials Horizons* 7, 1888–1900 (2020), DOI `10.1039/D0MH00385A`: CT-state EL linewidths in multiple OSC systems narrowed on cooling; the paper gives the high-temperature classical Marcus variance `sigma_D^2 = 2 lambda k_B T`, shows low-temperature saturation, and argues for a Franck–Condon/Keil treatment with low-frequency vibrational modes. It explicitly warns that single-temperature optical tails need not measure a static DOS.
- Göhler et al., *Physical Review Applied* 15, 064009 (2021), DOI `10.1103/PhysRevApplied.15.064009`: temperature-dependent CT absorption/emission with electro-optical reciprocity temperature validation; dynamic/vibrational broadening dominated the investigated systems.
- These papers concern other OSC material systems. They justify the discriminator physics, **not** the numerical R2 synthetic parameters below.

## Governing equations

The planning dynamic linewidth variance is the Keil/semi-classical harmonic-mode form

`σ_D²(T) = λ ħω coth[ ħω / (2 k_B T) ]`

and the static-plus-dynamic alternative is

`σ_T²(T) = σ_S² + σ_D²(T)`.

Symbols:
- `σ_D`, `σ_T`, `σ_S`: dynamic, total, and static Gaussian linewidth standard deviations, meV;
- `λ`: reorganization energy, meV;
- `ħω`: effective vibrational quantum, meV;
- `k_B = 0.08617333262 meV K^-1`;
- `T`: absolute temperature, K.

Dimensional check: `λ ħω` has units meV²; `coth()` is dimensionless; therefore both variance terms are meV².

### Independent high-temperature check

For `x = ħω/(2 k_B T) << 1`, `coth(x) ≈ 1/x + x/3 + ...`, so

`σ_D²(T) ≈ 2 λ k_B T + λ(ħω)²/(6 k_B T) + ...`.

Thus the Keil model must approach classical Marcus broadening at high temperature.

For the **synthetic planning prior** `ħω = 15 meV`, the exact Keil/Marcus variance ratio is:

| T (K) | Keil / Marcus | excess over Marcus |
|---:|---:|---:|
|120|1.16949|16.95%|
|150|1.10978|10.98%|
|180|1.07674|7.67%|
|240|1.04346|4.35%|
|270|1.03440|3.44%|
|300|1.02790|2.79%|
|330|1.02308|2.31%|

**Decision-driving consequence:** the existing AT-04 grid `240/270/300/330 K` sits mostly in the near-classical regime and provides weak curvature leverage for separating static from dynamic broadening. A low-temperature point near 120–150 K adds substantially more model leverage.

## Frozen synthetic assumptions

Nominal mechanism-recovery generator:

- temperatures: `120/150/240/270/300/330 K`;
- `ħω = 15 meV`, literature-motivated planning prior, not an R2 fit;
- `λ = 150 meV`, synthetic planning value;
- H1 static variance per substrate: `σ_S² = max(100, 1600 + 600 z) meV²`, `z ~ N(0,1)`;
- H2/H3/H4 nominal linewidth generator: `σ_S² = 0`;
- linewidth measurement noise: `2 meV` one-sigma nominal sensitivity case;
- v3.3 `ΔVnr` mechanism effect SD `10 mV`, random noise SD `4 mV`;
- H4 thresholds and generator retained from v3.3;
- low-dimensional classifier only; H5/EPC remains excluded.

The numerical `σ_S`, `λ`, `ħω`, and noise values above are **synthetic assumptions**. They must be replaced or bounded by R2 reference measurements before experimental interpretation.

## New H1 feature

For each synthetic substrate, fit in variance space

`σ²(T) = a + λ_fit f(T)`

where

`f(T) = ħω coth[ħω/(2 k_B T)]`

and `ħω` is fixed by an independent vibronic prior. The fitted intercept `a` is used only as a **static-variance proxy**. It is not called measured static disorder without model-selection evidence.

The v3.3 classifier is expanded so H1 can earn held-out predictive support through either:

1. `E_U -> ΔVnr`, or
2. temperature-derived static-variance proxy `a -> ΔVnr`.

H3 retains the ideality predictor. H4 retains injection/state-filling priority alerts. Any candidate still needs at least 20% LOSO-MAE improvement over intercept-only.

## Nominal confusion-matrix result

`5,000` synthetic datasets per true H1/H2/H3/H4 class were evaluated for the nominal 2 meV linewidth-noise case.

| independent substrates | H1 | H2 | H3 | H4 |
|---:|---:|---:|---:|---:|
|5|73.38%|71.78%|73.56%|100%|
|7|84.84%|81.46%|86.74%|100%|
|9|91.02%|87.26%|93.90%|100%|

Wilson 95% Monte Carlo intervals for the N=7 nominal run:
- H1: 83.82–85.81%;
- H2: 80.36–82.51%;
- H3: 85.77–87.65%;
- H4: 99.92–100%.

### Seed sensitivity

Ten additional 2,000-dataset-per-class seeds at `N=7`, 2 meV linewidth noise gave:

- H1 recovery 84.3–86.55%;
- H2 80.15–83.25%;
- H3 86.35–88.65%;
- H4 100%.

The >=80% all-class gate therefore survives this seed check, but H2 remains close enough to 80% that the design is **conditional rather than robustly overpowered**.

### Linewidth-noise sensitivity at N=7

Seeded sensitivity runs from 1–4 meV linewidth noise all remained near or above the 80% per-class gate under the stated generator. H2 is the limiting class (~80–82%), demonstrating the main tradeoff: adding another H1 predictor improves H1 recovery but creates additional false-H1 competition against the null.

## What changed relative to v3.3

- `N=5` still fails confirmatory mechanism recovery and remains exploratory.
- Under this **specific synthetic static-disorder generator**, adding 120/150 K linewidth information makes `N=7` cross the >=80% all-class synthetic recovery gate.
- `N=9` remains preferable for a strong-publication margin: H1 exceeds 90% only at N=9 in the nominal run.

This does **not** establish that seven R2 substrates will be sufficient experimentally. The new result is conditional on a measurable static contribution, fixed/independently constrained vibrational energy, and the stated noise model.

## Conventional/null explanations and discriminator limits

1. **Dynamic vibronic broadening can mimic disorder tails.** A room-temperature or high-temperature `E_U`/linewidth is not a static-DOS measurement by itself.
2. **Multiple vibrational modes can invalidate a one-mode intercept interpretation.** The 2020 study shows that high- and low-frequency modes can generate misleading high-T extrapolations.
3. **Temperature-dependent injection/state filling can shift EL spectra.** H4/reciprocity checks remain mandatory.
4. **Contact/interface recombination can alter voltage loss without bulk-tail changes.** `V_OC`-intensity remains a competing H3 discriminator.
5. **EPC/vibronic loss is not H1.** Residual behavior after H1–H4 is not evidence for H5/EPC.

## Measurement-design correction

The earlier AT-04 temperature set `240/270/300/330 K` remains appropriate for reference metrology and the modern-OPV MLJ program, but it is **not sufficient by itself for a strong static-vs-dynamic CT-linewidth interpretation**. If R2 mechanism classification is pursued, add low-temperature EL/FTPS points provisionally at `120 K` and `150 K`, subject to:

- device function and non-destructive thermal cycling;
- actual DUT temperature validation;
- injection-density control;
- adequate CT-tail/EL SNR;
- no frozen-condensation/environment artifact;
- independent constraint on the relevant vibronic-mode scale where practical.

## Publication level

`Exploratory / reproduced synthetic calculation`. The equations, executable generator/classifier and machine-readable outputs are committed. The high-temperature limit is independently cross-checked analytically. There is no experimental support yet.

## Single best next increment

Before fabricating more substrates, perform an **R2 low-temperature feasibility qualification** on a non-proprietary reference: verify that the weak-EL device survives and remains measurable at 120/150 K, establish linewidth repeatability/temperature accuracy/injection dependence, and replace the synthetic 1–4 meV linewidth-noise range with an empirical uncertainty distribution. Then rerun the committed recovery simulation with measured noise.
