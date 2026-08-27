# Evidence record — R2 calibration estimator lineage v3.31

Date checked: 2026-08-27

## Repository evidence

- PR #6 (`Hourly quantum-energy: empirical calibration covariance`) is closed and merged.
- PR #6 merge commit: `4d315b65b8cb131b3a62eb352cb0cee6ff77ebcf`.
- The seven files declared by PR #6 are present on `main`.
- PR #7 has the same high-level v3.19 objective but remains open and non-mergeable as of this audit.
- PR #7 proposes differently named estimator/synthetic/spec paths and a different covariance-deconvolution/adequacy strategy.

These are repository-state facts, not physical evidence.

## Claim boundary

The evidence supports a governance/provenance conclusion only: PR #6 is the reviewed canonical implementation on `main`; PR #7 is an unmerged overlapping review candidate. It does not establish that the canonical model is physically correct for a real facility.

## Scientific uncertainty retained

The merged v3.19 evidence record already leaves open: residual correlation after low-order removal, session-dependent stretch/shape, nonstationarity under configuration changes, and prospective held-out validation. v3.31 retains those risks unchanged.

## Conventional counterexample

Different code branches can yield different outputs because their estimators differ, even with identical raw data. Such disagreement is not automatically evidence of new physics or irreducible metrology uncertainty.

Discriminator: freeze one canonical implementation, run prospective held-out calibration data through it unchanged, and treat failure as a model-revision trigger.
