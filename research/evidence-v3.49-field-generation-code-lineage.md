# v3.49 — field-generation paper/code lineage audit

## Changed evidentiary state

**Claim class: independent reproduction / lineage audit.**

The 2026 Nature Photonics field-dependent-generation paper remains strong primary evidence that field-dependent free-charge generation can limit FF in the material systems studied. However, the project's stronger reproducibility wording is narrowed: the **current public author-code revision is not yet established as the exact implementation of the paper's first-order Stark rate model**.

The paper states that its rate-coefficient calculation focuses on the first-order Stark effect, using an interfacial CT separation of about 3.5 nm and an internal field of about `1e7 V/m`, giving an approximately 35 meV linear shift. It separately estimates second-order polarizability shifts at only `0.0035–0.035 meV`.

The inspected public code revision `d5e805ec69359f36be6e1da17a401ed8d64721a3` contains `functions/marcus_equation_stark.m` at blob `5eb9f1fad1737601e23dab39f56494474f9b8053`. That helper contains a quadratic polarizability shift and no first-order dipole term. The public `kDis_stark.m` blob `3a1bffbc0b671e36d53cceaccb9f79813befff01` calls that helper. The example workflow `MarcusTransfer_JV_0620_334.m` blob `3ba0c6c0dd61d65046522851a913ba56ddb62655` uses `RCT=1.5 nm`.

This is a **lineage question**, not an accusation of error: the paper does not pin the figure-generating Git commit, so the inspected current public revision may differ from the exact analysis revision.

## Primary-source provenance

- Zhang et al., *Overcoming the fill-factor limit of organic solar cells*, Nature Photonics, version of record 2026-06-19, DOI `10.1038/s41566-026-01946-8`.
- Paper code-availability link: `HuotianZhang/DriftFusionOPV_FieldDependent`.
- Public code inspected at commit `d5e805ec69359f36be6e1da17a401ed8d64721a3`.
- No repository-level `LICENSE` file was observed in the inspected recursive tree. The upstream implementation is therefore not copied here; this packet independently evaluates the equations/constants needed for the lineage check.

## Governing equations and units

### Paper-text first-order scale

For a one-electron CT dipole change approximated by separation `r`,

`|DeltaE_1| = q |F| r` in joules.

Dividing by `q` joules per eV gives

`|DeltaE_1|[eV] = |F|[V/m] * r[m]`.

At `F=1e7 V/m` and `r=3.5e-9 m`,

`|DeltaE_1| = 0.035 eV = 35 meV`.

Dimensional check: `(V/m)*m = V`, and a one-electron energy of one volt corresponds numerically to one eV after division by `q`.

### Inspected public helper's quadratic term

The inspected helper corresponds to

`|DeltaE_2| = 0.5 * alpha_CT * F^2 / q`,

with

`alpha_CT = 4*pi*epsilon0*(85 A^3)*1e-30*(d_CT/d_ref)^4`,

and `d_ref=1.5e-10 m`.

Using its example `d_CT=1.5 nm` and `F=1e7 V/m`, the independent standard-library calculation gives:

- implied polarizability proxy: `850000 A^3`;
- quadratic shift: `0.029513559045876218 eV = 29.5136 meV`;
- ratio to the paper's stated second-order upper scale (`0.035 meV`): `843.2445441678921`.

If the same public-code scaling is evaluated at the paper's 3.5 nm first-order separation, it gives `0.8748401885080096 eV`, `24.995433957371702` times the paper's 35 meV first-order scale. This is a **counterfactual sensitivity check**, not evidence that the published simulation actually passed 3.5 nm into this public helper.

## Independent and negative checks

Executable reproduction:

```bash
python3 models/field_generation_code_lineage_v349.py --self-test
```

Expected terminal marker:

`FIELD_GENERATION_CODE_LINEAGE_V3.49: PASS`

Checks include:

1. direct paper-text first-order `F*r` evaluation;
2. independent reconstruction of the public helper's quadratic expression from constants and blob-provenance, without importing/copying upstream code;
3. zero-field limiting case for both expressions;
4. `F^2` scaling check: halving field must quarter the quadratic shift;
5. frozen numerical outputs at absolute relative tolerance `1e-12`.

No stochastic calculation is used.

## Strongest conventional explanations / failure modes

1. **Revision mismatch:** the paper's figure-generating code may exist in an earlier, later, unpublished, or untagged revision. This is the leading explanation and is why the result is classified `LINEAGE_UNRESOLVED`, not `CODE_CONTRADICTS_PAPER`.
2. **Different helper/path:** another file or parameter path may implement the first-order term used for the published figure. The inspected public tree was searched structurally and the cited `kDis_stark` path calls the quadratic helper, but a full MATLAB execution/figure reconstruction has not been completed here.
3. **Documentation/unit intent mismatch:** comments or scaling in the public helper may not reflect the intended physical polarizability model. This cannot be resolved by reinterpretation; it requires an author-pinned revision or figure-generating archive.

At least one failure mode is quantitatively bounded in this increment: the inspected helper's own constants produce a second-order scale hundreds of times larger than the paper's stated second-order range under its 1.5 nm example setting.

## Decision impact

- **Keep:** v3.45's first-order Marcus–Stark counterexample remains a valid independent reimplementation of the paper-text model and a useful warning against blindly minimizing reorganization energy.
- **Narrow:** do not call the authors' current public code an independently reproduced implementation of the paper's first-order field model.
- **Do not infer:** this lineage discrepancy does not establish that the paper's experimental TDCF/PL conclusions are wrong, nor that D18/PY-IT/eC9 has the same field-dependent-generation limitation.
- **Program implication:** PR #39's prospective physical TDCF/PL discriminator becomes more important, not less; the project should rely on its own blinded physical evidence rather than treating current upstream code availability as sufficient validation.

## Falsifier / retirement condition

This lineage concern is retired if an author-pinned revision, release, archived supplement, or figure-generating script can be identified that (a) contains the stated first-order Stark term on the rate path used for Fig. 4g/h and (b) reproduces a paper figure or frozen numeric reference within a predeclared tolerance.

## Next physical discriminator

Run the already-proposed blinded B0 TDCF + bias-dependent-PL baseline to establish real field-generation repeatability and safe acquisition settings. That physical result is more decision-relevant than further speculative refinement of the upstream model lineage.
