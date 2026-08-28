# v3.46 evidence record — field-dependent generation

Date: 2026-08-27 (America/Chicago)

## Established external evidence used

Zhang et al., *Overcoming the fill-factor limit of organic solar cells*, Nature Photonics, version of record 2026-06-19, DOI `10.1038/s41566-026-01946-8`, reports field-dependent free-charge generation and an associated Voc–FF trade-off in the organic-solar-cell systems studied, using TDCF, bias-dependent PL, device measurements and modelling. The paper identifies source data at Zenodo DOI `10.5281/zenodo.20082078` and public model code at `https://github.com/HuotianZhang/DriftFusionOPV_FieldDependent`.

This is **material-system precedent**, not D18/PY-IT/eC9 evidence.

## New project evidentiary state

**Prospective protocol:** B0/B1/B2 useful-work interpretation now has an executable field-generation discriminator. TDCF is primary; bias-dependent PL/J-V is supporting; absorbed-photon normalization, morphology/thickness and contact/transport controls are mandatory. The independent unit for a strong useful-work claim remains the fabrication lot.

**Engineering assumption still open:** a B1/B2 interface state that lowers nonradiative loss can preserve field-robust charge generation. No physical noninferiority margin has been invented; it must be derived prospectively from B0 repeatability, instrument capability and power analysis before unblinding.

**Synthetic/model result:** the committed arithmetic fixture yields `L_B0=0.12`, `L_B2=0.25`, `D_B2=+0.13`. These values test estimator sign and code only and have no material-property meaning.

## Strong nulls/conventional explanations

1. FF changes may arise from transport, contacts, series resistance or non-geminate recombination without any field-dependent generation change.
2. Absorption, thickness or morphology changes may alter PL/apparent generation without an Ex-to-CT field-sensitivity change.
3. Fluence, heating, prebias history or TDCF timing can generate apparent arm differences.

The prospective packet requires measurements that can distinguish the first two; the third remains an execution-control requirement.

## Kill/narrow gate

If an arm lowers `DeltaVnr` but violates the prospectively frozen field-generation noninferiority rule and fails to improve stabilized FF/Pmax, classify the result as voltage-loss/mechanism science, not useful-work/platform validation.
