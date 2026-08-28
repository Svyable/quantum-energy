# v3.60 — D18 molar-mass manufacturing confound bound

## Changed evidentiary state

**Established external evidence:** Cardoso et al., *ACS Omega* (2026), DOI `10.1021/acsomega.5c12462`, systematically varied D18 molar mass and fabricated blade-coated D18:Y6:PC70BM devices under ambient conditions over a reported active area of 0.55 cm². The paper reports low-molar-mass D18 (~12–14 kg mol⁻¹) devices below 2% PCE, high-molar-mass D18 (~83–93 kg mol⁻¹) devices at 7.8–8.0% PCE, and a commercial D18 reference (~92 kg mol⁻¹) at 8.9% PCE. The source states that averages/standard deviations correspond to eight independent devices per system.

**Engineering-control consequence:** D18 molar-mass/batch provenance is now treated as a serious manufacturing and causal-attribution confound for the B0/B1/B2 commercial-bridge campaign. A comparison that changes PY-IT/interface processing while also changing or failing to record the D18 lot cannot cleanly attribute a device-level effect to the intended interface/EPC variable.

This increment **does not** establish a D18/PY-IT/eC9 molar-mass acceptance window and does not claim the effect size transfers from D18:Y6:PC70BM to D18:eC9 or D18:PY-IT:eC9.

## Source/version provenance

Primary source:

- Renata S. Cardoso et al., “Tuning Molar Mass of the D18 Polymer via Stille Polymerization: Impact on Morphology and Large-Area Blade-Coated Organic Solar Cells,” *ACS Omega* 11(10), 16489–16500 (2026).
- DOI: `10.1021/acsomega.5c12462`
- Published online: 2026-03-02; issue date: 2026-03-17.
- Article license reported by the publisher: CC BY 4.0.
- This repository independently reimplements only the arithmetic/control logic; no upstream code or dataset is copied.

Machine-readable source facts and classifications are frozen in `research/data/d18-molar-mass-manufacturing-bound-v360.json`.

## Quantitative bound

Let

- `P_high,min = 7.8%`, the lower edge of the source's summarized high-Mw PCE range;
- `P_low < 2.0%`, the source's stated low-Mw PCE ceiling;
- `P_com = 8.9%`, the commercial-D18 reference PCE.

The conservative source-summary multiplier is

`M = P_high,min / 2.0% = 7.8 / 2.0 = 3.9`.

Because the source states `P_low < 2.0%`, not `= 2.0%`, the actual ratio implied by these source summaries is strictly

`P_high,min / P_low > 3.9`.

This is dimensionless. It is a bound on the reported source systems only; it is not a predicted scale penalty or target-material effect.

The high-Mw source range as a fraction of its commercial D18 reference is

`7.8 / 8.9 = 0.876404...`

through

`8.0 / 8.9 = 0.898876...`.

Thus high-Mw experimental batches reached about 87.6–89.9% of the commercial-reference PCE in this source configuration. This arithmetic does not establish equivalence of morphology, lifetime, stabilized power, or scale robustness.

## Independent calculation and controls

Run:

```bash
python models/d18_molar_mass_manufacturing_bound_v360.py
```

The executable uses ordinary floating-point arithmetic and independently recomputes the decimal source summaries with exact `fractions.Fraction` arithmetic. Predeclared numerical agreement tolerance is `1e-12` absolute.

Controls/limiting cases:

1. `lot_id=true`, `mw_recorded=true`, `same_lot_randomized=true` is the only positive causal-attribution fixture.
2. Missing Mw provenance fails closed.
3. Different/uncontrolled D18 lots across compared arms fail closed.
4. Missing D18 lot identity fails closed.
5. Positive-PCE/domain and area checks prevent invalid division or an implied area penalty.

The independent arithmetic path is an implementation cross-check, not independent physical replication.

## Prospective B0/B1/B2 control

For an interface/process comparison to be eligible for strong causal interpretation, record:

1. D18 supplier/synthesis lot identifier;
2. measured molar-mass characterization or supplier batch-specific characterization, including method/version where available;
3. the same D18 lot randomized across B0/B1/B2 within each fabrication lot.

If multiple D18 lots are intentionally studied, retain `D18 lot` as a fabrication-level grouping factor rather than pooling devices as independent repeats. Preserve the hierarchy

`material lot -> fabrication lot -> substrate -> device/pixel -> session -> measurement`.

No numerical Mw pass/fail threshold is frozen here. A physical threshold would require target-chemistry baseline data, supplier specifications tied to real lots, or prospective power/robustness evidence.

## Uncertainty and sensitivity

The abstract/main-text summaries used here do not provide a formal uncertainty for the summarized `~12–14`, `~83–93`, `<2%`, `7.8–8.0%`, or `8.9%` values. None is invented.

The decision-driving bound deliberately uses the least favorable stated high-Mw PCE (`7.8%`) and the exclusive low-Mw ceiling (`2.0%`). The conclusion `ratio > 3.9` therefore does not depend on choosing a value inside the low-Mw `<2%` interval.

The principal uncertainty is **transferability**, not arithmetic: the source uses D18:Y6:PC70BM, while the commercial bridge uses D18:eC9 and D18:PY-IT:eC9.

## Serious conventional explanations / failure modes

1. **Morphology/electrical-quality mediation.** The source associates molar mass with film organization, morphology, shunt resistance, charge transport, aggregation and solvent compatibility. Therefore the performance difference is not a mechanism-pure direct effect of chain length. This is precisely why Mw is a confound to control rather than a new EPC claim.
2. **Material-system non-transferability.** Y6:PC70BM may respond differently to D18 molar mass than eC9/PY-IT:eC9. The magnitude and even detailed optimum may not transfer.
3. **Solvent/process interaction.** The source reports that solvent choice interacts with molar mass; a target process could reduce, reverse or reshape the observed dependence.
4. **Best-device versus stabilized-useful-work distinction.** Source PCE values do not by themselves satisfy this program's stabilized-Pmax, field-generation or durability gates.

The current increment directly bounds failure mode 1 as an attribution problem: same-lot randomization prevents a D18-lot change from being aliased with B0/B1/B2 arm identity.

## Falsifier / narrowing experiment

Run the prospective B0/B1/B2 experiment over multiple characterized D18 lots, randomizing all arms within each D18 lot and measuring the existing multi-objective outputs. If arm effects and arm rankings remain invariant across the verified lot range with appropriately bounded lot×arm interaction, the target-chemistry relevance of this confound can be narrowed quantitatively.

## Manufacturing and safety relevance

The source is manufacturing-relevant because it uses ambient blade coating and demonstrates that polymer synthesis/batch properties and solvent selection can dominate scalable device quality. It also keeps safety/environmental tradeoffs visible: Stille-derived material provenance and halogenated-solvent compatibility must not be hidden behind a PCE-only optimization. This increment does not assign unsupported EHS scores or claim that a particular solvent/process is required for the target bridge.

## Technical/business delta

Before v3.60, the commercial bridge could conceptually compare B0/B1/B2 while treating “D18” as a material label. After v3.60, lot-resolved D18 molecular-weight provenance is a required causal/manufacturing control. This reduces the risk of spending spectroscopy or scale-up effort on an apparent PY-IT/interface signal that is actually donor-batch/process variation.

The result strengthens, rather than replaces, the existing requirements for field-dependent generation, DeltaVnr/Voc, stabilized Pmax, morphology/contact/transport controls, durability and eventual second-material validation.

## Next physical discriminator

The highest-value follow-on is a real target-chemistry B0/B1/B2 campaign in which all arms share characterized D18 lots within fabrication lots. That dataset can estimate D18-lot variance and lot×arm interaction while simultaneously testing field robustness and stabilized useful work; only then is a target-specific Mw tolerance justified.
