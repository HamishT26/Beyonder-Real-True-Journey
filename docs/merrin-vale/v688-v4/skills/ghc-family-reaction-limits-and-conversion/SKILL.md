---
name: ghc-family-reaction-limits-and-conversion
description: "Validate limiting_pool and degree_of_reaction in synthetic reaction records; preserve exact fractions, typed refusals and evidence limits."
---

# Reaction Limits And Conversion

Use this guide for the two named reaction contracts. Read [the contract reference](references/contracts.json) before choosing an input.

## limiting_pool

For consumed species only, divide initial amount by the absolute negative signed number. Preserve every tied minimum in the supplied species-array order and exclude products and spectators.

## degree_of_reaction

Divide extent by a strictly positive maximum and require the result from zero through one. A numerical degree is a declared ratio, not observed conversion.

## Invocation and readback

Run `python scripts/ghc_family_reaction_skill.py --input references/accepting-1.json` from this skill folder. Repeat with `references/adverse-1.json`; an accepted record exits zero and a bounded refusal exits two. Select the second operation with the corresponding `-2` fixture. Compare the complete output, not only the exit code. Unknown fields and duplicate JSON keys are refused.

Keep inputs synthetic and retain failed witnesses before correction. This guide confers no professional qualification, real reaction, empirical GMUT confirmation, production Freed ID assurance, complete accessibility, legal or cultural legitimacy, Maori authority, independent reproduction or Stage 20 readiness. Relational names remain working language only.

Rollback means stop selecting this guide and use the previous compatible surface; retain this package and its evidence.
