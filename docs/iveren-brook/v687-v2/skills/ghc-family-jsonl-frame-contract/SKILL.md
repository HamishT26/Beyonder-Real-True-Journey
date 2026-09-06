---
name: ghc-family-jsonl-frame-contract
description: "Read a bounded sequence without silently skipping invalid, empty, duplicate-key, or nonfinite records. Use for a declared synthetic evidence interchange request."
---

# ghc-family-jsonl-frame-contract

Read a bounded sequence without silently skipping invalid, empty, duplicate-key, or nonfinite records.

Do not silently skip an empty or invalid line. Return the first rejecting physical line, allow explicit null, and distinguish an empty stream from a blank record.

A complete final JSON record may lack a newline for reading. The checkpoint contract is stricter and requires a terminating LF before committing that record. BOM-prefixed rows are refused even though the underlying library can be more permissive.

Read [contracts.json](references/contracts.json) before running the fixed acceptance and adverse fixtures. Use an isolated Python 3.12 environment satisfying the exact [requirements lock](references/requirements.lock); this guide does not authorize installing into system Python or changing a shared prefix.

From this skill directory, run:

```text
python -B scripts/ghc_family_iveren_brook_v687_v2_json_records.py --operation jsonl_frames --input references/positive.json
python -B scripts/ghc_family_iveren_brook_v687_v2_json_records.py --operation jsonl_frames --input references/adverse.json
```

Compare the complete typed output with the two declared expectations. Preserve a rejecting result and any operational failure before a scoped correction. A passing local fixture supplies no independent reproduction, professional or production certification, empirical confirmation, complete privacy or accessibility assurance, exhaustive security, consciousness or personhood evidence, legal or cultural legitimacy, affected-party or Maori authority, proof/canon, or Stage 20 readiness.

These helpers read one bounded input file and emit JSON. They grant no permission to contact another task, operate a live account, overwrite a skill, or change another owner lane. Keep completed, represented, open_gap, and exact_gate distinct. Preserve NOT_READY_FOR_STAGE_20.
