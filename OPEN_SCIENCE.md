# Open Science Charter

This project is being developed in public for broad societal benefit. The goal is not to make the strongest possible claim; it is to make the strongest claim that survives transparent evidence, reproducible calculation, and adversarial review.

## Publication principles

1. **Reproducibility before rhetoric.** Every quantitative result should be reconstructable from committed inputs, equations/code, units, software/environment information, and a deterministic seed where randomness is used.
2. **Claim classes stay explicit.** Material statements must be labeled as one of: established evidence, engineering assumption, falsifiable hypothesis, synthetic/model result, experimental result, or novel invention concept.
3. **Primary sources first.** Prefer primary papers, standards, manufacturer datasheets for instrument specifications, and original datasets. Reviews may orient the work but should not silently replace primary evidence for decisive claims.
4. **Uncertainty is part of the result.** Report measurement uncertainty, numerical sensitivity, parameter uncertainty, and model dependence whenever they could change an engineering or scientific decision.
5. **Null and negative results remain public.** Failed mechanisms, contradictory observations, unfavorable sensitivity analyses, and retired assumptions belong in the permanent record.
6. **Conventional explanations are mandatory controls.** A quantum-mechanism interpretation must outperform plausible optical, thermal, morphological, electrostatic, contact, tunneling, measurement, and statistical alternatives.
7. **Prospective tests outrank retrospective fits.** Prefer preregistered predictions, blinded analyses, held-out materials/devices, and precommitted thresholds.
8. **No false precision.** Significant figures, tolerances, confidence intervals, and model outputs must reflect the weakest relevant input and the model's validity domain.
9. **Corrections are first-class contributions.** If a calculation, citation, assumption, or conclusion is wrong, correct it visibly; do not erase the history that explains the change.
10. **Safety and environmental burden are part of technical performance.** Lead-containing materials, solvents, vacuum processes, UV exposure, thermal cycling, and waste streams must be documented alongside efficiency or transport metrics.

## Minimum publication packet for a quantitative claim

A result is not publication-ready until the repository contains, where applicable:

- exact claim and scope;
- source inputs with provenance and version/date;
- equations or executable code;
- SI units and dimensional check;
- nominal calculation;
- independent recomputation or alternate derivation;
- uncertainty propagation;
- sensitivity analysis for decision-driving parameters;
- assumptions and validity domain;
- null/conventional comparator;
- raw or minimally processed data where legally and practically shareable;
- processing script/notebook and fixed random seed;
- reviewer checklist with unresolved objections;
- correction history if the result supersedes earlier work.

## Publication levels

- **Exploratory:** idea, assumption, or synthetic planning model; not evidence of physical performance.
- **Reproduced:** calculation/code reruns from committed inputs and passes unit/numerical checks.
- **Cross-checked:** independent method or implementation agrees within a predeclared tolerance.
- **Experimentally supported:** measured data pass calibration, controls, uncertainty, and preregistered gates.
- **Prospectively validated:** prediction succeeds on blinded/held-out data or a second material/process system.

Only the final two levels justify strong physical or platform claims.

## Open-source licensing

The repository is intended to remain open. Before a formal tagged release, the project should explicitly select licenses for code, documentation/data, and hardware/CAD rather than relying on an implicit GitHub-public status. License selection should preserve the intended public-benefit and contributor terms and should be recorded in the release PR.
