# R2 v3.40 — transfer-sensor placement representativeness qualification

## Status and claim class

**Engineering protocol with synthetic software fixtures. Not an experimental result.**

v3.39 qualifies temporal fidelity of a dummy-package logger. v3.40 addresses a different failure mode: even a fast logger can be placed where it does not represent the temperature or humidity experienced by the dummy/device location. This protocol bounds package-to-device-location disagreement before qualified R2 primaries travel.

Passing v3.40 does **not** establish shipping safety, device stability, facility equivalence, electrical stability, or an open-quantum mechanism.

## Measurement design

Use a dimensionally representative dummy in the intended carrier/package. Place the candidate transfer logger in its intended shipping location and a calibrated reference sensor as close as practicable to the dummy/device plane without materially changing airflow or thermal mass. Record placement drawings/photos or dimensional descriptions, calibration identifiers, carrier/package IDs, timestamps, and deviations.

For both temperature and RH, execute at least 3 independent controlled runs in each transient direction (`UP`, `DOWN`). Samples within one transient are correlated technical observations and do not increase independent-run count.

The reference and logger records must be paired within the already-qualified v3.39 sampling gap. v3.40 does not create a looser timing rule.

## Governing model

At paired observation `i`,

`e_i = y_ref,i - y_logger,i`,

where `y` is temperature [degC] or relative humidity [%RH]. The difference has the same unit as the channel.

If standard uncertainties are `u_ref,i` and `u_logger,i` with correlation coefficient `rho_i`, then

`u_e,i = sqrt(u_ref,i^2 + u_logger,i^2 - 2 rho_i u_ref,i u_logger,i)`.

Dimensional check: every term inside the square root has squared channel units, so `u_e` has the channel unit. `rho` is dimensionless.

For the decision screen, define

`E_channel = max_i ( |e_i| + u_e,i )`.

A channel passes only if a **prospectively declared** representativeness threshold `epsilon_channel` exists with provenance and

`E_channel <= epsilon_channel`.

No default temperature/RH representativeness limit is supplied. Missing thresholds yield `INCOMPLETE`, not an implicit pass.

## Correlation/systematic treatment

If `rho_i` is not justified, the gate evaluates `rho=-1`, which gives the largest possible standard uncertainty for nonnegative component uncertainties:

`u_e = u_ref + u_logger`.

This is conservative for a difference observable. Sensitivity must be shown at `rho={-1,0,+1}` where meaningful. Common calibration components should be represented explicitly rather than silently counted twice.

Known limiting cases:

- equal `u_ref=u_logger=0.1` with `rho=-1` gives `u_e=0.2`;
- equal uncertainties with `rho=+1` give `u_e=0`, the perfect common-mode limit;
- increasing positive correlation cannot increase uncertainty of the difference when component uncertainties are fixed and nonnegative.

## Synthetic software fixtures

These values test arithmetic only; they are not device, facility, logger, or shipping performance.

With a synthetic prospectively declared 1.0 degC representativeness threshold, `|e|max=0.6 degC`, `u_ref=u_logger=0.1 degC`, and undeclared correlation (therefore `rho=-1`),

`E = 0.6 + 0.1 + 0.1 = 0.8 degC`,

which passes the synthetic threshold.

Changing only `|e|max` to 0.9 degC gives

`E = 0.9 + 0.1 + 0.1 = 1.1 degC`,

which fails. The 1.0 degC threshold is a software fixture only and must not be reused as a physical shipping criterion without separate provenance.

Predeclared numerical tolerance for exact synthetic arithmetic: `1e-12` in channel units.

## Status logic

- `QUALIFIED_FOR_DECLARED_REPRESENTATIVENESS`: required provenance, pairing, independence, uncertainty declarations, and both channel gates pass.
- `FAIL_REPRESENTATIVENESS`: complete evidence exists and at least one channel exceeds its prospectively declared threshold.
- `INCOMPLETE`: thresholds, calibration/placement provenance, uncertainty, run independence, timing qualification, or required data are missing.

All functional runs are reported unless a frozen QC rule excludes them. Exclusions and reasons remain in the raw record.

## Conventional explanations / adversarial cases

A logger/reference disagreement can arise from ordinary package physics rather than an instrumentation defect: airflow shielding, package thermal mass, chamber spatial gradients, sensor self-heating/contact, multi-time-constant response, time-alignment error, calibration drift, or the reference sensor itself perturbing the package. These explanations remain live.

The discriminator is repeated bidirectional controlled testing with frozen geometry, calibration traceability, v3.39 timing qualification, residual inspection, and placement sensitivity where disagreement appears.

## Kill/narrow gates

Do not treat transfer exposure records as representative of the R2 device location if:

- a required channel lacks a prospectively declared threshold and provenance;
- reference/logger pairing exceeds the v3.39 qualified gap;
- either calibration or placement identity is missing;
- fewer than 3 independent runs exist in either transient direction for a channel;
- conservative `E_channel` exceeds the declared threshold;
- geometry changes between qualification and transfer without requalification;
- residual structure indicates that one scalar bound hides a material placement- or direction-dependent effect.

## Practical next use

Run v3.40 on the same dummy/carrier/package/logger configuration qualified under v3.39. If it passes under justified project requirements, the environmental ledger can state that logger readings are bounded proxies for the tested dummy/device location. If it fails, modify sensor placement/package geometry or carry a device-adjacent sensor; do not reinterpret the failed gradient as harmless without evidence.
