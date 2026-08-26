# 2026-08-26 — v3.9 automated publication reproducibility gate

## What changed

Added an automated GitHub Actions gate that reruns the v3.8 published `EQE_EL -> DeltaVnr` benchmark and the v3.7 raw-spectrum numerical self-tests on every pull request and on pushes to `main`.

## Claim classes

- **Established evidence:** the v3.8 source paper provides published `EQE_EL`/nonradiative-loss benchmark values; exact SI values of `k_B` and `q` are fixed definitions; current official release pages identify the software/action versions recorded below.
- **Reproduced calculation:** the existing v3.8 benchmark and v3.7 numerical self-tests are now encoded as CI requirements.
- **Cross-check:** `DeltaVnr` is independently recomputed from SI `J/K` and `C` constants rather than the primary eV/K path.
- **Engineering assumption:** stability across the six tested Python/scientific-stack combinations is a useful minimum software portability gate. It does not establish experimental robustness.
- **Synthetic/model result:** the v3.7 raw-spectrum smoke and self-tests remain synthetic verification only.
- **Novel invention concept:** none introduced this run.

## External provenance checked 2026-08-26

- NumPy PyPI: 2.5.2 released 2026-08-09.
- SciPy release news: 1.18.1 released 2026-08-21.
- `actions/checkout` tag v7.0.1 resolves to commit `3d3c42e5aac5ba805825da76410c181273ba90b1`.
- `actions/setup-python` tag v7.0.0 resolves to commit `5fda3b95a4ea91299a34e894583c3862153e4b97`.

## Quantitative verification contract

The CI gate checks:

1. v3.8 literature benchmark maximum rounded-value error remains <=1 mV;
2. independent SI and primary eV/K `DeltaVnr` paths agree within `2e-15 V`;
3. the frozen benchmark CSV matches executable output within `1e-12` numerical tolerance;
4. v3.7 photon conservation remains `<2e-6` at 1 nm grid;
5. integration convergence ratios remain between 3.5 and 4.5 when step size halves;
6. nonlinear-fit and independent FWHM noiseless linewidth regressions remain inside their frozen gates;
7. the deliberate missing-Jacobian negative control remains `>5 meV` discriminating;
8. a deterministic raw-spectrum CLI smoke run creates complete outputs under seed `20260826`.

## Software sensitivity

The workflow spans Python 3.12/3.13/3.14 crossed with:

- baseline: NumPy 2.3.5 / SciPy 1.17.0;
- current stable on 2026-08-26: NumPy 2.5.2 / SciPy 1.18.1.

A stack-dependent failure is treated as a software/numerical compatibility problem until diagnosed, not as physical evidence.

## Statistical independence

No new physical samples or experimental statistics are introduced. The smoke-run Monte Carlo is deterministic software testing and must not be counted toward R2 mechanism power.

## Conventional/null explanations for failure

Dependency/API drift, floating-point/optimizer changes, accidental fixture edits, unit/sign/Jacobian regressions, or an earlier calculation defect must be investigated before any physical interpretation.

## Corrections / supersession

No existing scientific result is corrected this run. The change strengthens publication enforcement around already-committed calculations.

## Unresolved risks

- The workflow has not yet been tested against native real-facility reference data because none are present in the public repo.
- Baseline SciPy 1.17.0 is newly frozen for compatibility testing; v3.7 explicitly recorded NumPy 2.3.5 but not a SciPy version in its published metadata.
- GitHub-hosted runner images can change underneath `ubuntu-latest`; Python and scientific packages are pinned, but OS-level libraries are not yet container-digest pinned.
- Passing CI cannot validate physical assumptions such as Gaussian CT spectra, detector linearity, equilibrium injection, or reciprocity.

## Single best next increment

When a redistributable real facility/native reference package becomes available, commit an immutable reduced fixture containing wavelength calibration, radiometric response, dark/background, detector linearity metadata, and repeated weak-EL reference spectra, then require the frozen v3.7 path to process it without retuning. If such data remain unavailable, the next publication-infrastructure increment should container-pin the scientific CI environment and add cryptographic fixture hashes/provenance manifests.
