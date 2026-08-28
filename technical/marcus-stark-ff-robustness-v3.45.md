# Marcus–Stark field-robustness gate v3.45

## Status and claim class

**Synthetic/model result; exploratory.** This increment adds a reproducible counterexample to the idea that reducing electron–phonon coupling (EPC) or reorganization energy is automatically beneficial for useful photovoltaic work.

It does **not** claim that D18/PY-IT/eC9, PM6:Y6, or any project device has the synthetic parameters used below. It does not predict a device fill factor (FF), Pmax, or commercial performance.

## New evidence motivating the gate

Zhang et al. (Nature Photonics, 2026, DOI `10.1038/s41566-026-01946-8`) report a persistent open-circuit-voltage/FF trade-off in organic solar cells associated with field-dependent free-charge generation. Their measurements and modelling identify the Ex→CT transition as a field-sensitive bottleneck and represent its rate with Marcus theory plus field-induced Stark shifts.

The paper gives the forward-rate dependence

\[
k_{\mathrm{Ex\to CT}}(F)\propto
\exp\left[
-\frac{(\lambda+\Delta G_{\mathrm{CT-Ex}}+
\Delta E_{\mathrm{CT}}(F)-\Delta E_{\mathrm{Ex}}(F))^2}
{4\lambda k_BT}
\right].
\]

For a first-order Stark scale, the authors discuss an interfacial CT separation of approximately 3.5 nm and an internal field of approximately \(10^7\) V/m, yielding an approximately 35 meV shift. They report second-order shifts of only about 0.0035–0.035 meV for the cited polarizability range. The article also uses TDCF and bias-dependent PL to diagnose field-dependent generation.

This result matters directly to the program because the existing commercial bridge seeks lower EPC/reorganization and lower non-radiative voltage loss. A voltage-loss improvement can be real while useful-work improvement fails if Ex→CT formation becomes strongly field dependent.

## Normalized-rate derivation

Define the net field-induced Ex–CT energy change

\[
\delta(F)=\Delta E_{\mathrm{CT}}(F)-\Delta E_{\mathrm{Ex}}(F)
\]

and

\[
A=\lambda+\Delta G.
\]

The unknown Marcus prefactor cancels in the normalized rate:

\[
R(\delta)=\frac{k(\delta)}{k(0)}
=\exp\left[
-\frac{2A\delta+\delta^2}{4\lambda k_BT}
\right].
\]

For opposite first-order CT orientations, use \(+\delta\) and \(-\delta\). Define the conservative local metric

\[
R_{\mathrm{worst}}
=\min\{R(+|\delta|),R(-|\delta|)\}
=\exp\left[
-\frac{\delta^2+2|A||\delta|}
{4\lambda k_BT}
\right].
\]

The orientation asymmetry has the exact closed form

\[
\left|\ln\frac{R_+}{R_-}\right|
=\frac{|A\delta|}{\lambda k_BT}.
\]

All exponent terms are dimensionless. \(\lambda,\Delta G,\delta,k_BT\) are energies in eV. Rate ratios and log-asymmetry are dimensionless.

### Activationless limiting case

At the Marcus activationless condition

\[
\Delta G=-\lambda,
\]

we have \(A=0\), so

\[
R_+=R_-=
\exp\left[-\frac{\delta^2}{4\lambda k_BT}\right].
\]

Thus first-order orientation asymmetry vanishes at this point, although the quadratic-in-\(\delta\) rate penalty remains.

### Analytic reorganization-energy window

Let \(\Delta G=-g<0\). For \(0<\delta<2g\),

\[
R_{\mathrm{worst}}=
\exp\left[-\frac{\delta^2+2|\lambda-g|\delta}
{4\lambda k_BT}\right]
\]

is maximized at

\[
\lambda=g=-\Delta G.
\]

For \(\lambda<g\), the exponent decreases monotonically as \(\lambda\) approaches \(g\). For \(\lambda>g\) and \(\delta<2g\), it increases monotonically away from \(g\). This is an analytical counterexample to a universal “smaller \(\lambda\) is better” rule.

It is **not** proof that a real OPV should be engineered to \(\lambda=-\Delta G\); MLJ/vibronic structure, disorder, electronic coupling, delocalization, diffusion, back-transfer, orientation distributions and device electrostatics can move or erase this optimum.

## Published-scale dimensional check

For one electron separated by \(d=3.5\) nm in a field \(F=10^7\) V/m,

\[
|\delta|=qFd,
\]

and converting joules to eV cancels the elementary-charge factor numerically:

\[
|\delta|_{\rm eV}=Fd
=(10^7)(3.5\times10^{-9})
=0.035\ {\rm eV}=35\ {\rm meV}.
\]

This independently reproduces the scale quoted in the paper. It does not establish that this field or separation applies to the project's D18/PY-IT/eC9 devices.

## Frozen synthetic counterexample

Planning fixture only:

- \(T=300\) K;
- \(\Delta G=-0.100\) eV;
- \(|\delta|=0.035\) eV;
- \(\lambda\) swept from 0.05 to 0.25 eV.

Selected results:

| λ (eV) | R+ | R− | Rworst | max/min orientation rate |
|---:|---:|---:|---:|---:|
| 0.05 | 1.552714 | 0.400975 | **0.400975** | 3.872346 |
| 0.10 | 0.888285 | 0.888285 | **0.888285** | 1.000000 |
| 0.15 | 0.737405 | 1.157970 | **0.737405** | 1.570332 |
| 0.20 | 0.671866 | 1.322116 | **0.671866** | 1.967828 |
| 0.25 | 0.635373 | 1.431572 | **0.635373** | 2.253121 |

Under this synthetic condition, lowering \(\lambda\) from 0.15 eV to 0.05 eV reduces the worst-orientation retention from about 0.74 to about 0.40. The best point on the frozen grid is \(\lambda=0.10\) eV, exactly the activationless match \(-\Delta G\).

This does not say that the mean device generation rate falls by the same amount. \(R_{\rm worst}\) deliberately asks a narrower adversarial question: **does the proposed microscopic change create a locally vulnerable orientation/field regime?**

## Sensitivity

The committed CSV sweeps \(|\delta|=10,35,70\) meV. For the same synthetic \(\Delta G=-100\) meV:

- at 10 meV: \(R_{\rm worst}=0.808/0.990/0.932/0.903/0.887\) for \(\lambda=50/100/150/200/250\) meV;
- at 35 meV: \(0.401/0.888/0.737/0.672/0.635\);
- at 70 meV: \(0.100/0.623/0.464/0.401/0.367\).

The conclusion that very small \(\lambda\) can be less field robust survives this deliberately broad synthetic field-energy sweep. The sweep is not a confidence interval.

## Independent checks

`models/marcus_stark_field_robustness_v3_45.py` performs:

1. direct subtraction of two Marcus exponents versus the independently simplified normalized-ratio equation;
2. the zero-field limit \(R=1\);
3. activationless \(R_+=R_-\);
4. the analytic orientation-asymmetry identity;
5. a central finite-difference derivative versus the analytic derivative;
6. the independent \(F d=0.035\) eV dimensional check;
7. a grid check that the frozen synthetic optimum occurs at \(\lambda=-\Delta G\).

CI independently recalculates the principal fixture without importing the production module.

## Reproducibility-lineage note

The paper links a public MATLAB repository, `HuotianZhang/DriftFusionOPV_FieldDependent`. At commit `d5e805ec69359f36be6e1da17a401ed8d64721a3`, the visible `functions/marcus_equation_stark.m` calculates a quadratic polarizability Stark term. The Nature Photonics main text separately estimates the first-order dipole shift as ~35 meV and states that Fig. 4g is based on the first-order Stark effect.

This is recorded as a **lineage question, not an accusation of error**. v3.45 independently implements the published main-text equation and first-order scale; it does not claim reproduction of the authors' full drift–diffusion simulation. A stronger external reproduction should identify the exact source-data/code revision used for Fig. 4g–i.

No upstream code is copied into this repository.

## Prospective program gate

Before a strong useful-work claim for B1/B2, measure field dependence rather than assuming a lower \(\lambda\) or lower \(\Delta V_{nr}\) is sufficient.

Preferred discriminators:

- bias-dependent PL;
- TDCF;
- or an independently justified equivalent field-dependent generation measurement.

These sit alongside stabilized J–V/Pmax, charge-generation, morphology, contact and transport controls.

**Kill/narrow rule:** if an interface arm lowers non-radiative voltage loss but shows materially worse field-dependent charge generation and fails to improve stabilized FF/Pmax, preserve the voltage-loss result as mechanism science but do not promote it as useful-work or platform validation.

v3.45 deliberately sets no universal threshold for \(\beta\), PL quench, TDCF, \(R_{\rm worst}\), FF, or field robustness. Physical acceptance limits require prospective measurement capability and baseline evidence.

## Conventional alternatives and validity limits

Field-dependent FF can also be affected by ordinary:

- morphology and interfacial population;
- transport/non-geminate recombination;
- contact/selective-layer limitations;
- series/shunt resistance;
- energetic disorder;
- exciton lifetime and diffusion;
- built-in-voltage/electrostatic changes;
- optical generation changes.

Classical Marcus is only one model family. Any real mechanism claim must survive the project's existing Marcus/MLJ/disorder model competition and direct experiments.

## Files

- `machine/marcus-stark-field-robustness-v3.45.json`
- `models/marcus_stark_field_robustness_v3_45.py`
- `models/marcus_stark_field_robustness_expected_v3_45.csv`
- `research/evidence/marcus-stark-fill-factor-v3.45.md`
