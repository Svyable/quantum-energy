# Evidence record — v3.8 ΔVnr literature benchmark

## Primary source

Li, Y. et al. **Asymmetric electron acceptor enables highly luminescent organic solar cells with certified efficiency over 18%**. *Nature Communications* 13, 3113 (2022).

https://www.nature.com/articles/s41467-022-30225-7

## Source claims used

The paper reports measured external electroluminescence quantum efficiencies and corresponding non-radiative voltage losses for PM6 blended with Y6, BO-4F, BO-4Cl, BO-5Cl and BO-6Cl. In the article text, the reported `EQE_EL` values are `6.2e-5`, `1.3e-4`, `1.4e-4`, `1.02e-3` and `7.2e-4`; the reported non-radiative losses are `0.250`, `0.231`, `0.229`, `0.178` and `0.187 V`, respectively.

These are **published experimental values**. They are used only as an external calculation benchmark.

## Internal result class

`models/delta_vnr_literature_benchmark.py` independently evaluates

`ΔVnr = -(k_B T/q) ln(EQE_EL)`

at 300 K using the published `EQE_EL` values as dimensionless fractions.

The resulting maximum absolute discrepancy against the rounded published voltage-loss values is `0.464 mV`. Algebraic inversion of each published pair implies `T=299.44–299.89 K`.

Classification: **reproduced calculation + independent algebraic cross-check**, not experimental reproduction.

## Important boundary

The sub-millivolt numerical agreement does not imply the source experiment or our future AT-04 measurement has sub-millivolt measurement uncertainty. The source values are rounded, and the benchmark checks the governing relation/unit convention, not detector performance.

## Conventional/error explanation explicitly tested

Percent/fraction unit confusion is a plausible software/data-ingestion failure. Deliberately multiplying the already fractional `EQE_EL` values by 100 creates an approximately 119 mV error. Future pipelines must record source representation and normalize to a dimensionless fraction exactly once.
