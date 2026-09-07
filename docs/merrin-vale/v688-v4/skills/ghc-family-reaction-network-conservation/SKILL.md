---
name: ghc-family-reaction-network-conservation
description: "Validate pathway_sum and moiety_certificate in synthetic reaction records; preserve exact fractions, typed refusals and evidence limits."
---

# Reaction Network Conservation

Use this guide for the two named reaction contracts. Read [the contract reference](references/contracts.json) before choosing an input.

## pathway_sum

Treat each matrix column as a declared pathway and sum columns with exact rational weights. Reject ragged matrices and weight mismatches; do not turn formal pathway weights into observed kinetic flux.

## moiety_certificate

Multiply a declared row-weight vector by every stoichiometric column. Report every residual, whether all are zero, and whether the weight vector itself is zero. A formal certificate is not physical conservation evidence.

## Invocation and readback

Run `python scripts/ghc_family_reaction_skill.py --input references/accepting-1.json` from this skill folder. Repeat with `references/adverse-1.json`; an accepted record exits zero and a bounded refusal exits two. Select the second operation with the corresponding `-2` fixture. Compare the complete output, not only the exit code. Unknown fields and duplicate JSON keys are refused.

Keep inputs synthetic and retain failed witnesses before correction. This guide confers no professional qualification, real reaction, empirical GMUT confirmation, production Freed ID assurance, complete accessibility, legal or cultural legitimacy, Maori authority, independent reproduction or Stage 20 readiness. Relational names remain working language only.

Rollback means stop selecting this guide and use the previous compatible surface; retain this package and its evidence.
