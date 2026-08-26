# Session v3.3 — R2 mechanism-classification synthetic recovery

## What changed

A blinded synthetic recovery study was run against the frozen v3.2 H1–H4 mechanism-audit logic before physical R2 fabrication. The result narrows the allowed claim: **five independent substrates are not sufficient for confirmatory H1/H2/H3 classification under the nominal planning assumptions.**

Five substrates remain the R2 reference-qualification and fabrication-variance pilot. The mechanism-audit publication layer is now explicitly separate.

## Synthetic/model result

Nominal planning scenario:

- 5 independent substrates;
- 10 mV mechanism-driven `DeltaVnr` effect SD for H1/H3;
- 4 mV `DeltaVnr` random noise SD;
- 2,000 simulated datasets per true class;
- frozen seed `20260826`.

Per-class recovery:

- H1 bulk disorder: 66.55% (95% Wilson 64.45–68.58%)
- H2 null/thickness confound: 79.15% (77.31–80.87%)
- H3 interface/contact: 76.50% (74.59–78.31%)
- H4 injection/state-filling artifact: 100% in this deliberately alert-positive synthetic case

At the same nominal effect/noise assumptions:

- 7 substrates: H1 79.75%, H2 86.85%, H3 88.65%
- 9 substrates: H1 88.20%, H2 90.15%, H3 94.85%

These are synthetic planning probabilities, not experimental success rates.

## Verification performed

- Exact lot/substrate independence preserved at the classifier input; repeated pixels/sessions are not synthetic independent groups.
- LOSO predictions exclude the held-out substrate from fitting.
- Intercept-only prediction uses only the remaining substrates.
- Independent normal-CDF calculation gives synthetic H4 detection probability `0.9999999979` over five substrates; Monte Carlo 100% is consistent.
- Analytic non-H4 false-H4 probability across five substrates is approximately `1.57e-4` under the frozen synthetic alert-noise assumptions.
- Ten additional seed checks preserved the decision: five-substrate H1 recovery 64.2–69.8%; nine-substrate H1 recovery 87.0–91.8%.
- Runtime used locally for deterministic check: Python 3.13.5, NumPy 2.3.5.

## Assumptions

The effect sizes and noise models are engineering assumptions. They must be replaced or updated when R2 reference data provide empirical noise distributions. Normality and independence between the synthetic alert observables are also assumptions.

## Null / conventional explanations

The classifier does not contain H5/EPC as a recoverable class. A residual after H1–H4 is **not** EPC evidence. H1 uses an empirical `EU` descriptor; H3 uses empirical ideality. Neither is a unique microscopic label.

## Correction / superseded scope

Earlier program text could be interpreted as treating five R2 substrates as enough for the full mechanism-discrimination pilot. The corrected scope is:

- `N=5`: reference qualification / fabrication variance + exploratory mechanism audit;
- confirmatory mechanism classification: must first pass a design-level synthetic recovery gate, with `N=9` currently the practical nominal design under the tested assumptions.

No experimental result is superseded because no R2 dataset exists yet.

## Files added

- `models/r2_mechanism_recovery.py`
- `models/r2_mechanism_confusion_nominal_v3_3.csv`
- `models/r2_mechanism_recovery_sensitivity_v3_3.csv`
- `technical/r2-mechanism-recovery-v3.3.md`

## Unresolved risks

- Five-substrate mechanism classification is underpowered at 10 mV effect / 4 mV noise.
- Seven substrates are borderline for H1 at an 80% planning standard.
- Nine substrates still recover H1 below 90% in the nominal run.
- The H4 generator is intentionally strong and should later be stress-tested at smaller injection artifacts.
- The synthetic model omits H1/H3 mixtures and model misspecification; real devices may exhibit multiple mechanisms simultaneously.

## Single best next increment

Add an orthogonal temperature-dependence discriminator for H1 (static-vs-dynamic FTPS/EL broadening), then rerun the confusion matrix. The objective is to determine whether mechanistic information, rather than sample count alone, can raise H1 recovery above 80–90%.
