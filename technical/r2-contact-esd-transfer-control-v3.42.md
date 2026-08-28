# R2 contact-state and ESD transfer control — v3.42

## Purpose and claim boundary

**Claim class:** engineering protocol / falsifiable conventional-confound discriminator.

R2 transfer work already treats remounting, contact changes, particles, shipping, and ESD/EOS as plausible ordinary explanations for apparent cross-session or cross-facility changes. This increment makes one part of that problem executable: every transfer campaign can preserve a matched PRE/POST low-stress dark-I–V fingerprint plus an ESD-sentinel record, without treating either as mechanism evidence.

A PASS under this protocol means only that the tested device/contact state stayed inside prospectively declared electrical-state limits and no declared sentinel/QC failure occurred. It does **not** establish facility equivalence, device lifetime, shipping qualification, ESD immunity, or any quantum mechanism.

## Why this is high value

A facility-transfer disagreement can be produced by ordinary terminal/contact effects: changed probe pressure, shifted pad registration, contamination, oxide/interfacial change, fixture compliance, damage, or ESD/EOS. Conversely, agreement after transfer can be falsely reassuring if no electrical-state fingerprint was preserved. The discriminator is therefore intentionally orthogonal to the primary weak-EL observable.

## Required hierarchy and independence

Preserve `lot -> substrate -> device/pixel -> session -> measurement`.

The independent experimental unit remains the **substrate**. Voltage points within one dark-I–V sweep and repeat sweeps inside one session are correlated technical observations. They do not create extra substrate-level sample size.

## Prospective configuration freeze

Before qualified primaries are measured, freeze and record:

- exact voltage grid;
- current compliance;
- settling time;
- integration/aperture/filter settings relevant to the electrical measurement;
- temperature target and tolerance;
- fixture and instrument IDs;
- pad/probe orientation and contact procedure;
- raw-data path and analysis commit;
- PRE/POST acceptance thresholds with provenance;
- sentinel technology/type, placement, calibration/lot, and interpretation rule.

The machine contract intentionally leaves the probe conditions and pass thresholds `null`. Missing limits/configuration produce `INCOMPLETE`, not a fabricated PASS.

## Governing calculations

At matched voltage point `V_k`, define

`delta_I_k = I_POST(V_k) - I_PRE(V_k)`.

Units: ampere. Sign convention is POST minus PRE.

With standard uncertainties `u_pre,k`, `u_post,k` and PRE/POST correlation `rho_k`,

`u_delta,k = sqrt(u_pre,k^2 + u_post,k^2 - 2 rho_k u_pre,k u_post,k)`.

Units remain ampere because every term under the square root is A².

If correlation is unknown, the decision calculation uses `rho=-1`, giving the conservative limiting case

`u_delta = u_pre + u_post`.

This protects against claiming excessive precision. When `rho=+1` and the same systematic uncertainty appears equally in PRE and POST, the shared systematic can cancel in the difference; that cancellation may be used only with documented covariance provenance.

Two descriptive paired metrics are frozen:

`RMS_shift = sqrt(mean(delta_I_k^2))` [A]

and

`Z_max = max_k |delta_I_k| / u_delta,k` [dimensionless].

Neither metric has a universal acceptance threshold in v3.42. A threshold must be prospectively declared with a defensible instrument/device/configuration basis before a PASS is possible.

## Synthetic software fixture

The committed fixture is synthetic and exists only to verify arithmetic:

- voltage grid: -0.1, 0, +0.1 V;
- `I_pre = [1, 0, 4] nA`;
- `I_post = [1, 2, 3] nA`;
- all `u_pre = u_post = 0.5 nA`;
- `rho=0`.

Therefore `delta_I = [0, 2, -1] nA` and

`RMS_shift = sqrt((0² + 2² + (-1)²)/3) nA = sqrt(5/3) nA = 1.2909944487358057 nA`.

For each point,

`u_delta = sqrt(0.5² + 0.5²) nA = 0.7071067811865476 nA`,

so

`Z_max = 2 / 0.7071067811865476 = 2.8284271247461903`.

These numbers are not device performance and must never be quoted as measured R2 behavior.

## Independent checks and limiting cases

The executable validator checks the primary covariance equation. Independent/limiting checks are:

1. `rho=-1`: `Var(POST-PRE)=(u_pre+u_post)^2`, therefore `u_delta=u_pre+u_post` for positive standard uncertainties.
2. `rho=+1` with equal shared systematic terms: `u_delta=0` for that perfectly common component.
3. identical PRE and POST currents: `RMS_shift=0` and `Z_max=0` exactly.
4. missing thresholds/configuration: status cannot become PASS.

The numerical software tolerance is `1e-12` for dimensionless fixture comparisons, with scale-aware use for the ampere-valued synthetic RMS quantity. There is no stochastic seed because the validator is deterministic and uses only the Python standard library.

## ESD sentinel interpretation

A sentinel is required as a transfer record, but v3.42 deliberately does not invent an ESD threshold or assume the sentinel measures the electric stress at the DUT. Required provenance includes sentinel ID/type, calibration or lot, placement, PRE/POST state, response/interpretation rule, and raw record path.

A changed sentinel may support the ordinary explanation that the package experienced an electrical event. An unchanged sentinel cannot prove no damaging DUT-local event occurred unless the sentinel response function, placement, and coupling are shown applicable. Missing response provenance is `INCOMPLETE`.

## Status logic

- **PASS:** complete PRE/POST matched data; frozen configuration matches; raw paths/provenance/uncertainty/sentinel record complete; every prospectively declared electrical-state limit is satisfied; no visual/electrical/sentinel QC failure.
- **FAIL:** complete interpretable data and any declared limit is exceeded, or a frozen sentinel/visual/electrical rule declares failure.
- **INCOMPLETE:** missing pair, mismatched configuration, missing raw/provenance/uncertainty, missing sentinel record, or absent acceptance limits.
- **BLOCKED:** an upstream transfer-fixture/metrology gate makes the measurement uninterpretable.

## Predefined exclusions

Allowed exclusions are restricted to prospectively frozen instrument overrange/compliance rules or devices already declared nonfunctional before PRE by an existing frozen QC rule. A large POST shift is not an exclusion reason. Every functional sample remains reportable.

## Sensitivity and uncertainty

The most influential interpretation inputs are the PRE/POST covariance assumption, measurement uncertainty, probe condition, temperature, contact geometry, and acceptance threshold. The decision can change when any of these change; therefore a threshold or covariance model is configuration-specific rather than universal.

The conservative `rho=-1` default increases `u_delta` relative to independent (`rho=0`) terms. This makes standardized shifts smaller, so `Z_max` alone is not permitted to hide a physically large RMS current change. Both the ampere-valued shift and standardized diagnostic are retained, and pass limits must be prospectively frozen.

## Conventional/null explanations and discriminator

Principal conventional explanation: an apparent transfer/facility change in weak EL or `Delta V_nr` is caused by contact/electrical-state alteration rather than metrology or device physics of interest.

Discriminator: matched PRE/POST electrical-state fingerprints under the same frozen configuration plus independent handling/sentinel records. If the dark-I–V state changes materially, mechanism-facing transfer interpretation is narrowed or blocked until contact/handling causes are resolved. If it does not, contact-state change is bounded only to the sensitivity of the frozen electrical test; it is not eliminated universally.

## Safety / EHS

The protocol does not prescribe deliberate ESD stress to qualified R2 primaries. Any intentional ESD/EOS qualification belongs on suitable dummies/sentinels under an approved laboratory procedure. Current compliance and probe conditions must be frozen from device/instrument safety evidence before primary execution.

## Files

- `machine/r2-contact-esd-control-v3.42.json`
- `technical/data/r2_contact_esd_control_template_v3.42.csv`
- `tools/check_r2_contact_esd_control_v3_42.py`
- `.github/workflows/r2-contact-esd-control.yml`

## Kill / narrow gate

Do not pool or interpret a transferred R2 primary as clean cross-session/cross-facility evidence when v3.42 returns FAIL or INCOMPLETE for a contact/ESD reason. Preserve the negative result and diagnose fixture, contact, sentinel, temperature, ageing, and instrument alternatives before repeating mechanism-facing acquisition.
