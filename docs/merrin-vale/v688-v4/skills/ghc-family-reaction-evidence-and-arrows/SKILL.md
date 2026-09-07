---
name: ghc-family-reaction-evidence-and-arrows
description: "Validate reaction_evidence and arrow_semantics in synthetic reaction records; preserve exact fractions, typed refusals and evidence limits."
---

# Reaction Evidence And Arrows

Use this guide for the two named reaction contracts. Read [the contract reference](references/contracts.json) before choosing an input.

## reaction_evidence

Keep stoichiometric, kinetic, thermodynamic and deployment evidence roles distinct. Missing labels remain gaps; even complete synthetic labels support no external claim. Real-evidence or unsupported-claim promotion requires its separate gate.

## arrow_semantics

Preserve the literal arrow and distinguish relation, net forward, both directions and equilibrium declaration. No arrow establishes measured equilibrium or kinetics; reject a preclaimed observation.

## Invocation and readback

Run `python scripts/ghc_family_reaction_skill.py --input references/accepting-1.json` from this skill folder. Repeat with `references/adverse-1.json`; an accepted record exits zero and a bounded refusal exits two. Select the second operation with the corresponding `-2` fixture. Compare the complete output, not only the exit code. Unknown fields and duplicate JSON keys are refused.

Keep inputs synthetic and retain failed witnesses before correction. This guide confers no professional qualification, real reaction, empirical GMUT confirmation, production Freed ID assurance, complete accessibility, legal or cultural legitimacy, Maori authority, independent reproduction or Stage 20 readiness. Relational names remain working language only.

Rollback means stop selecting this guide and use the previous compatible surface; retain this package and its evidence.
