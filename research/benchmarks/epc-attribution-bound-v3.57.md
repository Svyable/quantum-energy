# v3.57 EPC attribution bound

## Changed evidentiary state

**Claim class: literature-derived quantitative bound.** The anchor paper's own approximate decomposition does not support treating electron-phonon coupling (EPC) alone as accounting for the full reported non-radiative voltage-loss reduction in either representative comparison. This retires a possible over-strong causal shortcut; it does not dispute that EPC is important.

Primary source: Luo et al., *Nature Communications* 17 (2026), DOI `10.1038/s41467-026-68731-7`, version of record 2026-02-26. The paper reports total qDeltaVnr reductions of about 55 meV for the PA comparison and 38 meV for the SMA comparison, while its EPC-only analysis reports about 35 meV and 20 meV respectively. The same discussion also identifies energetic offset, outer reorganization energy and hybridization/electronic-coupling contributions, so an EPC-only causal story is not warranted.

## Calculation

For each system define

`f_EPC = DeltaVnr_EPC_only / DeltaVnr_total`

and the nominal non-EPC-only gap

`g = DeltaVnr_total - DeltaVnr_EPC_only`.

Results:

- PA / D18:PY-IT comparison: `35/55 = 0.63636`, or **63.64%**, with nominal gap **20 meV**.
- SMA / D18:eC9 comparison: `20/38 = 0.52632`, or **52.63%**, with nominal gap **18 meV**.

These ratios are arithmetic summaries of approximate paper values, not independently measured causal fractions. Coupled mechanisms need not add linearly.

## Sensitivity and uncertainty

The source prefixes these prose values with `~` and does not give uncertainty for these summary numbers. No physical uncertainty is invented here. Instead, a transparent adversarial sensitivity asks how large an equal-magnitude perturbation `epsilon`, applied in opposite directions (`total -> total-epsilon`, `EPC -> EPC+epsilon`), would be needed to erase the nominal gap. Algebraically `epsilon_star = g/2`.

- PA: `epsilon_star = 10 meV`.
- SMA: `epsilon_star = 9 meV`.

These are sensitivity distances only, not confidence intervals. Because source approximation uncertainty is not supplied, the exact physical causal fraction remains unresolved.

## Independent and negative checks

The executable computes each fraction in floating point and independently cross-checks with exact rational arithmetic at frozen absolute tolerance `1e-12`. A limiting fixture with EPC-only = total must return fraction 1 and zero gap. A negative fixture with EPC-only > total is intentionally flagged as incompatible with a naive additive decomposition rather than silently normalized.

Reproduce with:

```bash
python models/epc_attribution_bound_v357.py
```

Expected state: `"checks": "PASS"`, PA fraction `0.6363636363636364`, SMA fraction `0.5263157894736842`.

## Failure modes / conventional explanations

1. **Model-decomposition dependence:** the paper's EPC-only contribution is simulation-derived and mechanisms are coupled; the ratio is not an experimentally isolated causal share.
2. **Approximate prose values:** the reported `~` summaries lack formal uncertainty, so the numerical fractions should not be overinterpreted.
3. Energetic offset, outer reorganization, hybridization/electronic coupling, morphology and transport can co-vary with interface population.

The current increment directly bounds the first over-strong interpretation by showing that even the source's own nominal decomposition leaves a substantial gap beyond EPC-only.

## Decision delta

For D18/PY-IT/eC9, do not optimize or gate on EPC/reorganization alone. A prospective useful-work test must retain energetic-offset/hybridization controls, field-dependent generation, DeltaVnr/Voc, FF/stabilized Pmax, morphology/transport/contact controls and durability. A favorable EPC signal remains mechanism evidence unless the downstream electrical and field-robustness gates pass.

## Falsifier

Revise this bound if a corrected primary source or provenance-complete raw/model release shows the quoted EPC-only and total reductions were defined on incompatible bases that invalidate the ratio comparison, or materially changes the values/interpretation.

## Correction history

Before commit, the first local executable run failed because fixture keys (`total_mev`, `epc_only_mev`) did not match the initial function parameter names. The implementation was corrected without changing inputs, equations, tolerance, or conclusion; the rerun passed. This was a software-interface defect, not a scientific correction.
