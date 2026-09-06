---
name: ghc-family-event-prefix-reducer
description: "Reduce a synthetic ordered event prefix and preserve one-send terminal states without performing any live send. Use for a declared synthetic evidence interchange request."
---

# ghc-family-event-prefix-reducer

Reduce a synthetic ordered event prefix and preserve one-send terminal states without performing any live send.

Require contiguous integer sequence numbers beginning at one; booleans are not sequence numbers. Only declared state transitions are accepted.

Acknowledged, opaque, and rejected terminal states forbid resending. Unavailability can end a validated prefix before a send. All counts describe submitted synthetic events; this runner never invokes a messaging tool.

Read [contracts.json](references/contracts.json) before running the fixed acceptance and adverse fixtures. Use an isolated Python 3.12 environment satisfying the exact [requirements lock](references/requirements.lock); this guide does not authorize installing into system Python or changing a shared prefix.

From this skill directory, run:

```text
python -B scripts/ghc_family_iveren_brook_v687_v2_receipt_events.py --operation event_prefix --input references/positive.json
python -B scripts/ghc_family_iveren_brook_v687_v2_receipt_events.py --operation event_prefix --input references/adverse.json
```

Compare the complete typed output with the two declared expectations. Preserve a rejecting result and any operational failure before a scoped correction. A passing local fixture supplies no independent reproduction, professional or production certification, empirical confirmation, complete privacy or accessibility assurance, exhaustive security, consciousness or personhood evidence, legal or cultural legitimacy, affected-party or Maori authority, proof/canon, or Stage 20 readiness.

These helpers read one bounded input file and emit JSON. They grant no permission to contact another task, operate a live account, overwrite a skill, or change another owner lane. Keep completed, represented, open_gap, and exact_gate distinct. Preserve NOT_READY_FOR_STAGE_20.
