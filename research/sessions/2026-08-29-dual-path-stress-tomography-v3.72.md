# Session — 2026-08-29 — v3.72 dual-path stress tomography

## Changed evidentiary state

Converted the v3.71 mechanism-redundancy hypothesis into a prospective two-stress experiment that can distinguish broad PY-IT morphology/domain stabilization from heterojunction-specific resilience.

No project device result is added.

## New evidence integrated

- Song et al., Matter 2022, DOI `10.1016/j.matt.2022.03.012`: direct PM6:BTP-eC9:PY-IT evidence for PY-IT entanglement, suppressed BTP-eC9 diffusion/crystallization and improved 85 C dark-N2 thermal robustness.
- Reese et al., Solar Energy Materials and Solar Cells 2011, DOI `10.1016/j.solmat.2011.01.036`: ISOS research stability framework and stress separation.
- 2026 J. Mater. Chem. C, DOI `10.1039/D5TC03674G`: recent encapsulated OPV light-stress implementation at 100 mW cm^-2, MPP tracking and controlled 50 C.

## Protocol delta

Arms: A0/A2/B0/B2.

Stress T: 85 C, dark, N2.

Stress L: encapsulated, 100 mW cm^-2, MPP tracking, controlled 50 C; exact spectrum/UV condition and duration must be frozen before unblinding.

Primary useful-work metrics: stabilized Pmax, Voc/Jsc/FF, field-generation observable, absorption/thickness, contact/transport diagnostic and morphology/packing witness.

## Analysis delta

For metric M and arm/stress:

`y = ln(M_after/M_before)`.

`Delta_A = y_A2-y_A0`.

`Delta_B = y_B2-y_B0`.

`Psi = Delta_B-Delta_A`.

Independent identity:

`exp(Psi)=(R_B2/R_B0)/(R_A2/R_A0)`.

Across stress types:

`Omega=Psi_T-Psi_L`.

## Synthetic software check

Fixture only:

- T retentions A0/A2/B0/B2 = 0.78/0.88/0.72/0.86;
- L retentions = 0.90/0.91/0.80/0.84.

Expected:

- Psi_T = 0.0570531894488;
- exp(Psi_T) = 1.05871212121;
- Psi_L = 0.0377403279828;
- exp(Psi_L) = 1.03846153846;
- Omega = 0.0193128614660.

These are not physical thresholds or expected effects.

## Falsifiers

- morphology/contact/optical controls fully explain PY-IT retention;
- A/B interaction disappears within measured uncertainty;
- T and L are experimentally non-orthogonal and produce the same confounded change;
- normalized retention improves but absolute stabilized Pmax does not;
- donor-free architecture remains unqualified.

## Next physical increment

Run A0 and B0 baseline repeatability through both stress workflows first. Freeze physical effect margins and sample count from real capability before unblinding A2/B2.
