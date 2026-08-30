# 2026-08-30 — QG0b material reproduction readiness v3.76

## Intended changed evidentiary state

Move the quantum-geometry branch from QG0a minimal-model verification to a material-specific reproduction audit without overstating aggregate-value checks as an independent transport reproduction.

## Preflight

- canonical repository: `Svyable/quantum-energy`
- starting `main`: `da0d40cba585a722be7ae28dcfab37b9e7d58c99`
- PR #69 / v3.75 was already merged before this run continued
- no open pull requests were found at QG0b start
- fresh branch: `automation/quantum-energy-20260830-1249-qg0b`

## Primary source audited

Thompson et al., **Topologically enhanced exciton transport**, *Nature Communications* 16, 11448 (2025), DOI `10.1038/s41467-025-66276-9`.

Supporting methodology: Jankowski et al., **Excitonic topology and quantum geometry in organic semiconductors**, *Nature Communications* 16, 4661 (2025), DOI `10.1038/s41467-025-59257-5`.

## Findings

### 1. Published ratios are internally consistent

Printed 300 K values:

- polypentacene: 1.76 versus 0.61 cm^2/s -> exact printed-value ratio 2.885245901639344...
- polyheptacene: 0.44 versus 0.103 cm^2/s -> exact printed-value ratio 4.271844660194175...

The source's approximately 3x / 4.5x prose is rounded. No correction to the paper is implied.

### 2. The bond-reordered control is unusually strong but computational

The idealized SSH two-hopping spectrum is invariant under swapping `t1` and `t2`. v3.76 independently checks this over a dense k grid using the polypentacene figure-caption pair `0.33/0.52 eV`.

This supports the source's logic of changing topology while controlling the idealized band dispersion. It does not make the trivial arm a separately realized material.

### 3. The public record does not yet support an exact independent 300 K recomputation

The article states that plot datasets and first-principles calculation input files are available upon request. Public supplementary information supplies substantial methodology, but the current project packet does not contain the complete momentum-resolved transport data or all final run inputs required to reconstruct the reported Eq. 7 totals.

Therefore the frozen state is:

- `reproduction_level=AGGREGATE_VALUES_AND_CONTROL_LOGIC_VERIFIED`
- `material_transport_reproduction=BLOCKED_PENDING_NUMERIC_DATA_OR_FULL_INDEPENDENT_RECOMPUTATION`
- `physical_project_result=NONE_EXTERNAL_COMPUTATIONAL_EVIDENCE_ONLY`

### 4. Topology is not a free robustness guarantee

The paper's modeled topological excitons can have larger geometric/group velocity while also suffering stronger exciton-phonon scattering/dephasing. Net transport enhancement is material-dependent. Defects and interfaces remain outside the clean-bulk demonstration.

This narrows the project hypothesis from "topology protects transport" to:

> quantum geometry may provide intrinsic velocity/transport headroom that is valuable only when its gain exceeds scattering, disorder, lifetime and sink-delivery penalties.

### 5. Method dependence remains a real falsifier

The supporting 2025 work places the topology transition differently at DFT and GW levels. Future QG0c work must publish that dependence rather than select the method that gives the preferred topology.

## Files added

- `machine/qg0b-material-reproduction-v3.76.json`
- `models/qg0b_material_transport_audit_v376.py`
- `models/qg0b_material_transport_expected_v376.csv`
- `technical/qg0b-material-reproduction-v3.76.md`
- `research/evidence/qg0b-material-reproduction-v3.76.md`
- `research/requests/qg0b-author-data-request-v3.76.md`
- `research/sessions/2026-08-30-qg0b-material-reproduction-v3.76.md`
- `.github/workflows/qg0b-material-reproduction-v376.yml`

## Agent replication packet

Run:

```bash
python models/qg0b_material_transport_audit_v376.py --check-expected
```

Expected key output:

- `QG0b material transport audit v3.76: PASS`
- `polypentacene_ratio=2.885245901639344`
- `polyheptacene_ratio=4.271844660194175`
- `ssh_swap_max_abs_spectral_diff=0.000e+00` (or numerically negligible under a different implementation)
- `reproduction_level=AGGREGATE_VALUES_AND_CONTROL_LOGIC_VERIFIED`
- `material_transport_reproduction=BLOCKED_PENDING_NUMERIC_DATA_OR_FULL_INDEPENDENT_RECOMPUTATION`
- `physical_project_result=NONE_EXTERNAL_COMPUTATIONAL_EVIDENCE_ONLY`

Negative-control command:

```bash
python models/qg0b_material_transport_audit_v376.py --claim-reproduced
```

It must return non-zero while the missing-input register is non-empty.

## Strongest conventional/null explanations

1. The reported advantage is specific to a clean computational bulk/counterfactual and may disappear with realistic interfaces or defects.
2. Stronger topological-state scattering can outweigh geometric velocity in another material.
3. Reduced-model topology can be qualitatively right while quantitative material diffusion is wrong.
4. Higher-level electronic structure can move the phase boundary.
5. Higher diffusion alone may not improve finite-lifetime sink capture or stabilized useful work.

## Anti-drift check

This run did not add another OPV metrology refinement. It advanced a distinct high-upside platform branch while keeping fabrication spend gated behind material-specific computational reproduction.

## Single best next increment

QG0c: independently reconstruct one material-specific **free-exciton** topology/quantum-geometry result, preferably polypentacene, from versioned public inputs. Do not add phonon-limited transport until the required source data are obtained or the full exciton-phonon calculation is independently reconstructed.
