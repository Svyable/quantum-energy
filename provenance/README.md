# Scientific provenance manifests

This directory records the exact identity of scientific fixtures used by publication/reproducibility gates.

## Current frozen source manifest

`scientific-fixtures-v3.10.json`

The manifest records repository-native Git blob SHA-1 values for the frozen files. CI verifies those identities with `git hash-object` and independently emits SHA-256 digests of the checked-out bytes into each job summary.

## v3.11 release manifest and attestation

`tools/generate_scientific_attestation_manifest.py` deterministically derives a SHA-256 release manifest from the frozen v3.10 fixture set. It first verifies each Git blob identity, then records SHA-256 and byte length. The generated JSON excludes timestamps and current HEAD so unchanged fixtures regenerate byte-identical output.

Ordinary PR CI generates that manifest and independently checks every recorded digest with the operating-system `sha256sum` implementation.

`.github/workflows/scientific-release-attestation.yml` runs on `v*` tags or manual dispatch. It generates the manifest as `dist/scientific-fixtures-v3.11.sha256.json`, uploads it as a workflow artifact, and creates a GitHub artifact attestation that binds the manifest digest to the repository/workflow/commit provenance.

**Claim boundary:** neither a SHA-256 match nor a valid artifact attestation establishes that a physical model, experiment, calibration, or performance claim is scientifically correct. Provenance is necessary publication infrastructure, not experimental validation.

## Change policy

A frozen scientific fixture may be changed, but a PR that changes it must also:

1. explain why the scientific fixture changed;
2. update or supersede the source manifest visibly;
3. state which published/synthetic results may be affected;
4. rerun all downstream calculations and regression fixtures;
5. record any changed outputs as a correction or intentional new version, never by silently replacing history;
6. regenerate the SHA-256 release manifest through the reviewed generator rather than editing digests by hand.

Do not describe Git SHA-1 values as modern archival signatures or proofs of authorship. They are repository-native content identities. SHA-256 is the archival digest path; GitHub artifact attestation adds workflow/repository/commit provenance to a generated release manifest.

## Runtime-container decision

A custom digest-pinned OCI scientific runtime is intentionally deferred while the deterministic Python workload continues to pass the multi-Python/multi-stack publication matrix. It should be reconsidered when native/system-library sensitivity, GPU/native extensions, or a promised external executable environment makes a single immutable runtime scientifically useful. A future container digest should itself enter this provenance and attestation scheme.
