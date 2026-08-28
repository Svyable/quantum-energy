# D18/PY-IT/eC9 prospective durability gate v3.48

## Evidentiary state

**Claim class:** prospective protocol with synthetic arithmetic fixtures. No D18/PY-IT/eC9 durability result is claimed.

This protocol closes one downstream gap in the useful-work chain: an interface arm that improves initial stabilized `Pmax` must not be promoted as durable useful work if the advantage disappears under a prospectively frozen stress exposure. It complements, and does not replace, the open field-generation and stabilized-Pmax PRs.

Primary procedural precedent is Reese et al., *Solar Energy Materials and Solar Cells* 95 (2011) 1253-1267, DOI `10.1016/j.solmat.2011.01.036`. ISOS procedures support comparable stability testing/reporting; they are not product qualification tests and do not establish D18/PY-IT/eC9 lifetime.

## Prospective freeze

Before arm identities are released, freeze:

- stress class and exact exposure conditions;
- stress duration/end criterion;
- stabilized-MPP tracking and sampling rules;
- B0 pairing within fabrication lot;
- device QC/exclusion rules;
- temperature, irradiance, area, contact and encapsulation controls;
- physical durability noninferiority margin and its provenance;
- lot-level analysis commit.

`machine/d18-pyit-ec9-durability-v3.48.json` deliberately leaves stress conditions, duration, and physical noninferiority margin `null`. Until defensible B0 repeatability/instrument/power evidence fills them prospectively, a durability PASS is `INCOMPLETE`.

## Quantities

For arm `x` and elapsed stress time `t`:

`R_x(t) = P_x(t) / P_x(0)`.

For contemporaneous B0 and candidate arm:

`g(t) = P_arm(t)/P_B0(t) - 1`.

`D(t) = R_B0(t) - R_arm(t)`; positive `D` means worse normalized retention for the candidate.

For a declared stress interval `T`:

`A_x = (1/T) integral_0^T R_x(t) dt`, and `D_A = A_B0 - A_arm`.

`R`, `g`, `D`, `A`, and `D_A` are dimensionless. Time units cancel in `A` when numerator and denominator use the same unit. No accelerated-stress result may be converted to field lifetime without a separately validated acceleration model.

## Decision semantics

A strong durable-useful-work PASS requires the already-separate initial useful-work and field-generation gates plus a prospectively frozen durability margin. This packet does not set that margin.

A direct kill/narrow condition does not need an invented margin: if a candidate begins with favorable paired stabilized `Pmax` but its paired **absolute** `Pmax` advantage reverses by the prospectively frozen stress endpoint, it cannot support durable-useful-work validation for that exposure. Retain such a result as initial-performance/mechanism science and report the degradation crossover.

## Synthetic negative fixture

Synthetic/planning arithmetic only, in arbitrary power units:

- `t = [0, 100, 200] h`
- B0 `Pmax = [1.00, 0.96, 0.92]`
- candidate `Pmax = [1.05, 0.99, 0.90]`

Results:

- initial gain = `+5.0%`;
- endpoint gain = `-2.17391304347826%`;
- endpoint normalized-retention penalty = `+6.28571428571429%`;
- integrated retention B0 = `0.96`;
- integrated retention candidate = `0.935714285714286`;
- integrated retention penalty = `0.0242857142857143`.

Thus a favorable initial-power result can be erased by degradation. This is a negative software fixture, not a prediction about B1/B2.

## Verification and falsification

Run:

`python3 models/d18_pyit_ec9_durability_v348.py --self-test`

Expected marker: `PASS_SYNTHETIC_FIXTURE`.

The primary direct-ratio path is independently checked with `exp(log(P_arm)-log(P_B0))-1` at `1e-12` absolute tolerance. Additional tests enforce zero-change limiting behavior and 100x power-unit invariance.

Serious conventional explanations include: (1) temperature/irradiance/tracker/contact drift masquerading as degradation; (2) encapsulation or electrode degradation unrelated to the proposed EPC/interface state; (3) ordinary morphology/thickness changes that alter both initial power and stability. The current protocol directly bounds the first class through contemporaneous B0 and recorded conditions; the others require post-stress morphology/contact/encapsulation diagnostics before mechanism attribution.

Statistical hierarchy remains `lot -> substrate -> device -> session -> measurement`; repeated time points do not increase independent lot count.
