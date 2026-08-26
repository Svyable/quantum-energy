# Session v3.11 — scientific release attestation

## What changed

Added a deterministic SHA-256 fixture-manifest generator, an independent sha256sum cross-check in publication CI, and a tag/manual release workflow that uploads and cryptographically attests the generated manifest.

No physical model, scientific fixture, literature benchmark, experimental result, or performance number was changed.

## Evidence / source provenance

External publication-infrastructure source checked 2026-08-26:

- GitHub artifact-attestation documentation: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations

GitHub API tag resolution checked 2026-08-26:

- `actions/attest@v4` = `1e69f48acb82d1966a394da916b4c1698aa569d6`
- `actions/upload-artifact@v4` = `ea165f8d65b6e75b540449e92b4886f43607fa02`

The fixture membership and repository-native Git blob identities remain those reviewed in `provenance/scientific-fixtures-v3.10.json`.

## Classification

- **Established evidence:** GitHub artifact attestations bind artifact digests to workflow/repository/commit provenance; they do not validate scientific truth.
- **Engineering assumption:** the v3.10 fixture set is the correct current set of decision-driving publication fixtures.
- **Synthetic/model result:** none added.
- **Experimental result:** none added.
- **Novel invention concept:** none added.

## Calculation / verification

For each fixture byte string `B`:

`sha256 = SHA256(B)`.

The generator first enforces the already frozen Git-object identity, then computes SHA-256 using Python `hashlib`.

Independent check: workflow code reconstructs a GNU/coreutils-style check file from the generated JSON and runs `sha256sum -c` over the original fixtures. This is a separate implementation from `hashlib`.

Pre-commit tool tests performed:

1. Python syntax compilation passed.
2. Functional test in a temporary Git repository with two fixtures passed.
3. The temporary test verified source-anchor ancestry, frozen Git blob identity, deterministic output, exact `--check` regeneration, and SHA-256 equality against a separately computed digest.

These tests validate the new publication tool, not physical science.

## Units / dimensional analysis

SHA-256 is a dimensionless 256-bit digest represented as 64 hex characters. Byte length is measured in bytes. No physical unit or material parameter is introduced.

## Uncertainty / sensitivity

There is no measurement uncertainty in equality of cryptographic digests. The important uncertainty remains whether the frozen fixture set and its scientific contents are correct and complete. Hashing cannot reduce model-form, calibration, statistical, or physical uncertainty.

The manifest is intentionally deterministic: current time and current Git HEAD are excluded so identical frozen fixtures regenerate identical bytes.

## Container assessment

A custom digest-pinned container is **deferred**. Exact dependency pins plus the current 3-Python × 2-scientific-stack matrix provide more useful cross-environment checking for the present deterministic workload. A container becomes justified if native/system-library sensitivity, GPU/native extensions, or a promised external executable environment enters the program.

## Statistical independence

Six CI matrix jobs and repeated release attestations are compatibility/provenance checks on the same artifacts, not independent scientific replications.

## Conventional / null explanations

A manifest/attestation failure is first interpreted as fixture drift, generator/verifier error, repository-history/check-out error, byte transformation, or workflow misconfiguration. A PASS is not evidence for EPC, R2 stability, open-quantum transport, or improved energy conversion.

## GitHub workflow decision

A fresh session branch `automation/quantum-energy-20260826-1557` was created from the open PR #2 head. The new work directly depends on v3.10 files that are not yet on `main`; opening a second PR against `main` would reproduce all v3.10 changes and create a true overlapping PR. Under the repository's documented exception, PR #2 should be advanced to this fresh branch head after verification rather than opening a duplicate PR.

## Files changed

- `tools/generate_scientific_attestation_manifest.py`
- `.github/workflows/scientific-release-attestation.yml`
- `.github/workflows/reproducibility.yml`
- `technical/scientific-release-attestation-v3.11.md`
- `research/sessions/2026-08-26-scientific-release-attestation-v3.11.md`
- `provenance/README.md`

## Corrections / superseded claims

No scientific claim is corrected. The v3.10 statement that runtime SHA-256 lacked a release-attestation path is superseded by this increment once the new workflow passes review/CI. The unresolved risk that GitHub-hosted runner images are mutable remains.

## Unresolved risks

- No redistributable real weak-EL facility reference dataset is available yet.
- A release attestation authenticates provenance of bytes, not scientific validity.
- GitHub-hosted runner images remain mutable even with the `ubuntu-24.04` label.
- The tag/manual attestation workflow still needs an actual successful run after this branch reaches the PR head.
- No digest-pinned OCI runtime is yet provided; this is a deliberate deferred engineering choice, not an oversight.

## Single best next increment

Obtain and publish a minimally sufficient real weak-EL reference/calibration package and run it through the frozen v3.7 raw-spectrum pipeline unchanged. If external data remain unavailable, the next publication increment should formalize a small, redistributable synthetic-to-real data-interface specification so facilities can export wavelength calibration, radiometric response, dark/background, linearity metadata, and repeated reference spectra in one standard schema.
