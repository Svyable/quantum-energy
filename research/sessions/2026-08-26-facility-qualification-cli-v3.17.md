# Session — v3.17 facility qualification CLI

Date: 2026-08-26

## Increment

Converted the merged v3.16 illumination/sweep preregistration into an executable facility-ready gate that reads the public CSV schema and emits a deterministic JSON qualification certificate.

## Claim classes

- Established/internal program state: v3.15/v3.16 estimator and metrology gates.
- Engineering assumptions: v3.16 numerical limits plus new provisional spectral-mismatch limits.
- Synthetic/model result: clean fixture and injected-fault behavior.
- Experimental result: none.
- Novel invention claim: none.

## Governing calculation

`n_id = [dVoc/dln(Phi)]/(k_B T/q)`.

The calibration axis is summarized by `ln(Phi_cal)=a+b ln(Phi_target)+epsilon`. Common multiplicative scale maps to `a`; axis gain/stretch maps to `b-1`; smooth shape error is quantified by maximum `|exp(epsilon)-1|`.

Measured calibration-axis distortion is propagated through an explicitly synthetic `Delta_n_curv=0.10` reference curve. The resulting curvature bias must remain <=0.01 in magnitude.

## Independent check

For `x_m=(1+a)x`, the analytic result is `Delta_n_measured=Delta_n_true/(1+a)`. At `a=0.005`, the expected bias is `-0.00049751243781`; the independent numerical path agrees within `1e-10`.

## Synthetic clean fixture

The frozen fixture passes every gate and produces a deterministic certificate. Key software-test outputs: calibration residual `6.25195e-4`, propagated curvature bias `-0.00128768`, point `Voc` uncertainty 0.3 mV, maximum temperature excursion ~0.05 K, reference-anchor drift ~0.1001%, `Voc` anchor drift 0.2 mV, median sweep difference 0.1 mV, and spectral-mismatch deviation 0.2%.

## Adversarial tests

One-at-a-time faults are injected for:
- 1 mV point uncertainty;
- 301 K DUT temperature;
- ~1% reference-anchor drift;
- 2 mV `Voc` anchor drift;
- 2 mV descending-sweep offset;
- spectral-mismatch factor 1.03;
- excessive smooth calibration-axis curvature;
- missing spectrum metadata.

Each fault must produce the intended FAIL/INCOMPLETE gate. These are synthetic software tests, not measured instrument sensitivity.

## Statistical independence

The CLI does not promote repeated intensity points, anchors, or sweep directions into independent substrate samples. Calibration uncertainty remains grouped by declared correlation labels.

## Corrections

No earlier arithmetic was corrected in this session. The interpretation is operationally narrowed: a missing required measurement-path field is now an explicit `INCOMPLETE`, never an implicit pass.

## Unresolved risks

- real facilities may express spectral mismatch or calibration covariance more richly than the v3.17 scalar fields;
- `voc_u_V` may be supplied from an instrument model rather than empirical repeats;
- a scalar mismatch factor may hide intensity-dependent spectral changes;
- the new spectral-mismatch numerical gates are provisional engineering assumptions;
- passing the CLI does not validate mechanism physics.

## Next increment

Run the unchanged CLI on a real facility export. If none is available, add a covariance-aware synthetic intensity-calibration benchmark that converts declared correlation groups into a full curvature uncertainty distribution rather than reporting only group summaries.
