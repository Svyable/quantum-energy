# Correction / supersession note — R2 calibration estimator lineage

Date: 2026-08-27

## What changed

The repository now records explicitly that merged PR #6 is the canonical v3.19 empirical calibration-covariance implementation. Open PR #7 is an overlapping earlier review candidate and is not a second canonical implementation.

## Why this note exists

Leaving two overlapping implementations visually active can cause agents or reviewers to select different code paths and mistake implementation disagreement for scientific uncertainty. The ambiguity is a provenance/governance defect even though the scientific history itself remains valuable.

## Affected claims

No measured result or numerical v3.19 result is recomputed by this note. The affected claim is narrower: “which implementation is authoritative for future R2 calibration analysis?” The answer is the merged `main` implementation sourced from PR #6 unless a later reviewed merge explicitly supersedes it.

## What is not claimed

This does not assert that every method choice in PR #7 is incorrect. It does not delete #7 history, convert synthetic results into measurements, or establish real facility calibration covariance.

## Downstream action

Agents should consult `machine/analysis-registry.json`. Prospective real calibration validation remains the scientific discriminator. If the canonical estimator fails that test, revise or replace it through a new reviewed PR and update the registry/correction history visibly.
