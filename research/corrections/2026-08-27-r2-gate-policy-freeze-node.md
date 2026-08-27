# Correction — v3.33 repeatability-freeze graph node

Date: 2026-08-27

## Error

The first branch draft of v3.33 represented nine policy gates and copied `reference_repeatability_holdout -> [reference_repeatability_training, reference_repeatability_freeze]` from the merged v3.27 contract, but did not itself include `reference_repeatability_freeze` as a graph node.

That left a dangling dependency and would correctly cause the topological validator to reject the policy.

## Correction

Before opening the PR:

- added explicit `reference_repeatability_freeze` stage;
- set its prerequisite to `reference_repeatability_training`;
- updated the gate count from 9 to 10;
- updated the validator and independent CI path to require a closed dependency graph;
- recomputed the exhaustive local prerequisite truth-table count as 81 cases;
- updated the technical specification accordingly.

## Impact

No experimental, physical, cost, performance, or mechanism result was affected. The correction strengthens the intended prospective-validation boundary: the holdout cannot execute unless both training and the freeze record pass.

The incorrect nine-node draft never reached `main` and no PR represented it as final. This note is retained because the repository policy treats corrections as first-class contributions.
