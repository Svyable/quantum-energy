# Scientific provenance manifests

This directory records the exact identity of scientific fixtures used by publication/reproducibility gates.

## Current manifest

`scientific-fixtures-v3.10.json`

The manifest records repository-native Git blob SHA-1 values for the frozen files. CI verifies those identities with `git hash-object` and independently emits SHA-256 digests of the checked-out bytes into each job summary.

## Change policy

A frozen scientific fixture may be changed, but a PR that changes it must also:

1. explain why the scientific fixture changed;
2. update or supersede the manifest visibly;
3. state which published/synthetic results may be affected;
4. rerun all downstream calculations and regression fixtures;
5. record any changed outputs as a correction or intentional new version, never by silently replacing history.

Do not describe the Git SHA-1 values as modern archival signatures or proofs of authorship. They are repository-native content identities. SHA-256 is used as a second runtime digest; a future archival/release workflow may commit SHA-256 manifests and signed release attestations.
