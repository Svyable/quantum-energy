# D18/PY-IT/eC9 stabilized useful-work protocol v3.47

## Changed evidentiary state

**Claim class:** prospective experiment/protocol. This increment makes the canonical `>=5%` relative stabilized-Pmax improvement across `>=3` independent lots executable and fail-closed. It is not an experimental result and does not assert that B1 or B2 improves power.

The protocol is intentionally downstream of voltage-loss and field-generation work. A lower `DeltaVnr` cannot earn a useful-work PASS unless stabilized electrical output also passes, and an arm that fails the field-generation discriminator cannot be rescued by a favorable snapshot J-V curve.

## Experimental unit and pairing

The independent unit is the **fabrication lot**. Within each qualified lot, B0 and the candidate arm must be fabricated and measured under the same prospectively frozen measurement configuration. Devices/sweeps within a lot are technical observations and do not increase `N_lot`.

All functional devices are reported unless a preregistered QC rule excludes them. Exclusions are frozen before arm unblinding.

## Governing quantities

For lot `l`, with stabilized maximum-power outputs `P_arm,l` and `P_B0,l`:

`g_l = P_arm,l / P_B0,l - 1`.

`g_l` is dimensionless. Positive values mean the candidate arm produces more stabilized power than its contemporaneous B0 control.

With non-negative absolute standard/engineering uncertainties `u_arm,l` and `u_B0,l`, a deliberately conservative interval diagnostic is

`g_l,low = (P_arm,l - u_arm,l)/(P_B0,l + u_B0,l) - 1`.

This is not a confidence interval unless the input uncertainties are themselves defined to support that interpretation. It is an uncertainty-robust engineering bound.

The lot-level summaries are

`g_bar = (1/N) sum_l g_l`

and

`g_bar_low = (1/N) sum_l g_l,low`.

## Prospective useful-work gate

The inherited project target is operationalized as PASS only when all are true:

1. at least three independent qualified fabrication lots;
2. every nominal lot-level gain is positive;
3. `g_bar >= 0.05`;
4. `g_bar_low >= 0.05`, so plausible measurement uncertainty does not overturn the inherited 5% target;
5. each `Pmax` value comes from a prospectively frozen stabilized-MPP procedure, not a favorable scan point;
6. irradiance, temperature, active-area definition, contact configuration, tracking algorithm/duration and stabilization criterion are matched or explicitly corrected with provenance;
7. the same arm does not fail the prospectively frozen field-generation discriminator;
8. no post-unblinding exclusion is introduced.

The `5%` and `>=3 lot` values are not new thresholds: they are inherited from `technical/current-specification.md` and `venture/business-plan.md` on run-base main SHA `9e61f8d761cc30b5ba12eef36c9935c35591c8f5`.

## Stabilization requirement

A lab executing this protocol must freeze its MPP-tracking method before unblinding and preserve the full time series. The project does **not** invent a universal tracking duration or derivative threshold here. Those settings must come from instrument capability and B0 baseline behavior. Snapshot or scan-only Pmax is supporting data, not the primary useful-work endpoint.

The ISOS stability framework was originally developed for OPVs and explicitly distinguishes more advanced procedures using MPP trackers; the later photovoltaic stability consensus emphasizes consistent reporting and MPP tracking where appropriate (Khenkin et al., *Nature Energy* 5, 35–49, 2020, DOI `10.1038/s41560-019-0529-5`). This is procedural precedent, not D18/PY-IT/eC9 performance evidence.

## Calculation verification

Synthetic arithmetic fixture only:

- B0 = `[1.00, 1.02, 0.98]`
- arm = `[1.08, 1.09, 1.04]`
- absolute uncertainty on every value = `0.005`

The resulting lot gains are approximately `8.0000%`, `6.8627%`, and `6.1224%`; `g_bar = 6.9950646925%`. Conservative lower gains are approximately `6.9652%`, `5.8537%`, and `5.0761%`; `g_bar_low = 5.9649915993%`. The fixture therefore passes.

Independent numerical cross-check: the primary ratio implementation `P_arm/P_B0 - 1` is compared with `exp(log(P_arm)-log(P_B0))-1` at absolute tolerance `1e-12`. A 100x unit scaling must leave every relative result unchanged. Limiting case `P_arm=P_B0` gives zero gain. Negative fixture `[1.08,0.99,1.04]` against the same B0 fails the same-sign condition.

No stochastic seed is used. Standard-library Python is sufficient.

## Strong conventional explanations / failure modes

1. **Transient or scan artifact.** A favorable J-V scan or early MPP transient can overstate sustained useful work. The discriminator is preserved full MPP tracking with a frozen stabilization rule; scan-only evidence cannot pass.
2. **Temperature/irradiance/area/contact confounding.** Small differences can create apparent power gains. The discriminator is contemporaneous within-lot B0 pairing plus recorded irradiance, temperature, active area, contact configuration and uncertainties.
3. **Morphology/thickness ordinary optimization.** A genuine Pmax gain could arise from conventional morphology or thickness changes rather than the proposed EPC/interface pathway. Therefore this gate establishes useful electrical work only; mechanism attribution still requires the independent interface/EPC, field-generation, morphology and contact evidence.

## Falsification and claim narrowing

A candidate is **falsified for the current useful-work stage gate** if the inherited 5%/3-lot stabilized-Pmax rule is not met robustly. If `DeltaVnr` improves but stabilized Pmax fails, retain the result as voltage-loss/mechanism science rather than platform validation.

## Reproduction

Run:

`python3 models/d18_pyit_ec9_stabilized_pmax_v347.py --self-test`

Expected terminal marker: `PASS_SYNTHETIC_FIXTURE`.

Real execution requires populating `data/templates/d18-pyit-ec9-stabilized-pmax-v3.47.csv` with raw-trace references and a frozen analysis commit before unblinding.
