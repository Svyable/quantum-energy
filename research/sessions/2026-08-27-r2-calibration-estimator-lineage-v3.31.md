# Research session — v3.31 R2 calibration estimator lineage

Date: 2026-08-27

## Increment

Resolved a repository-authority ambiguity caused by two overlapping v3.19 calibration-estimator PRs. PR #6 is merged and canonical; PR #7 remains visible as an unmerged, non-mergeable alternate review candidate.

## Inputs and provenance

- current `main` governance/specification files required by `automation/hourly-loop.md`;
- current open automation PR set;
- GitHub PR metadata for #6 and #7;
- current `main` file tree for the merged v3.19 implementation.

All inputs are repository provenance, not experimental measurements.

## Technical work

Added:

- `machine/analysis-registry.json`;
- `tools/validate_analysis_registry.py`;
- `technical/r2-calibration-estimator-lineage-v3.31.md`;
- correction and evidence records;
- venture decision gate;
- CI for structural authority checks;
- project-index entrypoint for agent discovery.

## Verification

The authority calculation is a finite-set check. Canonical v3.19 contains seven declared paths. The primary validator requires exact equality to those seven paths and verifies every path exists. It also requires the three distinct PR #7 alternate paths to remain absent from the canonical branch.

An independent CI path repeats the existence/absence and PR/merge-commit assertions without calling the primary validator. Tolerance is exact equality.

No stochastic calculation, physical unit conversion, or measurement uncertainty applies.

## Claim discipline

No experimental result is added. No synthetic output is promoted. No statement is made that PR #7 is scientifically worthless; only its authority status is narrowed. Real calibration covariance remains unestablished until prospective facility data pass the frozen metrology gates.

## Negative result retained

An open PR can remain visible after an overlapping alternative has merged. Therefore “open/newer-looking branch” is not a safe authority heuristic for agents. The repository now encodes that failure mode explicitly.

## Unresolved risks

- PR #7 still exists and human maintainers may choose to close it separately;
- the canonical v3.19 estimator still lacks prospective real held-out validation;
- analysis authority for other future overlapping PRs is not yet automatically registered unless maintainers extend the registry.

## Single best next increment

After human review of this lineage record, close or explicitly mark PR #7 superseded, then execute the first real prospective calibration holdout using only the canonical merged estimator and preserve any failure as a model-narrowing result.
