# v3.56 — Exciton-lifetime multi-objective counterexample

## Changed evidentiary state

**Claim class:** literature-derived experimental benchmark plus project-level inference.

A longer exciton lifetime is **not accepted as a monotonic standalone optimization target** for the D18/PY-IT/eC9 commercial bridge. In the primary 2026 Nature Photonics guest–host series, the optimized PM6:L8-BO:Y18-C3 (0.86:0.14 acceptor ratio) ternary has a *shorter* reported exciton lifetime than PM6:L8-BO while simultaneously showing a *higher* FF and *lower* voltage loss. This is a compact empirical counterexample to the simplistic rule “longer lifetime always means better FF/useful work” across compositions.

It does **not** refute the paper's mechanistic conclusion that suppressing exciton decay can mitigate field-dependent generation in the systems studied. Composition changes multiple variables at once. The narrower project decision is that lifetime must remain a covariate/discriminator alongside direct field-generation and useful-work measurements, not become a surrogate acceptance gate.

## Primary-source provenance

Zhang, H. et al., **Overcoming the fill-factor limit of organic solar cells**, *Nature Photonics* (version of record 19 June 2026), DOI `10.1038/s41566-026-01946-8`.

Main-text Fig. 5 discussion reports:

- PM6:L8-BO: exciton lifetime `990 ps`, FF `79.5%`, voltage loss `0.545 V`.
- PM6:Y18-C3: exciton lifetime `690 ps`, FF `68.8%`, voltage loss `0.502 V`.
- optimized PM6:L8-BO:Y18-C3 (0.86:0.14): exciton lifetime `870 ps`, FF `81.1%`, voltage loss `0.516 V`, PCE `20.1%`.

The caption states `n=8` independent devices per ratio for FF and voltage-loss plots and two independent films with six measurements per ratio for exciton lifetime/PLQY. The prose values do not provide standard errors; none are invented here.

## Governing calculations

For any quantity `x`, relative change from reference to arm is

`x_rel = x_arm / x_ref - 1`,

and absolute change is

`Delta x = x_arm - x_ref`.

### Y18-C3 binary → optimized ternary

- lifetime: `690 -> 870 ps`, `+26.087%`;
- FF: `0.688 -> 0.811`, `+0.123` absolute or `+17.878%` relative;
- voltage loss: `0.502 -> 0.516 V`, **+14 mV** (worse).

This is the intuitive direction emphasized by the authors: longer lifetime accompanies much higher FF, but some voltage-loss penalty remains relative to the low-loss Y18-C3 binary.

### L8-BO binary → optimized ternary

- lifetime: `990 -> 870 ps`, **−12.121%**;
- FF: `0.795 -> 0.811`, **+0.016 absolute / +2.013% relative**;
- voltage loss: `0.545 -> 0.516 V`, **−29 mV** (better).

Thus the optimized ternary improves both FF and voltage loss despite having the shorter lifetime. That sign pattern is the decision-driving counterexample.

All ratios are dimensionless; voltage-loss differences are in volts and are also reported in mV. No conversion of PCE to stabilized Pmax is made.

## Independent check

`models/exciton_lifetime_multiobjective_v356.py` recomputes the principal relative changes with two numerical representations:

1. floating-point arithmetic from the JSON inputs; and
2. exact `fractions.Fraction` arithmetic from the reported decimal values.

Agreement tolerance is frozen at `1e-12`. The decision is independently checked as an ordinal sign test: ternary lifetime lower than L8-BO, ternary FF higher, ternary voltage loss lower.

Run:

```bash
python models/exciton_lifetime_multiobjective_v356.py
```

Expected terminal state includes `"ordinal_counterexample": true` and `"checks": "PASS"`.

## Reporting-resolution sensitivity

This is **not measurement uncertainty**. As a conservative transcription-resolution check only, each reported value is expanded by half of its last reported digit:

- lifetime: ±0.5 ps;
- FF fraction: ±0.0005;
- voltage loss: ±0.0005 V.

Even under the adverse interval endpoints:

- ternary lifetime upper bound `870.5 ps` < L8-BO lower bound `989.5 ps`;
- ternary FF lower bound `0.8105` > L8-BO upper bound `0.7955`;
- ternary voltage-loss upper bound `0.5165 V` < L8-BO lower bound `0.5445 V`.

The counterexample therefore cannot be an artifact of the displayed rounding precision. Its physical uncertainty remains unknown from the prose values alone.

## Negative and limiting controls

The executable includes a synthetic monotonic positive-control fixture in which lifetime, FF and voltage-loss directions all improve together. That fixture must **not** trigger the counterexample classifier.

The empirical counterexample is falsifiable for the project: a controlled D18/PY-IT/eC9 intervention that varies lifetime while sufficiently holding energetic offset, morphology, transport/contact and optical variables fixed, and prospectively demonstrates monotonic lifetime-linked field-generation/FF improvement, would narrow or overturn transfer of this warning to the project system.

## Conventional explanations and validity domain

Two serious explanations remain live:

1. **Energetic co-variation.** Adding Y18-C3 changes energetic offset and likely other electronic properties together with lifetime. The observed ternary outcome does not isolate lifetime causally.
2. **Morphology/transport/contact/optical co-variation.** The source reports AFM/GIWAXS controls and argues against morphology as the primary cause, but those controls do not make lifetime uniquely causal or exclude every conventional device variable.

Validity domain is therefore strictly the reported PM6/L8-BO/Y18-C3 composition series. No lifetime optimum, FF improvement, or voltage-loss value is transferred to D18/PY-IT/eC9.

## Technical/business delta

The D18/PY-IT/eC9 program should add exciton lifetime as a mechanism-relevant observable when practical, but **must not optimize or gate on lifetime alone**. The existing direct field-generation requirement (TDCF plus bias-dependent PL or justified equivalent) and stabilized useful-work gate remain more decision-relevant. This reduces the risk of replacing one proxy (EPC/reorganization) with another proxy (lifetime) while missing a multi-objective penalty.

## Best next physical increment

Acquire blinded B0/B1/B2 exciton-lifetime data alongside the already-prioritized TDCF/bias-dependent-PL and stabilized-MPP measurements. Test whether lifetime adds predictive information about field robustness after energetic-offset and morphology/transport controls; do not freeze a physical lifetime threshold from this external system.
