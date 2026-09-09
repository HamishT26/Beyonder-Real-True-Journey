---
name: ghc-family-merkle-verify
description: Evaluate the bounded synthetic merkle verify contract and its authority reservation when exact integrity evidence is needed.
---

# ghc-family-merkle-verify

Use this phase-local skill only for the exact `merkle_verify` operation in Vesper v689-v7 synthetic fixtures.

1. Require exactly `op`, `payload`, and `synthetic: true`.
2. Run `ghc_family_merkle_verify_xor_parity.py` only for its declared operation pair.
3. Preserve input bytes and the complete typed envelope.
4. Keep invalid subjects failed at zero credit even when refusal checks pass.
5. Treat digests, deterministic bytes, Merkle paths, and recovery as correspondence evidence only.
6. Stop on real records, untrusted payloads, credentials, identity, rights, ownership, legal or cultural interpretation, Maori authority, production, or Stage 20.

A finite pass is same-owner software evidence only—not authenticity, consent, ownership, exhaustive security, independent reproduction, consciousness, personhood, empirical GMUT confirmation, or a Theory of Everything.
