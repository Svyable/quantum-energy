# Scientific provenance gate v3.10

## Status

**Publication/reproducibility infrastructure.** This increment adds no experimental evidence for R2, EPC, open-quantum transport, or photovoltaic performance.

## Problem

The v3.9 CI reruns scientific calculations across multiple Python/NumPy/SciPy combinations, but a green run alone does not prove that the scientific fixture itself was unchanged. A benchmark CSV, numerical harness, or requirement file could be edited in the same PR as the test that consumes it and still produce a self-consistent result.

The v3.10 gate therefore adds a second invariant: decision-driving scientific fixtures have a frozen repository-native content identity that must be changed explicitly and reviewed.

## Frozen fixture identity

`provenance/scientific-fixtures-v3.10.json` records the Git blob SHA-1 for:

- `models/delta_vnr_literature_benchmark.py`
- `models/delta_vnr_literature_benchmark_v3_8.csv`
- `models/r2_raw_spectrum_harness.py`
- `tests/reproducibility_gate.py`
- `requirements/ci-baseline.txt`
- `requirements/ci-current.txt`

These SHA-1 values are Git's native blob identities, not physical checksums or evidence. The verifier independently computes SHA-256 over the checked-out bytes at runtime and emits those SHA-256 values into the CI job summary. The SHA-256 values are a second digest path for audit/provenance; the committed gate currently asserts the Git blob identity because that identity was available directly from the canonical Git repository before this change.

### Why both hashes?

Git blob identity is exactly tied to repository content and naturally detects an accidental fixture edit. SHA-1 is no longer considered collision-resistant for adversarial cryptographic applications, so it should not be presented as a modern long-term archival signature. Runtime SHA-256 provides a stronger independent digest and should become the committed archival digest once a deliberate manifest-regeneration workflow is added.

No claim is made that this is a digital signature or proves authorship.

## Verification algorithm

`tools/verify_provenance.py` performs the following checks:

1. Load the frozen manifest and reject duplicate paths.
2. Require the manifest anchor commit to be an ancestor of the tested `HEAD`.
3. Require every frozen file to exist.
4. Recompute Git blob identity with `git hash-object` and compare it with the committed expected value.
5. Independently calculate SHA-256 and byte length for every frozen file.
6. For the active CI stack, parse exact `name==version` requirements and require the installed NumPy/SciPy versions to match exactly.
7. Emit a JSON runtime fingerprint containing repository `HEAD`, anchor, Python implementation/version, platform/machine, GitHub runner `ImageOS`/`ImageVersion`, active scientific-stack versions, Git blob identities, SHA-256 digests, and byte lengths.

Any mismatch fails the publication CI. Fixture changes are therefore possible, but they require an explicit manifest update that is visible in human review.

## Environment pinning boundary

The CI runner changes from mutable `ubuntu-latest` to the more specific `ubuntu-24.04` label. Official GitHub actions remain pinned to full commit SHAs and NumPy/SciPy remain exact-version pinned by the two CI requirement sets.

This is **not full environment immutability**. GitHub can update the contents of its hosted `ubuntu-24.04` runner image, and `actions/setup-python` currently receives major/minor Python selectors rather than an immutable interpreter artifact digest. Therefore each run records the actual runner image metadata and Python/package versions. A future container/digest lock remains useful if the numerical workload or publication burden justifies the maintenance cost.

## Decision-driving assumptions

- **Engineering assumption:** Git blob identity plus independent runtime SHA-256 is sufficient to detect accidental or ordinary silent drift of the current scientific fixtures.
- **Engineering assumption:** exact NumPy/SciPy version pins plus cross-version CI and recorded runner metadata are sufficient for the present deterministic calculations.
- **Not assumed:** CI or hashing validates detector physics, experimental calibration, reciprocity, device equilibrium, or model adequacy.

## Independent checks and limiting cases

The new provenance gate is independent of the scientific calculations themselves: `git hash-object` and SHA-256 operate on raw bytes and do not depend on the benchmark equations, nonlinear fit, or physical model.

The previous v3.9 numerical checks remain unchanged:

- exact-SI independent recomputation of `DeltaVnr = -(kBT/q) ln(EQE_EL)`;
- published benchmark regeneration;
- photon-conservation and grid-convergence checks;
- nonlinear-fit versus interpolation-FWHM linewidth cross-check;
- deliberate missing-Jacobian negative control.

Thus a green publication run now requires both **fixture identity** and **scientific numerical invariants**.

## Conventional/null explanations

A provenance failure is first interpreted as one of:

- intentional fixture edit without manifest update;
- accidental source/data edit;
- line-ending or working-tree transformation;
- dependency mismatch;
- checkout/repository corruption;
- an error in the provenance manifest or verifier.

It is not physical evidence and must never be presented as a scientific effect.

## Corrections / superseded claims

No physical claim is superseded. The v3.9 statement that `ubuntu-latest` was an unresolved environment-drift risk is narrowed: v3.10 removes the mutable alias by using `ubuntu-24.04`, but does **not** eliminate hosted-runner image drift. The remaining limitation is recorded explicitly rather than calling the environment fully pinned.

## Next publication-grade increment

The highest-value next step remains a redistributable real weak-EL facility reference package. Once available, add its minimally sufficient raw/calibration fixture to this same provenance scheme and require the **unchanged** v3.7 processing path to reproduce the reference before synthetic linewidth uncertainty is replaced with empirical uncertainty.
