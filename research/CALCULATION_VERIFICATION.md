# Calculation and Assumption Verification Protocol

This protocol applies to every quantitative result used in a scientific, engineering, manufacturing, or investor-facing claim.

## A. Input provenance

For each calculation record:

- symbol / variable name;
- value and unit;
- uncertainty or tolerance;
- source and source date/version;
- whether the value is measured, literature-derived, vendor-specified, fitted, assumed, or synthetic;
- transformation applied before use.

Never silently promote a planning value into an established material constant or measured result.

## B. Equation audit

Before accepting a result:

1. Write the governing equation explicitly.
2. Define every symbol.
3. Convert inputs to a consistent unit system, preferably SI internally.
4. Perform a dimensional-analysis check.
5. Check limiting cases and sign conventions.
6. State the validity regime of the equation/model.
7. Where multiple physical models are plausible, compute at least one competing model or explain why it is not applicable.

## C. Independent numerical check

Decision-driving calculations require two calculation paths whenever practical:

- primary executable implementation; and
- independent recomputation using a separate implementation, algebraic derivation, benchmark, or trusted reference case.

Agreement tolerance must be stated before interpreting the result. Copying the same formula into two cells is not an independent check.

## D. Numerical integrity

Executable work should record:

- software/runtime and relevant package versions;
- random seed for stochastic work;
- numerical tolerances and convergence criteria;
- mesh/time-step/sample-size sensitivity where relevant;
- conservation-law or normalization checks where relevant;
- machine-readable input and output files.

For transfer-matrix/open-quantum models, explicitly test conservation/normalization, known limiting cases, and convergence. Nonphysical outputs are failures, not results to smooth away.

## E. Uncertainty and sensitivity

For any result that controls a gate, cost, performance claim, or mechanism inference:

- propagate known measurement uncertainties;
- identify correlated/systematic terms separately from independent random terms;
- sweep influential assumptions over a defensible range;
- report which parameters dominate output uncertainty;
- distinguish confidence/credible intervals from engineering tolerance bands;
- state whether the decision changes anywhere inside the uncertainty range.

If a conclusion changes under a plausible input range, report it as conditional.

## F. Statistical integrity

- Preserve experimental hierarchy: lot → substrate → device/pixel → session → measurement.
- Do not count correlated pixels or repeated measurements as independent fabrication replicates.
- Predefine exclusions and outlier handling.
- Report all functional devices unless a preregistered QC rule excludes them.
- Prefer confidence bounds and effect sizes over threshold-only p-value language.
- For small-N models, favor low-dimensional/interpretable models and leave-one-group-out or prospective validation over high-capacity fitting.
- Synthetic power studies must be labeled synthetic and include their data-generating assumptions.

## G. Assumption register

Each material engineering assumption should include:

- assumption statement;
- numerical range if quantitative;
- origin/reason;
- consequence if wrong;
- experiment or source that could retire it;
- status: open / bounded / retired / falsified.

A repeated assumption does not become evidence through repetition.

## H. Claim-to-evidence audit

Before publication, trace each strong sentence to the smallest supporting evidence set. Check that:

- cited work actually supports the statement;
- the cited result applies to the material/device/regime claimed;
- correlation is not described as mechanism;
- a vendor specification is not described as independently verified performance;
- an accelerated-aging result is not converted directly into field lifetime without a validated acceleration model;
- modeled/synthetic values are not described as experimental measurements;
- prospective IP language does not become an unsupported novelty/FTO claim.

## I. Correction protocol

When an error is found:

1. Do not hide or silently overwrite the scientific history.
2. Add a correction note describing the error, affected files/claims, and impact.
3. Recompute downstream results.
4. Mark superseded assumptions/results explicitly.
5. Update the evidence map and any investor-facing summary affected by the correction.
6. Include the correction prominently in the PR body.

## J. Review checklist

A publication/release reviewer should be able to answer yes to all applicable items:

- [ ] Inputs are sourced and units are explicit.
- [ ] Dimensional analysis passes.
- [ ] Nominal arithmetic/code reruns.
- [ ] Independent cross-check agrees within the frozen tolerance.
- [ ] Limiting cases/conservation checks pass.
- [ ] Uncertainty and sensitivity are reported.
- [ ] Experimental hierarchy and sample size are represented correctly.
- [ ] Assumptions are labeled and falsifiable where possible.
- [ ] Null/conventional explanations were tested or bounded.
- [ ] Raw/minimally processed data and processing path are retained.
- [ ] Strong claims do not exceed the evidence level.
- [ ] Known negative results and corrections remain visible.
