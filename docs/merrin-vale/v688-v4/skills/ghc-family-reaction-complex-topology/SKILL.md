---
name: ghc-family-reaction-complex-topology
description: "Validate complex_registry and complex_incidence in synthetic reaction records; preserve exact fractions, typed refusals and evidence limits."
---

# Reaction Complex Topology

Use this guide for the two named reaction contracts. Read [the contract reference](references/contracts.json) before choosing an input.

## complex_registry

Canonicalize each positive-coefficient species multiset, assign nodes in first-encounter order and retain each directed edge, including parallel and self edges. Empty source and sink complexes remain explicit.

## complex_incidence

Place minus one at each source and plus one at each target in a separate edge column. A self edge is zero. Preserve isolated node rows and parallel edge columns; reject out-of-range indices.

## Invocation and readback

Run `python scripts/ghc_family_reaction_skill.py --input references/accepting-1.json` from this skill folder. Repeat with `references/adverse-1.json`; an accepted record exits zero and a bounded refusal exits two. Select the second operation with the corresponding `-2` fixture. Compare the complete output, not only the exit code. Unknown fields and duplicate JSON keys are refused.

Keep inputs synthetic and retain failed witnesses before correction. This guide confers no professional qualification, real reaction, empirical GMUT confirmation, production Freed ID assurance, complete accessibility, legal or cultural legitimacy, Maori authority, independent reproduction or Stage 20 readiness. Relational names remain working language only.

Rollback means stop selecting this guide and use the previous compatible surface; retain this package and its evidence.
