# FTPS + Voc-Intensity Mechanism Audit — preregistration v3.2

**Status:** preregistered analysis specification; no R2 experimental result is reported here.

## Why this increment exists

The v3.0 witness soft-sensor could correlate with `DeltaVnr` for multiple conventional reasons. This audit is designed to decide whether witness UV-vis is tracking a physically relevant loss variable or merely thickness/process history. It intentionally keeps competing explanations alive.

## Evidence boundary

### Established evidence

- Temperature-dependent CT absorption/emission can distinguish important classes of static versus temperature-activated/vibrational broadening, and electro-optical reciprocity can be used to validate device-temperature consistency: Göhler et al., *Phys. Rev. Applied* 15, 064009 (2021), DOI `10.1103/PhysRevApplied.15.064009`.
- Static distributions of CT-state energies can alter voltage-loss inference; neglecting static disorder can produce incorrect CT energy, reorganization-energy, and loss estimates. Injection-dependent EL peak shifts can be a signature of CT-state filling: Yan et al., *Nature Communications* 12, 3642 (2021), DOI `10.1038/s41467-021-23975-3`.
- A recent modern-OSC workflow combines FTPS-EQE and EL for `Eg`/`ECT`, exponential low-energy FTPS fitting for `EU`, and `DeltaVnr=(kT/q)ln(1/EQE_EL)`: *Chemical Science* (2025), DOI `10.1039/D4SC07146H`.

### Engineering assumptions frozen here

- R2 PM6:Y6 confirmatory empirical-tail window: **1.10–1.30 eV** at 300 K.
- Sensitivity windows: **1.08–1.28 eV** and **1.12–1.32 eV**.
- A window is usable only when every included point is positive after background treatment and the lowest-signal point is at least 10× the estimated dark-equivalent signal. If the primary window is not usable, the confirmatory `EU` result is **not estimable**; the window is not moved post hoc.
- EL state-filling alert threshold: absolute centroid/peak shift **>=5 meV** between `0.5×Jsc` and `2×Jsc`, provided the propagated spectral-energy uncertainty is <=2 meV. This is a planning discriminator, not a literature constant.
- `Voc`-intensity protocol: 300 K, at least 8 intensity points spanning nominally 0.1–1.2 sun-equivalent intensity, with device temperature stable to the AT-04 requirement.

## Governing calculations

### 1. Empirical Urbach descriptor

Within the frozen tail window:

`ln(EQE(E)) = a + E / EU`

so

`EU = 1 / slope[ln(EQE) versus E]`.

Units: the slope has units `eV^-1`, therefore `EU` is in eV. A positive slope is required. `EU` is treated as an **empirical energetic-tail descriptor**, not proof of one microscopic disorder mechanism.

### 2. Nonradiative voltage loss

`DeltaVnr = -(kB*T/q) ln(EQE_EL)`.

At `EQE_EL=1`, the limiting value is zero. Lower `EQE_EL` must produce larger positive `DeltaVnr`; code self-tests enforce this sign/limit.

### 3. Light-intensity ideality diagnostic

For relative intensity `I`:

`dVoc / dln(I) = n*kB*T/q`.

Thus

`n = slope_ln / (kB*T/q)`.

Independent log-base-10 form:

`n = slope_decade / [(kB*T/q)*ln(10)]`.

At 300 K, `kB*T/q = 25.851999786 mV`. For synthetic `n=1.30`, the expected slope is **77.384358 mV/decade**. The two derivations must agree to numerical precision. `n` is an empirical recombination diagnostic, not a unique assignment to a single pathway.

## Model hierarchy

A single symmetric Marcus CT fit is **not** a required truth model. The 2021 temperature-dependent study reports asymmetric absorption/emission and strong temperature-activated broadening in some systems, while the 2021 static-disorder study demonstrates cases where CT-energy distributions matter. Therefore:

1. **Empirical exponential tail (`EU`)** — confirmatory descriptor if the frozen window passes signal criteria.
2. **Single-state Marcus-like CT model** — candidate model, not default truth.
3. **CT-energy-distribution/static-disorder model** — competing candidate when injection EL or spectral residuals support it.
4. **Temperature-dependent dynamic/vibronic model** — required alternative when four-temperature data show systematic broadening inconsistent with a static model.

Complexity is promoted only if it improves held-out prediction/residual structure; a more complicated model does not win merely because it fits training data better.

## Competing hypotheses and discriminators

| ID | Conventional/mechanistic explanation | Expected discriminators | Decision rule |
|---|---|---|---|
| H1 | Bulk energetic/CT disorder drives the loss | FTPS `EU`/CT-tail features change with `DeltaVnr`; injection EL shape near operating density remains comparatively stable; thickness-only model is inferior | Supported only if mechanism features improve leave-one-substrate-out `DeltaVnr` MAE by >=20% over thickness/intercept baseline and the sign is stable under sensitivity windows |
| H2 | Thickness / optical-density confound | witness UV-vis and `Jsc` move; thickness-normalized FTPS tail and `DeltaVnr` do not show stable independent relation | If thickness-only performs within 20% of the best model, do not claim a loss soft sensor |
| H3 | Interface/contact recombination | `Voc`-intensity slope/empirical ideality and/or electrical diagnostics change while bulk FTPS tail is stable | Requires ideality/recombination predictor to improve held-out loss prediction; ideality alone is not a unique mechanism label |
| H4 | CT-state filling / injection artifact | EL centroid/peak or `EQE_EL` changes materially with injection; direct `DeltaVnr` disagrees with reciprocity | 5 meV injection spectral-shift alert or >20 mV direct-vs-reciprocity discrepancy flags direct `EQE_EL` as non-primary until resolved |
| H5 | Vibronic/EPC/triplet loss beyond static disorder | `DeltaVnr` residual remains after H1–H4; temperature/vibronic observables change | **Cannot be confirmed by FTPS + `Voc`-intensity alone.** It may only be retained as a candidate for the later EPC-specific experiment |

## Statistical / independence contract

- Hierarchy remains `lot -> substrate -> pixel -> session -> measurement`.
- Five R2 substrates are five fabrication-level groups; repeated pixels/sessions are not promoted to independent substrates.
- Soft-sensor/mechanism prediction uses **leave-one-substrate-out (LOSO)** validation.
- High-capacity ML is prohibited for this pilot.
- For substrate-level comparisons, candidate regressions are limited to low-dimensional, preregistered predictors.
- Primary predictive criterion is held-out MAE. AICc may be reported as a secondary diagnostic only when mathematically defined; it cannot override held-out failure.
- No automatic outlier deletion. Predeclared QC/deviation rules govern exclusions.

## Uncertainty propagation

For the linear Urbach fit, report the slope uncertainty/covariance and propagate `EU=1/m` as `sigma_EU ~= sigma_m/m^2` for a local first-order check, plus a bootstrap over spectral residuals as the primary uncertainty estimate when data exist.

For ideality:

`n = m / (kB*T/q)`.

Propagate slope and device-temperature uncertainty. Calibration/intensity systematic uncertainty is recorded separately from random fit uncertainty; correlated scale errors are not combined as if independent.

For `DeltaVnr`, propagate absolute `EQE_EL` calibration and device-temperature uncertainty using the full logarithmic relation. AT-04's total equivalent uncertainty gate remains <=10 mV.

## Sensitivity requirements

Before interpreting R2:

- recompute `EU` in the two frozen sensitivity windows;
- compare empirical tail, single-state CT, and disorder-aware alternatives;
- recompute ideality using both natural-log and log10 intensity equations;
- report whether H1–H4 classification changes when uncertain inputs are moved through their accepted range;
- if classification changes, report the result as **conditional/ambiguous** rather than selecting the preferred mechanism.

## Synthetic code verification

Executable checks live in `models/ftps_voc_audit.py`.

Frozen seed: `20260826`.

Synthetic self-test cases:

- `EU_true = 25 meV`, 1.10–1.30 eV, 2% log-domain noise; recovered `EU` must be within 0.5 meV.
- `n_true = 1.30`, 300 K, 0.1–1.2 relative intensity, 0.5 mV Gaussian `Voc` noise; recovered `n` must be within 0.05.
- independent natural-log and log10 ideality derivations must agree to `1e-12`.
- noise-free endpoint Urbach derivation must match the OLS truth to `1e-12 eV`.
- `DeltaVnr(EQE_EL=1)=0`; lowering `EQE_EL` must monotonically increase positive loss.

A local independent check performed when this specification was created gave `kBT/q=25.851999786 mV` and `77.384358 mV/decade` for `n=1.30` at 300 K. These are arithmetic checks, not experimental values.

## Publication gate

R2 witness spectra may be described as a mechanism-linked process sensor only if:

1. the frozen FTPS/EL/Voc-intensity audit completes without post-hoc window changes;
2. the LOSO prediction gate survives substrate-level independence;
3. H2 and H4 are rejected/bounded by their discriminators;
4. direct and reciprocity loss estimates are consistent inside the frozen uncertainty rule; and
5. the conclusion is robust to the frozen spectral windows and competing-model sensitivity analysis.

Even then, H5/EPC causality remains unproven until the later D18/PY-IT/eC9 experiment supplies EPC-specific evidence.
