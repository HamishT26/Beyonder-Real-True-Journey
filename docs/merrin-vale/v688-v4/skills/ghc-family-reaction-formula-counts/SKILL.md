---
name: ghc-family-reaction-formula-counts
description: "Validate flat_formula and grouped_formula in synthetic reaction records; preserve exact fractions, typed refusals and evidence limits."
---

# Reaction Formula Counts

Use this guide for the two named reaction contracts. Read [the contract reference](references/contracts.json) before choosing an input.

## flat_formula

Accept only a sequence of one- or two-letter atom symbols with bounded positive integer counts. Leading coefficients, grouping, zero counts and nontext input are outside this profile. Element existence is unverified.

## grouped_formula

Use a bounded stack for matching round and square groups. Apply terminal multipliers to every nested atom count; refuse empty, unmatched or too-deep groups. Group expansion does not identify a real substance.

## Invocation and readback

Run `python scripts/ghc_family_reaction_skill.py --input references/accepting-1.json` from this skill folder. Repeat with `references/adverse-1.json`; an accepted record exits zero and a bounded refusal exits two. Select the second operation with the corresponding `-2` fixture. Compare the complete output, not only the exit code. Unknown fields and duplicate JSON keys are refused.

Keep inputs synthetic and retain failed witnesses before correction. This guide confers no professional qualification, real reaction, empirical GMUT confirmation, production Freed ID assurance, complete accessibility, legal or cultural legitimacy, Maori authority, independent reproduction or Stage 20 readiness. Relational names remain working language only.

Rollback means stop selecting this guide and use the previous compatible surface; retain this package and its evidence.
