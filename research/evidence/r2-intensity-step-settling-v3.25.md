# Evidence note — R2 intensity-step settling v3.25

## Established evidence

- IEC TR 63228:2019 explicitly identifies instability with time and transient response to external stimulus as measurement challenges for emerging photovoltaic technologies including OPV. Source checked 2026-08-27: https://webstore.iec.ch/en/publication/64040
- NIST measurement terminology defines response time as the interval after an abrupt stimulus change until the response reaches and remains within specified limits around the final steady value. Source checked 2026-08-27: https://www.nist.gov/document/nist-tn-1551pdf
- NIST has longstanding step-response/transient-measurement methodology using measured system response rather than assuming instantaneous acquisition. Source checked 2026-08-27: https://www.nist.gov/publications/characterizing-transient-measurements-use-step-response-and-convolution-integral

These sources support the metrology principle. They do not report R2 response times, R2 performance, or any quantum mechanism.

## Engineering assumptions

- The existing project curvature-bias scale `|delta Delta_n_curv| <= 0.01` is retained as the allowable total settling-alias budget for this preflight.
- At least six repeated transients per required step class and at least six elapsed-time samples are initial operational minimums, not standards-derived sample-size requirements.
- The final three elapsed-time points are used as a provisional plateau estimator, with a separate late-window trend guard.
- The 95% normal multiplier is an engineering upper-envelope construction; it is not claimed as a fully calibrated confidence interval for arbitrary correlated/non-Gaussian transients.

## Synthetic/model results — not experimental evidence

For the frozen 17-point 0.05–2 sun geometric intensity grid and 7-point quadratic local-ideality estimator:

- numerical `||w||_1 = 143.8085097637075 V^-1`;
- independent analytic geometric-grid derivation gives the same value within `1e-10`;
- a curvature-bias budget of `0.01` therefore implies a conservative pointwise settling envelope of `69.536914 microvolt`;
- an idealized `n=1`, 300 K full-span `Voc` step is `0.0953649108583 V`;
- under a single-exponential synthetic transient, `tau=2 s` requires `14.4472164568 s` to fall below that envelope;
- dwell scales linearly with `tau` in that limiting model.

These are synthetic planning/verification calculations only.

## Falsifiable hypothesis

Under the exact source/detector/DUT/configuration used for randomized-order R2 acquisition, repeated large intensity steps will demonstrate a finite dwell after which the mean residual transient plus its uncertainty stays inside the curvature-derived voltage envelope at every later sampled time.

Failure means the static randomized-order `Voc(Phi)` interpretation must be narrowed or the acquisition protocol must be redesigned around the observed dynamics.

## Conventional/null explanations

Source regulation/heating, detector response, SMU filtering/autorange, device capacitance, trapping/photodoping, contact equilibration, thermal evolution, degradation, and spectral transients can all produce settling behavior. A measured time constant is therefore an acquisition-path observation, not mechanism evidence.

## Negative-result policy

- A transient that remains outside the envelope is a `FAIL`, not an outlier.
- A long late tail cannot be extrapolated into a pass with a convenient exponential fit.
- Fewer than the minimum repeated steps or an incomplete time grid is `INCOMPLETE`.
- If no practical dwell exists, the program must preserve that result and treat the measurement as history-dependent rather than forcing a static curvature claim.
