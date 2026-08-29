# Research session — 2026-08-29 — v3.70 donor-free acceptor-domain falsifier

## Changed evidentiary state

The D18/PY-IT/eC9 program gains a new prospective causal control: donor-free eC9 / PY-IT:eC9 arms can now falsify a purely D18-interface-specific explanation before B1/B2 mechanism promotion.

No physical D18/PY-IT/eC9 result is introduced.

## New primary evidence

Hart et al., *Molecular factors controlling charge pair generation in organic photovoltaic materials*, Nature Materials 25, 1209–1218 (2026), DOI `10.1038/s41563-026-02509-6`, published 2026-02-27. Source-data record: Zenodo `10.5281/zenodo.18151704`, v1.

The paper establishes that charge generation in molecular acceptors depends jointly on exciton binding energy, reorganization energy, energetic disorder, electronic coupling, packing and delocalization. It also demonstrates field-dependent IQE/PL/trPL as a direct donor-free NFA charge-generation probe.

Method-precedent arithmetic: reported Y5 IQE changes from 0.5% to 93%, a descriptive ratio of `0.93/0.005 = 186`. Float arithmetic is independently checked by exact rational arithmetic `93/100 / (5/1000) = 186`. This is source-material context only, not an eC9 threshold.

## New hypothesis

PY-IT may affect B1/B2 through at least two causal routes:

1. D18-containing penetrated-interface / EPC / CT-state changes;
2. donor-independent changes to eC9-rich packing, disorder, electronic coupling or delocalization.

A1/A2 donor-free controls test route 2 directly enough to reject a purely interface-specific interpretation when a reproducible donor-free field-response effect exists.

## Experimental matrix

- A0: eC9
- A1: PY-IT:eC9 = 0.1:1
- A2: PY-IT:eC9 = 0.2:1
- B0: D18:eC9
- B1: D18:PY-IT:eC9 = 1:0.1:1
- B2: D18:PY-IT:eC9 = 1:0.2:1

Donor-free primary measurements: field-dependent PL, IQE/validated charge-generation observable, trPL when possible, thickness/absorption, field calibration and morphology/packing witness data.

## Fail-closed logic

No physical effect-size, F50 or lot-count threshold is frozen in v3.70. Those remain deferred pending real A0/B0 repeatability, method capability and prospective power analysis.

The executable software fixtures exercise only semantic states:

- donor-free + donor-containing effects -> `MIXED_BULK_INTERFACE_EFFECT`;
- donor-free null + donor-containing effect -> `INTERFACE_SPECIFICITY_STRENGTHENED`;
- donor-free effect only -> `DONOR_FREE_EFFECT_PRESENT`;
- neither -> `NO_RESOLVED_EFFECT`;
- missing margins, insufficient hierarchy, bad field calibration or bad optical control -> `INCOMPLETE`.

The synthetic 0.05 fixture margin and three-lot fixture count are software values only.

## Cross-model design insight

v3.45 shows a simple Marcus–Stark field-robustness penalty can worsen when lambda is reduced away from energetic matching. Hart et al. show a richer delocalized-state model favors smaller exciton reorganization energy and larger electronic coupling for charge generation.

The combined design implication is not `minimize lambda`. It is to co-design:

- reorganization/EPC;
- energetic offset;
- electronic coupling / delocalization;
- field robustness;
- useful electrical work.

This is a novel project design concept, not an experimentally established manifold.

## Strongest conventional explanations

- PY-IT changes acceptor-rich morphology/packing/delocalization.
- Optical-density or thickness changes distort PL/IQE normalization.
- Contact/injection/internal-field artifacts create apparent donor-free response shifts.
- Donor-free morphology may not quantitatively transfer to the D18-containing blend.

## Files

- `research/protocols/d18-pyit-ec9-acceptor-domain-control-v3.70.json`
- `models/d18_acceptor_domain_control_v370.py`
- `technical/d18-pyit-ec9-acceptor-domain-control-v3.70.md`
- `.github/workflows/d18-acceptor-domain-control-v370.yml`
- `research/sessions/2026-08-29-acceptor-domain-falsifier-v3.70.md`

## Single best next increment

Quantitatively preregister the donor-free A0/A1/A2 acquisition geometry and electrostatic field model only after selecting a physically valid selective-contact architecture for eC9/PY-IT:eC9. Then acquire real A0 baseline repeatability before freezing any physical margins or unblinding A1/A2.
