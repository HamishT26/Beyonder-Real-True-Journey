---
name: ghc-family-stoichiometric-coefficient-orientation
description: "Validate signed_numbers and primitive_numbers in synthetic reaction records; preserve exact fractions, typed refusals and evidence limits."
---

# Stoichiometric Coefficient Orientation

Use this guide for the two named reaction contracts. Read [the contract reference](references/contracts.json) before choosing an input.

## signed_numbers

Side coefficients are positive integers. Subtract reactant from product coefficients by exact species label; retain spectator zeros. A signed number is a symbolic orientation convention.

## primitive_numbers

Clear rational denominators, then divide by the nonzero greatest common divisor. Preserve the original sign orientation and zero positions; refuse an all-zero equation.

## Invocation and readback

Run `python scripts/ghc_family_reaction_skill.py --input references/accepting-1.json` from this skill folder. Repeat with `references/adverse-1.json`; an accepted record exits zero and a bounded refusal exits two. Select the second operation with the corresponding `-2` fixture. Compare the complete output, not only the exit code. Unknown fields and duplicate JSON keys are refused.

Keep inputs synthetic and retain failed witnesses before correction. This guide confers no professional qualification, real reaction, empirical GMUT confirmation, production Freed ID assurance, complete accessibility, legal or cultural legitimacy, Maori authority, independent reproduction or Stage 20 readiness. Relational names remain working language only.

Rollback means stop selecting this guide and use the previous compatible surface; retain this package and its evidence.
