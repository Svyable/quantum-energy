# R2 reference-detector repeatability campaign v3.20

## Purpose and claim boundary

This preregisters a **prospective facility calibration campaign** that can validate whichever v3.19 empirical covariance estimator survives human review. It deliberately does not duplicate the two open v3.19 implementation PRs.

Passing this campaign can support a claim that the declared reference-detector repeatability model transfers to untouched sessions under the frozen facility configuration. It cannot establish DUT physics, EPC, open-quantum transport, absolute detector calibration accuracy, or facility-to-facility transfer.

## Evidence classes

**Established metrology evidence.** NIST Dataplot documents the balanced/unbalanced one-way random-effects variance-component estimator `max(0,(MSTR-MSE)/n0)`. NIST TN 1297 requires uncertainty components and relevant covariances to be represented in the measurement model and distinguishes statistically evaluated Type-A components from other uncertainty sources.

Sources checked 2026-08-26 America/Chicago:
- https://itl.nist.gov/div898/software/dataplot/refman1/auxillar/onewayan.htm
- https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-5-combined-standard-uncertainty
- https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty

**Engineering assumptions.** The session/sweep design, 24+6 partition, four sweeps/session, six training day-blocks, two holdout day-blocks, and the 30% planning precision gate are project choices. They are not NIST requirements.

**Synthetic/model results.** The committed Monte Carlo precision table is a planning calculation only.

## Experimental hierarchy

The calibration hierarchy is

`campaign -> day block -> session -> sweep -> intensity point`.

The 30 sessions are the repeatability units for session-level variation. Sweeps and intensity points are technical repeats and must not be counted as 120 or 2,040 independent sessions.

The training/holdout split is:
- sessions 1–24: **training**, acquired across six day blocks, four sessions/day;
- sessions 25–30: **prospective holdout**, acquired only after the estimator version/hash, basis, QC/exclusions, and scoring rule are frozen, across two additional day blocks, three sessions/day.

If the holdout fails, those six sessions become a documented negative result. They may inform redesign, but they may not be relabeled as a new validation set. A redesigned model requires a new untouched prospective holdout.

## Per-session acquisition

Each session contains exactly four full 17-point calibration sweeps:
- two ascending;
- two descending;
- within-session sweep order randomized from seed `20260826` in the committed schedule generator.

Each sweep requires:
1. pre-sweep dark/background record;
2. pre-sweep 1-sun reference anchor;
3. full 17-point grid;
4. post-sweep 1-sun reference anchor;
5. post-sweep dark/background record.

Detector gain state, source-spectrum ID/hash, reference-detector ID, geometry state, detector temperature, ambient temperature, raw signal units, operator/automation identity, and deviations are recorded. A detector/source/geometry/software configuration change creates a new campaign population unless the change itself was preregistered as a factor.

## Raw-data schema

Canonical raw schema:

`technical/data/r2_reference_repeatability_template_v3_20.csv`

`row_type` is one of `dark_pre`, `anchor_pre`, `grid`, `anchor_post`, `dark_post`. `qc_status` is frozen before model fitting. `exclusion_code` is blank unless one of the preregistered rules below applies.

### Predefined QC / exclusions

Exclude a sweep from the covariance fit only for:
- missing required raw or provenance fields;
- nonpositive target/calibrated intensity at a grid point;
- detector saturation/overrange declared by the instrument;
- source/detector/geometry configuration mismatch relative to the campaign lock;
- failed pre/post dark or anchor acquisition;
- explicit acquisition interruption or instrument fault recorded before analysis.

Do **not** exclude a sweep for a large residual, unfavorable covariance estimate, failed holdout score, or because it weakens a desired scientific conclusion. All excluded rows remain in the raw file with reason codes.

## Governing planning model

For session `s` and sweep `j`, the normalized planning model is

`y_sj = mu + A_s + e_sj`,

where:
- `A_s ~ Normal(0, sigma_between^2)` is session-level variation;
- `e_sj ~ Normal(0, sigma_within^2)` is sweep-level variation;
- `m = 4` sweeps/session.

All quantities in the planning simulation are dimensionless because they represent normalized log-intensity error. The relevant sensitivity coordinate is

`r = sigma_within / sigma_between`.

For a balanced one-way random-effects design,

`hat(sigma_between^2) = max(0, [MS_between - MS_within] / m)`.

Dimensional check: both mean squares have units of `y^2`; division by dimensionless `m` leaves a variance in `y^2`.

Known-limit/independent algebraic check:

`E[MS_between] = sigma_within^2 + m sigma_between^2`

and

`E[MS_within] = sigma_within^2`,

so the unconstrained method-of-moments difference targets `sigma_between^2`. The nonnegative truncation is a parameter-boundary rule, not proof that a true variance is zero.

## Finite-sample planning result

Executable source:

`models/r2_calibration_campaign_design_v3_20.py`

Frozen software assumptions:
- Python standard library only;
- RNG seed `20260826`;
- 20,000 synthetic campaigns per `(session count, r)` cell;
- candidate session counts `12,16,20,24,30`;
- `r = 0.25,0.50,0.75,1.00,1.50`;
- four sweeps/session.

Frozen CSV output:

`models/fixtures/r2_calibration_campaign_precision_v3_20.csv`

At 24 training sessions:
- `r=0.75`: 90th percentile absolute relative error of the estimated session SD = `0.27918`;
- `r=1.00`: corresponding value = `0.31115`.

At 30 sessions and `r=1.00` it is `0.27457`.

The simulated **variance** estimator remains near its known expectation: for 24 sessions the mean estimated variance / true variance is `0.9971` at `r=0.75` and `1.0015` at `r=1.00`. The SD estimator is slightly downward biased because of the square root, as expected.

### Decision implication

The 24-session training count is a conditional precision target: the planning 90th-percentile relative-error gate of 30% is met at `r<=0.75`, but not at `r=1.0` in the frozen simulation. Therefore the six holdout sessions serve two purposes: prospective transfer validation and, only **after** successful validation, additional information for the final production covariance estimate.

If real training data show within-session variability comparable to or larger than between-session variability, the program must not overstate session-covariance precision. Increase independent sessions or redesign the measurement path.

## Prospective freeze point

After session 24 and **before session 25** commit or archive:
- exact estimator implementation and commit hash;
- covariance basis/model form;
- systematic correction policy;
- QC/exclusion list;
- reference-detector calibration certificate/version;
- source/detector/geometry/software configuration hashes or identifiers;
- holdout scoring metrics and pass/fail thresholds;
- output schema.

No holdout row may be opened for model tuning before that freeze record exists.

## Holdout scoring requirements

The merged v3.19 implementation may define the exact standardized-residual/coverage metrics, but the following campaign-level rules are invariant:
- all six sessions must be scored with the frozen code without refitting;
- results are reported for every PASS/QC-eligible holdout sweep;
- ascending and descending sweeps are reported separately as a direction diagnostic;
- day-block and session identity remain visible;
- calibration-model failure is `FAIL/INCOMPLETE`, not a reason to alter the holdout partition;
- only after the frozen holdout decision is recorded may all 30 sessions be refit for a production covariance estimate.

## Conventional explanations / discriminators

A calibration covariance mode can arise from ordinary source regulation, detector nonlinearity, range switching, spectral drift, detector temperature, geometry, electronics, interpolation, or operator/session setup. The discriminator is repeat/reference data acquired independently of the DUT plus logged source/detector state.

Even a successful calibration campaign only removes or bounds a measurement-system explanation; it does not establish a specific DUT mechanism.

## Safety / environmental note

This protocol adds measurement time but no new material synthesis. Facility-specific electrical, optical-source, UV/NIR, thermal, vacuum, and laser/source safety SOPs remain controlling. No source should be operated outside its approved interlock/enclosure conditions for the sake of completing the randomized schedule.

## Kill / narrow rules

Narrow or stop the current covariance model if:
- training or holdout sessions show configuration nonstationarity;
- a direction effect remains after the declared model;
- the held-out sessions fail the frozen predictive score;
- a variance component repeatedly lands on the zero boundary while residual structure remains;
- systematic mean calibration shape is left uncorrected/unbudgeted;
- absolute reference-detector systematic uncertainty is missing;
- the measurement chain changes between training and holdout.

## Best next action after merge

Execute the 24-training + 6-heldout campaign at the first cooperating facility. Human review should first choose or reconcile the two open v3.19 estimator PRs so the exact freeze/scoring implementation is singular before session 25.
