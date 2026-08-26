# R2 Raw-Spectrum End-to-End Harness v3.7

## Status

**Synthetic/model verification only.** This increment tests whether the raw-counts analysis path can recover an injected CT linewidth without hidden preprocessing bias. It contains no measured R2 spectra, detector noise, or physical linewidths.

## Governing transform

`E = hc/lambda`. Photon conservation requires `N_E dE = N_lambda dlambda`, hence:

`N_lambda = N_E * hc/lambda^2`

and the inverse calibrated analysis must divide wavelength-density data by `hc/lambda^2` before fitting in energy coordinates.

Units close as `photons s^-1 eV^-1 * eV nm^-1 = photons s^-1 nm^-1`.

## Synthetic raw-count model

`C_sample ~ Poisson([N_lambda*eta(lambda)+D(lambda)+B(lambda)]t) + read_noise`, with separate background/dark records. Detector throughput, signal amplitude, dark/background rates, read noise, and calibration drift are explicitly synthetic planning assumptions until replaced by a facility calibration package.

## Independent checks

1. Photon-number integral conservation across wavelength/energy coordinates.
2. 2/1/0.5 nm grid convergence.
3. Nonlinear Gaussian linewidth fit versus interpolation-based FWHM on a noiseless spectrum.
4. Deliberately wrong no-Jacobian control.
5. Monte Carlo nominal, calibration-slope, background, signal-level, and seed sensitivity.

For a noiseless 80 meV synthetic Gaussian, curve-fit error is `1.42e-14 meV` and independent FWHM error is `5.686e-4 meV`. Omitting the Jacobian shifts the fitted center by `11.0505 meV`, demonstrating a concrete hidden-preprocessing failure mode.

At a 1 nm grid the photon-integral mismatch is `8.647e-7`. Grid refinement gives `3.459e-6`, `8.647e-7`, and `2.162e-7` at 2, 1, and 0.5 nm: essentially 4x improvement per halving.

## Correction made during this run

The first draft incorrectly required `<1e-10` conservation mismatch at 1 nm. That was false precision. The committed gate is `<2e-6` at 1 nm **plus** a 3.5–4.5 convergence-ratio check on successive grid halvings.

## Nominal synthetic recovery

Runtime: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, seed `20260826`, 300 simulations per temperature/scenario.

| T K | bias meV | RMSE meV | failures |
|---:|---:|---:|---:|
| 150 | +0.0136 | 0.1740 | 0 |
| 240 | -0.0170 | 0.1989 | 0 |
| 300 | -0.0154 | 0.2493 | 0 |
| 330 | +0.0016 | 0.2621 | 0 |

Frozen synthetic gate: absolute bias <=1 meV, RMSE <=2 meV, fit-failure fraction <=1% at every temperature. Nominal synthetic runs pass.

A 2% residual calibration slope causes <0.03 meV mean bias in this generator. A +/-10% background-scaling error is larger, reaching about 0.52 meV mean bias and 0.59 meV RMSE. Reducing the synthetic signal scale eightfold increases RMSE to about 0.97–1.32 meV at the tested 150/300 K points.

These are software operating-characteristic results, not facility performance.

## Claim boundary / null explanations

A correct linewidth pipeline does not identify static disorder or EPC. Real changes can still come from contacts/extraction, state filling, thermal gradients/Joule heating, detector nonlinearity, spectral truncation, multiple CT states, dynamic vibronic broadening, or irreversible material change.

## Release gate

Before real low-temperature linewidths enter H1–H4 recovery:

1. replace synthetic response/noise/background with real facility files;
2. rerun committed self-tests/convergence;
3. recover a reference linewidth independently measured or otherwise known;
4. determine empirical repeat linewidth SD;
5. retain failed/saturated bins without silent smoothing;
6. feed the empirical linewidth SD into `r2_low_temperature_execution.py`.

## Next increment

Ingest one real facility's wavelength calibration, response curve, dark/background, detector linearity limits, and repeat-reference spectra, then rerun this exact core analysis without changing the processing path.
