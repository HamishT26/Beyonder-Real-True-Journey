---
name: ghc-family-lts-authority-hold
description: Expose missing declared roles while keeping actual external authority and external action false. Use for declared finite labelled transition models.
---

# Release-role vacancy hold

Use the matching `lts_authority_hold` operation in the paired owner runner. Supply one JSON object on standard input. The exact request and expected envelope below define the finite contract. Model states are ordered; labels are explicit; there is no implicit fairness. AF and EG stutter at a deadlock, while deadlock inventory inspects raw edges.

```json
{"op":"lts_authority_hold","model":{"states":["s0"],"start":"s0","edges":[]},"required":["owner"],"supplied":[]}
```

Expected:
```json
{"ok":true,"value":{"vacant":["owner"],"actual_authority":false,"external_action":false,"outcome":"exact_gate"},"error":null}
```

Read the owner request profile before adapting the fixture. Unknown fields, duplicate states, dangling edges and malformed tokens are refused. Retain a failed subject separately from its passing refusal guard. A counterexample reaches only the declared model and property. Use the previous compatible caller if a check fails, retaining this candidate and its evidence.

Bounded same-owner synthetic evidence only; no empirical, participant, identity, professional, production, legal, cultural, affected-party, Maori-authority, complete privacy/accessibility, exhaustive-security, independent-reproduction, consciousness/personhood, AGI/ASI, Theory-of-Everything or Stage 20 claim. NOT_READY_FOR_STAGE_20.
