# AT-04 EQE_EL -> DeltaV_nr uncertainty budget v3.44

**Status:** synthetic planning / engineering specification. No measured R2 or AT-04 performance is reported here.

## Purpose

The canonical technical specification requires <=10 mV equivalent nonradiative-voltage-loss uncertainty, but that scalar target is not by itself an executable uncertainty budget. This increment makes the target component-level, correlation-aware, machine-checkable, and fail-closed.

## Governing equation

For external electroluminescence quantum efficiency `EQE_EL`,

`DeltaV_nr = -(k_B T / q) ln(EQE_EL)`.

Symbols and units:

- `DeltaV_nr`: nonradiative voltage loss [V]
- `k_B/q = 8.617333262e-5 V/K`: ratio derived from exact SI constants
- `T`: DUT temperature [K]
- `EQE_EL`: dimensionless external electroluminescence quantum efficiency

Dimensional check: `(V/K)(K) ln(1) = V`.

Sign and limits: for `0<EQE_EL<1`, `ln(EQE_EL)<0`, so `DeltaV_nr>0`; at `EQE_EL=1`, `DeltaV_nr=0`. The equation is not evaluated for nonpositive EQE_EL.

## First-order uncertainty propagation

For independent temperature and EQE terms,

`u_EQE = |d DeltaV_nr / d EQE_EL| u(EQE_EL) = (k_B T/q) [u(EQE_EL)/EQE_EL]`,

`u_T = |d DeltaV_nr / dT| u(T) = |-(k_B/q) ln(EQE_EL)| u(T)`.

Additional calibrated terms may already be expressed as equivalent voltage uncertainty. The reviewer must prevent double counting: for example, a radiometric-scale term cannot be added independently if it is already included inside the stated relative uncertainty of EQE_EL.

For components `u_i` with correlations `rho_ij`,

`u_c^2 = sum_i u_i^2 + 2 sum_{i<j} rho_ij u_i u_j`.

This is a standard variance-of-a-linear-combination identity, not a claim that every real AT-04 component is Gaussian or reducible to one scalar correlation. Component-level covariance should replace scalar correlation when calibration provenance supports it.

## Synthetic planning fixture

The machine contract intentionally uses synthetic assumptions to exercise the calculation path:

- `T = 300 +/- 1 K`
- `EQE_EL = 1e-6` with 10% relative 1-sigma uncertainty
- radiometric-scale equivalent uncertainty = 4 mV
- session-repeatability equivalent uncertainty = 3 mV
- background-subtraction equivalent uncertainty = 2 mV
- internal planning gate = 10 mV, inherited from `technical/current-specification.md`

These are not measurements and are not vendor specifications.

Nominal derived values:

- `DeltaV_nr = 357.1585759879732 mV`
- EQE-relative contribution = `2.5851999786 mV`
- temperature contribution = `1.1905285866265771 mV`

At zero correlation among the listed terms, the root-sum-square fixture is `6.091027601721118 mV`.

A declared sensitivity sweep treats only radiometric-scale and background-subtraction as correlated for demonstration:

- `rho=-0.5`: `5.3944987945988565 mV`
- `rho=0`: `6.091027601721118 mV`
- `rho=+0.5`: `6.71569931168218 mV`

The synthetic decision remains below the 10 mV planning gate over this narrow correlation sweep. That does **not** establish real-world compliance because the component magnitudes and covariance are synthetic.

## Independent calculation check

`models/at04_eqeel_uncertainty.py` computes analytic derivatives and independently recomputes them with central finite differences. Predeclared tolerances are `1e-9` relative for the temperature derivative and `2e-10` relative for the EQE derivative, with small absolute floors for floating-point behavior. The exact limiting case `EQE_EL=1 -> DeltaV_nr=0` is also enforced.

The CI workflow independently reparses the machine contract and re-derives the zero-correlation RSS without importing the production script.

## Validity regime and uncertainty hierarchy

First-order propagation is appropriate only when local linearization is adequate and the uncertainty representation is meaningful. At very large relative EQE uncertainty, near detection limits, or after censoring/background subtraction produces strongly non-Gaussian behavior, use a distribution-aware propagation or bounded interval analysis rather than this first-order approximation.

Uncertainty components are not statistical replicates. Repeated pixels, repeated integrations, or repeated sessions must retain the lot -> substrate -> device/pixel -> session -> measurement hierarchy. Correlated calibration terms are systematic until demonstrated otherwise.

## PASS / INCOMPLETE / FAIL semantics

A real AT-04 budget can be marked `PASS` only when:

1. every material component has provenance, date/version, units, and uncertainty basis;
2. correlations/shared calibrations have been reviewed rather than silently set to zero;
3. double counting has been excluded;
4. analytic and independent numerical checks pass;
5. the complete combined standard uncertainty is <=10 mV; and
6. the model validity regime is appropriate for the measured weak-EL data.

Missing provenance, missing covariance review, or an invalid linearization regime is `INCOMPLETE`, not PASS. A complete budget above 10 mV is `FAIL` for the present internal engineering target.

## Conventional/null explanation protected by this gate

A favorable apparent voltage-loss difference can arise from radiometric scale drift, background subtraction, temperature error, injection-state mismatch, or session correlation rather than a material/interface mechanism. The discriminator is a complete calibrated uncertainty budget plus independent reciprocity/measurement controls; unexplained residual agreement is not mechanism evidence.

## Kill/narrow rule

Do not release proprietary B0/B1/B2 mechanism claims if the complete measured AT-04 budget cannot meet the <=10 mV internal target with defensible covariance treatment. Improve metrology first or narrow the detectable-effect claim.
