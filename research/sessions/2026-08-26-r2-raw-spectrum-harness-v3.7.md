# Session v3.7 — raw-spectrum end-to-end recovery harness

## What changed

Built an executable synthetic test harness beginning at raw spectral counts and exercising background subtraction, radiometric correction, wavelength-to-energy spectral-density conversion, Gaussian linewidth extraction, QC, and sensitivity analysis.

## Evidence / provenance

No new material-performance evidence is introduced. Instrument architecture inherits v2.0/v3.6. All throughput/noise/signal values are synthetic planning inputs.

## Calculation verification

`E=hc/lambda` and photon conservation require `N_lambda=N_E*hc/lambda^2`. Dimensional check: `photons s^-1 eV^-1 * eV nm^-1 = photons s^-1 nm^-1`.

Independent checks: integral conservation; grid convergence; nonlinear fit versus FWHM; deliberate no-Jacobian control; calibration/background stresses; signal-level sensitivity; additional random seeds.

## Correction

The first implementation demanded `<1e-10` photon-integral mismatch at 1 nm and failed at `8.65e-7`. A 2/1/0.5/0.25 nm convergence study showed ~4x error reduction per step halving. The committed criterion is `<2e-6` at 1 nm plus the convergence-ratio check. No prior physical result is affected.

## Synthetic result

At seed `20260826`, 300 simulations per temperature gave maximum nominal absolute mean linewidth bias <0.02 meV, maximum RMSE ~0.262 meV, and zero fit failures. +/-10% background scaling was more damaging than a 2% linear calibration-slope residual but stayed below ~0.6 meV RMSE in this generator.

Across five additional seeds, nominal 150 K and 300 K RMSE stayed below ~0.25 meV.

These are software-verification outputs only.

## Statistical independence

Spectral bins and Monte Carlo repetitions are not independent device samples and do not increase the substrate sample count.

## Conventional explanations

Correct raw-spectrum recovery cannot distinguish contact effects, state filling, gradients, multiple CT states, vibronic broadening, or irreversible material changes.

## Unresolved risks

Real facility response may be less smooth; detector nonlinearity is not yet modeled; correlated calibration errors can differ from the synthetic slope; real CT spectra may be non-Gaussian/multimodal or spectrally truncated; real background drift may exceed the stress case.

## Next increment

Import one actual facility calibration/background/reference package and rerun the frozen analysis path.
