# D18/PY-IT/eC9 donor-free acceptor-domain falsifier v3.70

## Status

**Prospective experiment / falsifiable hypothesis. No physical project result yet.**

v3.70 adds a new causal control to the commercial bridge: test whether PY-IT changes field-dependent charge-generation behavior in **donor-free eC9-rich material** before attributing B1/B2 behavior only to the D18 donor–acceptor interface.

This is a conventional materials-physics control. A positive donor-free effect is not a quantum-mechanism result.

## Why this is new value

The current bridge hypothesis is intentionally interface-focused:

`D18/PY-IT/eC9 process -> penetrated interface -> EPC/reorganization -> CT kinetics / DeltaVnr -> useful electrical work`.

But PY-IT can also change ordinary properties of acceptor-rich domains:

- molecular packing;
- electronic coupling / state delocalization;
- energetic disorder;
- exciton lifetime and diffusion;
- local dielectric environment;
- morphology and percolation.

If one of those donor-independent changes improves charge generation, a favorable B1/B2 result could be real while the **interface-only causal story is wrong or incomplete**.

The new control asks the simplest adversarial question:

> Does adding PY-IT change eC9-rich charge-generation physics even when D18 is absent?

If yes, the program must fit a mixed bulk/domain + interface model. If no, interface-specific attribution becomes substantially stronger, although EPC is still not uniquely proven.

## Primary 2026 evidence

Hart et al., *Molecular factors controlling charge pair generation in organic photovoltaic materials*, **Nature Materials 25, 1209–1218 (2026)**, DOI `10.1038/s41563-026-02509-6`, combine donor-free NFA experiments with a delocalized-state model.

Their established findings relevant here are:

- charge generation depends jointly on exciton binding energy, reorganization energy, energetic disorder, electronic coupling and packing;
- including state delocalization is important to their model;
- material parameters that favor charge generation in neat acceptor domains also tend to favor low-offset heterojunction charge generation, even though neat-domain photogeneration itself is not claimed to drive heterojunction photocurrent;
- field-dependent PL, trPL and IQE can directly expose charge-generation behavior in donor-free NFA devices.

In one Y5 single-component device, the paper reports IQE increasing from about **0.5% at short circuit to 93% at 0.15 V nm^-1**, accompanied by about **30-fold PL quenching** and trPL lifetime reduction from **1.1 ns to <0.1 ns**. These values establish measurement leverage in that source material only; they are not eC9 thresholds.

The source-data record is Zenodo DOI `10.5281/zenodo.18151704`, v1.

## Cross-model design insight

v3.45 showed in a local classical Marcus–Stark model that blindly reducing reorganization energy can **decrease field robustness** when lambda becomes mismatched from the driving force.

Hart et al. independently show in a richer delocalized-state model that smaller exciton reorganization energy and larger electronic coupling can improve charge generation.

These are not contradictory because the objectives and models differ. Together they motivate a more useful design target:

**do not optimize lambda alone; co-design energetic matching, field robustness and delocalization/packing.**

That is a novel project design concept, not a claim that an optimum manifold has already been measured.

## Experimental arms

### Donor-free controls

- **A0:** eC9
- **A1:** PY-IT:eC9 = 0.1:1
- **A2:** PY-IT:eC9 = 0.2:1

The A1/A2 ratios mirror the PY-IT:eC9 guest proportions present in B1/B2 while removing D18.

### Donor-containing bridge

- **B0:** D18:eC9
- **B1:** D18:PY-IT:eC9 = 1:0.1:1
- **B2:** D18:PY-IT:eC9 = 1:0.2:1

The donor-free and donor-containing arms should share material lots and processing provenance wherever physically meaningful, while remaining distinct device architectures.

## Donor-free measurement package

A donor-free device must use a **qualified selective-contact architecture** that suppresses electrode-driven exciton dissociation sufficiently for the bulk acceptor response to be interpretable. Hart et al.'s Y5 stack is precedent for the method, not an automatically transferable eC9 stack.

Acquire:

1. field-dependent steady-state PL;
2. field-dependent photocurrent IQE, or another independently validated charge-generation observable;
3. trPL where signal permits;
4. active-layer thickness and area provenance;
5. explicit bias-to-field conversion assumptions and uncertainty;
6. absorption / optical-density controls;
7. morphology/packing witness data, preferably GIWAXS when available;
8. dark-current / injection / breakdown checks so high-field artifacts are not misclassified as photogeneration.

Do not extend the field merely to reproduce a literature number. The valid field range ends when injection, heating, breakdown, electrochemistry or contact artifacts invalidate the intended measurement model.

## Primary empirical outputs

Always retain the raw PL, trPL and IQE/photocurrent observables.

Derived quantities may include:

`Q_PL(F) = 1 - PL(F)/PL(F_ref)`

where `F_ref` is frozen before unblinding.

If a monotonic response cleanly spans its dynamic range, define an empirical midpoint `F50` by interpolation. `F50` may be reported only when:

- the observed curve brackets the midpoint;
- field calibration is valid;
- interpolation uncertainty is bounded;
- the same definition is applied to all arms.

A CGE reconstructed from PL/trPL/IQE requires a separately validated kinetic/optical mapping. If that mapping does not hold, report the observables separately instead of forcing them into a single efficiency number.

## Prospective inference logic

### 1. Donor-free effect present

If A1/A2 move beyond a prospectively frozen A0-based capability margin across independent fabrication lots, PY-IT has a donor-independent acceptor-domain effect.

This result **falsifies a purely D18-interface-specific explanation** unless a separate discriminator demonstrates that the donor-free change is irrelevant to B1/B2 operation.

### 2. Interface specificity strengthened

If A1/A2 remain inside donor-free margins but B1/B2 move beyond frozen B0 margins in field-generation / voltage-loss observables, interface-specific attribution is strengthened.

This still does not uniquely prove EPC; electrostatics, interface morphology and other interfacial explanations remain live.

### 3. Mixed bulk + interface effect

If both A and B families move materially, fit a mixed model. Do not choose the interface story simply because it is the preferred platform narrative.

### 4. No resolved effect

If neither family moves beyond capability-aware margins, the current perturbation is unresolved at the available precision.

### 5. Incomplete

Missing A0/B0 baselines, frozen margins, field calibration, optical controls or adequate independent-lot evidence yields `INCOMPLETE`, not a favorable interpretation.

## Threshold policy

**No physical effect-size or F50 threshold is frozen in v3.70.**

Real acceptance margins must come from:

- A0/B0 empirical repeatability;
- instrument and field-calibration uncertainty;
- lot/substrate/device variance;
- a prospective power analysis;
- the smallest scientifically meaningful effect after those quantities are known.

The arbitrary 0.05 margins and three-lot count used by the software fixtures test classifier semantics only and are not material expectations.

## Statistical independence

Preserve:

`material lot -> fabrication lot -> substrate -> device -> session -> field point / optical measurement`.

Voltage points, field points, spectra, transient averages, repeated scans and multiple pixels are technical repeats. They do not increase independent fabrication-lot N.

## Strongest conventional explanations

1. **Packing / delocalization:** PY-IT alters eC9 packing, disorder or electronic coupling in acceptor-rich domains.
2. **Optical confound:** thickness or absorption changes alter PL/IQE normalization.
3. **Contact / field artifact:** selective-contact differences, injection or uncertain internal field create apparent shifts.
4. **Architecture transfer:** donor-free films can organize differently from D18-containing blends, limiting quantitative mapping between A and B arms.
5. **Morphology mediation:** a real donor-free effect may still arise through ordinary morphology rather than a microscopic electronic-coupling change.

The first explanation is not an unwanted nuisance—it is the new falsifier this experiment is designed to expose.

## Reproduction packet

Machine-readable contract:

`research/protocols/d18-pyit-ec9-acceptor-domain-control-v3.70.json`

Software-only protocol validation:

```bash
python models/d18_acceptor_domain_control_v370.py
```

Expected state before real data:

- protocol validation PASS;
- Hart Y5 descriptive IQE ratio = 186;
- physical thresholds deferred;
- physical result = `NONE_PROSPECTIVE_PROTOCOL_ONLY`.

The executable includes fail-closed synthetic fixtures for mixed, interface-specificity, donor-free-only, null and incomplete states.

## Physical falsifier

The strongest direct falsifier is:

> A reproducible A1/A2 donor-free field-response change in the same direction as B1/B2.

That observation would force the program to stop describing the useful change as purely D18-interface-mediated until the bulk/domain contribution is quantitatively separated.

## Next value after v3.70

If A0/A1/A2 are feasible, the next high-value step is a **joint donor-free / donor-containing causal matrix** linking field-response, GIWAXS/packing, DeltaVnr and stabilized Pmax at the same material-lot level. That would test whether a delocalization/packing coordinate and an interface/EPC coordinate can be independently manipulated rather than merely correlated.
