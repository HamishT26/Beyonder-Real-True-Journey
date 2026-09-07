---
name: ghc-family-declared-reaction-models
description: "Validate deficiency_record and mass_action_monomial in synthetic reaction records; preserve exact fractions, typed refusals and evidence limits."
---

# Declared Reaction Models

Use this guide for the two named reaction contracts. Read [the contract reference](references/contracts.json) before choosing an input.

## deficiency_record

Calculate complexes minus linkage classes minus declared rank after range checks. The graph and rank are declarations, so the result remains represented and no dynamics theorem is applied.

## mass_action_monomial

Require an explicit declared_mass_action law. Multiply the nonnegative coefficient by nonnegative concentrations raised to bounded nonnegative integer orders. Keep units undeclared and measured kinetics false; do not infer orders from stoichiometry.

## Invocation and readback

Run `python scripts/ghc_family_reaction_skill.py --input references/accepting-1.json` from this skill folder. Repeat with `references/adverse-1.json`; an accepted record exits zero and a bounded refusal exits two. Select the second operation with the corresponding `-2` fixture. Compare the complete output, not only the exit code. Unknown fields and duplicate JSON keys are refused.

Keep inputs synthetic and retain failed witnesses before correction. This guide confers no professional qualification, real reaction, empirical GMUT confirmation, production Freed ID assurance, complete accessibility, legal or cultural legitimacy, Maori authority, independent reproduction or Stage 20 readiness. Relational names remain working language only.

Rollback means stop selecting this guide and use the previous compatible surface; retain this package and its evidence.
