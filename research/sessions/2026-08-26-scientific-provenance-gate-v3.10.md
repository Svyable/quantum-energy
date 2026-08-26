# Session v3.10 — scientific fixture provenance gate

## Increment

Added an explicit content-identity and runtime-fingerprint layer around the v3.9 publication CI so a calculation cannot be called reproduced merely because a test and the fixture it consumes were silently changed together.

This is **publication infrastructure**, not new physical evidence.

## Evidence/source provenance

No new material-physics source is introduced. The scientific sources and v3.7/v3.8 benchmark provenance remain unchanged.

Repository-native fixture identities were obtained from the canonical GitHub blobs on the v3.9 PR head before the v3.10 changes:

| file | frozen Git blob SHA-1 |
|---|---|
| `models/delta_vnr_literature_benchmark.py` | `c56aca82780fe2bc1d1584e782a8c52320337368` |
| `models/delta_vnr_literature_benchmark_v3_8.csv` | `c2924d6bba9f7bbea97b8dfcf6b66cbc8c44cbad` |
| `models/r2_raw_spectrum_harness.py` | `f35a0c7055c71a1a2865577886047ff4781ae72f` |
| `tests/reproducibility_gate.py` | `f56ac4951cce7dbadf2b3f6fb3d897823a7663ef` |
| `requirements/ci-baseline.txt` | `e374d105f4a05104e5d9a28f01eca13da03f6365` |
| `requirements/ci-current.txt` | `1f15567aece0660b4628e801b8f4f4eae22dddd1` |

The manifest anchor is the v3.9 PR head `24655934665818778e4a7fc07f408b8f7002c4d2`.

## Technical delta

New files:

- `provenance/scientific-fixtures-v3.10.json`
- `provenance/README.md`
- `tools/verify_provenance.py`
- `technical/scientific-provenance-gate-v3.10.md`
- `research/corrections/2026-08-26-v3.10-shallow-checkout.md`
- this session record

Updated:

- `.github/workflows/reproducibility.yml`

The workflow now uses the explicit `ubuntu-24.04` hosted-runner label instead of `ubuntu-latest`, verifies the fixture manifest before numerical tests, checks exact package versions against the selected requirement stack, computes SHA-256 over every frozen fixture, and writes a structured runtime fingerprint plus runner-image metadata into the GitHub job summary.

## Calculation / verification logic

This increment does not add a decision-driving physical equation. Its content-integrity calculation is:

`digest = H(file_bytes)`

where the committed repository identity uses Git's native blob SHA-1 and the independent runtime path uses SHA-256.

For each frozen fixture, CI must satisfy:

`git_hash_object(file) == manifest.git_blob_sha1`.

Independently, CI evaluates:

`sha256(file_bytes)`

and records the resulting 256-bit digest and byte length. The second digest is not compared with a precommitted SHA-256 value in v3.10; it is an independent audit value recorded in CI. A later archival-release increment can commit SHA-256 digests after an explicit manifest-regeneration procedure is reviewed.

### Independent-path rationale

The fixture identity check is independent of the scientific equation/model implementation: it operates on raw bytes, so it cannot pass merely because the physics calculation was changed consistently with its expected output.

The existing v3.9 independent scientific checks remain unchanged and are still required after provenance passes.

## Units / dimensional analysis

Cryptographic digests are dimensionless byte-string identities. File byte length is recorded in bytes. No physical unit conversion is involved.

## Limiting cases / negative controls

Expected failures include:

1. changing one byte in any frozen fixture without updating the manifest;
2. installing a NumPy/SciPy version different from the exact selected requirement file;
3. testing a commit that does not descend from the frozen anchor;
4. deleting a frozen fixture.

These are software/provenance failures, not physical results.

## Environment boundary

Moving from `ubuntu-latest` to `ubuntu-24.04` removes one mutable alias but does not freeze the hosted runner image. GitHub can update that image while retaining the label. Therefore v3.10 records `ImageOS`, `ImageVersion`, Python version, platform/machine, NumPy/SciPy versions, Git `HEAD`, fixture SHA-256 values, and byte lengths on every job.

No claim of fully digest-pinned or hermetic execution is made.

## Assumptions / hypotheses

### Engineering assumptions

- Repository-native blob identity is an adequate accidental-drift gate for this stage.
- Runtime SHA-256 provides an independent stronger digest suitable for audit logs.
- Exact scientific-package pins plus six-environment CI and recorded runner metadata are adequate for the current deterministic numerical workload.

### Physical hypotheses

No physical hypothesis is promoted, demoted, or tested by this increment.

### Novel invention concepts

None.

## Statistical independence

No physical samples or new Monte Carlo evidence are added. CI matrix jobs are software compatibility checks and must never be counted as independent scientific replications.

## Conventional/null explanations

A provenance mismatch is first treated as source/data drift, dependency mismatch, checkout transformation/corruption, or manifest/verifier error. It is not evidence for a material/device mechanism.

## Corrections / superseded claims

The first v3.10 CI run (`33008578861`) failed in all six jobs at the provenance step because the default shallow `actions/checkout` did not contain enough commit history for `git merge-base --is-ancestor` to prove the frozen anchor relationship. The fix was to set `fetch-depth: 0`; the ancestry invariant was retained rather than weakened. No scientific fixture or physical result changed. The correction is preserved in `research/corrections/2026-08-26-v3.10-shallow-checkout.md`.

One infrastructure limitation is narrowed: v3.9 identified `ubuntu-latest` as mutable; v3.10 uses `ubuntu-24.04` but explicitly retains hosted-image drift as an unresolved risk.

## Verification status

After the shallow-checkout correction, the full six-job publication matrix passed on GitHub Actions run `33008748725` for the reviewed head. The passing run verified fixture identities, exact dependency versions, runtime fingerprints, and every existing v3.9 numerical gate. v3.10 is therefore **reproduced publication infrastructure** in the project evidence-level terminology; it is not experimental evidence.

## Unresolved risks

- Git SHA-1 is repository-native content identity but is not a preferred modern adversarial archival signature.
- Runtime SHA-256 is logged, not yet a signed/release-attested archival manifest.
- `ubuntu-24.04` is a mutable hosted image label.
- Python selectors are major/minor rather than interpreter-artifact digests.
- No native real-facility calibration/reference dataset is available yet.
- Passing this gate cannot validate experimental detector/device physics.

## Single best next increment

When a redistributable real weak-EL reference package is available, add a reduced immutable raw/calibration fixture to the provenance manifest and require the unchanged v3.7 processing path to reproduce it. If real data remain unavailable, add a reviewed SHA-256 manifest-regeneration/release-attestation workflow and, where maintenance cost is justified, a digest-pinned container for the scientific gate.
