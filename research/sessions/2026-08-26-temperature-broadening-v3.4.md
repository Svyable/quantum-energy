# Session record — v3.4 temperature-dependent CT-broadening discriminator

## What changed

Added a preregistered low-temperature CT-linewidth discriminator to the R2 H1–H4 synthetic mechanism-recovery program.

The main correction is that the existing 240/270/300/330 K AT-04 grid should **not** be interpreted as a strong static-vs-dynamic disorder discriminator. For a representative synthetic `ħω=15 meV` low-frequency mode, the exact Keil linewidth variance differs from the classical Marcus high-T limit by only 4.35%, 3.44%, 2.79%, and 2.31% at 240/270/300/330 K. The proposed mechanism audit therefore adds provisional 120 K and 150 K points, where the differences are 16.95% and 10.98%.

## Evidence added

Primary sources:

1. Tvingstedt, Benduhn, Vandewal, *Materials Horizons* 7, 1888–1900 (2020), DOI `10.1039/D0MH00385A` — temperature-dependent CT-state linewidth narrowing, high-T Marcus behavior, low-T saturation, Franck–Condon/Keil interpretation, and warning against single-temperature static-disorder inference.
2. Göhler et al., *Physical Review Applied* 15, 064009 (2021), DOI `10.1103/PhysRevApplied.15.064009` — temperature-dependent CT absorption/emission, electro-optical reciprocity temperature validation, and dynamic/vibrational broadening dominance in the measured systems.

These studies are material-system precedents, not R2 measurements.

## Governing calculation

`σ_D²(T) = λ ħω coth[ħω/(2 k_B T)]`

with static alternative

`σ_T²(T) = σ_S² + σ_D²(T)`.

Independent high-temperature derivation:

`coth(x) = 1/x + x/3 + ...`, `x=ħω/(2k_BT)`, giving

`σ_D² ≈ 2λk_BT + λ(ħω)²/(6k_BT) + ...`.

This analytically cross-checks the code's convergence to classical Marcus broadening.

## Synthetic assumptions

- `ħω=15 meV`, `λ=150 meV`;
- 120/150/240/270/300/330 K;
- H1 `σ_S²=max(100,1600+600z) meV²`, `z~N(0,1)`;
- H2/H3/H4 nominal static variance zero;
- linewidth noise 2 meV nominal;
- ΔVnr effect/noise inherited from v3.3: 10/4 mV SD;
- 5,000 datasets per class for the nominal N=5/7/9 runs.

All values above are synthetic planning assumptions.

## Synthetic results

At 2 meV linewidth-noise SD:

- N=5 H1/H2/H3/H4 recovery = 73.38/71.78/73.56/100%.
- N=7 = 84.84/81.46/86.74/100%.
- N=9 = 91.02/87.26/93.90/100%.

Ten additional N=7 seeds (2,000 datasets/class) produced ranges:

- H1 84.3–86.55%;
- H2 80.15–83.25%;
- H3 86.35–88.65%;
- H4 100%.

Thus the new observable can make N=7 pass the program's >=80% **synthetic** recovery gate under the stated generator, but H2 remains near the boundary. N=9 retains the stronger margin and pushes H1 above 90% in the nominal run.

## Independent checks

- Dimensional analysis: both variance terms are meV².
- High-T asymptotic expansion independently reproduces the Marcus limit.
- `ħω=15 meV` exact Keil/Marcus ratios were recomputed directly from the governing equation and agree with the asymptotic direction.
- LOSO remains substrate-level; temperature points within a substrate are not promoted to independent fabrication samples.
- Multi-seed sensitivity preserves the N=7 >=80% decision under the current synthetic generator.

Runtime used for local verification: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0. Repository executable depends only on NumPy for the main confusion calculation.

## Conventional/null explanations

- Dynamic vibronic broadening can create optical tails and high-T intercept behavior that is not static DOS disorder.
- Multiple vibrational modes can make a one-mode fit misleading.
- Injection/state filling can alter EL and remains H4.
- Contact/interface recombination remains H3.
- H5/EPC is not inferred from residuals.

## Correction / supersession

Earlier use of the 240–330 K temperature set remains valid for AT-04 reference metrology and temperature-dependent voltage-loss work. It is now **narrowed**: it should not be described as sufficient for strong static-vs-dynamic CT-linewidth identification.

No experimental result is superseded; no R2 physical dataset exists.

## Business/deployment delta

The next capital decision changes from 'fabricate four additional confirmatory substrates' to 'first verify low-temperature measurement feasibility and actual linewidth noise on the non-proprietary R2/reference stack.' If the 120/150 K measurements are stable and precise, the synthetic result suggests a seven-substrate confirmatory design may carry sufficient information. If not, retain N=9 or redesign the discriminator.

## Unresolved risks

- R2 may not remain in a comparable operating/injection regime at 120 K.
- CT EL/FTPS SNR may degrade at low temperature.
- `ħω` may not be adequately represented by one 15 meV mode.
- H1 static contribution may be far smaller than the synthetic generator.
- The extra H1 predictor creates false-H1 competition, leaving H2 close to the threshold.

## Single best next increment

Run a non-proprietary **low-temperature R2/reference feasibility specification**: device-survival/thermal-cycle gate, injection and Joule-heating controls, CT-linewidth repeatability target, 120/150 K SNR requirement, condensation/vacuum controls, and an empirical noise-estimation plan. Replace the synthetic linewidth-noise distribution with measured reference data before choosing N=7 versus N=9.
