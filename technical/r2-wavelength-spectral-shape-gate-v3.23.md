# R2 wavelength-resolved spectral-shape gate v3.23

## Purpose and claim boundary

v3.23 closes a metrology gap left by the merged v3.17/v3.18 R2 stack and the currently open repeatability/systematic/preflight PRs: **the source spectrum may change shape as nominal irradiance is swept from 0.05 to 2 sun even when a scalar reference detector signal is well behaved**.

The tool qualifies only the declared source spectra and the declared reference/DUT spectral responsivities. `PASS` is not evidence for EPC, a recombination mechanism, or open-quantum transport.

## External basis

Sources checked 2026-08-27:

- IEC 60904-7:2019 describes correction of spectral-mismatch error arising jointly from the test/reference spectra and reference/DUT spectral responsivities; IEC lists the 2019 edition with stability date 2031: https://webstore.iec.ch/en/publication/26502
- NIST's photovoltaic spectral-responsivity paper gives the mismatch factor explicitly and states that it corrects both reference-vs-test device spectral-response mismatch and illumination-vs-reference-spectrum mismatch: https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=915586
- NIST SRI 6014 describes a calibrated reference photovoltaic cell whose irradiance spectral responsivity is traceable to SI through the NIST differential spectral responsivity method: https://www.nist.gov/sri/standard-reference-instruments/sri-6014-calibrated-reference-photovoltaic-cell
- NIST's photovoltaic characterization laboratory states that spectral irradiance measurements are used for spectral-mismatch calculations: https://www.nist.gov/laboratories/tools-instruments/photovoltaic-characterization-laboratory
- IEC TR 63228:2019 specifically notes unusual spectral responsivity, optical interference, nonlinearity, and other measurement challenges for OPV/perovskite/emerging PV devices: https://webstore.iec.ch/en/publication/64040

These references support the measurement method only. They do not support any R2 performance value.

## Input contract

The deterministic fixture generator emits three machine-readable CSVs:

1. source spectra: `spectrum_id,target_suns,wavelength_nm,spectral_irradiance_W_m2_nm`;
2. responsivity: `wavelength_nm,reference_responsivity_A_W,dut_responsivity_A_W`;
3. uncertainty components: `component_id,quantity,spectrum_id,wavelength_nm,loading_1sigma,note`.

All spectra must use one identical strictly increasing wavelength grid. The implementation intentionally refuses hidden interpolation because interpolation/model uncertainty is facility-specific and should be explicit rather than silently introduced.

The committed synthetic responsivity curves are analytic test shapes, not PM6:Y6 measurements and not a NIST device calibration.

Rows sharing `component_id` represent one correlated standard-normal latent component. This preserves systematic/common spectral modes rather than treating wavelength bins as independent samples.

## Governing equation

For test/source spectrum `E_s(lambda)`, reference spectrum `E_0(lambda)`, reference responsivity `R_r(lambda)`, and DUT responsivity `R_t(lambda)`,

`M_s = [int E_s R_t d lambda / int E_s R_r d lambda] * [int E_0 R_r d lambda / int E_0 R_t d lambda]`.

Every integral has units `(W m^-2 nm^-1)*(A W^-1)*nm = A m^-2`, so each ratio and `M_s` are dimensionless.

If the reference detector sets nominal irradiance ratio `Phi_ref`, the DUT-generation-equivalent axis is

`Phi_eff,s = Phi_ref,s * M_s`.

Therefore spectrum-dependent `M_s` is a distortion of the `ln(Phi)` axis used by the frozen local-ideality curvature estimator.

## Frozen R2 propagation

For synthetic software verification only, the frozen reference curve has `Delta_n_curv=0.10`.

`bias = Delta_n_curv(Phi_ref*M) - Delta_n_curv(Phi_ref)`.

Current project engineering limits are:

- `max |M_s-1| <= 0.01` — inherited provisional mismatch-deviation gate from v3.17;
- `|spectral curvature bias| <= 0.01` — inherited calibration-curvature-bias gate;
- `u_spectral(Delta_n_curv) <= 0.01` — v3.23 provisional engineering precision gate.

These are project gates, not IEC or NIST requirements.

## Covariance propagation

For latent component `k` with standard-normal amplitude `z_k`, source and responsivity inputs are perturbed multiplicatively in log space. The code evaluates

`l_sk = d ln(M_s)/d z_k`

by centered finite difference at `eps=1e-4`. The resulting `l_sk` is the signed loading that can be transferred into a v3.18 `ln_calibrated_suns` sidecar.

With curvature-axis sensitivity `g_s = d Delta_n_curv / d ln(Phi_eff,s)`, first-order variance is

`u_Delta^2 = sum_k [sum_s g_s l_sk]^2`.

No `sqrt(N)` credit is assigned to wavelength bins, spectra, or repeated measurements.

## Required limiting cases

1. Pure source scaling, `E_s(lambda)=a_s E_0(lambda)`, gives `M_s=1`.
2. Identical responsivities, `R_r(lambda)=R_t(lambda)`, give `M_s=1` for arbitrary source spectral shape.
3. One common multiplicative source radiometric-scale uncertainty is numerically invisible to `M_s`.

All three are enforced by the adversarial test.

## Synthetic fixture inputs

Deterministic analytic fixture, with no randomness in generation:

- 17-point 0.05–2 sun geometric target grid;
- 400–900 nm in 10 nm steps;
- two smooth synthetic source bands plus background;
- broad synthetic reference responsivity and a different synthetic DUT responsivity;
- intensity-dependent blue/red source-shape perturbation;
- four synthetic covariance modes: common source scale, source intensity/shape, reference-responsivity tilt, DUT-responsivity tilt.

`models/r2_spectral_shape_fixture_generator_v3_23.py` regenerates the input tables. CI compares generated-result metrics with the committed expected-output CSV.

## Synthetic verification outputs

Software-verification values only:

- maximum `|M_s-1| = 0.003180480548` (0.3180%);
- synthetic curvature bias `= +0.001215076355`;
- first-order spectral `u(Delta_n_curv) = 1.739868419e-05`;
- common-source-scale curvature loading `<1e-12`.

Independent nonlinear Monte Carlo:

- Python standard library RNG;
- seed `20260827`;
- 12,000 draws;
- nonlinear `u(Delta_n_curv)=1.737721670e-05`;
- relative difference from first order `=0.0012338573` (0.1234%);
- frozen tolerance `<=3%`.

This cross-check validates the synthetic numerical implementation only, not a physical R2 result.

## Sensitivity

| Shape factor | max `|M-1|` | synthetic curvature bias | decision |
|---:|---:|---:|---|
| 0 | ~0 | ~0 | PASS |
| 0.5 | 0.001650 | 0.000642 | PASS |
| 1 | 0.003180 | 0.001215 | PASS |
| 2 | 0.005929 | 0.002186 | PASS |
| 4 | 0.010440 | 0.003581 | FAIL mismatch-deviation gate |

Thus the synthetic decision is stable through 2x the nominal distortion but not 4x. This does not define a real-facility tolerance distribution.

## Statistical independence

Wavelength samples are quadrature points, not experimental replicates. The 17 intensity spectra are points within one source sweep unless the acquisition hierarchy says otherwise. Multiple scans of one source state are technical repeats. The existing lot -> substrate -> pixel -> session -> sweep -> intensity hierarchy remains controlling for DUT inference.

## Conventional/null explanations

An intensity-dependent `M_s` can arise from ordinary LED-channel weighting, lamp temperature, neutral-density-filter transmission, attenuator behavior, source heating, spectroradiometer nonlinearity, detector responsivity mismatch, range switching, geometry, or calibration interpolation. Such a result is a measurement-system effect and is not DUT physics.

The discriminator is wavelength-resolved source measurement plus independently calibrated reference/DUT responsivity under the actual source/attenuator/configuration.

## Stop / narrow rules

Do not treat `Voc`-intensity curvature as confirmatory if relevant source spectra or responsivities are missing, nominal mismatch/bias gates fail, spectral uncertainty fails its gate, nonlinear Monte Carlo differs from first-order propagation by >3% at the declared uncertainty magnitude, or source/attenuator/configuration changes without requalification.

## Best next experiment

At a cooperating facility, record the actual wavelength-resolved source spectrum at every frozen 0.05–2 sun intensity point with the same source/attenuator configuration used for `Voc`. Pair it with traceable reference-detector responsivity and measured R2 EQE/spectral responsivity. Run v3.23 before inspecting the DUT curvature result.