# D18/PY-IT/eC9 durability + mechanism-retention preregistration v3.61

## Claim class and changed state

**Claim class:** prospective protocol. No experimental durability result is claimed.

This increment converts the commercial bridge's vague `no unacceptable durability penalty` requirement into a falsifiable, machine-checkable experiment. It deliberately separates intrinsic **heat-only** and **light-driven** stress so a surviving or lost performance advantage cannot be hidden inside one generic stability number.

The protocol does not invent a new materials threshold. It carries forward the canonical project gate already on `main`: an arm must show at least **5% relative stabilized-Pmax improvement with the same sign across at least three independent lots** before strong useful-work language. Durability asks whether that advantage survives a source-grounded ageing horizon.

## Source provenance and scope

1. Luo et al., *Nature Communications* (2026), DOI `10.1038/s41467-026-68731-7`, reports that device measurements and thermal ageing were conducted in an inert glovebox. The main article methods inspected for this increment do not state a thermal-ageing temperature, duration, or a durability result used here. Therefore the anchor is **not promoted to durability validation**.
2. Khenkin et al., *Nature Energy* 5, 35–49 (2020), DOI `10.1038/s41560-019-0529-5`, provides an ISOS-based consensus framework. It explicitly distinguishes inert-atmosphere intrinsic tests, including heat-only `ISOS-D-2I` and light-only `ISOS-L-1I`; recommends recording sample/batch statistics and normalization values; recommends 800–1000 W m^-2 for light-soaking studies; and recommends `T80`, or at least 1000 h with `eta_1000` if T80 is not reached.

The second source is used as research-discipline precedent. This packet does **not** claim IEC certification and does not transfer perovskite-specific degradation mechanisms to OPV.

## Prospective design

### Materials arms

- `B0`: D18:eC9 baseline.
- `B1`: D18:PY-IT:eC9 = 1:0.1:1.
- `B2`: D18:PY-IT:eC9 = 1:0.2:1.

Randomize arms within fabrication lots and retain full `material lot -> fabrication lot -> substrate -> device -> stress session -> measurement` hierarchy. Pulses, repeated scans, pixels on one substrate, and repeated time points are not independent fabrication replicates.

### Stress discriminator A — intrinsic heat

`D2I_65C_DARK`:

- dark;
- 65 C;
- inert atmosphere;
- open-circuit/disconnected state;
- same-device stabilized-Pmax measurements at accepted checkpoints.

The 65 C condition is taken from the explicit D-2 elevated-temperature options in the ISOS-derived consensus, not optimized to produce a favorable result.

### Stress discriminator B — intrinsic light

`L1I_1SUN_RT`:

- inert atmosphere;
- 800–1000 W m^-2 illumination;
- room-temperature test class, with actual device temperature continuously/periodically measured and reported rather than assumed;
- maximum-power-point tracking when equipment supports it, otherwise a documented stabilized operation near MPP.

Report light-source type, spectrum/calibration reference, irradiance, MPPT hardware/algorithm or stabilized-bias procedure, temperature, encapsulation state, and interruptions.

## Governing quantities

For device `i`, stabilized useful-work retention is

`R_i(t) = Pmax_i(t) / Pmax_i(0)`.

`R_i` is dimensionless. `Pmax_i(t)` and `Pmax_i(0)` must use the same accepted area definition and compatible stabilized measurement procedure.

If T80 is reached, record the first prospectively valid time at which the selected T80 definition is satisfied. If T80 is not reached by 1000 h, report

`eta_1000,i = Pmax_i(1000 h) / Pmax_i(0)`.

Do not extrapolate field lifetime or acceleration factor without a separately validated model.

The arm-vs-B0 useful-work comparison remains

`G_arm(t) = Pmax_arm(t) / Pmax_B0(t) - 1`,

but inference must be performed at the independent-lot level rather than by pooling correlated devices. This packet does not prescribe a new statistical margin beyond the existing >=5% project gate.

## Paired mechanism-retention measurements

Acquire before stress and at the post-stress/1000 h endpoint, on prospectively selected devices or matched witnesses:

- `DeltaVnr` / `EQE_EL` or justified equivalent;
- field-dependent generation by TDCF, bias-dependent PL, or independently justified equivalent;
- `Voc`, `FF`, `Jsc`;
- at least one morphology or contact/transport control.

A favorable EPC/voltage-loss observable is not durable useful-work evidence if stabilized Pmax is lost. Conversely, loss of Pmax does not uniquely falsify EPC: morphology, contacts, transport, electrode/interlayer changes, and photochemistry remain live explanations.

## Frozen decision logic

1. All functional devices are reported unless a QC rule frozen before stress excludes them; exclusion code and reason remain in the data.
2. Champion-device survival is insufficient.
3. An arm is not called durable useful-work validation if its initial >=5% stabilized-Pmax advantage over B0 is absent at the frozen durability horizon.
4. If voltage-loss/EPC indicators remain favorable while stabilized Pmax advantage disappears, classify the result as mechanism science and test field-generation, transport/contact, morphology, and degradation explanations.
5. Heat-only and light-only outcomes are kept separate. Opposite trends are a useful discriminator, not values to average away.
6. No accelerated test is converted to field lifetime without a validated acceleration model.

## Serious conventional explanations

At least the following remain live:

- domain coarsening, vertical-composition drift, crystallization, or other morphology evolution;
- contact, electrode, PFN-Br/interlayer, series-resistance, or shunt changes;
- imperfect atmosphere/encapsulation causing photo-oxidation or other photochemistry;
- field-generation or transport deterioration unrelated to EPC;
- material/fabrication lot variation or correlated repeats masquerading as durability effects.

The separated dark-heat versus illuminated stress directly helps discriminate thermal/morphological degradation from light/electrical-operation-dependent degradation, but it does not uniquely identify either mechanism.

## Machine-readable contract and executable check

Contract:

`research/protocols/d18-durability-mechanism-retention-v3.61.json`

Run:

```bash
python models/d18_durability_mechanism_retention_v361.py
```

The executable validates the protocol, independently checks retention arithmetic using both floating point and exact rational arithmetic, tests the no-degradation limiting case, rejects non-positive baseline Pmax, and runs a negative fixture in which a synthetic initial >=5% advantage disappears at 1000 h.

The embedded fixture is **synthetic software-test data only**. It does not encode expected D18/PY-IT/eC9 degradation or a materials threshold.

## Falsification and next physical measurement

A durable interface/EPC useful-work claim is narrowed if real prospectively tracked data show that the initial useful-work advantage does not survive the durability horizon, especially when conventional degradation controls explain the loss.

The next physical action after this preregistration is execution on real B0/B1/B2 devices, ideally coordinated with the already-prioritized field-generation and stabilized-Pmax campaign so the same independent lots support initial-performance and durability inference.
