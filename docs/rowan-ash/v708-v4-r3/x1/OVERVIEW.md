# Rowan P03 X1 review overview

Fifteen finite model families were executed. The selected final view has 122 passing checks across fourteen original models and the separately corrected missing-observation model. The history contains 130 passing model checks plus one failed support diagnostic; it is not 131 distinct final tests. X2 and run4 have not started.

The most important finding is the omitted support condition: the original fixed observation pattern had probability zero under its accompanying inclusion law. Individual numeric expectations passed, but the joint model interpretation failed. M04 v2 uses one-half inclusion probabilities, gives that pattern probability one sixteenth, and refuses the original impossible input. The first source and result remain unchanged.

Other useful counterexamples include local Jacobian invertibility without global injectivity, calibrated constant predictions with zero resolution, and a likelihood ratio of 27/16 becoming posterior probability 3/19 only after prior odds are supplied.

| Model | Selected checks | Source revision |
| --- | ---: | ---: |
| design-information | 8 | 1 |
| structural-identifiability | 8 | 1 |
| measurement-error | 8 | 1 |
| missing-observations | 10 | 2 |
| nuisance-profiling | 8 | 1 |
| randomization-null | 8 | 1 |
| bounded-uncertainty | 8 | 1 |
| finite-sensitivity | 8 | 1 |
| likelihood-ratio | 8 | 1 |
| held-out-evaluation | 8 | 1 |
| multiple-comparison-accounting | 8 | 1 |
| distribution-shift | 8 | 1 |
| calibration-and-resolution | 8 | 1 |
| reproducible-source-binding | 8 | 1 |
| evidence-limits | 8 | 1 |

Read REVIEW-BATON.md, selected-results-index.json and METHOD-FLOW.json together. Package byte verification is separate from independent reproduction, source authority, Page delivery, lead review and further stage activation.
