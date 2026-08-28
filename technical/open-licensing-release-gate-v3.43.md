# v3.43 Open-licensing release gate

## Claim class

**Engineering governance specification.** This document proposes a reviewable license split for project-owned artifacts. It is not legal advice, does not grant a license by itself, and does not change the current fact that public GitHub visibility is not equivalent to an explicit reuse license.

## Problem

The repository is intentionally public and explicitly open-science, but `README.md` and `OPEN_SCIENCE.md` correctly state that formal software/data/documentation/hardware reuse terms are still unresolved. This is a deployment and reproducibility defect: downstream users need machine-readable, artifact-class-specific terms and clear third-party exclusions before a formal release can honestly be called open-source/open-hardware.

## Proposed artifact-class split

The machine authority for this proposal is `machine/licensing-manifest-v3.43.json`.

| Artifact class | Recommended license | Status |
| --- | --- | --- |
| Software | `Apache-2.0` | pending human approval |
| Documentation / research text | `CC-BY-4.0` | pending human approval |
| Structured project-owned data | `CC-BY-4.0` | pending human approval |
| Hardware / CAD source | `CERN-OHL-W-2.0` | pending human approval |

The recommendation is intentionally split rather than forcing one license onto unlike artifact types. The hardware recommendation uses CERN-OHL-W-2.0 rather than describing Markdown mechanical briefs as software.

## External provenance checked 2026-08-27

- Creative Commons states that CC licenses are applied by marking the work with the chosen license and that a CC license, once applied, is not revocable by the licensor. Source: https://creativecommons.org/chooser/ and https://creativecommons.org/version4/
- The Open Hardware Repository publishes the three CERN OHL v2 variants and identifies the weakly reciprocal form as `CERN-OHL-W-2.0`. Source: https://ohwr.org/licences/
- SPDX provides standardized short identifiers and license-list infrastructure. Source: https://spdx.org/licenses/

These sources establish license identity and application conventions. They do **not** establish that this project owns every right necessary to license every current repository artifact.

## Release logic

A formal release is blocked until all of the following are true:

1. exact license texts or canonical license files are committed;
2. directory/per-file notices map artifact classes to those licenses;
3. a third-party-material inventory has been reviewed;
4. contributor-rights / inbound-contribution expectations have been reviewed;
5. a human approval record accepts or amends the proposed split.

Machine rule:

`formal_release_allowed = AND(all prerequisite gates)`.

Every prerequisite is Boolean and dimensionless. In v3.43 every value is deliberately `false`, so the limiting case is unambiguous: one false prerequisite is sufficient to block a formal release. The validator additionally requires all six recorded gates to remain false in this proposal so an automation run cannot silently promote the recommendation into an effective license grant.

## Independent check

The primary validator loads the JSON manifest and checks class/license mappings and release-gate state. The CI workflow performs an independent check without importing the validator: it parses the JSON separately, asserts exactly four artifact classes, asserts the four expected SPDX identifiers, asserts exactly six release-gate keys, and independently evaluates `all(gates.values()) is False`.

Predeclared software tolerance: exact string/Boolean equality; no floating-point tolerance applies.

## Uncertainty and sensitivity

The dominant uncertainty is legal/provenance scope, not numerical uncertainty. Important unresolved cases include mixed files, external datasets, quotations, vendor documents, standards excerpts, trademarks, database rights, contributor ownership, patents/FTO, privacy, and export-control obligations.

Sensitivity of the decision is intentionally conservative: if any prerequisite remains unresolved, the formal-release decision remains `BLOCKED`. Changing one recommended license does not unblock release unless the full prerequisite set is completed and human-approved.

## Conventional / null explanation

A public repository can appear practically reusable because files are downloadable and forkable. The discriminator is an explicit rights grant plus scope/provenance review. Public accessibility alone is therefore treated as the null condition, not as evidence of open-source licensing.

## Kill / narrow gates

- If human/legal review finds a recommended license incompatible with project goals or artifact rights, replace that recommendation before release; do not preserve v3.43 merely for narrative continuity.
- If a file contains third-party material that cannot be redistributed under the project license, exclude, replace, or separately mark it.
- If a hardware artifact is only a prose concept and lacks source needed to make/modify it, do not market it as open hardware merely because CERN-OHL-W-2.0 is later applied.
- Do not describe the repository as formally licensed open source until the effective license files/notices are merged.

## Next execution step

After human review of the split, the highest-value follow-up is to create a path-level third-party/inbound-rights inventory, then commit the approved canonical license texts/notices and flip release gates only in a separate reviewed PR.
