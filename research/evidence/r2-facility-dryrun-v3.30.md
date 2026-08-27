# Evidence record — R2 facility dry-run packet v3.30

Date checked: 2026-08-27.

## Established repository evidence

The merged v3.27 machine contract defines seven required facility capability classes, 15 required packet roles, SHA-256/raw-source integrity requirements, `PASS/FAIL/INCOMPLETE` scientific gate semantics, execution dependencies, frozen configuration fields, and the statistical hierarchy used by R2.

Canonical source: `technical/data/r2_facility_capability_contract_v3_27.json` on `main`.

Open PR context reviewed: #7, #19, #20, #21. #19/#20 audit public facility evidence; #21 freezes direct-confirmation questions. None provides a candidate-independent executable packet interoperability test.

## New synthetic/software-verification claim

v3.30 claims only that the v3.27 packet contract can be represented and adversarially validated by committed standard-library software.

It does **not** establish real facility capability, measurement quality, R2 performance, EPC, open-quantum transport, or commercial performance.

## Exact finite-set calculation

The seven v3.27 capability classes reference 13 unique evidence roles. Two additional administrative roles (`analysis_freeze_record`, `packet_manifest`) yield 15 required roles total.

Independent implementation check: the validator reads `required_packet_roles` directly and separately reconstructs the union of all `evidence_roles`; exact equality and the expected administrative difference are required.

## Negative/adversarial results preserved by design

The self-test requires the following unfavorable cases to remain visible:

- missing required role -> `INCOMPLETE`;
- byte tamper -> `FAIL`;
- duplicate role -> `FAIL`;
- path traversal -> `FAIL`;
- complete synthetic packet -> `STRUCTURAL_PASS`, never scientific `PASS`.

## Conventional explanation / discriminator

Formatting success can be caused entirely by correct software packaging even when underlying measurements are scientifically poor. The discriminator is downstream evaluation of real measurements under the frozen scientific gates. Thus packet interoperability is necessary infrastructure, not mechanism evidence.

## Uncertainty boundary

No numerical measurement uncertainty is estimated. Real-facility capability remains epistemically unknown until direct evidence is supplied; missing material evidence stays `MISSING/INCOMPLETE` rather than being assigned an invented probability or zero uncertainty.
