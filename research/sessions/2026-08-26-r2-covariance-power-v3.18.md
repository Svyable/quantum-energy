# Session record — 2026-08-26 — v3.18 covariance-aware curvature uncertainty

## Increment

Added covariance-aware propagation from declared `Voc`, intensity-calibration, and spectral-mismatch uncertainty components into the frozen R2 `Delta n_curv` observable and the v3.15 planning-power interface.

## Why now

v3.17 carries correlation-group labels but cannot yet answer how much those correlated uncertainties matter to the actual curvature result. Treating all rows as independent would be scientifically wrong for common calibration effects.

## Quantitative checks

All values below are synthetic/software checks.

- 0.5% perfectly common intensity scale: `u(Delta n) ~= 2.15e-12`.
- 0.5% independent intensity-axis uncertainty at every point: `u(Delta n) = 0.005524884`.
- correlated quadratic intensity-axis mode, 0.5% max loading:
  - linear covariance `u(Delta n) = 0.006438705`;
  - independent 12,000-draw Monte Carlo `u ~= 0.006434494`.
- independent 0.5 mV `Voc` point uncertainty:
  - `u(Delta n) = 0.0224200905`;
  - planning power for synthetic 0.10 effect `= 0.993795964`, reproducing v3.15.
- combined 0.5 mV `Voc` + 0.5% quadratic-axis fixture:
  - `u(Delta n) = 0.02332632385`;
  - planning power `= 0.9900183826`.

The finite-difference axis Jacobian is checked at `eps=1e-6` versus `5e-7`.

## Interpretation change

No earlier arithmetic is superseded. The v3.17 uncertainty representation is narrowed: one scalar uncertainty/group per row is insufficient when multiple simultaneous correlated components exist. v3.18 adds an optional component sidecar rather than pretending the original field can encode a full covariance model.

## Conventional/null explanations preserved

Even a precise nonzero curvature can arise from contact/surface recombination, transport resistance, energetic disorder, carrier-density effects, state filling, illumination heating, sweep history, or calibration/model error. Covariance propagation only qualifies precision.

## Files

- `models/r2_covariance_power_v3_18.py`
- `models/r2_covariance_fault_injection_v3_18.py`
- `models/fixtures/r2_covariance_fixture_v3_18.csv`
- `models/fixtures/r2_covariance_components_v3_18.csv`
- `models/fixtures/r2_covariance_expected_v3_18.csv`
- `technical/r2-covariance-power-v3.18.md`
- `research/evidence/r2-covariance-power-v3.18.md`
- `research/sessions/2026-08-26-r2-covariance-power-v3.18.md`
- `venture/v3.18-covariance-power-decision.md`
- `.github/workflows/r2-covariance-power.yml`

## Unresolved risks

- actual facility covariance components are not yet measured;
- scalar spectral-mismatch uncertainty may be inadequate for intensity-dependent spectra;
- first-order propagation can fail under larger nonlinear distortions;
- `voc_u_V` is independent by default unless explicit sidecar components replace it;
- power remains a planning calculation and independent substrate variability remains separate.

## Next best increment

Run v3.17 and v3.18 unchanged on the first real facility export. If real data remain unavailable, build a calibration-component estimation procedure from repeated reference-detector sweeps that empirically separates common scale, smooth shape, drift, and point residual covariance rather than assigning those modes by assumption.
