# v3.46 — Prospective D18/PY-IT/eC9 field-generation protocol

## Changed evidentiary state

**Claim class:** prospective experiment/protocol. This increment does not claim measured D18/PY-IT/eC9 field robustness. It converts the v3.45 model warning into a blinded, lot-aware physical discriminator that must be passed before lower `DeltaVnr` can support a useful-work claim.

Primary source: Zhang et al., *Overcoming the fill-factor limit of organic solar cells*, Nature Photonics, version of record 2026-06-19, DOI `10.1038/s41566-026-01946-8`. The authors report TDCF and bias-dependent PL evidence for field-dependent free-charge generation in the systems they studied; source data are identified as Zenodo DOI `10.5281/zenodo.20082078`, and the paper identifies public model code at `HuotianZhang/DriftFusionOPV_FieldDependent`. This is method/mechanism precedent, not evidence that B0/B1/B2 behaves the same way.

## Arms and hierarchy

- B0: D18:eC9 baseline.
- B1: D18:PY-IT:eC9 = 1:0.1:1.
- B2: D18:PY-IT:eC9 = 1:0.2:1.
- Independent unit for the strong useful-work claim: **fabrication lot**.
- Preserve `lot -> substrate -> device -> session -> measurement`; pixels, repeat sweeps, or multiple biases do not increase independent lot count.
- Strong useful-work language still requires same-sign stabilized-Pmax improvement across at least three independent lots under the canonical program gate.

## Primary measurement

TDCF is the primary field-generation discriminator. Bias-dependent PL with J-V is supporting evidence and is not treated as a substitute for free-charge extraction unless an independently justified equivalent is validated.

Before coded-arm identities are released, freeze and commit: common prebias grid, reference bias, delay, collection bias, excitation wavelength/fluence, absorbed-photon normalization, temperature window, integration/timing settings, QC rules, and analysis commit. Instrument-safe values are intentionally left `null` in the machine contract rather than invented here.

For each device and preregistered prebias `V`, define

`r(V) = eta_FC(V) / eta_FC(V_ref)`

where `eta_FC` is absorbed-photon-normalized free-charge-generation efficiency from TDCF and `V_ref` is the frozen reference bias. `r` is dimensionless.

Define the worst field-dependent generation loss over the preregistered evaluation set

`L = max_V [1 - r(V)]`.

Within each independent lot, define the arm penalty relative to its contemporaneous baseline

`D_arm = L_arm - L_B0`.

Positive `D_arm` means worse field robustness than B0 under this sign convention. Dimensional analysis: `eta_FC`, `r`, `L`, and `D` are all dimensionless; voltage is used only to index the frozen physical conditions.

## Physical decision gate

No universal non-inferiority margin is asserted from the v3.45 synthetic model or from another material system. The physical margin remains `null` until it is prospectively justified from **B0 repeatability, instrument capability, and prospective power analysis**, then frozen before unblinding.

Fail-closed rule: a B1/B2 useful-work PASS is impossible if the margin was absent or selected after arm unblinding.

Kill/narrow rule: if an interface arm lowers `DeltaVnr`/raises `Voc` but has a field-generation penalty beyond the frozen margin and does not improve stabilized FF/Pmax, retain it as voltage-loss/mechanism science rather than platform/useful-work validation.

## Required companion controls

1. **Transport/contact null:** mobility, extraction, series resistance, contact selectivity, or non-geminate recombination can lower FF without a field-dependent generation change. Acquire the canonical J-V/contact/transport controls and do not assign a TDCF mechanism to an FF change that is absent in TDCF.
2. **Absorption/morphology null:** thickness, absorption, phase separation, or morphology can alter PL and apparent generation. Require absorbed-photon normalization plus morphology/thickness records paired to the same lot.
3. **History/heating null:** fluence, prebias history, delay timing, heating, or light soaking can alter TDCF/PL. Randomize/counterbalance acquisition order where practical and freeze timing/fluence/temperature before unblinding.

The current increment directly bounds the first two by requiring independent TDCF plus electrical and absorption/morphology controls in the same prospective packet; it does not claim those controls have passed experimentally.

## Synthetic arithmetic fixture — not physical evidence

Fixture retention arrays:

- B0: `[1.00, 0.98, 0.94, 0.88]` -> `L_B0 = 0.12`.
- B2: `[1.00, 0.97, 0.90, 0.75]` -> `L_B2 = 0.25`.
- Therefore `D_B2 = 0.13`.

Primary implementation uses `max(1-r)`; the independent algebraic check uses `1-min(r)`. Frozen tolerance is `1e-12`. Limiting case: perfectly field-independent `r(V)=1` gives `L=0`; worsening the minimum retention must increase `L`.

These numbers exist only to test code/sign conventions and are not material constants, expected B2 behavior, or a physical threshold.

## Reproduction

```bash
python3 models/d18_pyit_ec9_field_generation_v346.py --self-test
```

Expected JSON contains `L_B0=0.12`, `L_B2=0.25`, `D_B2=0.13`, and `PASS_SYNTHETIC_FIXTURE` within floating-point tolerance `1e-12`.

Machine contract: `machine/d18-pyit-ec9-field-generation-v3.46.json`.
Raw template: `data/templates/d18-pyit-ec9-field-generation-v3.46.csv`.

## Falsification and next physical measurement

The program hypothesis is narrowed if B1/B2 voltage-loss improvement is not accompanied by field-robust generation and stabilized electrical output across independent lots. The next discriminating measurement is a blinded baseline campaign that establishes B0 TDCF repeatability and instrument-safe timing/bias/fluence settings, enabling a prospective physical non-inferiority margin and power analysis before B1/B2 unblinding.
