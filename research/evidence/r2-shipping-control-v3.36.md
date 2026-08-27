# Evidence record — R2 shipping-control discriminator v3.36

Date: 2026-08-27

## Established/internal evidence used

- R2 is a metrology transfer standard whose cross-session/facility stability must be established before strong transfer claims.
- The merged v3.34 protocol uses A→B→A measurements to reduce linear home-facility time-drift aliasing.
- The merged v3.35 transfer carrier controls geometry/handling but has not yet established physical shipping stability.
- Repository verification rules require conventional explanations, statistical hierarchy, uncertainty, sensitivity, and prospective QC.

These statements are grounded in the reviewed repository `main` branch. No new external device-performance evidence is introduced.

## Engineering assumptions

- `5 mV` is used as a practical shipping-effect planning scale because the program already treats voltage-loss changes of that order as material for R2 transfer/fabrication precision. It is not a standards-derived shipping limit.
- A two-arm randomized TRAVEL/HOME difference-in-changes is an acceptable first discriminator for common elapsed ageing and home-facility drift.
- Normal equal-variance power calculations are acceptable for **synthetic planning only**; real data may require a different inferential model.

## Synthetic/model results

Frozen deterministic normal-approximation inputs: `delta=5 mV`, `sigma_change=3 mV`, two-sided `alpha=0.05`, target power `0.80`.

- Minimum equal arm size reaching the target under the nominal model: `n=6 substrates/arm`.
- Nominal power at `n=6`: `0.8229821534848882`.
- Power at `n=3`: `0.5324208639051091` — useful negative planning result.
- Sensitivity minimum `n/arm` for assumed `sigma_change = 2/3/4/5 mV`: `3/6/11/16`.

These are not experimental results and must not be used as measured R2 variability.

## Independent verification

The primary implementation evaluates the standard normal CDF through `math.erf` with frozen `z_0.975`. The independent implementation uses Python `statistics.NormalDist` for both the inverse CDF and CDF. Predeclared agreement tolerance: `1e-12` absolute power.

Estimator limiting cases are also frozen: identical arm changes produce zero effect; +5 mV travel versus 0 mV home produces +5 mV; swapping arms reverses sign.

## Conventional explanation preserved

Even perfect A→B→A metrology can be confounded if travel itself changes the DUT. Causes include handling, package shock, storage environment, remounting, contact change, encapsulation damage, and ordinary ageing. The TRAVEL/HOME randomized home-facility comparison is the discriminator proposed here.

## Unresolved evidence gaps

- no R2 substrate has yet been shipped under v3.35;
- real PRE/POST substrate-level SD is unknown;
- real distributions may be heteroscedastic or heavy-tailed;
- travel and home arms may experience different elapsed times or thermal histories;
- package shock/environment exposure is not yet quantitatively logged in this increment;
- the carrier material and physical fabrication tolerances remain to be qualified.

## Claim boundary

A v3.36 screen can identify or bound a shipping/handling confound under a specific configuration. It cannot by itself establish facility equivalence, device lifetime, commercial shipping robustness, EPC causality, or an open-quantum mechanism.
