# R2 Facility Capability Confirmation Protocol v3.29

## Purpose

This increment converts the merged v3.27 facility capability contract into a frozen, identical direct-confirmation questionnaire for real candidate laboratories. It is designed to follow the public-evidence audits in open PRs #19/#20 without duplicating their web research.

The protocol is an **engineering contract**, not experimental evidence. A favorable response does not establish device performance, EPC, open-quantum transport, commercial readiness, or a partnership.

## Claim classes

- **Established repository evidence:** v3.27 freezes seven facility capability classes, fifteen evidence packet roles, eleven configuration identifiers, data-integrity rules, and the statistical hierarchy.
- **Engineering assumption:** a standardized written confirmation protocol can resolve public-evidence ambiguity before experiment scheduling.
- **Falsifiable operational hypothesis:** at least one facility, or an explicitly bridged set, can answer the full questionnaire without weakening the frozen requirements.
- **Experimental results:** none introduced.
- **Synthetic/model results:** none introduced.
- **Novel invention concepts:** none introduced.

## Frozen questionnaire

Machine source: `technical/data/r2_facility_confirmation_questionnaire_v3_29.json`.

Every candidate receives the same:

- 8 global questions covering raw-data return, immutable/hash-bound files, excluded-row retention, configuration continuity, statistical hierarchy, prospective holdout discipline, uncertainty/provenance, and safety/EHS feasibility;
- 2 questions for each of the 7 v3.27 capability classes = 14 capability questions;
- 22 required question rows total;
- response vocabulary `YES / NO / CONDITIONAL / UNKNOWN`;
- configuration-limit, evidence, raw-data, uncertainty/provenance, access/scheduling, shipping/EHS, and data-rights fields.

No candidate is pre-populated with a favorable answer. The blank CSV template intentionally starts every response as `UNKNOWN`.

## Finite-set calculation and dimensional check

The number of required response rows is

`N_rows = N_global + 2 N_capability`

where:

- `N_global = 8` questions;
- `N_capability = 7` capability classes.

Therefore

`N_rows = 8 + 2(7) = 22`.

All terms are counts, hence dimensionless. The executable validator derives the 7 capability IDs from the merged v3.27 contract rather than maintaining a separate hidden list.

### Independent check

The validator separately constructs the expected global IDs `G01..G08` and capability IDs `C01A..C07B`, then requires the response template to contain exactly those 22 unique rows. This is independent of simply checking the JSON array length.

Predeclared tolerance: exact integer equality. Any missing, duplicate, or extra question is a hard failure.

### Limiting cases

- If all required answers for a capability are `YES` with evidence commitments, its direct-confirmation state can be `CONFIRMED`.
- Any required `NO` makes the capability `UNAVAILABLE` for the frozen protocol.
- Any unanswered/`UNKNOWN` required item keeps it `NEEDS_CONFIRMATION`.
- `CONDITIONAL` remains conditional until its explicit condition is satisfied; it is not silently promoted to `YES`.

## Uncertainty and sensitivity

The dominant uncertainty is epistemic rather than a measurement distribution. It is represented categorically by `UNKNOWN` and `CONDITIONAL`; assigning probabilities to undocumented capabilities would create false precision.

Sensitivity is structural: a single `NO` can invalidate a capability, while a single `UNKNOWN` prevents confirmation. The overall facility cannot be treated as execution-ready simply because most questions are favorable. This intentionally prevents averaging away a missing prerequisite.

No stochastic calculation is used, so random seed, Monte Carlo convergence, mesh, and time-step checks do not apply.

## Statistical independence

This protocol creates no experimental sample-size credit. Facility responses, webpages, and contacts are evidence/provenance records, not experimental replicates.

The downstream hierarchy remains:

`lot -> substrate -> device/pixel -> session -> sweep or step replicate -> measurement`.

If multiple facilities are ultimately used, `facility/configuration` must be added as an explicit factor and a bridge study is required before exchangeable pooling.

## Conventional/null explanation and discriminator

A sophisticated laboratory may own relevant equipment yet be unable to execute the exact frozen timing, range, raw-export, holdout, or provenance requirements. Conversely, a capability may exist even if it was absent from public webpages.

The discriminator is the same written questionnaire for every candidate, followed by a small dry-run evidence packet under v3.27. Reputation, publication record, and instrument ownership alone do not establish execution readiness.

## Anti-bias / exclusion rule

Requirements may not be removed, softened, reordered, or reinterpreted after seeing a preferred facility's response. Any scientifically justified change must produce a new version and be applied prospectively to every candidate.

Missing answers remain `UNKNOWN`. Silence is not an exclusion criterion and is not recoded as `NO` or `YES`.

## Safety and environmental boundary

The questionnaire explicitly asks whether requested work fits facility optical, electrical, thermal, source-duty, interlock, sample-acceptance, shipping, and EHS constraints. A scientific acquisition plan cannot override those constraints. A `NO` caused by safety incompatibility is a valid negative result, not a requirement to bypass a facility rule.

## Reproducibility

Run:

```bash
python tools/validate_r2_facility_confirmation_v3_29.py
```

The validator checks exact capability inheritance from v3.27, evidence-role consistency, response vocabulary, anti-bias semantics, 22-row template completeness/uniqueness, blank-template neutrality, hierarchy preservation, and non-claim boundaries.

## Decision gate

This protocol is ready for human review if the structural validator passes. Candidate facilities are **not** confirmed by this PR because no direct responses are supplied.

## Single best next increment

Send the frozen v3.29 questionnaire unchanged to the candidate facilities already audited in PRs #19/#20. Commit dated responses or source records, mechanically map each answer to `CONFIRMED / CONDITIONAL / UNAVAILABLE / NEEDS_CONFIRMATION`, and perform a dry-run v3.27 evidence packet before any full R2 campaign is scheduled.
