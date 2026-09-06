---
name: ghc-family-unicode-byte-distinction
description: "Report original and normalized bytes while refusing to infer identity equivalence from normalization. Use for a declared synthetic evidence interchange request."
---

# ghc-family-unicode-byte-distinction

Report original and normalized bytes while refusing to infer identity equivalence from normalization.

Keep both original and normalized UTF-8 bytes. Select NFC, NFD, NFKC, or NFKD explicitly and refuse an unknown form or an unpaired surrogate.

Normalization may change byte spelling while preserving some text relationships. Always retain identity_equivalence=false; this function cannot determine identity, cultural interpretation, or affected-party legitimacy.

Read [contracts.json](references/contracts.json) before running the fixed acceptance and adverse fixtures. Use an isolated Python 3.12 environment satisfying the exact [requirements lock](references/requirements.lock); this guide does not authorize installing into system Python or changing a shared prefix.

From this skill directory, run:

```text
python -B scripts/ghc_family_iveren_brook_v687_v2_text_integrity.py --operation unicode_bytes --input references/positive.json
python -B scripts/ghc_family_iveren_brook_v687_v2_text_integrity.py --operation unicode_bytes --input references/adverse.json
```

Compare the complete typed output with the two declared expectations. Preserve a rejecting result and any operational failure before a scoped correction. A passing local fixture supplies no independent reproduction, professional or production certification, empirical confirmation, complete privacy or accessibility assurance, exhaustive security, consciousness or personhood evidence, legal or cultural legitimacy, affected-party or Maori authority, proof/canon, or Stage 20 readiness.

These helpers read one bounded input file and emit JSON. They grant no permission to contact another task, operate a live account, overwrite a skill, or change another owner lane. Keep completed, represented, open_gap, and exact_gate distinct. Preserve NOT_READY_FOR_STAGE_20.
