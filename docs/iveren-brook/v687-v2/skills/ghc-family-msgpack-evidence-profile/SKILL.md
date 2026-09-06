---
name: ghc-family-msgpack-evidence-profile
description: "Freeze MessagePack bytes separately from CBOR and preserve scalar types and integer limits. Use for a declared synthetic evidence interchange request."
---

# ghc-family-msgpack-evidence-profile

Freeze MessagePack bytes separately from CBOR and preserve scalar types and integer limits.

Sort text map keys before encoding, retain array order, use binary-aware strict type handling, and refuse integers outside the declared 64-bit envelope.

Keep MessagePack byte expectations separate from CBOR. A matching roundtrip in one library does not prove interoperability with every other implementation.

Read [contracts.json](references/contracts.json) before running the fixed acceptance and adverse fixtures. Use an isolated Python 3.12 environment satisfying the exact [requirements lock](references/requirements.lock); this guide does not authorize installing into system Python or changing a shared prefix.

From this skill directory, run:

```text
python -B scripts/ghc_family_iveren_brook_v687_v2_binary_profiles.py --operation msgpack_profile --input references/positive.json
python -B scripts/ghc_family_iveren_brook_v687_v2_binary_profiles.py --operation msgpack_profile --input references/adverse.json
```

Compare the complete typed output with the two declared expectations. Preserve a rejecting result and any operational failure before a scoped correction. A passing local fixture supplies no independent reproduction, professional or production certification, empirical confirmation, complete privacy or accessibility assurance, exhaustive security, consciousness or personhood evidence, legal or cultural legitimacy, affected-party or Maori authority, proof/canon, or Stage 20 readiness.

These helpers read one bounded input file and emit JSON. They grant no permission to contact another task, operate a live account, overwrite a skill, or change another owner lane. Keep completed, represented, open_gap, and exact_gate distinct. Preserve NOT_READY_FOR_STAGE_20.
