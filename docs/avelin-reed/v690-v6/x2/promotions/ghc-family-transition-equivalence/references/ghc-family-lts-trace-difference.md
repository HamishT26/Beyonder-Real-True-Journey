---
name: ghc-family-lts-trace-difference
description: Find a shortest left trace absent on the right up to the declared depth; absence is bounded, not equivalence. Use for declared finite labelled transition models.
---

# Bounded trace inclusion counterexample

Use the matching `lts_trace_difference` operation in the paired owner runner. Supply one JSON object on standard input. The exact request and expected envelope below define the finite contract. Model states are ordered; labels are explicit; there is no implicit fairness. AF and EG stutter at a deadlock, while deadlock inventory inspects raw edges.

```json
{"op":"lts_trace_difference","model":{"states":["s0"],"start":"s0","edges":[]},"peer":{"states":["s0","s1"],"start":"s0","edges":[["s0","a","s1"],["s1","b","s0"]]},"depth":1}
```

Expected:
```json
{"ok":true,"value":{"word":null,"depth":1,"bounded":true},"error":null}
```

Read the owner request profile before adapting the fixture. Unknown fields, duplicate states, dangling edges and malformed tokens are refused. Retain a failed subject separately from its passing refusal guard. A counterexample reaches only the declared model and property. Use the previous compatible caller if a check fails, retaining this candidate and its evidence.

Bounded same-owner synthetic evidence only; no empirical, participant, identity, professional, production, legal, cultural, affected-party, Maori-authority, complete privacy/accessibility, exhaustive-security, independent-reproduction, consciousness/personhood, AGI/ASI, Theory-of-Everything or Stage 20 claim. NOT_READY_FOR_STAGE_20.
