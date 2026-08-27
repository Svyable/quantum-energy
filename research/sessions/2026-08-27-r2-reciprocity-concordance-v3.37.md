# Session — 2026-08-27 — R2 reciprocity concordance v3.37

## Increment

Made the existing 20 mV direct `EQE_EL` versus reciprocity-derived `Delta V_nr` agreement criterion executable as a paired-data metrology contract.

## Why this increment

Current open automation PRs cover shipping/handling state-change control (#28) and an older alternate calibration-covariance estimator (#7). This increment does not duplicate either. It closes a separate main-branch gap: the current specification names a reciprocity-concordance gate but did not provide a machine-readable raw template, executable status logic, or explicit shared-systematic sensitivity treatment.

## Quantitative verification

Primary metric: `d = direct - reciprocity`, in mV. Inherited decision window: `|d| <= 20 mV`.

Uncertainty diagnostic: `u_pair = sqrt(u_d^2 + u_r^2 - 2 rho u_d u_r)`. Independent implementation uses `Var(X-Y)=Var(X)+Var(Y)-2Cov(X,Y)` with `Cov=rho*u_d*u_r` and requires squared agreement within `1e-12 mV^2`.

Sensitivity is explicitly reported at `rho=-0.5,0,+0.5`. No stochastic simulation is used; seed is not applicable. Standard-library Python only.

Self-test fixtures cover the zero-difference, exact-boundary, just-over-boundary, sign-reversal, root-sum-square, perfectly shared, and perfectly anticorrelated limits. These are software fixtures only.

## Statistical independence

Paired pixel observations are metrology observations. Fabrication inference remains lot -> substrate -> device/pixel -> session -> measurement; repeated pixels/sessions do not create additional independent substrates.

## Conventional explanations

Disagreement can be caused by ordinary spectral-range, calibration, temperature, injection, background, or analysis-version effects. Agreement can also be spuriously strong through shared calibration systematics. The protocol therefore requires raw-data references, exact analysis commits, configuration matching, and a declared correlation treatment.

## Corrections / superseded claims

No prior numerical result is corrected. Interpretation is narrowed operationally: scalar agreement without independent provenance and shared-systematic accounting is insufficient to count as a valid reciprocity-concordance pass.

## Unresolved risks

Real R2 paired data are not yet present. The inherited 20 mV threshold remains a planning window rather than a standards-derived equivalence margin. Correlation structure may be more complex than a single scalar `rho`, especially across spectral calibration, temperature, and detector-chain components.

## Best next increment

Execute one prospective paired R2/AT-04 dataset through v3.37 using frozen direct and reciprocity analysis commits, then replace scalar `rho` with a component-level covariance map if real shared-systematic structure materially changes the interpretation.
