---
name: ghc-family-artifact-budget-contract
description: "Keep inclusive file and byte ceilings explicit, reject malformed counts, and recommend rotation at the file boundary. Use for a declared synthetic evidence interchange request."
---

# ghc-family-artifact-budget-contract

Keep inclusive file and byte ceilings explicit, reject malformed counts, and recommend rotation at the file boundary.

Use nonnegative integer file and byte counts; refuse booleans and fractional values. File limits must be between one and two thousand, and byte capacity must be positive.

Equality is at_limit, excess is exceeded, and the file boundary recommends rotation. Submitted counts are not live storage measurements, and this helper creates, moves, or deletes nothing.

Read [contracts.json](references/contracts.json) before running the fixed acceptance and adverse fixtures. Use an isolated Python 3.12 environment satisfying the exact [requirements lock](references/requirements.lock); this guide does not authorize installing into system Python or changing a shared prefix.

From this skill directory, run:

```text
python -B scripts/ghc_family_iveren_brook_v687_v2_checkpoint_budget.py --operation artifact_budget --input references/positive.json
python -B scripts/ghc_family_iveren_brook_v687_v2_checkpoint_budget.py --operation artifact_budget --input references/adverse.json
```

Compare the complete typed output with the two declared expectations. Preserve a rejecting result and any operational failure before a scoped correction. A passing local fixture supplies no independent reproduction, professional or production certification, empirical confirmation, complete privacy or accessibility assurance, exhaustive security, consciousness or personhood evidence, legal or cultural legitimacy, affected-party or Maori authority, proof/canon, or Stage 20 readiness.

These helpers read one bounded input file and emit JSON. They grant no permission to contact another task, operate a live account, overwrite a skill, or change another owner lane. Keep completed, represented, open_gap, and exact_gate distinct. Preserve NOT_READY_FOR_STAGE_20.
