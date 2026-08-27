# Session record — 2026-08-27 — R2 instrument temporal fidelity v3.26

## Increment

Added a pre-DUT electrical acquisition-chain temporal-fidelity gate so timestamp, range, aperture, filtering, and acquisition lag cannot be silently folded into source/DUT settling.

## Repo-state check

Read required main-branch governance/specification files and all open automation PRs before acting. Existing open work already covers calibration covariance/holdout, external calibration systematics, facility packet integrity, wavelength-resolved spectral mismatch, randomized acquisition-order drift, and optical/DUT settling. v3.26 is intentionally orthogonal.

## Quantitative decision

Open v3.25 derives a 69.5369142 uV total pointwise settling envelope. v3.26 provisionally allocates 20% = 13.9073828 uV to electrical acquisition-chain temporal error. The 20% allocation is an engineering assumption and must be revisited if v3.25 changes during review.

For a first-order electrical path, independent analytic dwell is

`t_min = d + tau ln(A/V_inst)`.

At synthetic `A=0.1 V`, zero delay, tau=0.05/0.1/0.2/0.5/1/2 s gives 0.3636/0.7271/1.4542/3.6355/7.2711/14.5421 s. These are software/planning results only.

## Verification

Adversarial test requirements:
- analytic first-order dwell frozen to 1e-12 s in the tau=0.2 s, d=0.05 s case;
- sampled nonparametric gate cannot qualify earlier than analytic limit;
- tau=2 s path fails a 3 s observation window;
- <6 replicates -> INCOMPLETE;
- autorange -> FAIL;
- ideal zero-residual path -> immediate qualification;
- diagnostic fitted tau recovers the injected value within 2%.

RNG seed `20260827`; Python standard library only.

## Negative / null result preserved

A slow apparent optical-step response is not automatically DUT dynamics. The instrument chain can create lag; filtering can also hide fast overshoot. Therefore optical settling evidence is incomplete until the electrical path is independently characterized under the exact same acquisition settings.

## Statistical independence

Transient time samples are correlated; replicate electrical steps are technical repeats and do not increase independent DUT/substrate count.

## Unresolved risks

- the reference electrical step itself needs characterized waveform uncertainty;
- correlated filter impulse-response uncertainty is not yet modeled;
- firmware buffering/compliance transitions may not be exposed by a simple first-order diagnostic;
- the budget depends on open v3.25 review outcome;
- no real acquisition chain has yet been tested.

## Next best increment

Run the gate on a real characterized ~100 mV electrical step through the exact intended R2 SMU/digitizer/cabling/software configuration, then lock those settings before optical/DUT settling acquisition.
