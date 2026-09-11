---
name: ghc-family-lts-product
description: Explore pairs reached when both models take the same explicit action label. Use for declared finite labelled transition models.
---

# Synchronous product reachability

Use the matching `lts_product` operation in the paired owner runner. Supply one JSON object on standard input. The exact request and expected envelope below define the finite contract. Model states are ordered; labels are explicit; there is no implicit fairness. AF and EG stutter at a deadlock, while deadlock inventory inspects raw edges.

```json
{"op":"lts_product","model":{"states":["s0"],"start":"s0","edges":[]},"peer":{"states":["s0","s1"],"start":"s0","edges":[["s0","a","s1"],["s1","b","s0"]]}}
```

Expected:
```json
{"ok":true,"value":[["s0","s0"]],"error":null}
```

Read the owner request profile before adapting the fixture. Unknown fields, duplicate states, dangling edges and malformed tokens are refused. Retain a failed subject separately from its passing refusal guard. A counterexample reaches only the declared model and property. Use the previous compatible caller if a check fails, retaining this candidate and its evidence.

Bounded same-owner synthetic evidence only; no empirical, participant, identity, professional, production, legal, cultural, affected-party, Maori-authority, complete privacy/accessibility, exhaustive-security, independent-reproduction, consciousness/personhood, AGI/ASI, Theory-of-Everything or Stage 20 claim. NOT_READY_FOR_STAGE_20.
