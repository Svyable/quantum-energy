# Evidence record — v3.43 open licensing release gate

Date checked: 2026-08-27

## Established external evidence

- Creative Commons provides version 4.0 licenses and guidance for applying a license to a work; it also warns that once applied, a CC license cannot be revoked by the licensor. Official sources: https://creativecommons.org/chooser/ and https://creativecommons.org/version4/
- The Open Hardware Repository publishes CERN Open Hardware Licence v2 permissive, weakly reciprocal, and strongly reciprocal variants, including `CERN-OHL-W-2.0`. Official source: https://ohwr.org/licences/
- SPDX maintains standardized short license identifiers and tooling. Official source: https://spdx.org/licenses/

## Repository-established state

Current `README.md` and `OPEN_SCIENCE.md` explicitly say that public visibility is not a complete open-source license and that software/data-documentation/hardware licensing must be chosen before a formal release.

## Engineering recommendation — not yet effective

v3.43 recommends, for human review only:

- software: `Apache-2.0`;
- documentation/research text: `CC-BY-4.0`;
- structured project-owned data: `CC-BY-4.0`;
- hardware/CAD source: `CERN-OHL-W-2.0`.

No license grant is claimed in this increment. The machine manifest deliberately sets `effective_date` to null and every release gate to false.

## Uncertainty / exclusions

This record does not establish ownership or relicensing rights for third-party datasets, papers, standards text, vendor material, trademarks, quoted excerpts, contributor-owned content, or patent rights. Those require path-level provenance/rightsholder review before release.

## Negative result / narrowing

A repository can be publicly readable and forkable while still lacking an explicit project reuse license. Therefore discoverability and public access are insufficient evidence for a formal open-source/open-hardware release.
