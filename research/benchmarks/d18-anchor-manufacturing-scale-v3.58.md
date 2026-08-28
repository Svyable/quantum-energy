# v3.58 — D18/PY-IT/eC9 anchor manufacturing-scale evidence boundary

## Changed evidentiary state

**Claim class:** established-evidence-derived engineering bound.

The D18/PY-IT/eC9 anchor paper supports a laboratory photovoltaic/device result, but its inspected Methods do **not** establish manufacturing-scale transfer for the repository's planned 1 cm² -> 10 cm² stage. The source reports a 0.041 cm² illuminated area, spin-coated active layer, inert-glovebox measurement, and Ag deposited by vacuum evaporation. The correct manufacturing evidence class is therefore `LAB_SCALE_ONLY`.

This is not a claim that scale-up will fail. It is a claim that scale-up has not yet been demonstrated by this anchor result.

## Primary-source provenance

Luo et al., *Suppressing electron-phonon coupling and energy loss in organic solar cells by modulating donor-acceptor penetrated-interface*, Nature Communications (2026), DOI `10.1038/s41467-026-68731-7`.

Inspected Methods facts:

- contact area: 0.042 cm²;
- illuminated/masked area: 0.041 cm²;
- active layer: spin-cast at 2000–2500 rpm for 30 s;
- PFN-Br-MA layer: spin coating;
- top electrode: Ag evaporation through a shadow mask at 3e-4 Pa;
- device measurement and thermal ageing: inside a glovebox under inert atmosphere.

No vendor capability, manufacturing yield, large-area uniformity, or roll-to-roll compatibility is inferred from these facts.

## Governing calculations

Let `A_pub` be the published illuminated device area and `A_target` a repository engineering scale-transfer reference area.

`M = A_target / A_pub`.

With `A_pub = 0.041 cm²`:

- to 1 cm²: `M_1 = 1 / 0.041 = 24.3902439024`;
- to 10 cm²: `M_10 = 10 / 0.041 = 243.9024390244`.

The contact-to-illuminated area excess fraction is

`(0.042 - 0.041) / 0.042 = 0.0238095238`, or 2.38%.

All quantities above are dimensionless ratios after area units cancel. The 1 cm² and 10 cm² values are existing project engineering stages, not literature-derived physical thresholds.

## Independent check and controls

`models/d18_anchor_manufacturing_scale_v358.py` recomputes the ratios in ordinary floating point and independently with exact rational arithmetic using `fractions.Fraction`. Agreement tolerance is frozen at `1e-12` absolute.

Limiting/control case: a device with illuminated area exactly 1 cm² reaches the first project scale stage.

Negative/adversarial case: zero or negative area is rejected rather than silently producing an infinite/meaningless scale multiplier.

Reproduce with:

```bash
python models/d18_anchor_manufacturing_scale_v358.py
```

Expected state: `classification = LAB_SCALE_ONLY` and `checks = PASS`.

## Uncertainty and sensitivity

The inspected Methods text does not provide a physical uncertainty for the 0.041 or 0.042 cm² areas. None is invented. These calculations therefore use the nominal reported values and should not be interpreted as confidence intervals.

The decision is insensitive to plausible last-digit transcription variation: even if the illuminated area were 0.042 cm², the multiplier to 1 cm² would still exceed 23.8×; if it were 0.040 cm², it would be 25×. This sensitivity band is a reporting-resolution thought experiment only, not measurement uncertainty.

## Statistical independence

No device-level sample count, yield distribution, spatial nonuniformity, lot variance, or scale-transfer statistics are inferred here. A champion small-area cell and repeated pixels on one substrate cannot establish manufacturing replication across larger-area independent lots.

## Strongest conventional/null explanations and failure modes

1. **Scale may transfer well:** the small-area architecture could scale with negligible loss when coating, drying, contact resistance, and thickness uniformity are controlled. The current source simply does not demonstrate that.
2. **Process replacement may preserve physics:** spin coating/glovebox/vacuum steps may be replaceable by scalable coating, ambient-compatible processing, or alternate electrodes without losing the interface/EPC effect.
3. Conversely, ordinary scale effects—sheet resistance, coating gradients, drying kinetics, defect density, electrode continuity, encapsulation, and contact geometry—could erase the effect without falsifying the microscopic mechanism.

The current increment directly tests only the evidentiary boundary, not these future scale outcomes.

## Falsifier / retirement condition

Retire or narrow `LAB_SCALE_ONLY` when a provenance-complete primary dataset demonstrates the same D18/PY-IT/eC9 architecture/process objective and claimed beneficial state on independently fabricated devices at >=1 cm², with area definition, stabilized output, yield/all-functional-device reporting, and relevant uniformity/contact controls.

## Technical/business delta

The anchor paper remains mechanism and lab-device evidence. It should not be used to imply manufacturing readiness. Before product-scale language or substantial scale-up capex, the program should require a prospective >=1 cm² transfer experiment that jointly retains stabilized Pmax, field-generation robustness, and the intended interface/EPC state.

## Safety / environmental boundary

The source process includes acetone/isopropanol cleaning, UV-ozone treatment, methanol-based interlayer coating, inert-glovebox operation, thermal processing, and high-vacuum Ag deposition. This note does not quantify EHS burden because source-specific quantities/exposure data are not reported; it flags these process steps for later manufacturing/EHS substitution analysis rather than treating them as production-ready.
