# Dual-path stress tomography v3.72

## Claim class

**Prospective protocol + synthetic method validation.** No A0/A2/B0/B2 stress result is claimed.

## Why this is new

v3.71 introduced the idea that two physically distinct charge-generation routes could provide graceful degradation if their sensitivities differ. v3.72 turns that into a discriminating experiment by using **two stress classes** rather than one.

The core question is not simply whether PY-IT improves stability. It is:

> Does PY-IT protect donor-free acceptor-rich material, the D18-containing heterojunction, or both—and does that protection depend on whether the perturbation is dark thermal morphology stress or illuminated operating stress?

A single ageing curve cannot answer that.

## Direct material precedent

Song et al., Matter 2022, DOI `10.1016/j.matt.2022.03.012`, studied PM6:BTP-eC9:PY-IT. They report that adding PY-IT creates entangled-chain morphology, suppresses BTP-eC9 diffusion/crystallization, and improves thermal robustness. Their devices were thermally stored at 85 C in dark N2; after 250 h the optimal ternary retained 85.5% of initial PCE and was reported ~7.2% higher than the binary system. They also observed suppressed crystallization after severe 160 C / 4 h annealing in the ternary.

This is unusually relevant chemical precedent because it uses **BTP-eC9 + PY-IT**, but the donor is PM6 rather than D18. It supports a thermal perturbation axis; it does not set D18/PY-IT/eC9 pass thresholds.

## Stress axes

### T — dark thermal morphology stress

Planning condition: **85 C, dark, N2**, with checkpoints frozen before unblinding.

Why:
- direct PM6:BTP-eC9:PY-IT morphology/stability precedent;
- ISOS-style thermal/shelf testing separates heat from light;
- expected to emphasize diffusion, crystallization, interface rearrangement and contact thermal effects.

This is an ISOS-inspired research stress, not product qualification.

### L — light operational stress

Planning condition: **encapsulated, 100 mW cm^-2, MPP tracking, controlled 50 C**, with exact spectrum/UV state and duration frozen prospectively.

A 2026 OPV stability study (DOI `10.1039/D5TC03674G`) used these conditions under an ISOS-L-1 implementation. We use it as recent operational precedent, not as a universal standard for this chemistry.

Why:
- adds photo/electrical operating stress rather than heat alone;
- helps identify whether thermal morphology robustness generalizes to operational photostability;
- exposes ETL/contact/light-driven failure modes that a dark oven does not.

## Arms

- A0: eC9 donor-free control
- A2: PY-IT:eC9 = 0.2:1 donor-free control
- B0: D18:eC9 baseline
- B2: D18:PY-IT:eC9 = 1:0.2:1

The A-arm donor-free architecture remains gated by v3.70/v3.71. If a clean electrical architecture is not qualified, A0/A2 remain optical/structural witnesses and no donor-free electrical generation claim is made.

## Required observables

At minimum for B0/B2 electrical interpretation:
- stabilized Pmax;
- Voc, Jsc and FF;
- prospectively defined field-generation observable;
- absorption/EQE normalization;
- thickness;
- contact/transport diagnostic;
- morphology/packing witness.

For A0/A2:
- thickness + absorption;
- PL / field-dependent PL where physically valid;
- trPL if available;
- GIWAXS/AFM or an explicitly justified morphology witness;
- electrical current only after donor-free architecture qualification.

## Analysis

For any positive metric M:

`R_arm,S = M_after / M_before`

`y_arm,S = ln(R_arm,S)`

For stress S:

`Delta_A,S = y_A2,S - y_A0,S`

`Delta_B,S = y_B2,S - y_B0,S`

`Psi_S = Delta_B,S - Delta_A,S`

The same interaction must independently satisfy:

`exp(Psi_S) = (R_B2,S / R_B0,S) / (R_A2,S / R_A0,S)`.

Stress selectivity is:

`Omega = Psi_T - Psi_L`.

### Interpretation

- Delta_A > 0, Delta_B > 0: PY-IT protection is not heterojunction-exclusive.
- Delta_A ~ 0, Delta_B > 0: interface-specific interpretation is strengthened.
- Delta_A > 0, Delta_B ~ 0: donor-free/domain effect without useful heterojunction benefit.
- opposite signs: trade-off; investigate mechanism before promotion.
- nonzero Omega: thermal and light stress do not produce the same interaction signature.

Symbols `~0` and `>0` are **not operational thresholds yet**. Physical margins must be frozen from baseline repeatability, measurement uncertainty and power before A2/B2 unblinding.

These are difference-in-differences style diagnostics, not automatically causal estimators. Strong causal language requires blocked/randomized fabrication, common histories, adequate hierarchy and controlled confounding.

## Synthetic fixture

Software-only retentions:

| stress | A0 | A2 | B0 | B2 |
|---|---:|---:|---:|---:|
| T | 0.78 | 0.88 | 0.72 | 0.86 |
| L | 0.90 | 0.91 | 0.80 | 0.84 |

Results:
- `Psi_T = 0.0570531894488`
- `exp(Psi_T) = 1.05871212121`
- `Psi_L = 0.0377403279828`
- `exp(Psi_L) = 1.03846153846`
- `Omega = 0.0193128614660`

These values test algebra and serialization only. They are not expected device performance.

## Experimental hierarchy

Preserve:

`material lot -> fabrication lot -> substrate -> device -> stress block -> checkpoint -> measurement`.

Stress time points, JV scans, spectra and repeated pixels are technical repeats. Strong useful-work interpretation still requires at least three independent fabrication lots.

Block A0/A2/B0/B2 fabrication and randomize sample position/order. Stress-matched controls must share chamber, illumination and timing history as closely as practical.

## Fail-closed conditions

Return **INCOMPLETE**, not a mechanism result, if:
- physical effect margins were not frozen before A2/B2 unblinding;
- A0/A2 architecture is unqualified but donor-free electrical current is used mechanistically;
- field/intensity/temperature calibration is missing;
- absorption or thickness changes can explain the signal;
- contact/transport changes are comparable to the claimed generation effect;
- stress histories differ materially across compared arms;
- fewer than three independent fabrication lots are used for a strong useful-work claim.

## Strongest conventional explanations

1. PY-IT simply suppresses BTP-eC9 crystallization/diffusion; no second generation route is needed.
2. Contact/transport stability creates better Pmax retention.
3. Optical absorption/thickness drift biases field-generation metrics.
4. Thermal and light stress both collapse onto the same morphology variable, so the two-axis interpretation is false.
5. Donor-free films are not representative of acceptor-rich domains in B2.
6. Relative retention improves while absolute stabilized Pmax remains inferior.

## Falsification rule

The dual-path resilience hypothesis is narrowed or rejected if PY-IT's apparent protection is fully explained by morphology/contact/optical controls, if A/B response patterns are indistinguishable after uncertainty, or if better normalized retention does not preserve absolute stabilized useful work.

## Next physical step

Run **baseline-only A0 and B0 qualification** for both T and L workflows first. Use measured repeatability and calibration uncertainty to freeze effect margins and sample count. Only then unblind A2/B2.
