# Evidence note — R2 facility qualification CLI v3.17

Date: 2026-08-26

## Evidence class

This increment contains **synthetic/model/software-verification results only**. No real facility or R2 measurement is introduced.

## Established/internal basis

v3.15 froze the 17-point 0.05–2 sun `Voc`-intensity grid, 7-point local-ideality primary estimator, 9-point sensitivity estimator, and <=0.5 mV point-level precision requirement. v3.16 preregistered calibration-shape, anchor-drift, sweep-history, and DUT-temperature gates.

## New result

The v3.17 CLI executes those gates on a facility CSV and emits a deterministic JSON certificate with `PASS`, `INCOMPLETE`, or `FAIL`. Missing required spectral/calibration information cannot silently pass.

The clean synthetic fixture passes all gates. One-at-a-time injected faults are detected for point noise, temperature excursion, reference drift, `Voc` drift, sweep hysteresis, spectral mismatch, and calibration shape. A pure 0.5% log-axis gain is independently checked against the analytic relation `Delta_n_measured=Delta_n_true/1.005` within `1e-10`.

## New engineering assumptions

Until real facility exports retire them, v3.17 provisionally requires `|spectral_mismatch_factor-1|<=1%`, relative spectral-mismatch uncertainty <=0.5%, and a stable source-spectrum ID across the sweep pair. These are project gates, not external-standard requirements.

## Conventional explanations preserved

Even a passing certificate cannot rule out contact/surface recombination, transport resistance, energetic disorder, state filling, carrier-density-dependent recombination, spectral-response-model error, or other device physics. It only says the declared measurement-path checks passed.

## Falsification / next evidence

Run the unchanged CLI on the first real facility export. If a real calibration or spectral uncertainty cannot be represented in the schema, treat that as a schema failure and revise prospectively before interpreting R2 curvature.
