# Evidence note — R2 light-intensity power design v3.15

## Established external evidence

Wang et al. (Advanced Materials, 2026; DOI `10.1002/adma.202523681`) report
light-intensity-dependent recombination/transport analysis in PM6:Y12 and show
that the applicable recombination description changes with donor fraction.
This supports using `Voc`-intensity behavior as a diagnostic while preserving
non-unique transport/contact/recombination explanations.

The v3.13/v3.14 repository benchmarks use the public Zenodo dataset
`10.5281/zenodo.20525023` and demonstrate real-data curvature / fit-window
dependence.

## Engineering assumptions introduced in v3.15

- 17 geometrically spaced points from 0.05 to 2 suns;
- `|Delta_n_curv|=0.10` as the minimum planning effect;
- `sigma_V <=0.5 mV` as the confirmatory point-estimate noise gate;
- 300 K for the power calculation;
- illustrative 5 s per point for incident-dose comparison only;
- standard planning irradiance 100 mW/cm^2 at one sun;
- between-substrate SD scenarios 0–0.10 in ideality contrast.

None is a measured R2 value.

## Synthetic/model result

Under independent Gaussian point noise with SD 0.5 mV, the 17-point / 7-point
local estimator has `SE(Delta_n_curv)=0.0224201` and analytic power 0.993796 for
a true contrast of 0.10. Independent Monte Carlo gives 0.992733 power and
0.04983 null false-positive probability.

At 1.0 mV point noise, power falls to about 0.607.

## Hypothesis

If R2 has a reproducible illumination-dependent recombination curvature of
magnitude at least 0.10 and the measurement system meets the 0.5 mV point-noise
gate, this design should resolve the curvature on a device without relying on
post-hoc smoothing selection.

## Claim boundary

Passing the power/measurement gate validates detectability of curvature, not its
physical origin. EPC/open-quantum attribution remains unsupported without the
orthogonal mechanism discriminators already preregistered.
