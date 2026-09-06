---
name: ghc-family-checkpoint-byte-boundary
description: "Accept only exact UTF-8 line boundaries whose committed prefix parses; retain incomplete suffix bytes. Use for a declared synthetic evidence interchange request."
---

# ghc-family-checkpoint-byte-boundary

Accept only exact UTF-8 line boundaries whose committed prefix parses; retain incomplete suffix bytes.

Interpret offset as a byte count over strict UTF-8, not a character count. A nonzero checkpoint must end immediately after LF, including the LF in CRLF.

Parse only the committed prefix and retain the pending suffix byte count. A malformed committed prefix is refused. A valid checkpoint does not prove a real job resumed, data was durable, or processing happened exactly once.

Read [contracts.json](references/contracts.json) before running the fixed acceptance and adverse fixtures. Use an isolated Python 3.12 environment satisfying the exact [requirements lock](references/requirements.lock); this guide does not authorize installing into system Python or changing a shared prefix.

From this skill directory, run:

```text
python -B scripts/ghc_family_iveren_brook_v687_v2_checkpoint_budget.py --operation checkpoint --input references/positive.json
python -B scripts/ghc_family_iveren_brook_v687_v2_checkpoint_budget.py --operation checkpoint --input references/adverse.json
```

Compare the complete typed output with the two declared expectations. Preserve a rejecting result and any operational failure before a scoped correction. A passing local fixture supplies no independent reproduction, professional or production certification, empirical confirmation, complete privacy or accessibility assurance, exhaustive security, consciousness or personhood evidence, legal or cultural legitimacy, affected-party or Maori authority, proof/canon, or Stage 20 readiness.

These helpers read one bounded input file and emit JSON. They grant no permission to contact another task, operate a live account, overwrite a skill, or change another owner lane. Keep completed, represented, open_gap, and exact_gate distinct. Preserve NOT_READY_FOR_STAGE_20.
