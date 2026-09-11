---
name: ghc-family-lts-evaluation-gap
description: List missing real evaluation modes from supplied evidence labels; this phase supplies none. Use for declared finite labelled transition models.
---

# Evaluation prerequisite missingness

Use the matching `lts_evaluation_gap` operation in the paired owner runner. Supply one JSON object on standard input. The exact request and expected envelope below define the finite contract. Model states are ordered; labels are explicit; there is no implicit fairness. AF and EG stutter at a deadlock, while deadlock inventory inspects raw edges.

```json
{"op":"lts_evaluation_gap","model":{"states":["s0"],"start":"s0","edges":[]},"required":["keyboard"],"supplied":[]}
```

Expected:
```json
{"ok":true,"value":{"missing":["keyboard"],"real_participants":0,"outcome":"open_gap"},"error":null}
```

Read the owner request profile before adapting the fixture. Unknown fields, duplicate states, dangling edges and malformed tokens are refused. Retain a failed subject separately from its passing refusal guard. A counterexample reaches only the declared model and property. Use the previous compatible caller if a check fails, retaining this candidate and its evidence.

Bounded same-owner synthetic evidence only; no empirical, participant, identity, professional, production, legal, cultural, affected-party, Maori-authority, complete privacy/accessibility, exhaustive-security, independent-reproduction, consciousness/personhood, AGI/ASI, Theory-of-Everything or Stage 20 claim. NOT_READY_FOR_STAGE_20.
