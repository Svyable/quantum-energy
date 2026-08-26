# Evidence record — R2 raw-spectrum harness v3.7

## External evidence added

None. This increment does not add a new material-performance or instrument-performance claim.

The hardware architecture inherits already recorded v2.0/v3.6 sources for the Linkam-class temperature stage, DUT-adjacent thermometry, and absolute/spectral EL chain. Those vendor/literature specifications remain external evidence; they are not reproduced performance.

## Synthetic/model evidence added

Committed raw-spectrum simulation and recovery code tests:

- wavelength ↔ energy photon-density transformation;
- numerical photon-integral conservation and grid convergence;
- independent Gaussian curve-fit vs FWHM linewidth extraction;
- a deliberately incorrect no-Jacobian control;
- Poisson/read-noise raw counts;
- background subtraction;
- wavelength-dependent throughput/calibration error;
- signal-level and random-seed sensitivity.

These are software operating-characteristic results only.

## Decision-driving synthetic result

Under the frozen generator and seed `20260826`, nominal linewidth recovery over 150/240/300/330 K has maximum absolute mean bias below 0.02 meV, maximum RMSE about 0.262 meV, and no fit failures in 300 simulations per temperature.

A ±10% background-scale stress is more influential than the tested 2% linear calibration-slope stress, reaching about 0.52 meV mean bias and 0.59 meV RMSE in this generator.

## Correction

An initial `<1e-10` photon-conservation tolerance at a 1 nm spectral grid was rejected after the implementation returned `8.647e-7`. Grid refinement showed ~4× error reduction per step halving, consistent with trapezoidal discretization. The committed criterion is `<2e-6` at 1 nm plus convergence-ratio checks.

See `research/corrections/2026-08-26-v3.7-discretization-tolerance.md`.

## Claim boundary

A synthetic PASS does not establish real facility precision, an R2 linewidth, static disorder, EPC, open-quantum transport, or useful electrical work.

Before physical mechanism inference, the exact analysis path must ingest real facility calibration/background/reference data and recover an independently characterized reference linewidth with empirical repeatability.
