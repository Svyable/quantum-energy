# Session — R2 contact-state / ESD transfer control v3.42

Date: 2026-08-27

## Increment

Added an executable prospective control for ordinary contact/electrical-state changes during R2 handling, shipping, remounting, and cross-facility transfer.

## Why now

The transfer program already controls fixture geometry, shipping/handling effects, environmental logging, logger bandwidth, and sensor representativeness. A remaining conventional explanation is that terminal/contact state or an ESD/EOS event changes the DUT while the optical/metrology chain is otherwise stable. That can mimic a facility or device-physics difference.

Open automation PR #33 addresses agent/public discovery and is non-overlapping.

## Artifacts

- `machine/r2-contact-esd-control-v3.42.json`
- `technical/data/r2_contact_esd_control_template_v3.42.csv`
- `tools/check_r2_contact_esd_control_v3_42.py`
- `technical/r2-contact-esd-transfer-control-v3.42.md`
- `research/evidence/r2-contact-esd-transfer-control-v3.42.md`
- `venture/v3.42-contact-esd-transfer-decision.md`
- `.github/workflows/r2-contact-esd-control.yml`

## Verification

The synthetic software fixture yields `RMS_shift=sqrt(5/3) nA=1.2909944487358057 nA` and `Z_max=2.8284271247461903`. The independent limiting cases are `rho=-1 -> u_delta=u_pre+u_post`, `rho=+1` with equal common terms -> zero difference uncertainty for that component, and identical PRE/POST currents -> zero physical and standardized shift.

The protocol leaves physical probe settings and pass thresholds unset until prospective provenance exists. Missing configuration or acceptance limits is `INCOMPLETE`, never an implicit PASS.

## Conventional explanations retained

Contact pressure/registration, contamination, oxide/interfacial changes, ESD/EOS, ageing, temperature mismatch, instrument compliance/offset, encapsulation damage, and package handling remain live explanations.

## Statistical hierarchy

Substrate remains the independent unit. Voltage points, repeated sweeps, and sentinel samples are correlated/technical observations and add no independent substrate count.

## Corrections

No prior numerical or scientific result was found to require correction in this increment.

## Best next increment

Execute the v3.42 protocol on the first dummy/carrier transfer qualification using a prospectively frozen safe dark-I–V configuration and a characterized sentinel. Use the observed repeatability and instrument covariance to propose evidence-backed limits before any qualified R2 primary can receive PASS status.
