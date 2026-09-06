---
name: ghc-family-json-key-uniqueness
description: "Reject duplicate decoded keys and nonfinite values before evidence can be assigned a stable meaning. Use for a declared synthetic evidence interchange request."
---

# ghc-family-json-key-uniqueness

Reject duplicate decoded keys and nonfinite values before evidence can be assigned a stable meaning.

Compare decoded keys within each object. Escaped and literal spellings of the same key collide; the same key in separate objects remains valid.

Refuse nonfinite constants and overflowing floating-point values. This guard checks key uniqueness and finite JSON values; it does not validate a domain schema or attest to the truth of the data.

Read [contracts.json](references/contracts.json) before running the fixed acceptance and adverse fixtures. Use an isolated Python 3.12 environment satisfying the exact [requirements lock](references/requirements.lock); this guide does not authorize installing into system Python or changing a shared prefix.

From this skill directory, run:

```text
python -B scripts/ghc_family_iveren_brook_v687_v2_json_records.py --operation json_unique --input references/positive.json
python -B scripts/ghc_family_iveren_brook_v687_v2_json_records.py --operation json_unique --input references/adverse.json
```

Compare the complete typed output with the two declared expectations. Preserve a rejecting result and any operational failure before a scoped correction. A passing local fixture supplies no independent reproduction, professional or production certification, empirical confirmation, complete privacy or accessibility assurance, exhaustive security, consciousness or personhood evidence, legal or cultural legitimacy, affected-party or Maori authority, proof/canon, or Stage 20 readiness.

These helpers read one bounded input file and emit JSON. They grant no permission to contact another task, operate a live account, overwrite a skill, or change another owner lane. Keep completed, represented, open_gap, and exact_gate distinct. Preserve NOT_READY_FOR_STAGE_20.
