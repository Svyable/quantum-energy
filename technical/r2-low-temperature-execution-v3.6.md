# R2 Low-Temperature Execution Package v3.6

## Status and purpose

This package makes the v3.5 low-temperature feasibility gate executable. It does **not** claim that 120 K or 150 K data establish static disorder, EPC, open-quantum transport, or useful-power improvement.

The primary low-temperature qualification point remains **150 K**. The **120 K point is conditional** and is attempted only if the 150 K operating-regime, self-heating, signal, repeatability, and recovery gates pass.

## Established external evidence

- Linkam HFS600E-PB4 probe stages support temperature/environment control below -195 °C to 600 °C, up to four positional electrical probes, a gas-tight chamber, and LN2 cooling with LNP96. Vendor capability only; not independently reproduced here: https://www.linkam.co.uk/hfs600e-pb4
- Lake Shore DT-670 silicon-diode thermometers cover the required range. The current vendor specification gives typical calibrated accuracy of about ±34 mK at 77 K and ±35 mK at 300 K, with recommended 10 µA excitation and reported sensor dissipation of ~10 µW at 77 K and ~5 µW at 300 K. These are vendor specifications, not mounted-DUT accuracy: https://www.lakeshore.com/products/categories/specification/temperature-products/cryogenic-temperature-sensors/dt-670-silicon-diodes
- Cernox sensors provide an alternative calibrated low-temperature thermometer family, with typical vendor-calibrated accuracy ±16 mK at 77 K and ±60 mK at 300 K: https://www.lakeshore.com/products/categories/specification/temperature-products/cryogenic-temperature-sensors/cernox

The program's **±1 K DUT accuracy gate is therefore dominated by mounting gradients, thermal contact, and electrical self-heating rather than the intrinsic calibration accuracy of a suitable calibrated sensor**. That statement is conditional on using a calibrated sensor within its specified range.

## Frozen thermal/electrical architecture

### Sample
- R2 coupon envelope: 25 × 25 × ~1.1 mm.
- Selected optical/electrical aperture: measured 3.10 × 3.10 mm.
- Existing perimeter contact pads remain the electrical interface.
- Sample stays mounted through the complete temperature sequence whenever the facility permits.

### Thermal stage

Preferred first execution path is a qualified external/core stage; a Linkam HFS600E-PB4 + LNP96 class system is compatible with the required range and probe count. A Janis/Lake-Shore optical cryostat remains an acceptable alternative if it provides equivalent raw temperature/electrical access.

No vendor-specific metal adapter is released until the selected facility supplies its stage drawing. The repository drawing therefore freezes the **device-side interface** and leaves the stage-side mounting boundary explicitly TBD.

### DUT temperature sensor

- Use a calibrated DT-670-class silicon diode or a calibrated sensor with equal-or-better uncertainty over 120–330 K.
- Mount the DUT sensor on the glass/substrate or thermally coupled carrier within 5 mm of the selected active pixel where practical, outside the optical and electrical keep-outs.
- Record the cold-finger/stage sensor independently.
- Four-wire/appropriate calibrated readout is required.
- Run a sensor-excitation self-heating check by comparing the nominal sensor excitation with a lower-excitation condition supported by the sensor/readout; a shift >0.1 K blocks the run until resolved.

## Temperature sequence

Nominal sequence:

1. 300 K baseline
2. 240 K
3. 150 K qualification
4. 120 K **only if 150 K passes**
5. 270 K
6. 330 K
7. return to 300 K

A monotonic cool-down is not required because reversibility is itself a control. Exact ordering may be adapted to facility constraints only if the change is preregistered before device data are interpreted.

### Frozen temperature gates

- `|T_DUT - T_set| <= 1 K`
- acquisition-period `SD(T_DUT) <= 0.25 K`
- no condensation/frost visible or optically detectable
- return-to-300-K recovery remains within the v3.5 planning gates

## Electrical self-heating characterization

At every qualified temperature acquire an injection/power ladder spanning at least:

`Jinj/Jsc = 0.1, 0.25, 0.5, 1, 2`

and include `5×Jsc` only if the device remains below the electrical and thermal safety limits.

For each point record synchronized `I`, `V`, `P = I V`, `T_DUT`, and `T_stage`.

Define the empirical low-power thermal coefficient

`R_th,eff = d(T_DUT - T_stage) / dP`.

This is an empirical local slope, not assumed to remain constant outside the measured range. The primary spectroscopy injection condition must satisfy **measured** self-heating `ΔT <= 0.5 K`. If the response is nonlinear, the measured `ΔT` at the actual point controls; do not extrapolate a linear fit.

## Dark / signal / repeatability sequence

For every candidate temperature:

1. detector shutter dark;
2. unbiased-device optical/electrical background;
3. injection ladder;
4. primary operating-point spectrum repeated at least three times;
5. immediate dark repeat;
6. bright transfer/reference check before and after the low-temperature block where practical.

Primary gates:

- integrated CT/near-gap spectral SNR `>=20` in the frozen fit window;
- no detector saturation;
- dark/background `<=10%` of the weakest accepted integrated signal;
- repeated linewidth-extraction SD entered into `technical/data/r2_low_temperature_qc_template.csv`;
- if empirical linewidth SD exceeds 2 meV, the v3.4 nominal recovery results are superseded for sample-size decisions and the recovery script must be rerun.

## Raw-data schema

Every spectrum/measurement row must preserve:

- run/session/device/pixel IDs;
- lot/substrate hierarchy;
- blind ID;
- timestamp;
- setpoint, DUT temperature time series, stage temperature time series;
- sensor IDs/calibration IDs/excitation settings;
- current, voltage, power, area, Jsc reference;
- wavelength/energy array;
- raw counts, dark counts, calibration array;
- integration time, gain/range, detector configuration;
- fixture/stage revision;
- software commit;
- operator deviation ID.

No smoothed-only spectra are acceptable as the raw record.

## Automatic recovery decision

`models/r2_low_temperature_execution.py` consumes the QC CSV. A temperature is usable only when all of these pass:

- explicit `usable` flag;
- DUT accuracy <=1 K;
- DUT stability <=0.25 K;
- measured self-heating <=0.5 K;
- spectral SNR >=20.

The script uses the **worst accepted empirical linewidth SD** as the synthetic recovery noise input and reruns the v3.4 H1–H4 generator on the actual usable temperature grid. A confirmatory mechanism sample design still requires `>=80%` synthetic recovery for every H1–H4 class. H5/EPC is not an output.

The committed CSV contains synthetic planning values only and is a schema/example, not R2 data.

## Calculation verification

Planning model inherited from v3.4:

`sigma_D^2(T) = lambda * hbarOmega * coth[hbarOmega/(2 k_B T)]`.

For synthetic `lambda=150 meV`, `hbarOmega=15 meV`:

- `d sigma/dT = 0.1806216 meV/K` at 120 K;
- `0.1763403 meV/K` at 150 K;
- `0.1537868 meV/K` at 240 K;
- `0.1407768 meV/K` at 300 K.

The analytic derivative was independently checked with a centered finite difference (`h=0.01 K`) and agreed to better than `2e-10 meV/K` at all four temperatures in Python 3.13.5.

At 150 K, even a 0.5 K temperature error contributes only ~0.088 meV of linewidth uncertainty **inside this synthetic one-mode model**. That does not bound transport-regime changes, thermal gradients, spectral-fitting error, or self-heating.

## Conventional explanations / falsifiers

A low-temperature linewidth change may result from:

- extraction/contact changes;
- injection/state filling;
- Joule heating;
- sample-stage thermal gradients;
- detector/background changes;
- dynamic vibronic broadening;
- multiple vibrational modes;
- physical degradation or incomplete recovery.

The measurement is usable for mechanism classification only after these are bounded. A residual is not evidence for EPC.

## Safety / EHS

- LN2 handling requires facility cryogen PPE, ventilation, oxygen-deficiency controls where applicable, and pressure-safe transfer procedures.
- All sample chambers/windows/feedthroughs must be rated for the selected environment and thermal cycle.
- Prevent condensation before electrical biasing.
- Electrical current/compliance limits must be frozen before the low-temperature run.

## Release decision

**PASS low-temperature execution qualification** means only that the qualified temperatures and empirical linewidth uncertainty can be fed into the public recovery model.

It does **not** release a physical mechanism claim. The subsequent sample-size/mechanism decision is made by the rerun recovery gate using measured uncertainty.
