# Session record — 2026-08-30 — v3.73 baseline stress capability

## Bounded increment

Advance the v3.72 dual-path stress-tomography experiment by inserting the preregistered A0/B0-only capability stage before A2/B2 unblinding.

## Changed evidentiary state

Before v3.73, the project had a four-arm stress design with deliberately deferred physical margins. After v3.73, another agent can feed real A0/B0 baseline exports into a standard-library analyzer that:

- collapses substrate summaries to fabrication-lot means;
- reports cell-level lot dispersion for A0/B0 under T/L;
- checks common lot history and required controls;
- computes a transparent future interaction-detection frontier over lot count and variance-inflation scenarios;
- fails closed instead of selecting a physical pass threshold.

No new project measurement is claimed.

## Quantitative synthetic verification

The frozen 5-lot software fixture gives:

- `s_A0,T = 0.0115974135` log-retention;
- `s_B0,T = 0.0191624633`;
- `s_A0,L = 0.00938083152`;
- `s_B0,L = 0.0167122709`;
- therefore `s_base = 0.0191624633`.

For two-sided alpha 0.05 and nominal power 0.80, using the explicit equal-variance planning proxy `m=1`:

- 3 future lots/arm -> MDE ratio-of-ratios departure ~6.40%;
- 5 -> ~4.92%;
- 7 -> ~4.14%;
- 9 -> ~3.64%;
- 12 -> ~3.15%.

These are software/planning numbers only. The treatment-arm variance and covariance are unknown.

## Independent checks

The CI path independently recomputes:

- cell lot means from the CSV;
- the maximum lot-level SD;
- the `m=1, n=5` MDE using `statistics.NormalDist` and a calculation path that does not import the production analyzer;
- fail-closed behavior when one calibration flag is changed to false.

## Nulls and failure modes

The capability stage can still fail because of:

1. donor-free eC9 film/electrical architecture instability;
2. lot-to-lot stress history mismatch;
3. contact/transport drift comparable to the future treatment effect;
4. optical/thickness drift;
5. baseline lot variance too large to resolve a useful interaction with feasible N;
6. treatment-arm variance later exceeding the baseline proxy.

A failed baseline capability run is a useful negative result and should stop A2/B2 unblinding.

## Statistical independence

Primary independent unit: fabrication lot. Substrates improve within-lot characterization but do not increase lot N. Technical repeats never count as independent samples.

## Next best increment

Run the exact v3.73 schema on real A0/B0 baseline exports. Freeze the smallest useful physical interaction margin, QC/exclusion limits and required lot count before A2/B2 labels are exposed. If A0 electrical architecture remains unqualified, run B0 electrical capability plus A0 optical/structural capability and keep the electrical interaction claim blocked.
