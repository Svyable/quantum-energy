# R2 direct-vs-reciprocity concordance protocol v3.37

## Purpose

This increment makes the existing R2/AT-04 planning requirement — direct `EQE_EL`-derived versus reciprocity-derived `Delta V_nr` agreement within 20 mV — executable and auditable. The 20 mV value is inherited from `technical/current-specification.md`; it is an engineering planning window, not a standards-derived equivalence limit.

This protocol is a **metrology consistency screen only**. Passing it does not establish EPC, open-quantum transport, improved photovoltaic performance, or facility equivalence.

## Inputs and provenance

Every paired row must identify lot -> substrate -> device/pixel -> session and record target/measured temperature, the two independently produced `Delta V_nr` values, their standard-uncertainty estimates, raw/minimally processed data references, exact analysis commits, configuration-match status, QC status, and a declared shared-systematic correlation coefficient `rho`.

The direct path is expected to inherit the repository relation

`Delta V_nr = -(k_B T / q) ln(EQE_EL)`.

The reciprocity path must preserve its own derivation and raw spectral inputs; this v3.37 wrapper intentionally does not replace or silently reimplement that analysis.

## Primary decision metric

For a matched pair,

`d = Delta V_nr,direct - Delta V_nr,reciprocity`.

All three quantities have units of mV. The dimensional check is therefore mV - mV = mV.

Status is:

- `PASS` if all required provenance/configuration/QC fields are complete and `|d| <= 20 mV`;
- `FAIL` if the complete pair has `|d| > 20 mV` or an invalid uncertainty/correlation input;
- `INCOMPLETE` if required data/provenance/configuration information is missing.

The sign convention is explicit: positive `d` means the direct path reports larger nonradiative voltage loss.

## Uncertainty diagnostic

For standard uncertainties `u_d`, `u_r` and declared correlation coefficient `rho`,

`u_pair = sqrt(u_d^2 + u_r^2 - 2 rho u_d u_r)`.

Here `u_d`, `u_r`, and `u_pair` are in mV and `rho` is dimensionless. The term under the square root has units mV^2.

The implementation independently recomputes the same quantity through `Var(X-Y)=Var(X)+Var(Y)-2Cov(X,Y)` with `Cov=rho*u_d*u_r`; squared agreement tolerance is `1e-12 mV^2` for software verification.

Required sensitivity values are reported for `rho = -0.5, 0, +0.5`. This sensitivity is diagnostic only: uncertainty does **not** relax the inherited 20 mV screen. Correlation structure must not be inferred from repeated pixels or sessions as though they were independent samples.

## Limiting cases

Executable self-tests freeze:

- equal values -> `d=0`, PASS;
- exactly +20 mV -> PASS;
- +20.000001 mV -> FAIL;
- exactly -20 mV -> PASS;
- `u=(3,4) mV`, `rho=0` -> `u_pair=5 mV`;
- equal 5 mV uncertainties with `rho=+1` -> zero difference uncertainty for the perfectly shared component;
- equal 5 mV uncertainties with `rho=-1` -> 10 mV.

These are arithmetic/software fixtures, not experimental R2 observations.

## Conventional explanations and discriminator

A disagreement can arise from spectral truncation, weak-tail bias, absolute radiometric calibration, temperature mismatch, injection/state filling, background subtraction, or analysis-version mismatch. Conversely, agreement can be spuriously strong when both paths share a common calibration systematic.

The discriminator is complete independent provenance plus explicit shared-systematic accounting; prospective agreement must survive frozen configuration and raw-data review rather than only matching final scalar values.

## Statistical hierarchy and exclusions

Fabrication inference remains `lot -> substrate -> device/pixel -> session -> measurement`. A paired pixel is one metrology concordance observation; repeated pixels or repeated sessions do not increase independent substrate N.

Predefined exclusions are identity/provenance mismatch, missing paired value/raw reference, frozen configuration mismatch, or unsafe/damaged sample state invalidating acquisition. Large or unfavorable disagreement is never an exclusion criterion.

## Validity regime and kill/narrow rule

The screen applies only to matched R2/AT-04 measurements under declared comparable conditions. If the 20 mV agreement gate fails, mechanism-facing interpretation should pause until calibration, temperature, injection, spectral-range, background, and analysis-provenance causes are diagnosed. If it passes, the conclusion is narrowly limited to metrology-path concordance under that configuration.

## Reproduction

Run:

`python models/r2_reciprocity_concordance_v3_37.py --self-test`

Then populate `technical/data/r2_reciprocity_concordance_raw_template_v3_37.csv` with real paired observations; blank/unknown fields remain `INCOMPLETE` rather than being imputed.
