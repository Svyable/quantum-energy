# D18:eC9 B0 field-generation baseline protocol v3.59

## Changed evidentiary state

**Claim class: prospective experiment/protocol.** The program now has a frozen, machine-checkable B0-only acquisition/analysis plan for field-dependent charge generation before any B1/B2 useful-work claim. This does **not** add experimental evidence and does **not** freeze a physical noninferiority margin. The next gate must be learned from real B0 repeatability and instrument capability, not from synthetic or cross-material values.

## Scope and rationale

Current `main` requires field-dependent generation evidence before a strong D18/PY-IT/eC9 useful-work claim. Repeated literature/model work has already established that field dependence can matter in OSCs; further retrospective polishing is lower value than a prospective physical falsifier. Open PR #51 covers a manufacturing-scale evidence boundary, so this increment does not duplicate that lane.

Material: **B0 = D18:eC9** only.

Primary observable: **TDCF** free-charge extraction versus prebias.

Orthogonal observable: **bias-dependent PL** on the same device when practical, otherwise a preregistered sibling device on the same substrate with identity retained.

No B1/B2 sample is unblinded or interpreted in this increment.

## Frozen bias coordinate

For each device measure `V_OC` under the same illumination/temperature condition used for the field-generation sequence, then define

`u = (V_OC - V_pre) / V_OC`.

Frozen sampling grid:

`u = 0, 0.25, 0.50, 0.75, 1.00`.

Thus `u=0` is prebias at measured `V_OC`; `u=1` is prebias at `0 V`. This is an **engineering sampling design**, not a physical acceptance threshold. Actual instrument pulse timing, delay, extraction field, optical fluence, repetition rate, temperature, illumination spectrum/intensity and settling criteria must be recorded in the raw run manifest before data are interpreted; this packet does not invent unavailable instrument settings.

## Hierarchy and independence

Preserve:

`lot -> substrate -> device -> session -> measurement`.

Repeated pulses, spectra, or voltage points are technical repeats, not independent fabrication replicates. No hero-device selection is allowed. Report every functional device unless a predeclared QC condition excludes it, and record the exclusion reason.

For a baseline intended to freeze a later B1/B2 gate, use data spanning the same independent-lot regime as the eventual useful-work claim. If fewer lots are available, the result is explicitly pilot-only and cannot define a confirmatory cross-lot margin.

## Derived quantities

For each TDCF device/session:

`R_TDCF = Q(u=0) / Q(u=1)`

and

`G_TDCF = Q(u=1) / Q(u=0) - 1`.

`R_TDCF` is a descriptive operating-field retention metric over the `V_OC -> 0 V` prebias span. It is not assumed mechanism-pure because extraction, recombination, capacitance and pulse-history artifacts can affect TDCF.

For PL:

`P_norm(u) = PL(u) / PL(u=0)`.

The PL curve is an orthogonal discriminator only. It is **not** converted into a charge-generation yield without a separately justified physical model.

## Gate-freeze rule

Status is frozen as:

`DEFERRED_PENDING_REAL_B0_DATA`.

A B1/B2 physical noninferiority margin may only be frozen after all of the following exist:

1. provenance-complete B0 data;
2. instrument capability/noise characterized in the same sessions;
3. retained lot/substrate/device hierarchy;
4. empirical repeatability reported without treating technical repeats as independent;
5. the principal TDCF and PL artifact explanations below are assessed.

It is explicitly forbidden to derive the physical margin from v3.45/v3.55 synthetic or cross-material model values.

## Serious conventional explanations and discriminators

1. **TDCF apparent field dependence from extraction/recombination/capacitive artifacts rather than generation.** Bound by preserving pulse timing/extraction settings, checking signal linearity versus excitation fluence where feasible, repeating acquisition order in a counterbalanced sequence, and testing whether the extracted-charge trend is reproducible across independent devices/sessions.
2. **PL bias response from electroabsorption, heating, carrier injection/contact effects, or recombination changes rather than Ex->CT generation.** Bound by dark/injection controls where appropriate, temperature monitoring, spectral-shape inspection rather than intensity alone, and requiring qualitative consistency with the independently acquired TDCF response before mechanism language is used.

A disagreement between TDCF and PL is a result, not a reason to discard one technique post hoc.

## Falsification / narrowing logic

If repeated B0 TDCF is flat within measured baseline repeatability across `u` and bias-dependent PL shows no reproducible operating-field response, a **large B0 field-generation limitation is narrowed for the measured regime**. If reproducible field dependence is present, those B0 data become the empirical basis for the later B1/B2 noninferiority margin.

Neither outcome alone proves the microscopic EPC/interface mechanism.

## Machine-readable data contract

Required CSV columns, in exact order:

`lot_id,substrate_id,device_id,session_id,technique,u,signal,signal_unit,qc_status`

Allowed techniques: `TDCF`, `PL`.

Allowed QC statuses are defined in the JSON contract. Exclusions require a separate recorded reason in the run manifest; the analysis CSV omits no functional `PASS` row.

## Reproduction

Validate the protocol and synthetic logic fixtures:

```bash
python models/d18_b0_field_generation_baseline_v359.py
```

Analyze a completed B0 CSV:

```bash
python models/d18_b0_field_generation_baseline_v359.py --csv path/to/b0_field_generation.csv
```

Expected no-data output includes:

- `protocol_validation = PASS`
- `physical_gate = DEFERRED_PENDING_REAL_B0_DATA`

The executable includes: unitless limiting cases, an independent log-domain TDCF retention calculation, a sign-reversal control that is not clamped away, PL normalization limit, and rejection of non-positive endpoint signals.

Synthetic fixtures test software logic only and are not material constants, measured device properties, or evidence.

## Uncertainty and sensitivity

No physical measurement uncertainty is available before acquisition, so none is fabricated. The eventual analysis must separately report instrument/session systematic terms and device/substrate/lot variation. Physical acceptance must remain deferred if the observed decision changes inside those empirical uncertainty bounds.

The fixed `u` grid is a sampling choice. If instrument capability prevents one or more points, record the deviation before interpretation and do not silently redefine the metric.

## Safety / manufacturing relevance

This protocol does not alter fabrication chemistry. Existing D18/eC9 solvent, UV, vacuum, thermal, electrical and waste controls remain applicable. Bias/illumination sequences must stay within the device/instrument safety envelope defined by the executing laboratory; this repository does not invent equipment ratings.

## Explicit non-claims

- No B0 field dependence has been measured here.
- No B1/B2 arm is superior or noninferior.
- No physical pass threshold is frozen.
- No TDCF or PL response is uniquely attributed to EPC.
- No useful-work or manufacturing-scale claim is advanced.

## Single best next increment

Execute this B0 protocol with provenance-complete raw traces across the intended independent-lot regime, quantify empirical repeatability and artifact sensitivity, then freeze the B1/B2 field-generation noninferiority margin **before** unblinding those arms.
