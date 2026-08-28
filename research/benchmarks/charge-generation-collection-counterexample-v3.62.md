# v3.62 — Charge-generation sufficiency counterexample

## Changed evidentiary state

**Established external experimental evidence + project arithmetic benchmark.** A 2026 PM6:Y12 donor-dilution study provides a direct conventional counterexample to the inference that efficient CT dissociation is sufficient for high collected photocurrent or useful electrical work. In the source's main-text Table 1, the 2% and 45% PM6 devices have nearly identical TDCF-derived short-circuit CT-dissociation efficiencies (`0.96` and `0.95` under selective Y12 excitation at 820 nm), yet measured IQE changes from `0.18` to `0.85`.

This does **not** establish a D18/PY-IT/eC9 transport penalty, threshold, or mechanism. It changes the project decision rule: field-generation evidence is necessary but cannot replace direct collection/transport and stabilized FF/Pmax evidence.

## Primary provenance

- Wang et al., *Rethinking Charge Transport and Recombination in Donor-Diluted Organic Solar Cells*, **Advanced Materials** (2026), DOI `10.1002/adma.202523681`.
- Source location: Section 2.3, Table 1.
- Public source dataset: Zenodo DOI `10.5281/zenodo.20525023`, v1.0, published 2026-06-03. The Zenodo record states that figure-supporting data are provided as CSV files.
- No upstream code or CSV is copied into this repository. The compact JSON contract records the exact Table 1 values used here.

The article states that solar-cell parameters in Figure 1 were extracted from 20 independently fabricated cells. This packet does not turn the Table 1 summary values into 20 independent observations or infer a confidence interval from that statement.

## Governing factorization and units

The source writes the internal quantum efficiency as the product

`IQE = eta_exc * eta_diss * eta_col`,

where all four terms are dimensionless. Therefore

`eta_col = IQE / (eta_exc * eta_diss)`.

`eta_exc` is exciton harvesting at the donor–acceptor interface, `eta_diss` is CT-exciton dissociation into separated charge carriers, and `eta_col` captures the competition between recombination and collection after generation.

For selective Y12 excitation at 820 nm:

- 2% PM6: `eta_exc=0.38`, `eta_diss=0.96`, `IQE=0.18`, so `eta_col = 75/152 = 0.493421...`.
- 45% PM6: `eta_exc=0.96`, `eta_diss=0.95`, `IQE=0.85`, so `eta_col = 425/456 = 0.932018...`.

Thus the CT-dissociation efficiencies differ by only **1 percentage point**, while the independently reconstructed collection term differs by a factor of **1.8889×** and IQE differs by **4.7222×**. The source itself attributes low-donor-fraction performance loss primarily to extraction/transport resistance and topology-limited hole transport, with recombination-model changes also present.

## Independent numerical check

Run:

```bash
python models/charge_generation_collection_counterexample_v362.py
```

The executable computes the primary path in floating point and independently reconstructs both collection factors with exact `fractions.Fraction` arithmetic. The predeclared agreement tolerance is absolute `1e-12`.

Expected key output:

- `eta_col(2%) = 0.4934210526315789`
- `eta_col(45%) = 0.9320175438596491`
- `collection_ratio_45pct_over_2pct = 1.8888888888888888`
- `decision = GOOD_DISSOCIATION_NOT_SUFFICIENT_FOR_GOOD_COLLECTION_OR_USEFUL_WORK`
- `checks = PASS`

## Limiting and negative controls

1. **No-collection-loss limit:** if `IQE = eta_exc * eta_diss`, the executable requires `eta_col=1`.
2. **Invalid-domain control:** zero or negative efficiency denominators are rejected rather than silently normalized.
3. **Inference negative control:** nearly equal `eta_diss` is not allowed to imply nearly equal collection; the source fixture has only a one-point dissociation difference but >1.5× collection separation.

## Uncertainty and sensitivity

The main-text Table 1 gives two-decimal summary efficiencies without formal uncertainty; none is invented. A transcription/reporting-resolution sensitivity only—not a confidence interval—perturbs each listed efficiency by `±0.005` within physical bounds. Under the adverse endpoints, the derived collection intervals are approximately:

- 2% PM6: `0.4710–0.5166`;
- 45% PM6: `0.9169–0.9474`.

Even the adverse interval ratio remains `>1.77×`, so the qualitative decision does not depend on the final printed digit.

The dominant uncertainty is not arithmetic but transferability: PM6:Y12 donor dilution is not D18:eC9 or D18:PY-IT:eC9, and the source's collection factor is model/factorization based on several measured inputs.

## Serious conventional explanations / failure modes

1. **Topology/transport limitation:** reduced donor connectivity and hole transport can suppress collection and FF despite efficient CT dissociation. This is the principal conventional mechanism supported by the source and is directly represented in the benchmark.
2. **Exciton-harvesting limitation:** at low donor fraction, selective Y12 exciton harvesting is also much worse (`0.38` versus `0.96`), so the total IQE difference is not attributable to collection alone.
3. **Recombination-model crossover:** the source reports a change from Langevin-like toward dispersive Smoluchowski-type behavior at very low donor fraction; TDCF extraction can itself become less reliable in connectivity-limited devices.

These alternatives mean the benchmark is a sufficiency counterexample, not a unique causal attribution to one loss channel.

## Project consequence

For the D18/PY-IT/eC9 commercial bridge, a favorable TDCF/bias-dependent-PL result cannot by itself satisfy useful-work evidence. A strong claim must still jointly retain:

- transport/collection controls;
- FF and stabilized Pmax;
- morphology/contact diagnostics;
- DeltaVnr/Voc;
- durability;
- independent-lot structure.

A future D18 arm that preserves field generation but loses FF/Pmax remains a negative useful-work result even if its generation metric looks excellent.

## Falsifier / revision trigger

Revise this benchmark if the primary Table 1 values or factorization are corrected, or if independent re-analysis of the deposited source data shows the quoted short-circuit dissociation and IQE values are not comparable as represented. A D18-specific physical conclusion requires real D18 data and is not supplied by this packet.
