---
name: ghc-family-reaction-conservation-residuals
description: "Validate element_residual and charge_residual in synthetic reaction records; preserve exact fractions, typed refusals and evidence limits."
---

# Reaction Conservation Residuals

Use this guide for the two named reaction contracts. Read [the contract reference](references/contracts.json) before choosing an input.

## element_residual

Join each signed species coefficient to its declared atom-count map, sum each element and retain unused-element zeros. Missing species or negative counts are refusal conditions. A zero residual is no physical-reaction observation.

## charge_residual

Join signed numbers to declared integer formal charges. Report the signed residual and a structural balanced flag, preserving neutral species. This establishes no electrochemistry or charge measurement.

## Invocation and readback

Run `python scripts/ghc_family_reaction_skill.py --input references/accepting-1.json` from this skill folder. Repeat with `references/adverse-1.json`; an accepted record exits zero and a bounded refusal exits two. Select the second operation with the corresponding `-2` fixture. Compare the complete output, not only the exit code. Unknown fields and duplicate JSON keys are refused.

Keep inputs synthetic and retain failed witnesses before correction. This guide confers no professional qualification, real reaction, empirical GMUT confirmation, production Freed ID assurance, complete accessibility, legal or cultural legitimacy, Maori authority, independent reproduction or Stage 20 readiness. Relational names remain working language only.

Rollback means stop selecting this guide and use the previous compatible surface; retain this package and its evidence.
