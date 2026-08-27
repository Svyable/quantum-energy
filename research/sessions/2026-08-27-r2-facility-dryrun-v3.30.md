# 2026-08-27 — R2 facility dry-run packet v3.30

## Increment

Added a candidate-independent, synthetic dry-run packet contract and validator that exercises every required v3.27 R2 facility packet role before real facility evidence is accepted.

## Why this increment

The current open automation work already covers an older calibration estimator (#7), duplicate public facility audits (#19/#20), and a frozen facility confirmation questionnaire (#21). Creating another facility audit or questionnaire would duplicate open work. The uncovered integration risk is that a candidate may answer “yes” yet be unable to return a provenance-safe packet matching the merged v3.27 machine contract.

## Claim classes

- **Established repository evidence:** v3.27 defines seven capabilities and 15 packet roles.
- **Engineering assumption:** a pre-measurement synthetic packet rehearsal can expose export/provenance incompatibilities cheaply.
- **Falsifiable operational hypothesis:** a cooperating facility that claims the needed capabilities can produce a structurally valid dry-run packet without undocumented transformations.
- **Synthetic/software result:** the committed self-test is designed to generate a deterministic 15-role synthetic packet and reject five adversarial conditions.
- **Experimental result:** none.
- **Novel invention concept:** none.

## Calculation verification

Decision-driving finite-set calculation:

`R = |union capability evidence roles| + |administrative roles| = 13 + 2 = 15`.

Units: counts; dimensionless.

Independent check is implemented by comparing the explicit v3.27 `required_packet_roles` set against a separately reconstructed capability-role union plus exactly `{analysis_freeze_record, packet_manifest}`. Tolerance: exact equality.

No stochastic calculation is used; no seed or convergence setting applies.

## Adversarial cases

Frozen self-test expectations:

1. complete deterministic synthetic packet -> `STRUCTURAL_PASS`;
2. missing `source_spectrum_data` row -> `INCOMPLETE`;
3. mutate bytes in `voc_intensity_raw` after manifest creation -> `FAIL`;
4. duplicate a manifest role -> `FAIL`;
5. replace a safe path with `../escape.txt` -> `FAIL`;
6. synthetic packet must never return plain `PASS`.

## Uncertainty / sensitivity

No measurement uncertainty is calculated. Facility capability uncertainty is epistemic and stays represented by missing evidence rather than probabilistic scoring.

The structural decision is maximally sensitive to any required role: one missing role keeps the packet incomplete; one integrity violation fails it. This non-compensatory behavior is intentional because the downstream experimental gates depend on specific prerequisite evidence.

## Statistical independence

Manifest rows and packet files do not create experimental sample size. The v3.27 hierarchy remains unchanged: lot -> substrate -> device/pixel -> session -> sweep or step replicate -> measurement.

## Conventional explanation

A packet can pass structural validation while containing bad measurements. Therefore v3.30 tests packaging/integrity only; real scientific gates remain the discriminator for metrology and mechanism claims.

## Safety / environmental

No physical experiment or shipment is authorized. Real facility EHS and instrument constraints remain controlling.

## Correction history

No earlier numerical/scientific result is corrected. Facility-integration interpretation is narrowed: a positive questionnaire response is insufficient without a dry-run evidence packet that demonstrates the promised export/provenance interface.

## Next increment

After review of #21, apply v3.30 unchanged to the first candidate’s example/dry-run export before scheduling scientific acquisition. Preserve unavailable roles as `MISSING/INCOMPLETE` and build only explicit, versioned adapters for documented format differences.
