# v3.69 — D18/eC9 durability stress-mode benchmark

## Changed evidentiary state

**Claim class: literature-derived experimental benchmark.** A primary target-near D18 system containing BTP-eC9 now provides a quantitative durability bound: the reported lifetime advantage of the ternary device is materially different under 65 °C aging versus continuous illumination. The program must therefore keep thermal and light-stress durability as separate evidentiary axes; one cannot stand in for the other without an experimentally validated acceleration/correlation model.

This is not target D18:PY-IT:eC9 durability evidence and is not a field-lifetime claim.

## Primary source and exact inputs

Primary source: Saisai Liu et al., *Central Molecular Stacking Regulator Boosts the Efficiency of Organic Solar Cells*, **Advanced Functional Materials** (published 2025-11-10), DOI `10.1002/adfm.202525577`. Retrieval/audit date: 2026-08-28.

The publisher article reports for D18:CS4 and D18:CS4:BTP-eC9, respectively:

| Stress mode | D18:CS4 T80 | D18:CS4:BTP-eC9 T80 |
|---|---:|---:|
| 65 °C aging | 1200 h | 2500 h |
| continuous illumination | 550 h | 710 h |

No formal uncertainty is provided for these abstract-level T80 values in the accessible primary-source record, so none is invented. Illumination intensity/spectrum, device temperature, atmosphere, encapsulation and T80 fitting details are not inferred here if not explicit in the inspected source text.

## Calculation

For stress mode `s`, define

`R_s = T80_ternary,s / T80_reference,s`

and relative lifetime gain

`G_s = R_s - 1`.

Both quantities are dimensionless because hours cancel.

Results:

- 65 °C: `R = 2500/1200 = 2.083333333333...`; `G = 1.083333...`, i.e. +108.33% relative lifetime.
- Continuous illumination: `R = 710/550 = 1.290909090909...`; `G = 0.290909...`, i.e. +29.09% relative lifetime.
- Stress-mode ratio-of-ratios: `(2500/1200)/(710/550) = 1.613849765258...`.

The ratio-of-ratios is descriptive only. It does not quantify an activation energy, acceleration factor, or field lifetime.

## Independent verification and tests

Run:

```bash
python models/d18_ec9_durability_stress_mode_v369.py
```

Expected output includes:

- `thermal_ratio=2.083333333333`
- `light_ratio=1.290909090909`
- `ratio_of_ratios=1.613849765258`
- `decision=STRESS_MODE_SPECIFIC_DURABILITY_REQUIRED`
- `checks=PASS`

The primary calculation uses floating-point arithmetic and is independently recomputed with exact `fractions.Fraction` arithmetic at predeclared absolute tolerance `1e-12`. Limiting case: equal T80 values give ratio 1. Negative/adversarial case: a shorter ternary T80 remains below 1. Non-positive T80 inputs fail closed.

Runtime: standard-library Python >=3.12. CI exercises 3.12, 3.13 and 3.14.

## Visible correction history

A pre-PR independent recomputation found that the ratio-of-ratios had initially been transcribed as `1.613372093...`. The correct arithmetic is `1.613849765258...`. The source T80 inputs, individual stress-mode ratios, and scientific decision were unchanged. The incorrect value is retained here in correction history rather than silently erased.

## Uncertainty and sensitivity

No statistical confidence interval can be reconstructed from the abstract values alone because replicate counts/distributions and T80 fit uncertainty are not supplied in the inspected text. Consequently, the project does not attach uncertainty bars or significance claims to the ratios.

The decision does not rely on the last digit of either ratio. The qualitative conclusion is that the *reported relative advantage differs substantially by stress mode*. The source values would need large revisions before the two ratios became equal; the correct next step is direct target-chemistry durability acquisition, not numerical polishing of these literature values.

## Statistical independence

The source values are treated as published device-level lifetime summaries, not independent project lots. They do not satisfy the program hierarchy `material lot -> fabrication lot -> substrate -> device -> session -> measurement`, and they do not count toward the >=3 independent-lot useful-work gate.

## Strongest conventional explanations / failure modes

1. **Different degradation mechanisms dominate thermal and light stress.** Morphology coarsening, interfacial diffusion, photochemistry and electrode/contact evolution need not scale together. This benchmark directly bounds the assumption that one stress mode can proxy all durability.
2. **Device-stack and composition differences.** D18:CS4:BTP-eC9 is target-near because it contains D18 and BTP-eC9, but it is not D18:PY-IT:eC9; CS4 can alter morphology, transport and stability independently of eC9.
3. **Unreported or incompletely inspected test details.** Atmosphere, encapsulation, illumination spectrum/intensity, thermal history and T80 extraction method can shift lifetimes. They must be frozen prospectively before target-system interpretation.
4. **T80 alone can hide mechanism loss.** A device may retain 80% PCE while field generation, ΔVnr, FF or another causal observable drifts; target durability should therefore pair stabilized Pmax with selected mechanism-retention measurements.

## Decision / kill-narrow rule

Do **not** use a thermal-only or light-only durability result to clear the commercial bridge's generic `no unacceptable durability penalty` gate. Until a validated cross-stress model exists, target D18/PY-IT/eC9 must be evaluated under separately preregistered thermal and continuous-light stress modes.

If B1/B2 improves initial ΔVnr or stabilized Pmax but degrades materially faster than B0 in either preregistered stress mode, retain the initial-performance result as mechanism/useful-work-at-time-zero science and narrow or stop the durability/platform claim.

No physical T80 acceptance threshold is invented here. Thresholds must be frozen from real B0 capability, instrument/protocol repeatability, intended use, or a justified prospective power analysis before B1/B2 unblinding.

## Next physical discriminator

Execute a blinded B0 durability baseline first, with separately frozen thermal and continuous-light conditions, stabilized Pmax tracking, full lot/device hierarchy, and enough mechanism-retention observables to distinguish active-layer degradation from contact/transport or measurement drift. Use the B0 distributions to freeze noninferiority margins and sample counts before B1/B2 durability unblinding.
