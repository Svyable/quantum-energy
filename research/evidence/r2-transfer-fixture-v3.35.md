# Evidence record — R2 transfer fixture v3.35

Date: 2026-08-27

## Established repository evidence

The current R2 technical specification defines a 25 × 25 × ~1.1 mm substrate, 3.10 × 3.10 mm measured aperture, 3.80 × 3.80 mm top-electrode window, exposed contact pads >=2.5 × 3.0 mm, Ø8 mm optical exclusion/collection zone, and ~18 × 18 mm encapsulation-lid planning envelope.

Open PR #26 identifies shipping/remounting/contact geometry as unresolved conventional explanations in cross-facility A→B→A transfer. No current-main or open automation PR found in the startup audit defined a fabrication-ready carrier/packing interface.

## Engineering assumptions added

- 40 × 40 × 4 mm carrier envelope.
- 25.30 × 25.30 × 1.35 mm substrate pocket.
- 20 × 20 mm central no-contact/no-clamp keepout.
- 0.5 ±0.2 N compliant retainer preload.
- >=5 mm vertical package clearance above the device.
- dummy screening: >=3 dummies × 10 remount cycles each.

All are provisional engineering values pending fabrication and physical qualification. No vendor specification or measured fixture performance is claimed.

## Calculations

`c=(25.30-25.00)/2=0.15 mm` planar clearance per side.

`b=(25.00-20.00)/2=2.50 mm` nominal edge-support band.

Both are independently recomputed by `models/r2_transfer_fixture_v3_35.py` with exact dimensional units and `1e-12` arithmetic tolerance.

## Null / negative boundary

Passing structural/dummy fixture checks does not establish electrical stability, safe shipment of real R2 primaries, facility equivalence, or mechanism evidence. A transfer shift may still arise from ageing, contact changes, calibration, source spectrum, thermal history, or other conventional effects.
