---
name: ghc-family-cbor-evidence-profile
description: "Freeze exact CBOR bytes for finite JSON-shaped evidence and refuse values outside the declared interchange profile. Use for a declared synthetic evidence interchange request."
---

# ghc-family-cbor-evidence-profile

Freeze exact CBOR bytes for finite JSON-shaped evidence and refuse values outside the declared interchange profile.

Use finite JSON-shaped values with text map keys, a depth limit, and the common signed/unsigned 64-bit integer envelope. This local profile excludes arbitrary tags, references, datetime objects, and bytes objects.

The canonical encoder sorts map keys according to its declared CBOR mode. Compare the exact hex output to the frozen vector. CBOR byte equality and decoded semantic equality are different checks.

Read [contracts.json](references/contracts.json) before running the fixed acceptance and adverse fixtures. Use an isolated Python 3.12 environment satisfying the exact [requirements lock](references/requirements.lock); this guide does not authorize installing into system Python or changing a shared prefix.

From this skill directory, run:

```text
python -B scripts/ghc_family_iveren_brook_v687_v2_binary_profiles.py --operation cbor_profile --input references/positive.json
python -B scripts/ghc_family_iveren_brook_v687_v2_binary_profiles.py --operation cbor_profile --input references/adverse.json
```

Compare the complete typed output with the two declared expectations. Preserve a rejecting result and any operational failure before a scoped correction. A passing local fixture supplies no independent reproduction, professional or production certification, empirical confirmation, complete privacy or accessibility assurance, exhaustive security, consciousness or personhood evidence, legal or cultural legitimacy, affected-party or Maori authority, proof/canon, or Stage 20 readiness.

These helpers read one bounded input file and emit JSON. They grant no permission to contact another task, operate a live account, overwrite a skill, or change another owner lane. Keep completed, represented, open_gap, and exact_gate distinct. Preserve NOT_READY_FOR_STAGE_20.
