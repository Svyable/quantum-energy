# R2 calibration estimator lineage v3.31

## Purpose

This increment resolves an analysis-authority ambiguity for agents and reviewers. Two overlapping v3.19 calibration-covariance implementations were proposed in PRs #6 and #7. PR #6 was selected and merged into `main` as commit `4d315b65b8cb131b3a62eb352cb0cee6ff77ebcf`; PR #7 remains open and non-mergeable as of 2026-08-27.

The machine-readable authority record is `machine/analysis-registry.json`.

## Claim classes

**Established repository evidence:** PR #6 is merged; its seven declared analysis/test/schema/spec/evidence/session/CI paths are present on `main`. PR #7 remains an unmerged review candidate.

**Engineering decision:** the merged PR #6 implementation is the canonical v3.19 calibration-covariance path. PR #7 remains visible provenance but must not be treated as a second equally authoritative analysis implementation.

**Experimental result:** none. No real facility calibration covariance is established by this lineage decision.

**Synthetic/model result:** none added in v3.31. Existing v3.19 synthetic verification remains bounded exactly as documented by the merged implementation.

## Authority rule

For an analysis implementation `a`, define the authority state

`A(a) ∈ {CANONICAL_MERGED, REVIEW_CANDIDATE, SUPERSEDED_REVIEW_CANDIDATE}`.

The decision rule is categorical, not probabilistic:

1. reviewed code merged to `main` is canonical until explicitly superseded by a later reviewed merge;
2. an open PR cannot silently outrank `main` merely because it is newer or still open;
3. overlapping unmerged alternatives remain visible in history and may inform a future reconciliation, but are not used as production analysis inputs;
4. changing the canonical implementation requires a new human-reviewed PR that documents numerical and scientific downstream impact.

There are no physical units in this rule.

## Exact canonical set

The canonical merged v3.19 set contains seven repository paths:

1. `models/r2_calibration_component_estimator_v3_19.py`
2. `models/r2_calibration_component_test_v3_19.py`
3. `models/fixtures/r2_calibration_repeats_template_v3_19.csv`
4. `technical/r2-calibration-components-v3.19.md`
5. `research/evidence/r2-calibration-components-v3.19.md`
6. `research/sessions/2026-08-26-r2-calibration-components-v3.19.md`
7. `.github/workflows/r2-calibration-components.yml`

The count is independently checked in CI and has no uncertainty: it is a finite repository-set assertion.

## Distinct PR #7 paths that are not canonical

The alternate review candidate includes differently named paths such as:

- `models/r2_calibration_components_v3_19.py`
- `models/r2_calibration_components_synthetic_v3_19.py`
- `technical/r2-calibration-component-estimator-v3.19.md`

Their absence from `main` is intentional. They are not deleted from Git history, and this decision does not assert that every idea in PR #7 is scientifically wrong. It asserts only that the repository has one reviewed canonical implementation today.

## Independent verification

Primary path: `tools/validate_analysis_registry.py` parses the registry, requires the exact canonical file set, checks each path exists, checks the known alternate distinct paths are absent from the canonical branch, and verifies the project index exposes the registry to agents.

Independent CI path: shell/Python checks separately verify the seven canonical paths exist, the three distinct alternate paths do not exist on the branch, and the registry identifies PR #6 / merge commit `4d315b...` as authority while retaining PR #7 as superseded-review provenance.

Predeclared tolerance is exact set equality; missing, extra, or contradictory authority records fail.

## Uncertainty and sensitivity

The authority state itself is discrete and has no measurement uncertainty. The scientific uncertainty of the calibration model is unchanged and remains material: point-residual correlation, session-dependent shape, configuration nonstationarity, and lack of prospective real held-out calibration validation remain unresolved.

Sensitivity of the governance decision is explicit: if a future reviewed PR demonstrates that an alternative estimator materially improves prospective held-out calibration performance without weakening uncertainty accounting, the registry must be updated in the same reviewed change that supersedes the canonical implementation. Until then, open-PR status alone cannot change authority.

## Statistical independence

This lineage audit creates no experimental sample-size credit. Repository files, commits, and PRs are provenance objects, not calibration replicates. The calibration hierarchy remains session → sweep → intensity point, and downstream DUT inference retains lot → substrate → device/pixel → session → measurement.

## Conventional/null explanation

An agent could produce conflicting results simply by selecting two different overlapping analysis implementations rather than because the underlying physics differs. The discriminator is a single reviewed canonical implementation plus prospective real-data validation, not majority voting among code branches.

## Kill / narrow gate

If the merged v3.19 implementation fails prospective held-out calibration validation, the claim must narrow to “software-verified planning estimator.” The correct response is a reviewed estimator revision or replacement, not silent fallback to an old open PR.
