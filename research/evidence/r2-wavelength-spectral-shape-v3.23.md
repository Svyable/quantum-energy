# Evidence note — R2 wavelength-resolved spectral mismatch v3.23

## Established evidence

Sources checked 2026-08-27.

1. IEC 60904-7:2019 describes spectral-mismatch correction arising jointly from test/reference spectra and reference/DUT spectral responsivities. IEC lists the 2019 fourth edition with stability date 2031.
   - https://webstore.iec.ch/en/publication/26502
2. NIST gives the PV spectral mismatch factor explicitly as the product of source-weighted test/reference responsivity ratio and reference-spectrum-weighted inverse ratio.
   - https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=915586
3. NIST SRI 6014 provides an example of an SI-traceable photovoltaic reference cell with calibrated irradiance spectral responsivity.
   - https://www.nist.gov/sri/standard-reference-instruments/sri-6014-calibrated-reference-photovoltaic-cell
4. NIST states that spectroradiometer irradiance measurements are used for spectral mismatch calculations in its photovoltaic characterization laboratory.
   - https://www.nist.gov/laboratories/tools-instruments/photovoltaic-characterization-laboratory
5. IEC TR 63228:2019 identifies unusual spectral responsivity, optical interference, temporal instability, and irradiance nonlinearity as measurement challenges relevant to emerging PV including OPV.
   - https://webstore.iec.ch/en/publication/64040

These sources establish metrology methodology only. They provide no R2 performance or mechanism evidence.

## Engineering assumptions

- The IEC mismatch formalism is an appropriate measurement-model basis for diagnosing the R2 reference-detector/DUT source-spectrum axis.
- Exact common wavelength grids are required in v3.23 rather than silently interpolating facility data.
- The existing project gates `|SMM-1|<=1%` and `|curvature bias|<=0.01` remain planning gates, not standard requirements.
- `u_spectral(Delta_n_curv)<=0.01` is a new provisional project gate.
- Different latent `component_id` values are independent unless a richer factorization is supplied.

## Falsifiable hypothesis

Across the frozen R2 0.05–2 sun sweep, wavelength-resolved spectral mismatch between the reference detector and DUT remains small enough that both nominal axis-curvature bias and propagated spectral uncertainty stay inside the preregistered project gates.

A failure is informative: it means a source/attenuator/spectral-response artifact can explain part of the apparent `Voc`-intensity curvature and must be corrected before mechanism inference.

## Synthetic/model result

The committed analytic stress fixture has maximum `|M-1|=0.00318048`, curvature bias `+0.00121508`, and first-order spectral curvature uncertainty `1.73987e-05`. A 12,000-draw independent nonlinear Monte Carlo with seed `20260827` gives `1.73772e-05`, a 0.123% difference.

These numbers are synthetic software checks, not measured facility properties.

## Conventional explanations preserved

LED-channel rebalance, lamp/source heating, filter wavelength dependence, source regulation, spectroradiometer nonlinearity, detector responsivity mismatch, geometry, electronics, and calibration interpolation can all generate intensity-dependent spectral mismatch. None is evidence for EPC/open-quantum transport.

## Novelty boundary

The spectral-mismatch calculation itself is established metrology and is not claimed as an invention. The project-specific contribution is an open executable integration of wavelength-resolved mismatch, signed covariance modes, and the frozen R2 curvature gate.