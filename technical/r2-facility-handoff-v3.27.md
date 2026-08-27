# R2 Facility Handoff v3.27

## Purpose

This document is the human-readable companion to `technical/data/r2_facility_capability_contract_v3_27.json`. It packages the open R2 metrology stack into one facility-neutral execution contract that a research agent, university/core facility, national laboratory, or industrial metrology partner can evaluate without reconstructing requirements from many pull requests.

This is an **engineering contract**, not experimental evidence. A facility matching the capability contract has not thereby demonstrated R2 performance or any EPC/open-quantum mechanism.

## Why this increment

Open work already covers calibration covariance, prospective holdout, external/reference systematics, packet integrity, wavelength-resolved spectral mismatch, randomized acquisition-order drift, optical/DUT settling, and electrical-chain temporal fidelity. The remaining integration failure mode is operational: a partner can satisfy one gate while unknowingly omitting evidence needed by another, or execute the gates in an order that contaminates a prospective holdout.

v3.27 therefore freezes:

1. capability classes;
2. evidence roles;
3. configuration identifiers;
4. gate dependencies;
5. PASS / FAIL / INCOMPLETE semantics;
6. statistical hierarchy and data-integrity rules.

## Required capabilities

A cooperating facility must either possess or coordinate access to all of the following before the complete R2 stack can be called executable:

- traceable broadband reference-detector calibration evidence;
- wavelength-resolved source spectra and declared reference/DUT responsivity curves;
- detector/source linearity characterization over the intended range;
- repeated reference-detector sweeps with session/day provenance;
- characterized electrical reference-step injection through the exact acquisition chain;
- repeated optical/DUT intensity-step transient acquisition;
- standard monotonic and frozen randomized-order `Voc`-intensity acquisition on the same qualified pixel;
- machine-readable raw exports, timestamps/configuration IDs, immutable source files, and SHA-256 manifesting.

A facility may be useful even if it does not satisfy every capability, but missing material evidence is `INCOMPLETE`, not a silent assumption of adequacy.

## Frozen configuration

The following identifiers are part of the scientific state, not optional administrative metadata:

`facility_id`, `source_id`, `reference_detector_id`, `smu_or_digitizer_id`, `range_id`, `filter_id`, `aperture_s`, `software_version`, `analysis_commit_sha`, `source_geometry_id`, `dut_fixture_id`.

Any material change requires either requalification or an explicit bridge study. Reusing a PASS from a materially different configuration is prohibited.

## Execution dependency graph

The machine contract freezes the following ordering:

1. freeze configuration;
2. packet preflight;
3. electrical-chain temporal-fidelity qualification;
4. optical/DUT settling qualification;
5. wavelength-resolved spectral-shape gate;
6. reference-repeatability training acquisition;
7. freeze estimator/QC/configuration/holdout scoring;
8. untouched prospective reference-repeatability holdout;
9. monotonic `Voc`-intensity acquisition;
10. randomized-order `Voc`-intensity acquisition;
11. combined uncertainty propagation.

This ordering is intentionally conservative. In particular, the untouched calibration holdout must not be used to tune the estimator, QC rules, or model basis.

## Status semantics

### PASS

All material evidence required by a gate is present and the frozen criterion passes.

### FAIL

Required evidence is present but a frozen criterion is violated. The failure remains in the public record and is not reclassified by post-hoc tuning. A revised method requires an explicitly new version and, where prospective validation is involved, new untouched data.

### INCOMPLETE

Material evidence or provenance is absent. Missing uncertainty terms, missing source files, or missing calibration applicability may not be represented as zero uncertainty or PASS.

## Statistical integrity

The hierarchy remains:

`lot -> substrate -> device/pixel -> session -> sweep or step replicate -> measurement`.

Repeated wavelengths, time samples, intensity points, pixels on one substrate, or sweeps in one session are not promoted to independent fabrication replicates. Any analysis that collapses this hierarchy must justify the approximation and cannot claim increased independent sample size merely from technical repeats.

## Data integrity

Raw and processed data remain separate. Every immutable source object is manifest-bound with SHA-256. Exclusions remain in the returned dataset with frozen reason codes. Corrected/processed products must link back to source hashes and analysis commit IDs.

Digest integrity establishes file identity, not authenticity of the facility, operator, or calibration issuer. Authentication remains a separate provenance problem.

## Null and conventional explanations

A completely qualified packet can still describe ordinary optical, electrical, thermal, contact, morphology, calibration, or statistical behavior. Passing the handoff contract only demonstrates that the measurement path is sufficiently specified to evaluate downstream hypotheses.

A facility qualification failure is therefore not a failure of the quantum-energy thesis. It is evidence that the measurement system or packet does not yet support the intended inference.

## Safety and environmental boundary

Facility SOPs, optical/electrical interlocks, source-duty limits, instrument ratings, thermal limits, chemical/material handling rules, and waste procedures are controlling. Randomized acquisition and qualification tests never override safety constraints.

No new materials or fabrication chemistry are introduced by v3.27.

## Agent/lab matching workflow

An agent evaluating a potential partner should:

1. compare publicly documented facility capabilities against the machine contract;
2. mark each capability `KNOWN_AVAILABLE`, `NEEDS_CONFIRMATION`, or `UNAVAILABLE` with source provenance;
3. never infer availability from a generic lab description when the exact metrology function is unclear;
4. identify the minimal missing capabilities and whether another facility can supply them without breaking configuration/provenance continuity;
5. present the lab with this contract and request confirmation before scheduling scientific acquisition;
6. record the final capability matrix in the repository before data collection.

## Reproducibility check

`tools/validate_r2_facility_capability_v3_27.py` checks:

- required capability IDs;
- evidence-role consistency;
- exact status semantics;
- frozen statistical hierarchy;
- dependency acyclicity and ordering;
- mandatory non-claims;
- SHA-256/raw-data/exclusion-retention integrity rules.

This validator verifies the contract structure only. It cannot certify that a real lab has the declared capability.

## Single best next increment

Prospectively score at least three real candidate facilities against the v3.27 machine contract using dated public evidence and direct-confirmation fields. The output should be a source-linked capability matrix, not a marketing ranking. Select a partner only after all decision-critical `NEEDS_CONFIRMATION` items are resolved or explicitly split across a provenance-preserving multi-facility workflow.
