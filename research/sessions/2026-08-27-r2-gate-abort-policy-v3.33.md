# Session — R2 gate abort/salvage policy v3.33

Date: 2026-08-27

## Increment

Added a dependency-aware execution policy that converts the merged v3.27 facility capability graph into explicit `PASS / FAIL / INCOMPLETE / BLOCKED` stop/continue semantics and evidence-salvage rules.

## Why this increment

Current main already contains the facility capability contract and prerequisite DAG. Open PR #24 addresses facility timing/quote planning; open PR #7 is superseded calibration-analysis provenance. Neither explicitly specifies what a facility/agent must do when a prerequisite fails while another branch remains independently executable.

## Files

- `technical/data/r2_gate_abort_policy_v3_33.json`
- `models/r2_gate_abort_policy_v3_33.py`
- `technical/r2-gate-abort-policy-v3.33.md`
- `research/evidence/r2-gate-abort-policy-v3.33.md`
- `research/sessions/2026-08-27-r2-gate-abort-policy-v3.33.md`
- `venture/v3.33-gate-abort-salvage-decision.md`
- `.github/workflows/r2-gate-abort-policy.yml`

## Verification design

The validator compares every v3.27 dependency-controlled gate with the v3.33 policy, requires exact set equality, checks acyclicity, and enumerates every local prerequisite combination over `{PASS, FAIL, INCOMPLETE}`. Adversarial examples verify that an optical-settling failure blocks Voc-intensity acquisition while leaving spectral/repeatability branches available, and that a failed prospective repeatability holdout blocks complete combined uncertainty propagation.

No stochastic values, vendor inputs, or experimental values are introduced.

## Claim boundary

This increment improves execution integrity. It does not establish device performance, mechanism, EPC, open-quantum transport, or commercial PV performance.

## Null/conventional explanation

Any blocked mechanism-facing acquisition may be caused entirely by conventional measurement-system deficiencies. The response is to preserve the diagnostic result, remediate, and rerun under a new recorded session/configuration—not to promote the failure into quantum evidence.

## Next best increment

Exercise the policy on a real facility dry-run/response packet. Record the first actual branch status vector, verify that the machine policy produces the same stop/continue decisions as human review, and version any newly discovered shared dependency before full R2 acquisition.
