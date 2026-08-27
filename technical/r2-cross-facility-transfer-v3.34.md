# R2 cross-facility ABA transfer screening — v3.34

## Scope and claim class

This is an **engineering protocol** for screening whether the R2 weak-EL transfer standard can be measured at a second facility without an obvious facility-dependent shift larger than the current project transfer/repeatability scale. It is not a statistical-equivalence certification, not a device-performance result, and not evidence for EPC or an open-quantum mechanism.

## Why A → B → A

A one-way A→B transfer confounds facility offset with irreversible device drift, shipping/handling change, and elapsed-time ageing. v3.34 therefore requires the same qualified primary device to be measured at home facility A, then facility B, then returned to A.

For device `d`:

- `A1_d`: home-facility ΔVnr before transfer [mV];
- `B_d`: second-facility ΔVnr [mV];
- `A2_d`: home-facility ΔVnr after return [mV];
- `t1_d < tB_d < t2_d`: elapsed acquisition times [h].

The interpolation weight is

`w_d = (tB_d - t1_d)/(t2_d - t1_d)`.

The home-facility reference at the B measurement time is

`A_interp,d = (1-w_d) A1_d + w_d A2_d`.

The facility residual is

`r_d = B_d - A_interp,d`.

All voltage-loss terms are mV; `w` is dimensionless, so `r` is mV.

Aggregate descriptive quantities are

`bias = mean_d(r_d)`

and

`RMS = sqrt(mean_d(r_d^2))`.

## Frozen engineering screen

A complete packet requires at least **three qualified primary devices**, each with one PASS A1/B/A2 record, blinded device identity, acquisition timestamps, frozen configuration identifiers, and raw/minimally processed evidence retained.

v3.34 uses a **5 mV** project engineering screen for both `|bias|` and `RMS`. This value is intentionally tied to the existing R2 ~5 mV transfer/repeatability scale but is a new screening assumption, not a standards-derived equivalence margin and not a publication-grade confidence bound.

- `PASS`: >=3 complete qualified devices, valid time/facility identities, `|bias| <= 5 mV`, and `RMS <= 5 mV`.
- `FAIL`: complete packet but either aggregate screen fails, time ordering is invalid, facility identity conflicts, or frozen configuration is violated.
- `INCOMPLETE`: missing A1/B/A2 evidence, provenance, timing, configuration, or fewer than three complete qualified primary devices.

A failed transfer is retained as a negative result. The 5 mV screen must not be widened after B data are seen.

## Independent and limiting-case checks

The executable `models/r2_cross_facility_transfer_v3_34.py` freezes an algebraically independent midpoint check: when `tB` is exactly halfway between A1 and A2,

`r = B - (A1 + A2)/2`.

It also freezes the physically useful linear-drift limiting case: A1=100 mV, A2=110 mV, midpoint B=105 mV gives `r=0`. Thus a purely linear home-facility drift need not be mistaken for a facility shift.

Adversarial synthetic/software cases require:

- 3 mV facility shift -> PASS;
- 7 mV shift -> FAIL;
- exactly 5 mV -> PASS;
- 5.000001 mV -> FAIL;
- only two complete devices -> INCOMPLETE;
- B acquired outside the A1/A2 time interval -> FAIL.

These are deterministic software tests, not measurements.

## Uncertainty and sensitivity

v3.34 intentionally does not claim a calibrated inferential confidence interval from three devices. The aggregate bias and RMS are descriptive engineering screens. Device-level measurement uncertainty must still be carried by the upstream AT-04/R2 analysis; correlated calibration/systematic terms must not be divided by `sqrt(N)` merely because multiple devices are present.

Sensitivity is exact at the engineering boundary: changing a common residual offset from 5.000000 to 5.000001 mV flips PASS to FAIL. The scientific conclusion is therefore conditional on the chosen 5 mV engineering screen until real transfer data justify a stronger statistical design.

## Statistical hierarchy

The independent unit for this first transfer screen is the **qualified device**, not the A1/B/A2 session. Repeated acquisitions on one device are correlated. The hierarchy is

`lot -> substrate -> device/pixel -> facility -> session -> measurement`.

The three-leg sequence does not triple N.

## Conventional/null explanations

A nonzero `r_d` can arise from ordinary calibration offset, source-spectrum mismatch, instrument temporal response, remounting/contact geometry, shipping shock, temperature history, encapsulation degradation, or nonlinear device ageing. It is not mechanism evidence.

The A-return leg discriminates only the linear component of home-facility drift. Nonlinear drift or a transfer-induced state change can still mimic facility bias. If A1→A2 drift is large/nonlinear or device history is suspect, narrow the conclusion and add denser home-facility bracketing rather than forcing equivalence.

## Safety / handling

Transfer must follow device shipping, encapsulation, temperature, electrical/optical, and facility EHS constraints. The protocol does not authorize bypassing interlocks or handling rules. Any shipping excursion or damage remains visible provenance.

## Required artifacts

- raw/minimally processed A1/B/A2 records;
- immutable file hashes and analysis commit IDs;
- calibration/configuration records for both facilities;
- device blind-ID map held according to the preregistration plan;
- shipping/handling/deviation log;
- executable v3.34 output and human review.
