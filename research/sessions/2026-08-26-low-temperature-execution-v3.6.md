# Session v3.6 — low-temperature execution package

Date: 2026-08-26

## What changed

Converted v3.5's low-temperature feasibility concept into an executable, vendor-portable qualification package:

- device-side mechanical/interface drawing (`technical/cad/r2_low_temperature_stage_interface_v3_6.svg`);
- thermal/electrical execution SOP and acceptance gates (`technical/r2-low-temperature-execution-v3.6.md`);
- machine-readable QC/uncertainty template (`technical/data/r2_low_temperature_qc_template.csv`);
- executable recovery tool that ingests the actually usable temperature grid and measured linewidth repeatability (`models/r2_low_temperature_execution.py`);
- evidence/provenance note and capital/deployment stop rules.

## Evidence added

Vendor-primary specifications were added for Linkam HFS600E-PB4 and Lake Shore DT-670/Cernox sensor families. These establish range and sensor calibration capability only; they do not establish mounted R2 temperature performance.

## Engineering assumptions frozen

- 150 K is the primary low-temperature qualification point.
- 120 K remains conditional.
- DUT accuracy <=1 K, stability SD <=0.25 K, measured self-heating <=0.5 K, spectral SNR >=20.
- A sensor-excitation self-heating check is required; >0.1 K shift blocks qualification.
- The actual device self-heating curve is measured from synchronized I/V/T rather than inferred from a generic thermal resistance.

## Equations and verification

Electrical heating:

`P = I*V`

`R_th,eff = d(T_DUT - T_stage)/dP`

The latter is an empirical local slope only; nonlinear data control directly.

Planning CT linewidth model:

`sigma_D^2(T)=lambda*hbarOmega*coth[hbarOmega/(2*k_B*T)]`.

Using synthetic `lambda=150 meV`, `hbarOmega=15 meV`, analytic `d sigma/dT` was independently checked against a centered finite difference (`h=0.01 K`) and agreed within `2e-10 meV/K` at 120/150/240/300 K using Python 3.13.5.

At 150 K the synthetic model gives `d sigma/dT=0.1763403 meV/K`; 0.5 K temperature error therefore maps to ~0.0882 meV linewidth error in that model. This is not an R2 uncertainty measurement.

The new recovery script was syntax-checked and executed on the committed synthetic-style schema with Python 3.13.5 / NumPy 2.3.5. A short smoke run correctly excluded the failing 120 K row, used 150/240/270/300/330 K, and returned `MECHANISM_SAMPLE_GATE=FAIL` for its low-simulation smoke case. That smoke result is a software-path check, not a power estimate and must not replace v3.4's committed higher-N simulations.

## Statistical independence

Temperature points and repeated spectra from one substrate remain repeated observations, not independent mechanism samples. The recovery classifier's `n_substrates` continues to mean independent substrates.

## Conventional / null explanations

Low-temperature linewidth or EL changes can still be caused by contact/extraction changes, injection/state filling, Joule heating, thermal gradients, detector/background drift, dynamic vibronic broadening, multiple modes, or irreversible device degradation. Passing the execution gate does not select H1 or EPC.

## Correction / narrowing

No prior numeric result was corrected this run. The v3.5 narrowing remains in force: 120 K is not a default point.

A new claim boundary was added: a calibrated thermometer's data-sheet accuracy cannot be substituted for installed DUT-temperature accuracy. The ±1 K gate must be demonstrated in the assembled measurement chain.

## Unresolved risks

- physical placement of a DUT-adjacent calibrated sensor may disturb optical/electrical access;
- exact stage-side adapter dimensions remain facility/vendor dependent;
- 150 K may already alter PM6:Y6 extraction/contact physics;
- weak EL may force impractically long integration;
- empirical linewidth noise may exceed 2 meV and erase the v3.4 sample-size advantage;
- the single-mode synthetic generator may not survive held-out model comparison.

## Single best next increment

Create the **facility-ready run manifest + analysis test harness** around a specific external/core setup: import its stage drawing and detector chain, freeze sensor mounting and wiring, generate synthetic raw spectra with dark/background/calibration artifacts, and verify that the complete raw-data-to-linewidth-to-recovery pipeline recovers known injected linewidths without hidden preprocessing bias.
