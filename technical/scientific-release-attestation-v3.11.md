# v3.11 — deterministic scientific-fixture manifest and release attestation

## Scope and evidence level

This increment is **reproducibility/publication infrastructure**. It adds no experimental evidence for R2, EPC, open-quantum transport, CT physics, or photovoltaic performance.

The purpose is to turn the reviewed v3.10 scientific-fixture set into a deterministic SHA-256 release artifact whose provenance can be cryptographically attested by GitHub Actions.

## Established external evidence

GitHub documents artifact attestations as signed provenance statements for produced artifacts. For public repositories, the feature is available on current GitHub plans. The documented workflow requires `contents: read`, `id-token: write`, and `attestations: write`, and uses the `actions/attest` action. The attestation binds an artifact digest to workflow/repository/commit provenance; it does **not** validate scientific truth.

Source checked 2026-08-26:
- https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations

Pinned action refs used in this repository were resolved directly through the GitHub API on 2026-08-26:
- `actions/attest@v4` → `1e69f48acb82d1966a394da916b4c1698aa569d6`
- `actions/upload-artifact@v4` → `ea165f8d65b6e75b540449e92b4886f43607fa02`

## Deterministic manifest relation

For each frozen fixture byte sequence `B_i`, the release manifest records

`d_i = SHA256(B_i)`

and its byte length `|B_i|`.

`d_i` is a dimensionless 256-bit digest represented as 64 hexadecimal characters. The generator first checks that

`git_hash_object(B_i) = frozen_git_blob_sha1_i`

from `provenance/scientific-fixtures-v3.10.json`, then independently computes `SHA256(B_i)`.

The JSON output is canonicalized by sorted keys, sorted fixture paths, two-space indentation, UTF-8, and a terminal newline. It intentionally omits timestamps and current Git HEAD so the same frozen fixture set produces byte-identical output across runs.

## Independent cross-check

The primary generator uses Python `hashlib.sha256`.

CI independently reconstructs a standard sha256sum check file from the generated JSON and runs the operating-system `sha256sum -c` implementation over every fixture. This is a separate digest implementation/path from the Python generator.

The generator itself was additionally syntax-checked and functionally tested before commit on a temporary Git repository containing two frozen fixtures. The test verified generation, exact `--check` regeneration, source-anchor ancestry, Git blob identity, and equality between the emitted SHA-256 value and a separately calculated SHA-256 value.

## Release workflow

`.github/workflows/scientific-release-attestation.yml` runs on `v*` tags and manual dispatch. It:

1. checks out full Git history;
2. generates `dist/scientific-fixtures-v3.11.sha256.json`;
3. independently checks every recorded digest with `sha256sum -c`;
4. uploads the manifest as a workflow artifact;
5. creates a GitHub artifact attestation for the manifest;
6. prints an explicit claim boundary: provenance is not physical validation.

The ordinary PR publication CI also generates and independently cross-checks the same manifest, but does not create signed attestations because PR CI should remain read-only.

## Uncertainty and sensitivity

Cryptographic digest comparison has no measurement uncertainty: equal byte strings produce equal SHA-256 values by definition. The relevant uncertainty is epistemic/system-boundary uncertainty:

- whether the frozen fixture list is complete;
- whether reviewed fixtures encode the correct scientific equations/benchmarks;
- whether dependencies/runtime are scientifically adequate;
- whether physical calibration and device assumptions are valid.

Those are handled by the existing numerical gates, evidence review, and future real-data fixtures—not by hashing.

Any one-byte fixture change necessarily changes its Git blob identity and, with overwhelming practical probability, its SHA-256 value. This is a content-drift gate, not a scientific significance test.

## Statistical independence

Multiple CI jobs or repeated attestations are not independent scientific replications. They are software/provenance checks on the same frozen content.

## Container decision

**Decision: defer a custom digest-pinned scientific container for now.**

Reasoning:

- current scientific dependencies are already exact-pinned in two environment files;
- the publication matrix intentionally tests three Python versions × two NumPy/SciPy stacks, which provides cross-environment evidence that would be partially hidden by forcing every job into one container;
- the workload is deterministic Python/NumPy/SciPy rather than compiler- or GPU-sensitive production code;
- a custom container adds its own base-image/SBOM/security-update maintenance burden.

This is an engineering judgment, not a statement that containers are unhelpful. Adopt a digest-pinned OCI image when at least one of the following becomes true:

1. a decision-driving result is materially sensitive to BLAS/system-library/compiler behavior;
2. a tagged release promises a specific executable environment to external labs;
3. a GPU/native-extension model is added;
4. package-level pins no longer reproduce the benchmark across supported runners.

At that point the image digest itself should be included in and attested by the same release provenance scheme.

## Conventional/null interpretation

A provenance or attestation PASS means only that identified bytes came through the stated workflow/repository/commit path. It does not imply that:

- the equations are physically correct;
- the experiment is calibrated;
- R2 is stable;
- EPC is causal;
- an open-quantum mechanism is present;
- photovoltaic performance is improved.

A failure should first be investigated as fixture drift, generator/verifier defect, checkout/history problem, line-ending/worktree transformation, or workflow/configuration error.

## Publication gate

A tagged scientific release should not advertise a frozen calculation fixture bundle unless:

- v3.10 Git-blob verification passes;
- v3.11 SHA-256 generation passes;
- independent `sha256sum` verification passes;
- the existing numerical reproducibility suite passes;
- the generated release manifest receives a valid GitHub artifact attestation;
- the release notes retain the distinction between provenance and experimental validation.
