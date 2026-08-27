# Evidence note — R2 facility packet preflight v3.22

## Established repository context

Merged R2 work already separates facility acquisition qualification from curvature uncertainty propagation. Open automation PRs #6/#7 estimate repeatability covariance, #8 preregisters prospective calibration holdout acquisition, and #9 represents absolute/reference systematics. None provides a packet-level integrity/completeness gate for a real facility handoff.

## Engineering assumption

A real facility packet should be rejected before scientific analysis if required raw/provenance objects are absent, byte hashes do not match, detector/source/configuration identities disagree, or metadata are detached from their claimed source objects.

## Synthetic/software verification

The committed adversarial suite uses only synthetic fixture content. It demonstrates the software state transitions `PASS`, `INCOMPLETE`, and `FAIL`; it is not experimental evidence.

## Falsifiable operational claim

Given a packet following the v3.22 manifest contract, any mutation of a manifested file without updating its digest is detected, and coordinated replacement of certificate/spectrum/linearity source bytes is detected unless the corresponding metadata source hash is also changed. This is an integrity claim about the implemented packet contract, not authenticity of the external issuer.

## Null / conventional boundary

Perfect packet integrity cannot exclude bad calibration, incomplete uncertainty models, source drift, thermal/contact effects, or ordinary device physics. Those remain downstream scientific questions.

## New external evidence

None. v3.22 adds software/provenance infrastructure and does not introduce a new literature-derived physical claim.
