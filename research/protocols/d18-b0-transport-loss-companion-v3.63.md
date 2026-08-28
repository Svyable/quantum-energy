# D18:eC9 B0 transport-loss companion protocol v3.63

## Changed evidentiary state

**Claim class: prospective experiment/protocol.** The commercial bridge now has a preregistered transport/collection discriminator to accompany the already-open B0 field-generation protocol. A favorable TDCF or bias-dependent-PL result is therefore not allowed to stand in for charge collection: the same lot/device mapping must also retain a measured illuminated-JV fill factor close enough to its transport-free pseudo-fill factor to survive a future B0-derived acceptance rule, and stabilized Pmax remains the useful-work sink metric.

No physical D18 transport-loss threshold is created here. The gate remains `DEFERRED_PENDING_REAL_B0_DATA` until real B0 repeatability, leakage/transient validity, and session-transfer uncertainty are measured.

## Why this is the bounded next step

Open PR #55 establishes a real external counterexample in which nearly equal TDCF-derived CT-dissociation efficiency coexists with a large collection difference. Open PR #52 already preregisters the B0 field-generation measurement. Repeating another generation-only benchmark would drift. This increment instead specifies the missing downstream conventional discriminator.

## Primary provenance

The method precedent is Sebastian Schiefer, Birger Zimmermann, Stefan W. Glunz, and Uli Wurfel, **“Applicability of the Suns-Voc Method on Organic Solar Cells,”** *IEEE Journal of Photovoltaics* 4, 271–277 (2014), DOI `10.1109/JPHOTOV.2013.2288527`. The study experimentally applied Suns-Voc to P3HT:PCBM organic solar cells and explicitly discusses transient/capacitive validity concerns.

For the contemporary transport-loss interpretation and stepwise reconstruction workflow, this protocol also uses Wang et al., **“Transport Resistance Dominates the Fill Factor Losses in Record Organic Solar Cells,”** *Advanced Energy Materials*, first published 2025-03-05, DOI `10.1002/aenm.202405889`. That source defines the pseudo-fill factor `pFF` from a transport-resistance-free `J(Vimp)` curve and uses `pFF - FF` as the additional FF loss associated with transport resistance. Its record-cell example is context only and is **not** a D18 threshold.

No upstream code or data is copied.

## Measurement pairing and hierarchy

Preserve

`material lot -> fabrication lot -> substrate -> device -> session -> measurement`.

Prefer the same B0 device for illuminated JV, Suns-Voc/pseudo-JV, TDCF, and bias-dependent PL when measurement order and device stability permit. If one technique is destructive or creates unacceptable history dependence, preregister a sibling-device mapping on the same substrate. Repeated intensity points, voltage points, scans, or pulses are technical repeats, not independent fabrication replicates.

## Required raw provenance

Retain, rather than only reporting a pFF number:

- the illuminated JV trace used for measured FF and Pmax;
- light-intensity-dependent Voc values used to construct `J(Vimp)`;
- generation-current estimates versus intensity and the reverse-bias point/range used;
- illumination calibration/reference and temperature record;
- leakage-current exclusion range;
- external-series-resistance handling;
- pseudo-JV interpolation/reconstruction procedure and software version.

The contemporary method constructs a transport-free curve by pairing the open-circuit implied voltage with recombination/generation current and shifting the recombination curve by the generation current at the target illumination. Low-light leakage, insufficient reverse bias for estimating generation current, sparse interpolation, capacitance, and transient response are therefore validity concerns, not nuisance points to remove after seeing the result.

## Governing quantities

Let `FF` be the measured illuminated-JV fill factor and `pFF` the pseudo-fill factor from the transport-free pseudo-JV reconstruction under matched conditions.

The descriptive transport-associated FF loss is

`DeltaFF_tr = pFF - FF`.

The retained fraction is

`R_FF = FF / pFF`.

Both are dimensionless except that `DeltaFF_tr` is conventionally described as an absolute fill-factor fraction or percentage-point loss after multiplying by 100.

For an accepted row the protocol requires, within numerical tolerance,

`0 < FF <= pFF <= 1`.

A measured `pFF < FF` is **not** clamped to zero. It is a method/data-consistency failure to investigate for calibration, transient, leakage, reconstruction, device-drift, or sign/normalization problems.

## Independent and negative checks

Run:

```bash
python models/d18_b0_transport_loss_companion_v363.py
```

The executable validates the contract and tests:

1. **Limiting case:** `FF=pFF` gives `DeltaFF_tr=0` and `R_FF=1`.
2. **Independent arithmetic representation:** a synthetic `FF=0.75`, `pFF=0.85` fixture is recomputed with exact `fractions.Fraction` arithmetic and compared to floating point at absolute tolerance `1e-12`.
3. **Negative/control:** `pFF<FF` fails closed rather than being silently normalized.
4. **Domain control:** zero/nonphysical fill factor is rejected.

The synthetic values only exercise implementation logic. They are not material constants, physical expectations, or acceptance thresholds.

Analyze a completed summary table with:

```bash
python models/d18_b0_transport_loss_companion_v363.py --csv path/to/b0_transport_summary.csv
```

The exact CSV schema is frozen in the JSON contract. Raw traces and their derivation records remain mandatory even though the lightweight executable consumes the derived summary table.

## Uncertainty and sensitivity

No D18 measurement uncertainty is available before acquisition; none is fabricated. The physical noninferiority/acceptance rule must remain deferred until B0 data quantify at least:

- same-device/session repeatability of FF and pFF;
- session/illumination-calibration drift;
- leakage-limited low-intensity range;
- sensitivity to the generation-current reverse-bias estimate;
- any measurable device drift caused by technique ordering.

External series resistance and active-layer transport are coupled in the raw measured-versus-pseudo difference unless explicitly separated. A pFF gap is therefore a conventional collection/transport discriminator, not a unique morphology, mobility, contact, or EPC diagnosis.

## Serious conventional explanations / failure modes

At least five remain live:

1. capacitive or transient Suns-Voc response masquerading as steady-state transport loss;
2. low-light leakage/shunt current corrupting Voc-versus-intensity data;
3. contact/electrode external series resistance contributing to the FF gap;
4. generation-current or illumination-calibration error shifting the reconstructed pseudo-JV;
5. device drift between field-generation, illuminated-JV, and Suns-Voc measurements.

The current increment directly bounds the prior interpretive failure in which good field-generation evidence could be promoted without an explicit transport-loss measurement. It does not uniquely distinguish the five explanations above.

## Frozen decision logic

- `physical_gate = DEFERRED_PENDING_REAL_B0_DATA`.
- Do not import the literature record-cell `7.8` percentage-point pFF–FF example as a D18/PY-IT/eC9 threshold.
- A later B1/B2 arm with favorable field-generation observables but materially degraded measured FF relative to its own pFF remains collection/transport-limited and is not useful-work validation unless stabilized Pmax and the conventional-control stack also pass.
- The numerical meaning of “materially degraded” must be frozen from real B0 repeatability/instrument capability before B1/B2 unblinding.
- All functional samples remain visible unless a prospectively frozen QC rule excludes them.

## Falsifier and next physical measurement

If provenance-complete B0 measurements across the intended independent-lot regime show `pFF` and `FF` indistinguishable within empirical method repeatability while field-generation and stabilized Pmax are also robust, a large transport-resistance FF penalty is narrowed for B0 under those conditions. If `pFF-FF` is reproducibly positive, transport/collection remains a live downstream bottleneck even when TDCF/PL looks favorable.

The next physical increment is therefore one combined B0 execution: provenance-complete TDCF + bias-dependent PL + illuminated JV + Suns-Voc/pseudo-JV on the same mapped devices/lots, followed by a B0-derived transport and field-generation acceptance freeze before B1/B2 unblinding.
