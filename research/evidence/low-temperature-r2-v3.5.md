# Evidence supplement — low-temperature R2 feasibility (v3.5)

## Established evidence

### PM6:Y6 operating regime on cooling
Perdigón-Toro et al., *Advanced Materials* 32, 1906763 (2020), DOI `10.1002/adma.201906763`.

Relevant bounded findings:
- PM6:Y6 free-charge generation was reported to have a very small activation energy in the studied device.
- Photovoltaic EQE decreased only weakly on cooling toward ~150 K; the spectral shape remained essentially unchanged down to roughly 125 K.
- A steeper EQE reduction below ~150 K was observed and discussed as potentially reflecting charge-transport/extraction or recombination effects.
- Voc remained approximately linear with temperature down to roughly 100 K under the reported conditions.

**Program consequence:** PM6:Y6 literature supports attempting 150 K, but does not justify assuming 120 K represents the same operating regime. 120 K is conditional on an empirical equivalence test.

### CT linewidth / dynamic broadening
Tvingstedt, Benduhn & Vandewal, *Materials Horizons* 7, 1888–1900 (2020), DOI `10.1039/D0MH00385A`.

**Program consequence:** temperature-dependent CT EL linewidth can distinguish high-temperature Marcus-like broadening from low-temperature vibronic saturation, but one-temperature optical tails are not direct static-DOS measurements.

### Device temperature and reciprocity
Göhler et al., *Physical Review Applied* 15, 064009 (2021), DOI `10.1103/PhysRevApplied.15.064009`.

**Program consequence:** retain DUT-adjacent temperature metrology and reciprocity checks. Stage setpoint alone is insufficient for a mechanism claim.

## Engineering assumptions introduced in v3.5

These are not literature facts:
- 150 K primary low-temperature gate;
- 120 K conditional gate;
- normalized EQE cosine similarity >=0.995;
- local Voc(T) deviation <=20 mV;
- injection-induced DUT heating <=0.5 K;
- CT/near-gap spectral SNR >=20;
- repeat linewidth SD <=2 meV to reuse the v3.4 nominal synthetic recovery model unchanged;
- post-cycle recovery |ΔVoc|<=10 mV, |ΔVnr|<=5 mV, |ΔPmax|<=5%.

## Synthetic/model result

Using inherited synthetic priors `lambda=150 meV`, `hbarOmega=15 meV`:
- 1 K temperature error maps to about 0.176 meV linewidth error at 150 K and 0.181 meV at 120 K in the one-mode model;
- exact one-mode variance exceeds the high-temperature Marcus approximation by 10.98% at 150 K and 16.95% at 120 K.

These values quantify information leverage only. They do not show that R2 follows the one-mode model.

## Explicit non-claims

- No R2 low-temperature device has been measured.
- PM6:Y6 literature does not prove the proposed R2 encapsulation/contact stack is stable at 120 or 150 K.
- Passing 150 K feasibility would not establish static disorder, EPC, open-quantum transport, or an energy-conversion advantage.
