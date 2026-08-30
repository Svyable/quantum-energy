# Baseline stress capability v3.73

## Status

**Prospective protocol + synthetic software verification.** No A0/B0 stress measurement is claimed in this increment.

v3.72 defines the four-arm A0/A2/B0/B2 stress-tomography experiment. v3.73 inserts a deliberate baseline-only stage before A2/B2 unblinding so the experiment does not choose physical margins or sample counts from synthetic examples.

## Why baseline-only first

NIST distinguishes repeatability (same measurement conditions) from reproducibility (changed conditions) and recommends characterizing measurement repeatability, reproducibility and stability rather than using those words as vague labels. The ISOS OPV consensus similarly separates dark, thermal and light stress categories as research comparison procedures.

Therefore v3.73 asks a narrower question before treatment-arm inference:

> Can A0 and B0 be fabricated, stressed and remeasured with enough lot-level stability that a future A/B interaction has a defensible detection capability?

## Experimental hierarchy

Preserve:

`material lot -> fabrication lot -> substrate -> device/pixel -> stress block -> checkpoint -> measurement`

The primary statistical unit is the **independent fabrication-lot mean log retention**. Two substrates per arm/stress/lot are required as a minimum implementation check, but those substrates do not become independent fabrication lots. Repeated JV scans, spectra, pixels or time points remain technical repeats.

Minimum baseline design:

- A0 and B0 only;
- both T and L stress blocks;
- at least 3 independent fabrication lots per A0/B0 x T/L cell;
- 5 lots preferred for the first stable capability estimate;
- at least 2 substrate summaries per lot/arm/stress;
- identical lot IDs represented in all four cells so common fabrication history can be inspected.

## Required controls before electrical interpretation

Every analyzed substrate summary must have:

- positive before/after primary metric values;
- completed intensity/temperature/electrical calibration metadata;
- matched declared stress history;
- optical control pass;
- contact/transport control pass;
- for A0, donor-free film-integrity qualification.

Any missing/failing item returns `INCOMPLETE` rather than silently excluding the row.

## Primary metric and transform

Primary capability metric: stabilized `Pmax`.

For positive metric `M`, substrate log retention is

`y_i = ln(M_after/M_before)`.

For each fabrication lot, arm and stress:

`ybar_l = mean_i(y_i)`.

For each A0/B0 x T/L cell, report:

- number of independent fabrication lots;
- mean lot log retention;
- geometric mean retention `exp(mean(ybar_l))`;
- sample SD of independent lot means.

Define a conservative baseline dispersion proxy

`s_base = max(s_A0,T, s_B0,T, s_A0,L, s_B0,L)`.

This does not claim the treatment arms A2/B2 have the same variance.

## Planning detection-capability frontier

For the future four-arm interaction, a transparent sensitivity scenario assumes equal future lot count `n` per arm and treatment-arm lot-level SD no larger than `m*s_base` under a stated variance multiplier `m`.

With independent arm-level variance as the deliberately simple planning approximation,

`SE_proxy = 2*m*s_base/sqrt(n)`.

For two-sided alpha=0.05 and nominal power 0.80,

`MDE_log = (z_0.975 + z_0.80) * SE_proxy`.

Report also

`MDE_ratio = exp(MDE_log)-1`.

The committed frontier uses:

- `n = 3, 5, 7, 9, 12` lots per arm;
- `m = 1.0, 1.5, 2.0`.

### Critical interpretation boundary

This is **not** a guaranteed power calculation for the future treatment comparison because:

- A2/B2 variance is unknown;
- within-lot covariance among four arms is unknown;
- real stress and measurement errors may be correlated;
- A0 donor-free electrical execution may remain unavailable;
- the smallest scientifically useful effect has not yet been chosen.

The frontier answers: *what interaction size could this baseline process plausibly resolve under explicit variance scenarios?*

It does **not** answer: *what interaction size would count as a physical success?*

## Baseline common-history diagnostics

Within each stress, compute the per-lot baseline difference

`D_S,l = y_B0,S,l - y_A0,S,l`.

Also compute the baseline stress-selectivity difference

`Omega0_l = D_T,l - D_L,l`.

These values reveal how much A0/B0 differ before PY-IT is introduced. They are characterization outputs, not a treatment effect.

## Stress-history discipline

### T — dark thermal
The v3.72 planning condition remains 85 C, dark, inert atmosphere. Record actual device/sample temperature history, chamber location, atmosphere, duration and any excursions. Do not convert thermal exposure time into field lifetime without a validated acceleration model.

### L — operational light
Record irradiance, spectrum/UV content, device temperature, MPP algorithm, MPP history, duration and J-V checkpoint procedure. A nominal `1 sun` label is insufficient without the actual measurement record.

ISOS provides a comparison framework; it is not IEC qualification.

## Synthetic fixture

The committed 5-lot fixture is **software verification only**. Its lot-level log-retention SDs are intentionally nonzero. The expected maximum baseline SD is approximately

`s_base = 0.0191624633`.

Under the `m=1`, `n=5` planning scenario, the model yields approximately

- `MDE_log = 0.0480175688`;
- `MDE_ratio = 0.0491890881` (~4.9% ratio-of-ratios departure).

Those numbers are not D18/PY-IT/eC9 thresholds and cannot be copied into a preregistration as physical acceptance criteria.

## Physical threshold freeze rule

Before A2/B2 unblinding, freeze:

1. the useful-work-relevant physical effect margin for `Psi_T`, `Psi_L` and/or `Omega`;
2. required lot count based on measured A0/B0 capability and explicit treatment-variance sensitivity;
3. stress duration/checkpoints;
4. exclusions/QC;
5. optical/contact drift limits based on qualified measurement capability;
6. field-generation metric and its uncertainty.

If the useful physical effect is smaller than the process can resolve with a feasible lot count, **do not unblind treatment arms**; improve the process or abandon that inference target.

## Strong nulls retained

A narrow baseline SD does not establish mechanism redundancy. Future apparent protection may still be explained by:

- PY-IT suppression of eC9 diffusion/crystallization;
- contact/transport stabilization;
- optical/thickness stability;
- generic stress resistance affecting both routes;
- donor-free architecture artifacts;
- normalized retention improvement without absolute Pmax advantage.

## Reproduction

```bash
python models/baseline_stress_capability_v373.py \
  models/baseline_stress_capability_fixture_v373.csv \
  --output-json /tmp/v373.json
```

Expected synthetic status:

`BASELINE_CAPABILITY_ESTIMATED`

Expected physical result:

`NONE_BASELINE_CAPABILITY_ONLY`.
