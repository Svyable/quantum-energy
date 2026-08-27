# R2 Transfer Fixture and Shipping Interface v3.35

## Purpose

Define a fabrication-ready mechanical brief for repeatable cross-facility handling of the 25 mm square R2 weak-EL transfer substrate without clamping the central device/encapsulation region. This is an engineering specification, not evidence that shipping/remounting is harmless.

## Established inputs

From `technical/current-specification.md` on main (read 2026-08-27): substrate 25 × 25 × ~1.1 mm; measured aperture 3.10 × 3.10 mm; top-electrode window 3.80 × 3.80 mm; minimum residual aperture/electrode margin 0.10 mm; exposed contact pads >=2.5 × 3.0 mm; optical exclusion/collection zone Ø8 mm; encapsulation lid ~18 × 18 mm planning.

## Engineering assumptions

Carrier outer envelope 40 × 40 × 4 mm. Substrate pocket 25.30 × 25.30 × 1.35 mm. Central no-contact/no-clamp keepout 20 × 20 mm. Nominal retainer preload 0.5 ±0.2 N. Minimum vertical package clearance above the device 5 mm. Material remains deliberately unfrozen pending EHS, contamination, ESD, solvent/outgassing, and encapsulation-compatibility review.

These values are design assumptions, not measured tolerances or vendor capabilities.

## Governing geometry

Planar clearance per side:

`c = (W_pocket - W_substrate)/2 = (25.30 - 25.00)/2 = 0.15 mm`.

Nominal edge-support band outside the central keepout:

`b = (W_substrate - W_keepout)/2 = (25.00 - 20.00)/2 = 2.50 mm`.

All terms are lengths in mm; dimensional consistency is direct. The validator independently recomputes both identities and uses `1e-12 mm` arithmetic tolerance. Fabrication tolerance must be supplied by the fabricator; any tolerance stack capable of reducing planar clearance below 0.05 mm or edge support below 2.0 mm requires redesign.

## Mechanical interfaces

Use two perpendicular hard edge datums and one compliant opposite-corner retainer. No clamp, adhesive, foam, screw, or spring may load the 20 × 20 mm central keepout or encapsulation lid. At least one carrier edge must remain relieved/open for contact-pad access. The carrier must not intrude into the Ø8 mm optical exclusion zone around the selected pixel.

The carrier is the transferred object between facilities. The substrate should remain seated in it for A1→B→A2 whenever facility hardware allows, reducing unnecessary remount operations. If a facility requires removal, record that as a configuration/deviation event rather than silently treating the transfer as identical.

## Shipping insert

The secondary insert restrains the carrier perimeter, not the device. Maintain >=5 mm assumed free vertical clearance above the device. No packing foam/tape/adhesive contacts the substrate, lid, active face, or electrical contacts. Record packed and received photos, carrier ID, blind substrate ID, orientation, and package-integrity identifier where available.

## Qualification and falsification

Before qualified R2 primaries are used, screen at least three dimensionally representative dummy substrates for 10 insertion/removal cycles each (30 total handling cycles). These counts are engineering screening assumptions, not statistical power claims.

Kill/narrow gates:
- visible substrate edge damage, fixture interference, contact obstruction, or encapsulation loading -> FAIL;
- missing required inspection/provenance -> INCOMPLETE;
- any material incompatibility, conductive debris, particle shedding, or unsafe state -> FAIL pending redesign;
- failure to reproduce datum seating -> redesign before cross-facility transfer.

A successful dummy screen proves only mechanical handling compatibility under the screened configuration. It does not establish device electrical stability, shipping robustness, or facility equivalence.

## Conventional explanation / discriminator

A cross-facility measurement shift can arise from ordinary remounting geometry, contact pressure, substrate edge damage, particles, encapsulation loading, or shipping handling rather than intrinsic device/facility physics. The discriminator is frozen carrier geometry plus pre/post inspection and, later, measured A→B→A device behavior under the v3.34 protocol.

## Statistical hierarchy

Dummy handling cycles are repeated technical operations, not independent devices. For physical transfer inference preserve `lot -> substrate -> device/pixel -> facility -> session -> measurement`; do not convert 30 dummy cycles into N=30 device evidence.

## Safety/environment

No carrier material is selected yet. Material selection must consider facility EHS, electrical insulation, low shedding, device/encapsulant compatibility, contamination, outgassing where relevant, and safe handling. Schedule or reproducibility goals never override facility safety rules.
