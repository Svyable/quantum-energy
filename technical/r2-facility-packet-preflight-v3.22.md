# R2 Facility Packet Preflight v3.22

## Purpose

This increment adds a facility-handoff boundary before any R2 analysis. It answers one narrow question: **is the packet complete, byte-integrity checked, and internally consistent enough to enter the measurement-analysis pipeline?**

A `PASS` is not a metrology qualification, uncertainty result, device-performance result, or mechanism claim.

## Required packet roles

The manifest must bind exactly one file for each required role:

- `voc_intensity_raw`
- `reference_repeatability_raw`
- `reference_certificate_metadata`
- `reference_certificate_source`
- `source_spectrum_metadata`
- `source_spectrum_data`
- `detector_linearity_metadata`
- `detector_linearity_data`
- `analysis_freeze_record`

Every manifest entry carries a relative path, SHA-256 digest, and byte count. Duplicate roles or paths are failures. Absolute paths and `..` traversal are failures.

## Status semantics

The gate is deliberately asymmetric:

`PASS = all required evidence present AND all integrity/identity checks pass`.

`INCOMPLETE` means a required evidence object/field/file is absent. Missing evidence is never converted to zero uncertainty or an implicit pass.

`FAIL` means evidence is present but malformed, tampered relative to its manifest, internally contradictory, path-unsafe, or metadata-to-source binding is broken.

These are logical states; no statistical confidence claim is attached to them.

## Identity binding

The top-level manifest freezes:

- packet ID;
- facility ID;
- protocol version;
- reference-detector ID;
- source-spectrum ID;
- instrument-configuration ID;
- creation timestamp.

The raw `Voc` and reference-repeatability CSVs must use the same detector and spectrum IDs. Certificate, source-spectrum, detector-linearity, and analysis-freeze metadata are checked against the same declared identities/configuration.

## Source binding

Metadata are not accepted as detached summaries. The following SHA-256 links must resolve to the exact source/data bytes included in the packet:

- certificate metadata -> original certificate source;
- spectrum metadata -> spectrum data;
- detector-linearity metadata -> linearity data.

This is an integrity/provenance link only. It does not authenticate the issuer or establish that the source content is scientifically adequate.

## Raw schemas checked

The `Voc` CSV must at minimum contain:

`lot_id, substrate_id, pixel_id, session_id, sweep_id, sequence_index, target_suns, calibrated_suns, reference_detector_id, source_spectrum_id, voc_V, qc_status`.

The repeatability CSV must at minimum contain:

`session_id, sweep_id, sequence_index, target_suns, calibrated_suns, reference_detector_id, source_spectrum_id, qc_status`.

Allowed QC states at this preflight layer are `PASS`, `PENDING`, and `EXCLUDED`. This gate does not decide whether an exclusion is scientifically justified; the frozen QC rule/version in the analysis-freeze record remains controlling.

## Verification

The committed standard-library adversarial test constructs a deterministic synthetic packet and requires:

1. complete packet -> `PASS`;
2. byte change after manifest creation -> `FAIL`;
3. missing certificate source -> `INCOMPLETE`;
4. detector-ID contradiction with rehashed bytes -> `FAIL`;
5. `../` path traversal -> `FAIL`;
6. source file swapped and manifest rehashed while metadata still points to the old source -> `FAIL`.

The source-binding test is important because a top-level manifest alone cannot detect a coordinated file replacement unless the metadata also commits to the underlying source/data object.

CI additionally checks Python 3.12/3.13/3.14 syntax/tests and independently recomputes a generated packet file digest with the host `sha256sum` utility before running the Python preflight.

## Calculation / dimensional audit

No physical model is introduced. File size is in bytes; SHA-256 is a 256-bit digest represented as 64 lowercase hexadecimal characters. Detector/source/configuration identifiers are categorical strings. Intensity and voltage columns are not numerically interpreted beyond CSV structure at this preflight layer, so no device-physics unit conversion is performed here.

## Statistical independence

No packet row, sweep, pixel, substrate, or session is counted as a statistical replicate by this tool. The experimental hierarchy remains `lot -> substrate -> pixel -> session -> sweep -> intensity`. Repeatability/session covariance is separate work; packet completeness gives no `sqrt(N)` credit.

## Conventional/null explanation

A packet can be perfectly complete and internally consistent while the experiment is still wrong: a detector may be miscalibrated, a spectrum may be inappropriate, an uncertainty model may be incomplete, or a DUT effect may be conventional contact/thermal/optical physics. The discriminator is the downstream v3.17 qualification, covariance/systematic analysis, controls, and prospective validation—not packet integrity.

## Engineering assumptions

- SHA-256 plus byte count is sufficient for repository-level accidental/tamper detection in the handoff workflow.
- Facility operators supply truthful IDs and metadata; this tool does not authenticate identities or signatures.
- One detector/source/configuration population per packet is intentional. Mixed populations should be split or handled by a later explicit multi-population schema.

## Kill / narrow gates

Do not begin confirmatory analysis when preflight is `INCOMPLETE` or `FAIL`. Do not reinterpret a `PASS` as evidence that v3.17/v3.18/v3.19/v3.21 gates pass.

## Single best next increment

Run this preflight unchanged on the first real facility handoff packet. Preserve every missing role as `INCOMPLETE`, then map the real certificate/spectrum/linearity content into the external-systematic budget without inventing absent uncertainty terms.
