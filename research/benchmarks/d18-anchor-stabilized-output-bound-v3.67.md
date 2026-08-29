# v3.67 — D18/PY-IT/eC9 stabilized-output evidence boundary

## Changed evidentiary state

**Claim class: primary-source evidence boundary plus project decision rule.** The target anchor now has a sharper output-evidence classification. Luo et al. report that the optimized `D18:PY-IT:eC9 = 1:0.2:1` pseudo-bulk-heterojunction device gains approximately 20 meV in `Voc`, exceeds 18% PCE, and does not sacrifice `Jsc` or FF. However, the inspected main-article Methods describe a conventional J–V scan with about 5 ms delay per voltage point and do not describe maximum-power tracking or a stabilized-Pmax trace.

Therefore the published target result is **scanned J–V/PCE evidence, not evidence that the repository's stabilized useful-work gate has passed**. This is a negative evidentiary result, not a claim that the device would fail under stabilization.

## Why this is the bounded next increment

The current program already has merged prospective B0 field-generation and pseudo-FF/FF transport protocols, plus durability logic. Open PRs #58 and #59 cover manufacturing scale and HTL/contact confounding. Another protocol or scale benchmark would drift. The most decision-relevant unresolved shortcut is whether the target anchor's headline PCE can stand in for sustained useful electrical work. It cannot, on the inspected public main-article record.

## Primary source and exact scope

Yongmin Luo et al., *Suppressing electron-phonon coupling and energy loss in organic solar cells by modulating donor-acceptor penetrated-interface*, **Nature Communications** 17, 2026 (2026), DOI `10.1038/s41467-026-68731-7`; published 2026-01-26, version of record 2026-02-26.

Main-article facts used:

- Fig. 5f is the optimal `D18-PY-IT-eC9` device at ratio `1-0.2-1` under the pseudo-bulk-heterojunction/layer-by-layer ternary strategy.
- The article states an approximately `20 meV` `Voc` increase, `>18%` efficiency, and no sacrifice in `Jsc` and FF.
- Methods report a Keysight B2901A J–V measurement under AM1.5G on a `0.041 cm²` illuminated area, with about `5 ms` delay per voltage point.
- Searches of the inspected main article for `maximum power`, `MPPT`, `stabilized`, and `stabilised` returned no method/result description.

The scope is deliberately narrow: **the inspected main article does not establish stabilized-Pmax evidence**. This packet does not assert that supplementary, unpublished, or later stabilized measurements do not exist.

## Quantitative/unit audit

The only new arithmetic is a unit conversion of the reported approximate per-point delay:

`t_delay,s = t_delay,ms / 1000 = 5 / 1000 = 0.005 s`.

The conversion is dimensionally exact once the nominal `5 ms` source value is accepted. The executable independently checks ordinary floating-point conversion against `Fraction(5,1000)` at absolute tolerance `1e-12`.

Crucially, **0.005 s is not interpreted as a stabilization duration or device time constant**. The source says it is an approximate delay associated with J–V stepping. No total scan duration is reconstructed because the reported voltage-step wording is not sufficiently precise to support that inference.

## Existing project gate; no new threshold

`technical/current-specification.md` already requires:

- at least `5%` relative **stabilized** `Pmax` improvement;
- the same sign across at least `3` independent lots;
- field-dependent-generation evidence;
- conventional morphology/contact/transport controls;
- durability before strong platform/useful-work promotion.

v3.67 adds no new physical threshold. It only prevents a scanned PCE result from silently satisfying a stabilized-output requirement.

## Independent, limiting, and negative checks

Run:

```bash
python models/d18_anchor_stabilized_output_bound_v367.py
```

The standard-library validator checks:

1. **Independent numeric representation:** `5 ms -> 0.005 s` by float and exact rational arithmetic.
2. **Limiting case:** a hypothetical evidence record containing a stabilized-output trace and at least three independent material lots is classified as stabilized-output evidence present.
3. **Negative control:** a J–V scan without a stabilized-output trace remains `SCANNED_JV_ONLY_NOT_STABILIZED_PMAX_GATE` even if its nominal performance is favorable or many devices are imagined.
4. **Fail-closed control:** no output evidence is never upgraded to useful-work evidence.
5. **Hierarchy-domain control:** a negative lot count is rejected.

These controls test the evidence classifier, not device physics.

## Uncertainty and sensitivity

No formal uncertainty is invented for the article's approximate `~20 meV`, `>18%`, or `~5 ms` statements. The decision is insensitive to ordinary rounding of those values because it depends on **measurement type**: a J–V scan and a stabilized maximum-power trace answer different questions.

Systematic terms that can separate scanned and sustained output include scan-rate/delay response, capacitance/transients, illumination or temperature drift, conditioning, and degradation. This increment estimates none of them because no target stabilized trace is available in the inspected record.

## Statistical independence

The target paper's optimized device result is not converted into a project lot-level effect. The machine-readable contract assigns `0` independent material lots **established for the optimized-output project gate**, meaning zero qualifying project-gate lots are established by the inspected publication—not that the authors fabricated only one device. No device count is invented.

For the eventual project test, preserve `material lot -> fabrication lot -> substrate -> device -> session -> measurement`. Pixels, scans, and voltage points are not independent lots.

## Serious conventional explanations / failure modes

At least three ordinary explanations remain live:

1. **Scan-versus-steady-state response.** Capacitive, transient, hysteretic, thermal, or conditioning behavior can make a J–V maximum differ from sustained maximum-power output.
2. **Voltage gain without sustained power gain.** A `Voc` increase can coexist with unchanged instantaneous `Jsc`/FF yet fail to yield a durable stabilized-Pmax improvement after operating-point relaxation or ageing.
3. **Reproducibility/lot confounding.** An optimized device-level result does not establish the same-sign improvement over independent material/fabrication lots.

None of these explanations says the anchor result is wrong. They define what still has to be tested before useful-work language.

## Decision and falsifier

**Decision change:** do not cite the anchor's `>18%` scanned PCE as evidence that H-EPC has passed the repository's useful-work gate. It remains valuable target-chemistry device evidence supporting continued testing.

**Falsifier/retirement condition:** prospectively measure D18:eC9 versus D18:PY-IT:eC9 stabilized-Pmax traces across at least three independent material lots, while retaining the already-merged field-generation and transport/contact controls. If the interface arm clears the existing `>=5%` relative stabilized-Pmax gate with the same sign across lots, this output-evidence gap is retired for that measured regime.

## Technical/business delta

The commercial bridge remains promising but has not yet crossed from voltage-loss/scan-performance evidence into sustained useful-work validation. This avoids treating a headline efficiency number as equivalent to operational power, and it focuses the next experimental spend on the measurement that can actually change the commercialization decision.

## Corrections/superseded claims

No prior measurement or literature value is corrected. No physical tolerance is relaxed. This increment narrows only an evidentiary interpretation: scanned PCE is not stabilized Pmax.

## Single best next increment

Execute the combined B0/B1/B2 target-chemistry campaign on real devices, with **stabilized Pmax as the sink metric on the same lot hierarchy used for TDCF/bias-dependent PL and pseudo-FF/FF**, and freeze empirical noninferiority margins from B0 before unblinding B1/B2.
