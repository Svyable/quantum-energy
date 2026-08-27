# Session 2026-08-26 — R2 light-intensity grid and power study v3.15

## What changed

Converted v3.14's local ideality estimator into a physical R2 acquisition
design and preregistered statistical power calculation.

## Frozen design

- 17 log-spaced intensity points, 0.05–2 suns.
- primary local estimator: 7-point quadratic in ln(intensity).
- mandatory smoothing sensitivity: 9-point.
- primary contrast: local `n_id` near 1 sun minus local `n_id` near 0.1 sun.
- confirmatory point-estimate `Voc` noise gate: <=0.5 mV SD.
- all functional devices retained under frozen QC rules.
- independent substrate hierarchy preserved.

## Calculation verification

The committed script uses an explicit 3x3 solver to derive local regression
weights. A separate NumPy pseudoinverse calculation agreed to a maximum weight
difference of `1.78e-14`.

For the nominal 0.5 mV / 0.10-effect scenario:

- analytic power: 0.993795964;
- independent 30,000-repetition Monte Carlo: 0.992733333;
- Monte Carlo null false-positive: 0.049833333.

The noiseless quadratic limiting case exactly recovers the injected local
ideality contrast.

## Important negative result

At 1.0 mV point-level `Voc` noise the primary planning power for a 0.10
curvature falls to about 0.607. The experiment therefore cannot claim
confirmatory curvature merely by collecting the nominal grid when metrology
noise is too high.

## Heating/dose boundary

Using the v2.5 0.0961 cm2 aperture and 100 mW/cm2 one-sun planning irradiance,
maximum incident power at 2 suns is 19.22 mW. Five seconds per point would
deliver about 457.45 mJ incident energy over the 17-point sweep.

This is not converted into a temperature prediction. Measured DUT temperature
is the acceptance variable.

## Statistical hierarchy

Repeated intensity readings and post-sweep anchors are technical repeats, not
independent samples. The mechanism-level interpretation remains at the
substrate/device level.

## External evidence

Primary contextual source: Wang et al., Advanced Materials (2026), DOI
`10.1002/adma.202523681`, plus public Zenodo dataset
`10.5281/zenodo.20525023` already used by v3.13/v3.14.

## Unresolved risks

- R2's true point-level noise is unknown;
- intensity calibration may have correlated/nonlinear errors;
- sweep direction/history may change the curve;
- illumination can heat the device;
- between-substrate curvature variance may exceed the 0.075 planning scenario;
- ideality curvature remains mechanistically non-unique.

## Single best next increment

Build and publish the **illumination calibration + sweep-history qualification
package**: reference photodiode calibration, intensity nonlinearity check from
0.05–2 suns, DUT-temperature versus intensity, ascending/descending hysteresis,
anchor-drift analysis, and a raw data schema that lets the 17-point power model
ingest measured point noise and calibration covariance unchanged.
