# Research session — 2026-08-27 — v3.45 Marcus–Stark field robustness

## Bounded increment

Add a reproducible adversarial gate asking whether an interface/EPC design that lowers non-radiative voltage loss can become more vulnerable to field-dependent Ex→CT generation and therefore fail to improve FF/Pmax.

This is intentionally non-overlapping with open PR #36, which concerns AT-04 EQE_EL uncertainty propagation.

## New external evidence

Primary source: Zhang et al., Nature Photonics 2026, DOI `10.1038/s41566-026-01946-8`.

The paper directly reports a Voc–FF trade-off driven in some systems by field-dependent free-charge generation, identifies Ex→CT as the field-sensitive step, gives a Marcus–Stark rate equation, and estimates a ~35 meV first-order Stark shift from ~3.5 nm CT separation at ~`1e7 V/m`.

Existing commercial-bridge anchor retained: Luo et al., Nature Communications 2026, DOI `10.1038/s41467-026-68731-7`.

## Calculation

From the published Marcus form, with `A=lambda+DeltaG`,

`R(delta)=k(delta)/k(0)=exp[-(2 A delta+delta^2)/(4 lambda kB T)]`.

For opposite first-order orientations,

`R_worst=exp[-(delta^2+2|A||delta|)/(4 lambda kB T)]`.

For fixed `DeltaG=-g<0` and `0<delta<2g`, the model's worst-orientation retention is maximized at `lambda=g=-DeltaG`.

## Frozen synthetic fixture

- T = 300 K;
- DeltaG = -0.100 eV;
- delta = 0.035 eV published-scale diagnostic;
- lambda = 0.05/0.10/0.15/0.20/0.25 eV.

Key synthetic results:

- lambda 0.05 eV: Rworst = 0.400975; orientation rate ratio = 3.87235;
- lambda 0.10 eV: Rworst = 0.888285; ratio = 1;
- lambda 0.15 eV: Rworst = 0.737405; ratio = 1.57033.

Therefore a lower lambda is not monotonically more robust at fixed DeltaG in this model.

## Independent checks

The executable implementation includes direct-vs-algebraically-simplified ratio agreement, dimensional `F*d=0.035 eV` reproduction, activationless symmetry, zero-field limit, analytic orientation-asymmetry identity, finite-difference derivative and synthetic-grid optimum.

CI also performs a separate calculation path without importing the production module.

## Uncertainty and sensitivity

The paper's 35 meV scale is approximate and is not treated as a measured project parameter. The synthetic audit sweeps 10/35/70 meV. No confidence interval is claimed.

Physical decisions remain conditional on measured energetic offsets, reorganization parameters, field dependence, morphology and device electrostatics.

## Statistical independence

No experimental samples are added. The sweep points are correlated calculations and provide zero substrate/device sample-size credit.

## Adversarial/null interpretation

Rworst is deliberately a local worst-orientation metric; an orientationally averaged device can behave differently. Full Marcus/MLJ/disorder competition and measured bias-dependent PL/TDCF are needed before physical inference.

## Program change

Future useful-work interpretation should require field-dependence evidence. Lower DeltaVnr alone is insufficient if FF/Pmax is sacrificed.

## Single best next increment

Before B0/B1/B2 fabrication release, write a prospective field-dependent-generation measurement protocol for the named D18/PY-IT/eC9 arms using bias-dependent PL and, where facility access permits, TDCF. Freeze voltage/field range, optical normalization, morphology/contact controls, and a baseline-relative decision rule before unblinding.
