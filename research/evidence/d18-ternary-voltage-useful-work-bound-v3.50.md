# v3.50 evidence note — D18/PY-IT/eC9 voltage-only useful-work bound

## Changed evidentiary state

**Claim class:** derived literature bound / decision aid, not a new measurement.

The primary D18/PY-IT/eC9 paper reports that its optimized pseudo-bulk ternary device gains approximately **20 meV in `Voc`**, exceeds 18% efficiency, and shows no sacrifice in `Jsc` and FF. That favorable voltage result is useful mechanism/optimization evidence, but the reported ~20 mV voltage increment by itself is **insufficient evidence for this repository's >=5% relative stabilized-`Pmax` useful-work gate** unless the baseline `Voc` were at most 0.4 V.

This is a necessary-condition bound on the isolated voltage contribution. It does **not** say that the paper's total PCE gain is <=5%, because `Jsc` and/or FF may also improve and the paper statement "no sacrifice" is not numerically equivalent to holding them exactly fixed. It also does not replace prospective stabilized-MPP measurements.

## Primary-source provenance

Luo, Y. et al., *Suppressing electron-phonon coupling and energy loss in organic solar cells by modulating donor-acceptor penetrated-interface*, **Nature Communications 17, 2026 (2026)**, DOI `10.1038/s41467-026-68731-7`.

- Published: 2026-01-26; version of record: 2026-02-26.
- Data record cited by the article: `10.6084/m9.figshare.29390669`.
- Article statement used here: optimized D18-PYIT-eC9, ratio 1-0.2-1, approximately 20 meV higher `Voc`, >18% efficiency, no sacrifice in `Jsc` and FF.
- The article reports additional data are available via its main/SI material and the cited Figshare record. This increment does not claim to have reconstructed Fig. 5f or stabilized-power traces.

## Governing equation and dimensional check

By definition,

`FF = Pmax / (Voc Jsc)`,

so for equal illumination/area conventions,

`Pmax = Voc Jsc FF`.

Isolating only the voltage contribution by holding `Jsc` and FF fixed gives

`G_V = Pmax,1/Pmax,0 - 1 = (Voc,0 + deltaVoc)/Voc,0 - 1 = deltaVoc/Voc,0`.

`G_V` is dimensionless because volts divide by volts. The existing project target is `G_target = 0.05`. Solving the boundary condition `G_V = G_target` gives

`Voc,0,max = deltaVoc / G_target`.

For literature-derived `deltaVoc ~= 0.020 V`,

`Voc,0,max = 0.020 V / 0.05 = 0.400 V`.

Thus any baseline `Voc > 0.400 V` yields a voltage-only relative power contribution below 5% for a +20 mV shift.

## Independent check, limiting cases, and sensitivity

`models/voltage_only_useful_work_bound_v3_50.py` evaluates the gain two ways:

1. `deltaVoc/Voc,0`;
2. the explicit ratio `(Voc,0 + deltaVoc)/Voc,0 - 1`.

Agreement tolerance is `1e-12` in dimensionless gain. A frozen synthetic arithmetic negative fixture uses `Voc,0 = 0.8 V`, giving `0.020/0.8 = 0.025`, i.e. **2.5%**, which fails the 5% gate. This 0.8 V value is a code fixture, not a D18/PY-IT/eC9 measured property.

Sensitivity to the approximate literature shift is linear:

| `deltaVoc` | voltage-only `Voc,0` boundary for 5% |
|---:|---:|
| 15 mV | 0.300 V |
| 20 mV | 0.400 V |
| 25 mV | 0.500 V |

The decision changes only if the actual paired `Jsc`/FF contributions raise total stabilized `Pmax`, or if the project target is changed for independently justified reasons. A 100x common voltage-unit scaling leaves the dimensionless gain unchanged; `deltaVoc=0` gives zero gain.

## Uncertainty and validity domain

The source describes the voltage increase approximately; no source measurement uncertainty for the ~20 meV summary value is assigned here. Therefore this is a **sensitivity bound**, not an uncertainty-qualified reproduction of device performance. The 15–25 mV range is an explicit arithmetic sensitivity interval around the reported approximate value, not a confidence interval and not a material-property uncertainty.

The decomposition is valid only for isolating the voltage term under fixed `Jsc`, FF, illumination, and area conventions. It must not be used to infer total stabilized power when those terms vary.

## Statistical independence

No new device observations are analyzed, so there is no new independent experimental sample count. A champion literature device or repeated J–V scans must not be converted into independent fabrication-lot evidence. The repository's >=3 independent-lot stabilized-`Pmax` gate remains unchanged.

## Serious conventional explanations / failure modes

1. **Ordinary `Jsc` or FF improvement could supply the missing power gain.** This increment directly bounds only the voltage contribution; exact paired stabilized-power data are required to resolve the total useful-work question.
2. **Transient/champion J–V performance can differ from stabilized MPP.** The cited paper's >18% optimized-device statement does not by itself establish the repository's stabilized-`Pmax` criterion.
3. **Mechanism attribution is non-unique.** Even a real power gain could arise from morphology, contacts, thickness, transport, or optical changes rather than the proposed P-interface/EPC mechanism; field-generation and morphology/contact controls remain required.

## Falsification and decision consequence

This bound is falsified if the algebraic power identity/decomposition is wrong, if the source's ~20 meV statement is mis-provenanced, or if the canonical project useful-work threshold is not 5%. It does not predict a device result.

**Decision consequence:** do not count the literature's favorable ~20 mV `Voc` increment as satisfying the project's useful-work gate. The physical bridge still requires paired, prospective stabilized-MPP evidence, with `Jsc`, FF, field-generation robustness, durability, and lot independence preserved.

## Reproduction

```bash
python models/voltage_only_useful_work_bound_v3_50.py
```

Expected key output: `voc0_max_for_voltage_only_target_V = 0.4`, negative fixture gain `0.025`, status `PASS`.
