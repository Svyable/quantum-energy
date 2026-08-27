# 2026-08-27 — R2 transfer fixture v3.35

## Increment

Added a mechanical carrier/shipping interface for R2 cross-facility transfer so remounting and handling become controlled, inspectable variables rather than undocumented confounds.

## Startup audit

Read the required main-branch governance/specification files and all open automation PRs. Open work covers facility timing (#24), gate abort/evidence salvage (#25), A→B→A transfer analysis (#26), and older superseded calibration work (#7). No overlapping fabrication-ready transfer carrier/packing specification was found.

## Decision

Use a 40 mm square carrier with a 25.30 mm substrate pocket and 20 mm central keepout, edge datums plus compliant retention, contact/optical relief, and perimeter-only shipping restraint. Material is intentionally not selected until compatibility/EHS review.

## Verification

The executable validator independently recomputes 0.15 mm planar clearance/side and 2.50 mm edge-support band, verifies the neutral A1/B/A2 inspection template, and freezes dummy-first screening. No stochastic calculation applies.

## Unresolved risks

Fabrication tolerance, carrier material compatibility, preload repeatability, actual R2 contact-pad placement, shipping shock/vibration, ESD, contamination, and facility-specific holder interfaces remain unmeasured.

## Next increment

Fabricate/print the fixture only after human review, dimensionally inspect it, then run the frozen dummy-cycle qualification before placing a qualified R2 primary in the carrier.
