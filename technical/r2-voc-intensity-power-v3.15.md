# R2 light-intensity grid and measurement-power preregistration — v3.15

## Status

This is a **planning and preregistration artifact**, not an experimental result.

It converts the v3.14 real-data local-ideality benchmark into an executable R2
measurement design. The primary purpose is to ensure that the planned
`Voc`-versus-light-intensity measurement has enough information to detect a
predeclared curvature signal without confusing technical repeats with
independent devices.

## Scientific boundary

Local ideality curvature is not a unique mechanism label. Surface/contact
recombination, transport resistance, energetic disorder, carrier-density
dependent recombination, state filling, and mixtures can all produce curvature.
The result remains a discriminator to be interpreted jointly with FTPS/sEQE,
injection-resolved EL, temperature dependence, and controls.

## Frozen grid

Primary R2 grid: **17 geometrically spaced intensities from 0.05 to 2.0 suns**.

The spacing ratio is

`r = (2.0 / 0.05)^(1/16) = 1.259298684`.

The grid therefore places analysis anchors at approximately:

- low anchor: `0.099851882 suns`;
- high anchor: `1.001483382 suns`.

The primary local estimator remains the v3.14 7-point quadratic derivative in
`x = ln(Phi)`. The 9-point estimator remains a mandatory smoothing sensitivity.

A 17-point grid was selected over the 13/15/19-point planning alternatives
because it retains a 7-point local support span of about **3.99× in intensity**,
close to the density of the published v3.14 benchmark, while maintaining high
planning power at the 0.5 mV point-noise gate. A 15-point grid has slightly
better pure slope-noise power in the chosen anchor contrast but broadens the
7-point local support to about 4.86×; 19 points improve locality but add dose and
increase slope-noise for a fixed seven-point window.

## Primary curvature observable

Define

`Delta_n_curv = n_id(Phi ~= 1 sun) - n_id(Phi ~= 0.1 sun)`.

For the local quadratic estimator,

`n_id = [dVoc / d ln(Phi)] / (k_B T / q)`.

Because the fitted derivative is linear in the measured `Voc` values, the
contrast can be written

`Delta_n_curv = sum_i w_i Voc_i`.

With independent point-estimate uncertainty `sigma_V`,

`SE(Delta_n_curv) = sigma_V * sqrt(sum_i w_i^2)`.

The weights have units `V^-1`, so `SE(Delta_n_curv)` is dimensionless.

The primary two-sided planning test uses alpha=0.05. The v3.15 script calculates
power both analytically from the normal distribution and independently by Monte
Carlo.

## Effect-size assumption

The **minimum planning effect is |Delta_n_curv| = 0.10**.

This is an engineering assumption, not an established physical threshold. It is
chosen as a material curvature signal smaller than the roughly 0.19 difference
between the low- and high-illumination global slopes observed in the external
PM6:Y12 benchmark used in v3.13. R2 may have a smaller, larger, or absent effect.

Sensitivity results are also reported for 0.05 and 0.15.

## Point-level metrology gate

The confirmatory curvature label requires an empirically demonstrated
**point-estimate `Voc` uncertainty <= 0.5 mV SD** under the actual R2 acquisition
protocol.

At the 17-point grid, 300 K and `sigma_V=0.5 mV`:

- 7-point `SE(Delta_n_curv) = 0.0224201`;
- analytic power for a true 0.10 contrast = **0.993796**;
- independent 30,000-repetition Monte Carlo power = **0.992733**;
- Monte Carlo null false-positive rate = **0.04983**.

At `sigma_V=1.0 mV`, planning power for the same 0.10 contrast falls to about
**0.607** for the 7-point estimator. Therefore a noisy sweep is not rescued
post hoc by interpretation. The metrology must be improved and the point-level
uncertainty gate re-passed.

Technical samples or repeated readings are never counted as independent
substrates. Any averaging used to reach the 0.5 mV point-estimate gate must be
validated empirically; no `1/sqrt(N)` improvement is assumed for autocorrelated
reads.

## Acquisition hierarchy and replicate structure

The hierarchy remains:

`lot -> substrate -> pixel/device -> session -> intensity point -> raw readings`.

For each independent nominal R2 substrate:

1. measure one complete 17-point sweep on the nominal Pixel A;
2. block sweep direction across substrates (nominally 3 ascending / 2
   descending for the five-substrate pilot), with assignment frozen before
   unblinding;
3. repeat three anchors near 0.1, 0.316, and 1.0 suns after the primary sweep
   to estimate short-term drift/repeatability;
4. keep all raw readings and timestamps;
5. monitor DUT temperature continuously or at sufficient cadence to verify the
   temperature gate;
6. report the full curve even when the primary contrast is null.

The anchor repeats estimate technical drift; they do not increase biological or
fabrication sample count.

## Illumination and heating budget

The frozen v2.5 aperture is `3.10 mm x 3.10 mm = 9.61 mm^2 = 0.0961 cm^2`.

Using the standard one-sun planning irradiance `100 mW/cm^2`:

- incident power at one sun = **9.61 mW**;
- maximum incident power at two suns = **19.22 mW**.

For an **illustrative** five seconds of total dwell/acquisition per grid point,
a single 17-point sweep corresponds to about **457.45 mJ incident optical
energy** on the aperture.

This is not a heat-load calculation. Absorptance, thermal sinking, spectrum,
fixture, and convection/radiation determine actual temperature. The physical
gate is measured DUT temperature, not the incident-energy estimate.

A sweep is confirmatory only if the predefined DUT-temperature band is
maintained and there is no monotonic thermal drift sufficient to explain the
curvature. If the temperature gate fails, the sweep is a metrology failure.

## Between-substrate sensitivity

The five-substrate pilot can estimate a mean curvature only if
substrate-to-substrate variability is not too large.

Using the nominal 0.5 mV point-noise model and a true mean contrast of 0.10:

- assumed between-substrate SD 0.050 -> five-substrate planning power ~0.983;
- SD 0.075 -> ~0.815;
- SD 0.100 -> ~0.588.

For the last case, the same normal planning approximation reaches ~0.833 at
nine substrates and ~0.922 at twelve.

These are **synthetic design sensitivities**. The actual between-substrate
variance must be estimated from the physical pilot. It is not permissible to
inflate sample size after inspecting a favorable mechanism direction without
recording the adaptive decision.

## Predeclared decision rules

### Measurement PASS
All are required:

- complete 17-point grid;
- empirical point-estimate `Voc` SD <=0.5 mV;
- DUT temperature and illumination calibration gates pass;
- anchor repeats show no drift large enough to account for the observed
  curvature;
- 7-point and 9-point curves have the same qualitative curvature direction;
- all functional devices are reported under the frozen QC rules.

### Measurement NARROW
Use only exploratory language if:

- `0.5 < sigma_V <= 1.0 mV`;
- 7- and 9-point interpretations disagree;
- a sweep-direction effect is visible;
- between-substrate variance makes the five-substrate mechanism estimate
  underpowered.

### Measurement FAIL / repeat metrology
No confirmatory mechanism interpretation if:

- `sigma_V >1.0 mV`;
- DUT-temperature gate fails;
- illumination calibration or sweep-history effects are comparable to the
  curvature;
- exclusions were changed after unblinding.

## Independent checks performed before commit

- analytic normal-theory power versus a 30,000-dataset Monte Carlo;
- null false-positive rate check;
- independent NumPy pseudoinverse calculation of the local-contrast weights
  versus the repository's explicit 3x3 Gaussian-elimination calculation:
  maximum coefficient difference `1.78e-14`;
- noiseless quadratic limiting case recovers the injected local-ideality
  contrast;
- explicit units/dimensional analysis;
- grid/dose sensitivity across 13, 15, 17 and 19 points.

## Null and conventional explanations preserved

Even a precise nonzero `Delta_n_curv` may be caused by:

- contacts or surface recombination;
- transport resistance;
- carrier-density-dependent bulk recombination;
- energetic disorder/traps;
- light-induced heating;
- sweep history or slow photophysical relaxation;
- intensity-calibration nonlinearity;
- mixed mechanisms.

Therefore this grid improves the R2 discriminator but cannot establish EPC or
open-quantum transport by itself.

## Primary source context

The external real-data benchmark remains:

- Wang et al., *Rethinking Charge Transport and Recombination in Donor-Diluted
  Organic Solar Cells*, Advanced Materials (2026), DOI
  `10.1002/adma.202523681`.
- Public dataset: Zenodo `10.5281/zenodo.20525023`.

The article's broader result is that transport and recombination regimes can
change with blend composition; this reinforces the requirement not to use
ideality as a unique mechanism label.
