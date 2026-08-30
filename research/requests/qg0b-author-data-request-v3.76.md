# QG0b source-data request packet v3.76

## Purpose

This is a concise reproducibility request for the 300 K phonon-limited material transport results in Thompson et al., *Nature Communications* 16, 11448 (2025), DOI `10.1038/s41467-025-66276-9`.

The project has independently checked the printed aggregate ratios and SSH bond-reordered spectral-control identity. We have **not** reproduced the material-specific transport calculation and want to avoid reconstructing undocumented numerical choices incorrectly.

## Requested artifacts

For polypentacene and polyheptacene, including each bond-reordered trivial control where applicable:

1. Numeric data underlying the phonon-limited diffusion plots, especially the 300 K points.
2. Final first-principles/material input files used for the reported transport calculation, with software/version notes if available.
3. Momentum-grid exciton energies `E_nu(Q)` used in the transport sum.
4. Momentum-grid conventional and geometric/interband velocity contributions, or the raw quantities sufficient to recompute them.
5. Momentum-grid exciton-phonon scattering/dephasing rates `Gamma_nu(Q)`, or the raw exciton-phonon matrices/phonon information sufficient to recompute them.
6. Exact acoustic/optical hopping-displacement coupling parameters and the mapping to the cited oligoacene parametrization.
7. Structural coordinates/unit cells and any final Wannier/SSH/BSE mapping files corresponding to the transport curves.
8. Temperature grid, momentum-grid convergence settings, broadening/tolerance choices and any exclusions/branch selections required to reproduce Eq. 7 numerically.

## Verification target

The first target is intentionally narrow:

- independently recompute the reported 300 K `D_ph` values;
- compare with 1.76/0.61 cm^2/s for polypentacene and 0.44/0.103 cm^2/s for polyheptacene;
- separately verify the conventional-band, geometric-velocity and scattering contributions where the supplied data permit.

A reproduction packet will preserve the source files unchanged, record hashes, and publish any discrepancies or null result. No project-material claim will be inferred from the reproduction.

## Licensing / redistribution

Please also indicate the reuse/redistribution terms for supplied plot data and calculation inputs. If redistribution is not permitted, the project will publish hashes, retrieval instructions and derived checks without republishing restricted source files.
