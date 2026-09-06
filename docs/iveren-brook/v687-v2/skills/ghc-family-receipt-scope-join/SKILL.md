---
name: ghc-family-receipt-scope-join
description: "Require owner, phase, head, scope, result, and evidence class to match before granting local-only receipt credit. Use for a declared synthetic evidence interchange request."
---

# ghc-family-receipt-scope-join

Require owner, phase, head, scope, result, and evidence class to match before granting local-only receipt credit.

Require exact owner, phase, head, and scope strings, an actual boolean passed field, and the synthetic evidence class. List every mismatched binding in contract order.

This joins supplied records; it does not run Git, validate an external receipt, or grant deployment or route authority. A completed local conjunction has external_credit=false.

Read [contracts.json](references/contracts.json) before running the fixed acceptance and adverse fixtures. Use an isolated Python 3.12 environment satisfying the exact [requirements lock](references/requirements.lock); this guide does not authorize installing into system Python or changing a shared prefix.

From this skill directory, run:

```text
python -B scripts/ghc_family_iveren_brook_v687_v2_receipt_events.py --operation receipt_join --input references/positive.json
python -B scripts/ghc_family_iveren_brook_v687_v2_receipt_events.py --operation receipt_join --input references/adverse.json
```

Compare the complete typed output with the two declared expectations. Preserve a rejecting result and any operational failure before a scoped correction. A passing local fixture supplies no independent reproduction, professional or production certification, empirical confirmation, complete privacy or accessibility assurance, exhaustive security, consciousness or personhood evidence, legal or cultural legitimacy, affected-party or Maori authority, proof/canon, or Stage 20 readiness.

These helpers read one bounded input file and emit JSON. They grant no permission to contact another task, operate a live account, overwrite a skill, or change another owner lane. Keep completed, represented, open_gap, and exact_gate distinct. Preserve NOT_READY_FOR_STAGE_20.
