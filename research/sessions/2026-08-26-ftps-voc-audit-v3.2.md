# v3.2 — FTPS + Voc-intensity mechanism-audit preregistration

## What changed

This session converted the v3.1 recommendation into an executable, falsifiable analysis package before R2 data exist.

Added:

- `technical/ftps-voc-mechanism-audit.md`
- `models/ftps_voc_audit.py`
- `models/ftps_voc_synthetic_expected.csv`

## Evidence/source provenance added

Primary/current sources checked in this session:

1. Göhler et al., *Physical Review Applied* 15, 064009 (2021), DOI `10.1103/PhysRevApplied.15.064009`: temperature-dependent CT absorption/emission, electro-optical reciprocity, and evidence that temperature-activated/vibrational broadening can dominate in tested systems.
2. Yan et al., *Nature Communications* 12, 3642 (2021), DOI `10.1038/s41467-021-23975-3`: CT-energy static disorder can alter voltage-loss inference; injection-dependent EL can probe state filling.
3. *Chemical Science* (2025), DOI `10.1039/D4SC07146H`: recent modern-OSC example using FTPS-EQE + EL for energy-loss analysis, exponential low-energy FTPS fitting for Urbach energy, and EQE_EL for nonradiative loss.
4. Jiang et al., *Nature Communications* 14, 5079 (2023), DOI `10.1038/s41467-023-40806-9`: suppressed electron-phonon coupling can reduce nonradiative loss while morphology/transport remain coupled confounders.
5. Luo et al., *Nature Communications* (published 26 January 2026), DOI/article `s41467-026-68731-7`: current penetrated-interface/EPC commercial-bridge anchor.

## Calculation checks

Decision-driving equations were written explicitly and unit/sign checked.

### Urbach descriptor

`ln(EQE)=a+E/EU`, therefore `EU=1/slope`.

- slope units: `eV^-1`
- `EU` units: `eV`
- positive slope required in the chosen low-energy tail
- noise-free independent two-endpoint derivation agrees with the OLS truth in the synthetic check

### Ideality diagnostic

Natural-log derivation:

`n = [dVoc/dln(I)] / (kBT/q)`.

Independent base-10 derivation:

`n = [dVoc/dlog10(I)] / [(kBT/q) ln(10)]`.

At 300 K using `kB=8.617333262e-5 eV/K`:

- `kBT/q = 25.851999786 mV`
- for synthetic `n=1.30`, expected slope = `77.384358 mV/decade`

The two derivations agree algebraically and in the deterministic synthetic calculation.

### Nonradiative loss

`DeltaVnr = -(kBT/q) ln(EQE_EL)`.

Limiting/sign checks:

- `EQE_EL=1 -> DeltaVnr=0`
- decreasing `EQE_EL` increases positive `DeltaVnr`

## Synthetic verification

Frozen seed: `20260826`.

Local independent calculation during specification creation used Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0 and recovered:

- `EU_true=25.000000 meV`
- seeded OLS `EU_fit=25.002282 meV`
- noise-free endpoint cross-check `25.000000 meV`
- `n_true=1.300000`
- seeded ideality recovery `1.285977`
- natural-log and log10 ideality derivations agree to numerical precision

These are **synthetic/code-verification values, not measurements**.

## Assumptions frozen

- Confirmatory PM6:Y6 empirical-tail window: 1.10–1.30 eV at 300 K.
- Sensitivity windows: 1.08–1.28 and 1.12–1.32 eV.
- If the confirmatory window fails its signal/background criterion, `EU` is reported not estimable rather than moving the window.
- Injection state-filling alert: >=5 meV spectral shift between 0.5× and 2× `Jsc`, provided propagated spectral-energy uncertainty is <=2 meV.
- `Voc`-intensity: at least eight points over nominally 0.1–1.2 sun equivalent at 300 K.

All are engineering/preregistration assumptions, not universal material constants.

## Statistical independence

The audit preserves the program hierarchy:

`lot -> substrate -> pixel -> session -> measurement`.

Five R2 substrates remain five fabrication-level groups. Repeated pixels and sessions cannot inflate the fabrication sample size. Model comparison uses leave-one-substrate-out prediction; high-capacity ML is prohibited.

## Conventional/null explanations retained

- H1 bulk energetic/CT disorder
- H2 thickness/optical-density confound
- H3 interface/contact recombination
- H4 CT-state filling/injection artifact
- H5 vibronic/EPC/triplet loss beyond static disorder

Important narrowing: **FTPS + Voc-intensity cannot confirm H5/EPC causality by itself.** A residual after H1-H4 may preserve H5 as a candidate only; EPC-specific evidence remains required from the later D18/PY-IT/eC9 experiment.

## Correction / supersession

This session narrows earlier language that could be read as treating a single-state CT/Marcus fit as the default mechanism model. The current specification explicitly requires empirical-tail, static-disorder, and temperature-dependent/dynamic alternatives where appropriate. No prior experimental result is changed because no R2 experimental data exist yet.

## Unresolved risks

- The fixed 1.10–1.30 eV tail window may be unusable on the actual R2 signal floor; preregistration intentionally accepts `not estimable` rather than window shopping.
- Five substrates have low model-selection power; mechanism classification may remain ambiguous.
- Ideality factor is not unique to one recombination mechanism.
- Urbach energy is an empirical descriptor and cannot uniquely separate static disorder from vibronic/dynamic broadening.
- H5/EPC requires separate mechanism-specific evidence.

## Single best next increment

Run a synthetic blinded-recovery study for H1–H4 using the exact R2 hierarchy and realistic FTPS/EL/Voc noise. Quantify the confusion matrix and determine whether the frozen 5-substrate design can distinguish thickness, disorder, interface-recombination, and injection-artifact scenarios before physical fabrication.
