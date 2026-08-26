# R2 H1-H4 Synthetic Recovery Study — v3.3

**Status:** synthetic planning result. No physical R2 device data are reported here.

## Decision changed

The five-substrate R2 design remains appropriate for **reference qualification / fabrication-variance screening**, but it is **not strong enough to support a confirmatory H1-vs-H2-vs-H3 mechanism-classification claim** under the nominal synthetic assumptions tested here.

For a mechanism-classification publication claim, this program now requires either:

1. **nine independent substrates** at the nominal planning regime; or
2. a separately preregistered design that demonstrates comparable per-class recovery with lower metrology noise / larger effect and passes this same synthetic recovery framework.

Seven substrates are a useful intermediate design but are borderline for H1 at the frozen 80% planning threshold in this deterministic run (`79.75%`).

## Why this study exists

v3.2 froze a low-dimensional FTPS + `Voc`-intensity decision logic for H1–H4. Before fabrication, we need to ask whether that logic can recover a known generating mechanism when only the planned number of **independent substrates** is available.

The study deliberately preserves the hierarchy `lot -> substrate -> pixel -> session -> measurement`. Only substrate-level synthetic observations enter the H1/H2/H3 model comparison. Repeated pixels or sessions are not counted as independent fabrication units.

## Synthetic generating assumptions

These are engineering assumptions, not measured R2 properties.

| Quantity | Nominal synthetic value | Status |
|---|---:|---|
| independent substrates | 5, with 7 and 9 sensitivity cases | assumed design variable |
| mechanism-driven `DeltaVnr` effect SD | 10 mV | synthetic assumption; 5 and 15 mV sensitivity cases |
| `DeltaVnr` random noise SD | 4 mV | synthetic assumption; 2 and 6 mV sensitivity cases |
| H1 `EU` latent response | `24 + 3 z` meV plus 1 meV noise | synthetic mechanism model |
| H3 ideality latent response | `1.25 + 0.15 z` plus 0.03 noise | synthetic mechanism model |
| non-H4 EL shift noise | 1.2 meV SD | synthetic assumption |
| non-H4 direct-minus-reciprocity noise | 4 mV SD | synthetic assumption |
| H4 EL shift | 7 meV mean, 1.5 meV SD | synthetic alert-positive case |
| H4 direct-minus-reciprocity | 25 mV mean, 6 mV SD | synthetic alert-positive case |
| simulations per true class | 2,000 | Monte Carlo resolution |
| frozen seed | `20260826` | deterministic reproducibility |

The 10 mV effect scale is chosen because the commercial bridge already treats a 10–20 mV EPC-mediated voltage contribution as scientifically relevant. It is **not** asserted as the expected R2 effect.

## Classifier frozen for this study

### H4 — injection/state-filling artifact

H4 receives priority if **any substrate** crosses either v3.2 alert:

- absolute EL spectral shift `>=5 meV`; or
- absolute direct-minus-reciprocity `DeltaVnr >20 mV`.

### H1 / H3 / H2

If H4 is not triggered, compute leave-one-substrate-out (LOSO) MAE for:

- intercept-only model (`H2` null);
- one-predictor `EU -> DeltaVnr` model (`H1`);
- one-predictor ideality -> `DeltaVnr` model (`H3`).

H1 or H3 is selected only if its LOSO MAE improves by **>=20%** relative to intercept-only and beats the other one-predictor model. Otherwise the result is H2.

No high-capacity model is permitted.

## Nominal confusion matrix

Scenario: five substrates, 10 mV effect SD, 4 mV `DeltaVnr` noise SD, 2,000 simulations per true class.

Rows are true mechanism; columns are predicted mechanism.

| true | H1 | H2 | H3 | H4 | recovery | 95% Wilson interval |
|---|---:|---:|---:|---:|---:|---:|
| H1 | 1331 | 582 | 87 | 0 | 66.55% | 64.45–68.58% |
| H2 | 206 | 1583 | 210 | 1 | 79.15% | 77.31–80.87% |
| H3 | 73 | 397 | 1530 | 0 | 76.50% | 74.59–78.31% |
| H4 | 0 | 0 | 0 | 2000 | 100.00% | 99.81–100.00% |

### Interpretation

At the nominal synthetic regime, **five substrates fail the intended confirmatory mechanism-identification standard**. H1 is most vulnerable: nearly 30% of true H1 simulations collapse into the H2 null because five held-out groups do not reliably establish the `EU -> DeltaVnr` predictive relation.

This is a useful negative result. It does not invalidate the five-substrate R2 reference pilot; it narrows what that pilot is allowed to claim.

## Sample-count and sensitivity results

| independent substrates | effect SD | noise SD | H1 | H2 | H3 | H4 | macro accuracy |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 10 mV | 4 mV | 66.55% | 79.15% | 76.50% | 100% | 80.55% |
| 7 | 10 mV | 4 mV | 79.75% | 86.85% | 88.65% | 100% | 88.81% |
| 9 | 10 mV | 4 mV | 88.20% | 90.15% | 94.85% | 100% | 93.30% |
| 5 | 5 mV | 4 mV | 41.95% | 79.15% | 46.15% | 100% | 66.81% |
| 5 | 15 mV | 4 mV | 76.05% | 79.15% | 87.35% | 100% | 85.64% |
| 5 | 10 mV | 2 mV | 80.30% | 79.15% | 91.80% | 100% | 87.81% |
| 5 | 10 mV | 6 mV | 53.05% | 79.15% | 58.10% | 100% | 72.58% |

The H2 recovery is nearly unchanged in these sensitivity rows because this synthetic H2 generator has no true `DeltaVnr` relation and the false-positive rate is primarily controlled by the frozen 20% LOSO-improvement rule and small-N chance correlations, not the H1/H3 effect parameter.

## Independent cross-checks

### 1. Analytic H4 alert check

For the synthetic H4 generator:

- `EL_shift ~ Normal(7, 1.5^2) meV`;
- `direct_minus_recip ~ Normal(25, 6^2) mV`.

Under independence, the probability that **all five** substrates miss both H4 alerts is approximately `2.14e-9`, so the analytic expected H4 detection probability is `0.9999999979`. The 2,000-simulation result of 100% is therefore consistent with an independent normal-CDF calculation.

For a non-H4 substrate with `EL_shift ~ N(0,1.2^2)` and direct-minus-reciprocity `~N(0,4^2)`, the analytic probability of at least one false H4 alert over five substrates is approximately `1.57e-4`; the nominal Monte Carlo produced one H4 false positive among 2,000 H2 datasets and none for H1/H3, compatible with the small expected rate.

### 2. Seed robustness

Ten additional deterministic 500-simulation/class runs were checked during specification development.

- Five-substrate H1 recovery range: **64.2–69.8%**; H2: **77.6–84.2%**; H3: **71.8–77.8%**.
- Nine-substrate H1 recovery range: **87.0–91.8%**; H2: **89.0–92.8%**; H3: **93.0–95.2%**.

The decision (five exploratory, nine confirmatory under nominal assumptions) is therefore not an artifact of one seed.

## Dimensional / numerical checks

- `DeltaVnr`, `EU`-derived voltage effects, and thresholds are represented in mV/meV explicitly; no unit mixing is used inside the classifier.
- LOSO operates over independent substrate groups only.
- Each held-out prediction is trained on `N-1` substrates; the held-out substrate is never used to fit its own predictor.
- The intercept-only LOSO baseline is the mean of the other substrates, not the global mean including the holdout.
- Wilson intervals quantify Monte Carlo classification-rate uncertainty; they do **not** represent experimental confidence intervals.

Runtime used for the committed deterministic calculations during this run: Python 3.13.5, NumPy 2.3.5.

## Conventional / null explanations preserved

This synthetic study does not establish any physical mechanism. In particular:

- H1 recovery does not prove `EU` is microscopic static disorder;
- H3 recovery does not make ideality a unique interface-recombination mechanism;
- H2 represents the conventional/null outcome where mechanism predictors do not earn held-out predictive value;
- H4 is a measurement-state/injection artifact class, not a quantum mechanism;
- H5/EPC remains outside this classifier and cannot be inferred from a residual.

## Program correction / narrowed claim

**Superseded wording:** earlier material could be read as implying that five R2 substrates were adequate for the mechanism-discrimination pilot generally.

**Corrected scope:** five substrates remain the current reference-qualification/fabrication-variance pilot. Mechanism classification from FTPS + `Voc`-intensity is exploratory at `N=5`. Under the nominal synthetic design assumptions, a confirmatory H1–H4 publication claim should use **nine independent substrates**, or first demonstrate an alternative design with comparable preregistered recovery.

## Publication gate added

Before calling an R2 H1–H4 classification confirmatory, the exact proposed design must demonstrate on committed synthetic recovery tests:

- **>=80% recovery for every H1–H4 class**, and
- preferably **>=90% recovery for every conventional H1–H3 class** for a strong publication claim,
- with sensitivity to effect size and measurement noise reported.

At nominal assumptions, `N=9` clears 80% for all classes and 90% for H2/H3, while H1 is 88.2%; therefore even `N=9` should be described as a practical confirmatory design rather than perfect identification. A stronger H1 claim requires either lower noise, more substrates, or a more informative independent observable.

## Files

- `models/r2_mechanism_recovery.py`
- `models/r2_mechanism_confusion_nominal_v3_3.csv`
- `models/r2_mechanism_recovery_sensitivity_v3_3.csv`

## Single best next increment

Add a **second independent H1 discriminator** before increasing sample count blindly: simulate and preregister temperature-dependence of the FTPS tail/EL broadening as an orthogonal dynamic-vs-static-disorder observable. Then rerun the confusion matrix to determine whether five or seven substrates can achieve >=80–90% H1 recovery without relying only on `EU -> DeltaVnr` correlation.
