# Evidence note — low-temperature execution v3.6

Date: 2026-08-26

## Established evidence / vendor specifications

1. **Linkam HFS600E-PB4** — vendor page states temperature/environment control below -195 °C to 600 °C, up to four positional probes in a gas-tight chamber, and LN2 cooling to below -195 °C with LNP96. This establishes range/probe compatibility only; it does not independently verify our mounted-device temperature accuracy. Source: https://www.linkam.co.uk/hfs600e-pb4
2. **Lake Shore DT-670** — vendor specification covers 1.4–500 K for relevant packages, recommended excitation 10 µA, typical calibrated accuracy about ±34 mK at 77 K and ±35 mK at 300 K, and reported dissipation ~10 µW at 77 K / ~5 µW at 300 K. Source: https://www.lakeshore.com/products/categories/specification/temperature-products/cryogenic-temperature-sensors/dt-670-silicon-diodes
3. **Lake Shore Cernox** — vendor specification gives calibrated cryogenic thermometry across the required range, including typical accuracy ±16 mK at 77 K and ±60 mK at 300 K. Source: https://www.lakeshore.com/products/categories/specification/temperature-products/cryogenic-temperature-sensors/cernox

## Engineering inference

A calibrated sensor's intrinsic calibration uncertainty is much smaller than the program's ±1 K DUT accuracy gate. Therefore the dominant risk is expected to be the installed measurement chain: thermal gradients, mounting/contact, readout, self-heating, and electrical device heating. This is a design inference, not a measured R2 result.

## Synthetic calculation verification

Planning model:

`sigma_D^2(T)=lambda*hbarOmega*coth[hbarOmega/(2*k_B*T)]`

with explicitly synthetic `lambda=150 meV`, `hbarOmega=15 meV`.

Analytic linewidth temperature derivatives:

- 120 K: 0.1806215513 meV/K
- 150 K: 0.1763403375 meV/K
- 240 K: 0.1537868466 meV/K
- 300 K: 0.1407767773 meV/K

Independent centered finite-difference check with `h=0.01 K` agreed to better than `2e-10 meV/K` at every point in Python 3.13.5.

At 150 K, the model maps 0.5 K temperature error to ~0.0882 meV linewidth error and 1 K to ~0.1763 meV. These values are **synthetic-model sensitivities**, not experimental uncertainty bounds.

## Claim boundary

The v3.6 execution package qualifies measurement feasibility and supplies measured uncertainty to the existing synthetic mechanism-recovery gate. It does not establish H1, EPC, open-quantum transport, or a useful-power effect.
