---
name: ghc-family-rc-consistency-gap
description: Local and global consistency distinction for bounded synthetic binary relations; use when distinguish nonempty join, pairwise consistency, fixed point and exact global consistency.
---

# Local and global consistency distinction

Use operation rc_consistency_gap with runners/ghc-family-relations-x1-4.txt. The caller accepts one JSON request file containing contract_id, operation, and a fixture. Read planning/fixtures.json relative to the phase root. Variables and relation scopes are explicit; values are binary, relations have at most 32 unique rows, and costs are integer model units.

Distinguish nonempty join, pairwise consistency, fixed point and exact global consistency.

Acceptance: Every relation must equal its full-join projection; nonempty alone is insufficient.

Preserve empty relations, isolated variables, and duplicate scopes with distinct relation identifiers. A missing declared join tree does not prove that no join tree exists. A nonempty natural join does not establish that every original tuple is globally supported. An all-empty relation family can satisfy projection equality while having no satisfying assignment.

The caller emits ok, the original contract identifier, an input digest, one core outcome and an exact value. Invalid field sets, out-of-domain tuples, bad trees and unbounded inputs return a refusal with zero subject completion credit. Retain the subject separately from its passing refusal check. Verify the actual input digest and expected-value receipt before using the result.

The intended outcome is completed. No finite output promotes an empirical, participant, production, identity, professional, legal, cultural, affected-party or Maori-authority claim. Independent reproduction and complete accessibility/security remain unproved.

Rollback is additive: retain the frozen request and every failed response, and use a separately named narrow correction. This guide changes no shared installation or public authority.
