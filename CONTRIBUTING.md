# Contributing

Contributions are welcome if they improve reproducibility, falsifiability, safety, manufacturability, or explanatory power.

## What makes a strong contribution

Good contributions include:

- independent reproduction of a published calculation;
- correction of an equation, citation, unit, uncertainty budget, or assumption;
- a conventional/null explanation that could invalidate a quantum interpretation;
- a preregistered experiment or simulation with explicit pass/fail criteria;
- raw or minimally processed data plus processing code;
- improved calibration, metrology, reliability, manufacturing, or EHS controls;
- a negative result that narrows the design space;
- prior art that changes an invention or commercialization claim.

## Pull-request expectations

Each PR should state:

1. the exact claim or program element changed;
2. whether each new material statement is established evidence, engineering assumption, falsifiable hypothesis, synthetic/model result, experimental result, or invention concept;
3. sources and versions for external inputs;
4. calculations/checks performed;
5. uncertainty and sensitivity relevant to the conclusion;
6. conventional/null alternatives considered;
7. files/data/code needed to reproduce the result;
8. unresolved objections and what would falsify the conclusion.

Do not remove inconvenient negative results merely because a newer model fits better. Supersede them with an explanation.

## Quantitative work

Follow `research/CALCULATION_VERIFICATION.md`. A quantitative claim should not be promoted to publication-ready until another calculation path or reviewer can reproduce it from committed inputs.

## Scientific tone

Use the narrowest accurate wording. In particular:

- do not use `quantum` as a synonym for unexplained or nanoscale;
- do not infer long-lived electronic coherence from efficient transport alone;
- do not call a correlation causal without a discriminator/control;
- do not call a model prediction a measurement;
- do not call a public vendor specification an independently reproduced capability;
- do not call an invention patentable or free-to-operate without an actual search and appropriate review.

## Safety

Flag hazards and environmental burdens directly. Proposed fabrication work should identify relevant solvent, lead/heavy-metal, vacuum, UV, electrical, thermal, waste, and shipping controls where applicable.

## Review posture

Reviewers are encouraged to try to break the claim. A PR that survives serious counterexample search, arithmetic checking, alternative models, and uncertainty analysis is more valuable than one that merely reads smoothly.
