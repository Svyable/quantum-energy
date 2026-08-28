# v3.64 — Thick-film transport scale-transfer bound

## Changed evidentiary state

**Claim class: established external experimental evidence plus project engineering bound.** A primary 2025 *Nature Communications* study shows that zero-field mobility alone can fail as a screening criterion for long-distance transport in thick-film organic solar cells. The authors instead combine zero-field mobility, field dependence, and hopping-frequency/critical-length behavior, and they validate the transport change with 300 nm devices.

For the project, this changes one decision: future thick-film or area-scale D18/PY-IT/eC9 transfer cannot satisfy its transport/manufacturability control with a zero-field mobility number alone. At least one field-sensitive transport/collection observable plus direct FF and stabilized-Pmax evidence must remain part of the scale-transfer gate.

This is **not** a D18/PY-IT/eC9 measurement, threshold, or proof that critical length is a unique causal variable.

## Primary provenance

- *Critical length screening enables 19% efficiency in thick-film organic solar cells*, **Nature Communications** (2025).
- DOI: `10.1038/s41467-025-64808-x`.
- Source system used for the quantitative benchmark: 300 nm D18:L8-BO versus D18:L8-BO:BTP-eC9.
- No upstream code or raw data are copied; the exact main-text summary values used are recorded in the companion JSON.

The source reports that higher zero-field mobility does not necessarily imply longer critical length, because long-distance transport also depends on mobility field dependence and hopping frequency. In its 300 nm D18:L8-BO comparison, BTP-eC9 addition reduced transient-photocurrent extraction time from `0.93 us` to `0.43 us`. The same comparison reduced defect-state density from `6.17e16` to `4.94e16 cm^-3`, changed the short-circuit-current light-intensity exponent from `0.97` to `0.99`, reduced ideality factor from `1.89` to `1.70`, and reduced FTPS Urbach energy from `23.0` to `20.8 meV`. The optimized ternary device reached 19.0% PCE at 300 nm, with a reported critical length of 62.8 nm.

## Quantitative audit

Define extraction-time speedup

`S_t = tau_control / tau_modified`

and fractional time reduction

`R_t = 1 - tau_modified / tau_control`.

Both are dimensionless. Using the printed source summaries,

`S_t = 0.93 / 0.43 = 2.1627906977...`

and

`R_t = 1 - 0.43/0.93 = 0.5376344086...`,

so the reported TPC extraction time is about **53.76% lower**, or **2.16x faster by the reciprocal-time descriptive metric**.

The same arithmetic gives a defect-density reduction of

`1 - 4.94/6.17 = 0.1993517018...` (**19.94%**)

and an Urbach-energy reduction of

`1 - 20.8/23.0 = 0.0956521739...` (**9.57%**).

These simultaneous changes are precisely why the result is not mechanism-pure: morphology, vertical composition, trapping/disorder, recombination, and transport all move together.

## Independent calculation and checks

Run:

```bash
python models/thick_film_transport_scale_bound_v364.py
```

The standard-library executable calculates the ratios in floating point and independently recomputes the printed decimal values with exact `fractions.Fraction` arithmetic. Predeclared absolute agreement tolerance is `1e-12`.

Controls:

1. **Limiting case:** equal control/modified values return ratio `1` and reduction `0`.
2. **Negative control:** a modified extraction time twice the control produces a negative `-1` fractional reduction rather than being clamped to an improvement.
3. **Domain control:** zero or negative denominator inputs fail closed.
4. **Reporting-resolution sensitivity:** treating each two-decimal TPC time as `±0.005 us` for a non-statistical last-digit sensitivity still leaves the speedup above `2x`.

The exact-arithmetic path is an implementation cross-check, not independent physical replication.

## Uncertainty and sensitivity

The selected main-text summary values do not provide formal measurement uncertainties in the text used here, so none are invented. The `±0.005 us` exercise only tests sensitivity to printed two-decimal reporting resolution; it is not a confidence interval.

The dominant uncertainty for this program is transferability. D18:L8-BO:BTP-eC9 is not D18:eC9 or D18:PY-IT:eC9, and the source ternary changes morphology, vertical phase distribution, defect density, energetic disorder, and recombination concurrently.

## Serious conventional explanations

At least three remain live:

1. **Morphology/vertical-distribution mediation.** BTP-eC9 produces more continuous aggregation and changes vertical donor/acceptor distribution, either of which can improve collection without critical length being the sole cause.
2. **Trap/recombination mediation.** The source simultaneously reports lower defect density, lower ideality factor, and lower Urbach energy; TPC improvement can therefore reflect several ordinary transport/recombination changes.
3. **Technique/model dependence.** TPC extraction time is not a unique microscopic mobility constant, and the critical-length construction itself depends on the source transport model and field-dependent mobility characterization.

The current increment does not choose among those explanations. It only falsifies the weaker engineering shortcut that a favorable zero-field mobility value is sufficient evidence for thick-film scale robustness.

## Project decision rule

For a future D18/PY-IT/eC9 scale-transfer arm at substantially increased active-layer thickness or area:

- do not use zero-field mobility alone as the transport/manufacturability pass;
- retain a field-sensitive collection/transport discriminator (for example the already-preregistered pseudo-FF/FF gap, TPC/TDCF-derived collection information, or another independently justified equivalent);
- measure FF and stabilized Pmax in the scaled geometry;
- retain morphology/contact controls and the material-lot hierarchy;
- do not import the source's 62.8 nm critical length, 300 nm thickness, or 2.16x extraction-time ratio as a D18/PY-IT/eC9 threshold.

This rule complements, rather than replaces, the B0 field-generation and transport-loss protocols already merged to `main`.

## Falsifier / narrowing test

This project-level bound would be narrowed if a prospectively designed target-chemistry study demonstrated that zero-field mobility alone predicts held-out thick-film/scale-transfer FF, stabilized Pmax, and collection across independent lots/thicknesses as well as field-sensitive transport metrics within predeclared uncertainty. Until then, zero-field mobility remains an incomplete scale-transfer proxy.

## Technical/business delta

The commercial bridge now has a stronger manufacturing boundary: scale-up decisions must protect long-distance collection rather than optimize a convenient thin-film mobility proxy. That reduces the risk of advancing a formulation that looks adequate in standard mobility characterization but loses useful work when thickness, area, morphology, or field profile changes.

## Next physical increment

Execute the existing provenance-complete B0 D18:eC9 field-generation + pseudo-FF/FF campaign, but include at least one intentionally thicker target-chemistry device set or held-out thickness condition once the baseline is functioning. That would directly test whether the target stack develops the same long-distance collection vulnerability instead of relying on cross-material transfer.
