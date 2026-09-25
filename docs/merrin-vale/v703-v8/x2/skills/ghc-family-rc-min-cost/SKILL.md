---
name: ghc-family-rc-min-cost
description: Minimum synthetic assignment cost for bounded synthetic binary relations; use when return the minimum declared integer cost and every minimizing solution.
---

# Minimum synthetic assignment cost

Use operation rc_min_cost with runners/ghc-family-relations-x2-3.txt. The caller accepts one JSON request file containing contract_id, operation, and a fixture. Read planning/fixtures.json relative to the phase root. Variables and relation scopes are explicit; values are binary, relations have at most 32 unique rows, and costs are integer model units.

Return the minimum declared integer cost and every minimizing solution.

Acceptance: Dynamic min-sum factors versus exhaustive integer costs; no monetary interpretation.

Preserve empty relations, isolated variables, and duplicate scopes with distinct relation identifiers. A missing declared join tree does not prove that no join tree exists. A nonempty natural join does not establish that every original tuple is globally supported. An all-empty relation family can satisfy projection equality while having no satisfying assignment.

The caller emits ok, the original contract identifier, an input digest, one core outcome and an exact value. Invalid field sets, out-of-domain tuples, bad trees and unbounded inputs return a refusal with zero subject completion credit. Retain the subject separately from its passing refusal check. Verify the actual input digest and expected-value receipt before using the result.

The intended outcome is completed. No finite output promotes an empirical, participant, production, identity, professional, legal, cultural, affected-party or Maori-authority claim. Independent reproduction and complete accessibility/security remain unproved.

Rollback is additive: retain the frozen request and every failed response, and use a separately named narrow correction. This guide changes no shared installation or public authority.
