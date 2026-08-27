# R2 transfer environmental-exposure ledger v3.38

## Purpose and claim class

**Engineering protocol / falsifiable conventional-confound control.** This increment does not report an experiment and does not establish a safe shipping envelope. It makes transport exposure observable so temperature, humidity, shock, timing gaps, package identity, and logger provenance cannot silently disappear from HOME/TRAVEL or A→B→A interpretation.

Principal conventional explanation addressed: an apparent cross-facility ΔVnr shift may be caused by device state change during handling/transport rather than a facility-dependent measurement offset. The discriminator is a complete exposure record paired with the randomized HOME/TRAVEL state-change control and the A→B→A measurement sequence.

## Required inputs

Each sample row records UTC timestamp, temperature `T` [degC], relative humidity `RH` [%RH], acceleration magnitude `a` [g], standard/expanded instrument uncertainty as supplied by the logger record (`u_T`, `u_RH`, `u_a` in matching units), and immutable transfer/substrate/logger/carrier/package identifiers. Logger model, calibration reference/date and timebase are required provenance.

The contract freezes a provisional maximum sample-gap screen of 900 s. **900 s is a synthetic planning assumption, not a device-safety, reliability, or standards-derived limit.** It is intended only to reject materially incomplete transport records until the chosen logger/process supports a justified interval.

Temperature, RH and acceleration acceptance limits are deliberately `null` by default. Missing limits mean `LIMITS_UNKNOWN`; they are never interpreted as zero and cannot yield a materials/shipping PASS.

## Governing calculations

For consecutive UTC samples at times `t_i`, define

`g_i = t_(i+1) - t_i` [s]

and

`g_max = max_i(g_i)` [s].

The exposure log is timing-complete only if every `g_i <= g_limit`, equivalently `g_max <= g_limit`. The executable checks both forms independently and requires agreement.

For an upper engineering limit `L_x` on a measured channel `x`, the conservative screening value is

`x_upper = max_i(x_i + u_i)`

and the limit passes only when `x_upper <= L_x`.

For a lower temperature limit `L_T,low`,

`T_lower = min_i(T_i - u_T,i)`

and the limit passes only when `T_lower >= L_T,low`.

Units remain those of the measured quantity because addition/subtraction combines like dimensions. UTC differences produce seconds. No conversion from acceleration in `g` to m/s² is needed for a declared `g`-based packaging limit; if a future limit is expressed in SI acceleration the converter must be explicit.

## Sign, limiting-case and uncertainty checks

- Zero uncertainty reduces conservative extrema to observed extrema.
- Increasing positive uncertainty can only make an upper-limit screen harder to pass and a lower-limit screen harder to pass.
- Exactly 900 s is accepted; any larger gap is incomplete under the frozen planning screen.
- A missing engineering limit yields `LIMITS_UNKNOWN`, never implicit acceptance.
- A sample timestamp without timezone is rejected; all comparisons are normalized to UTC.
- Measurements before/after the declared transfer window may bracket it, but the first sample must be at or before transfer start and the last at or after transfer end.

Instrument uncertainty is treated conservatively row-by-row for threshold screening. This is not a full stochastic propagation model and does not model correlated calibration error, logger response time, unobserved short-duration shocks between samples, package thermal lag, or device-local microclimate. Those remain explicit systematic risks.

## Statistical independence

Exposure rows are time-series observations from one transfer, **not independent devices**. Multiple logger samples do not increase substrate-level N. The experimental hierarchy remains lot → substrate → device/pixel → session → measurement, with transfer exposure as linked provenance for the substrate/transfer event.

## Status semantics

- `LOG_COMPLETE`: provenance and required channels are present, time coverage brackets the declared transfer, and no gap exceeds the planning completeness screen.
- `INCOMPLETE`: provenance/data/timing defect; preserve the data but do not use it to dismiss transport as a confound.
- `WITHIN_DECLARED_LIMITS`: every non-null declared engineering limit passes after conservative uncertainty expansion, and all four expected limits were supplied.
- `EXCEEDS_DECLARED_LIMIT`: at least one supplied limit fails.
- `LIMITS_UNKNOWN`: at least one required environmental acceptance limit is absent. This is the default until material/package-specific limits have provenance.

A log status and a limit status answer different questions. Neither proves electrical stability, facility equivalence, shipping certification, or any quantum mechanism.

## Machine artifacts

- contract: `machine/r2-transfer-environment-v3.38.json`
- raw template: `data/templates/r2-transfer-environment-v3.38.csv`
- validator/self-test: `models/r2_transfer_environment_v3_38.py`

Run:

```bash
python models/r2_transfer_environment_v3_38.py --self-test
python models/r2_transfer_environment_v3_38.py \
  --contract machine/r2-transfer-environment-v3.38.json \
  --csv path/to/real-transfer.csv
```

## Kill / narrow gate

If transport exposure is incomplete or exceeds a documented relevant limit, do not attribute a subsequent device shift solely to facility metrology. Diagnose transport/handling first or narrow the claim to “facility-plus-transfer path.” If exposure is complete and within justified limits but the HOME/TRAVEL control still shows a material state change, the environmental ledger has not eliminated handling/remounting/contact or other unmeasured transport effects; those remain live conventional explanations.
