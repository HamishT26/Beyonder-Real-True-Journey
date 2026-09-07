---
name: ghc-family-reaction-extent-feasibility
description: "Validate extent_update and extent_interval in synthetic reaction records; preserve exact fractions, typed refusals and evidence limits."
---

# Reaction Extent Feasibility

Use this guide for the two named reaction contracts. Read [the contract reference](references/contracts.json) before choosing an input.

## extent_update

Compute each declared amount as its initial amount plus signed number times extent using exact fractions. Initial and resulting amounts must be nonnegative. A negative extent is algebraically allowed when amounts remain feasible.

## extent_interval

Intersect all nonnegative-amount constraints. Positive signed numbers give lower bounds; negative numbers give upper bounds; spectators give neither. Preserve null for an unbounded end and include finite endpoints.

## Invocation and readback

Run `python scripts/ghc_family_reaction_skill.py --input references/accepting-1.json` from this skill folder. Repeat with `references/adverse-1.json`; an accepted record exits zero and a bounded refusal exits two. Select the second operation with the corresponding `-2` fixture. Compare the complete output, not only the exit code. Unknown fields and duplicate JSON keys are refused.

Keep inputs synthetic and retain failed witnesses before correction. This guide confers no professional qualification, real reaction, empirical GMUT confirmation, production Freed ID assurance, complete accessibility, legal or cultural legitimacy, Maori authority, independent reproduction or Stage 20 readiness. Relational names remain working language only.

Rollback means stop selecting this guide and use the previous compatible surface; retain this package and its evidence.
