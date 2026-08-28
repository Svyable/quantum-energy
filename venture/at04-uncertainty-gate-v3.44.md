# Venture gate — AT-04 uncertainty budget v3.44

## Decision

Do not advance proprietary B0/B1/B2 mechanism fabrication or major in-house metrology capex merely because a nominal EQE_EL calculation exists. Advance only after a real reference run populates the component-level AT-04 uncertainty budget and the complete provenance-backed combined standard uncertainty is `<=10 mV` under defensible covariance treatment.

## Why this matters commercially

A voltage-loss effect that is comparable to unresolved calibration/background/temperature/session uncertainty cannot support a credible process-control claim, investor-facing mechanism statement, or spend decision. The budget therefore acts as a capital-efficiency gate: fix metrology before paying for proprietary materials or scaling a weak signal.

## PASS

A real run is eligible to unlock the next stage only when all material uncertainty components are measured or otherwise provenance-backed, covariance/shared calibrations are reviewed, double counting is excluded, the propagation regime is valid, independent arithmetic checks pass, and combined standard uncertainty is `<=10 mV`.

## FAIL / INCOMPLETE

A complete budget above 10 mV is `FAIL` for the current internal target. Missing provenance, unresolved shared covariance, suspected double counting, or an invalid first-order approximation is `INCOMPLETE`, not PASS.

## Synthetic fixture boundary

The v3.44 synthetic fixture evaluates to approximately 5.39–6.72 mV over its declared correlation sensitivity. That result is software/planning evidence only and must not be represented as facility capability, device performance, vendor performance, or experimental qualification.

## Best next spend

The next justified spend is a bounded reference qualification that records component calibration provenance and covariance. If measured weak-signal behavior invalidates first-order propagation, the next software increment should be distribution-aware propagation before proprietary-material release.
