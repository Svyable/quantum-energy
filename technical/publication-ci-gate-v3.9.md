# v3.9 — Automated scientific publication gate

## Purpose

Turn two already-published numerical checks into mandatory, executable pull-request checks:

1. the external `EQE_EL -> DeltaVnr` literature regression from v3.8; and
2. the raw-spectrum wavelength/energy/Jacobian/linewidth self-tests from v3.7.

This increment adds **publication infrastructure**. Passing CI does not add experimental evidence for R2, EPC, open-quantum transport, or photovoltaic performance.

## Frozen checks

`tests/reproducibility_gate.py` fails unless all of the following hold:

- the v3.8 published `DeltaVnr` benchmark passes its <=1 mV rounded-literature gate;
- an independent SI-constant implementation agrees with the primary eV/K implementation within `2e-15 V` per benchmark point;
- the committed v3.8 CSV agrees with executable output within `1e-12` numerical tolerance;
- the v3.7 raw-spectrum photon-number conservation error is `<2e-6` on the frozen 1 nm grid;
- trapezoid integration error improves by approximately fourfold when the wavelength grid is halved (`3.5 < ratio < 4.5` for 2->1 nm and 1->0.5 nm);
- noiseless nonlinear-fit linewidth error is `<1e-6 meV`;
- independent FWHM linewidth error is `<0.01 meV`;
- deliberately omitting the wavelength/energy Jacobian still produces a center shift `>5 meV`, so the negative control remains discriminating.

The workflow separately reruns `models/delta_vnr_literature_benchmark.py` and byte-compares its regenerated CSV against the committed file. It also executes a deterministic `nsim=8` raw-spectrum smoke run with seed `20260826` to exercise the complete command-line path and output creation.

## Independent calculation path

The primary v3.8 implementation uses `k_B = 8.617333262145e-5 eV/K`.

The CI cross-check instead computes

`DeltaVnr = -(k_B T / q) ln(EQE_EL)`

using the exact SI constants:

- `k_B = 1.380649e-23 J/K`
- `q = 1.602176634e-19 C`.

The two paths must agree within `2e-15 V`. This is an implementation/unit cross-check, not an uncertainty statement about the source measurements.

## Software-environment sensitivity

The same tests run on Python 3.12, 3.13, and 3.14 under two pinned scientific stacks:

### Baseline compatibility stack

- NumPy `2.3.5`
- SciPy `1.17.0`

NumPy 2.3.5 matches the version recorded in the v3.7 raw-spectrum work. SciPy 1.17.0 is frozen as the baseline optimizer version for this CI layer.

### Current-stable compatibility stack frozen 2026-08-26

- NumPy `2.5.2`
- SciPy `1.18.1`

As of 2026-08-26, PyPI lists NumPy 2.5.2 as the latest NumPy release (2026-08-09), and SciPy lists 1.18.1 as released 2026-08-21.

The purpose of running both stacks is to detect numerical/library drift before it reaches a scientific interpretation. A disagreement blocks publication until diagnosed; the newer stack does not automatically supersede the historical baseline.

## GitHub Actions supply-chain control

The workflow does not use floating action tags. It pins official GitHub actions to full commit SHAs resolved from their verified release tags during this session:

- `actions/checkout` v7.0.1 -> `3d3c42e5aac5ba805825da76410c181273ba90b1`
- `actions/setup-python` v7.0.0 -> `5fda3b95a4ea91299a34e894583c3862153e4b97`

Workflow permissions are read-only (`contents: read`) and checkout credentials are not persisted.

## Uncertainty and validity boundary

CI tests software reproducibility under frozen synthetic/literature inputs. It does **not** test:

- detector linearity or dark/background behavior at a real facility;
- radiometric or wavelength calibration uncertainty;
- spectral truncation;
- device temperature gradients;
- injection-state equilibrium;
- R2 sample drift;
- correctness of Gaussian/single-mode physical assumptions for a real CT spectrum.

Those remain empirical gates.

## Conventional failure explanations

A CI failure is not evidence of new physics. First explanations to test are:

1. dependency/API drift;
2. floating-point or optimizer behavior change;
3. accidental committed-data edit;
4. unit/sign/normalization regression;
5. changed numerical tolerance or preprocessing;
6. genuine correction to an earlier implementation.

Any genuine correction must follow `research/CALCULATION_VERIFICATION.md`: visible correction note, downstream impact audit, and explicit supersession.

## Program consequence

Future quantitative PRs now have a machine-enforced minimum gate for two critical calculation paths. This reduces the risk that a dependency update, unit conversion, or preprocessing change silently creates an apparent effect on the same millivolt scale as the program's target mechanism signal.

The next expansion should occur only after real facility-native reference data are available: add those files as immutable fixtures (or open-license reduced fixtures when raw data cannot be redistributed) and make the frozen v3.7 processing path pass them without retuning.
