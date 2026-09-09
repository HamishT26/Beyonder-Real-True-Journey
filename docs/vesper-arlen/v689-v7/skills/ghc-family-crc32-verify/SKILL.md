---
name: ghc-family-crc32-verify
description: Evaluate the bounded synthetic crc32 verify contract and its refusal boundary when exact byte-integrity evidence is needed.
---

# ghc-family-crc32-verify

Use this phase-local skill only for the exact `crc32_verify` operation in Vesper v689-v7 synthetic fixtures.

1. Require a UTF-8 JSON request with exactly `op`, `payload`, and `synthetic: true`.
2. Run `ghc_family_crc32_envelope_crc32_verify.py` only for its declared two-operation pair.
3. Preserve the input and the complete `ok`, `value`, `error` envelope.
4. Retain an invalid subject at zero success credit even when its refusal predicate passes.
5. Stop on real records, untrusted material, production use, credentials, identity conclusions, rights decisions, legal or cultural interpretation, Maori authority, or Stage 20.

A matching finite result is same-owner software evidence only. It does not establish authenticity, ownership, consent, professional preservation fitness, exhaustive security, independent reproduction, consciousness, personhood, empirical GMUT confirmation, or a Theory of Everything.
