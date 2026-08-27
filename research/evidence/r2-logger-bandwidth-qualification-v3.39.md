# Evidence record — R2 logger bandwidth qualification v3.39

Date: 2026-08-27

## Evidence/source provenance

No new external physical-performance evidence is added. This protocol is derived from the merged R2 transfer-control architecture on `main` plus open PR #30, which correctly treats its 900 s logger gap as a synthetic completeness assumption rather than a physical qualification result.

## New evidence class

**Synthetic/model verification only.** The executable fixtures establish arithmetic and decision-rule behavior, not real logger performance.

Synthetic first-order fixture: `tau=120 s`, `y0=20`, `y_inf=40`, sampled at 0/30/60/120/240/360 s. Primary log-linear and independent pairwise derivations both recover 120 s within `1e-10 s`; RMS model residual is below `1e-12` channel units. The provisional 5-samples-per-tau rule therefore gives `gap_max=24 s`.

Sensitivity: synthetic `tau={60,120,300} s` maps linearly to `gap_max={12,24,60} s`. Decision implication: the fastest qualified response controls; no single fixed gap is defensible across configurations without response evidence.

Synthetic conservative acceleration checks: `(0.95-0.03)/(1.00+0.02)=0.90196078...` passes the provisional 0.90 screen; `(0.94-0.03)/(1.00+0.02)=0.89215686...` fails.

## Claim boundary

These fixtures verify software arithmetic and expose assumptions. They do not show that a real logger follows a first-order model, that a real package is safe, that shocks are bounded, or that transfer conditions preserve R2 device state.

## Conventional explanations preserved

Sensor lag, chamber slew, package gradients, hysteresis, nonlinear RH response, accelerometer resonance/orientation/clipping, reference bandwidth, and unlogged ESD/light/particles/contact changes remain live. Residual structure and controlled dummy qualification are the discriminators.
