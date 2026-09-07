---
name: ghc-family-riff-chunk-walk
description: Walk complete RIFF WAVE byte envelopes, preserving unknown and duplicate chunk identifiers, exact offsets, payload sizes, and padding bytes. Use for owner-scoped synthetic evidence; no real audio or authority decisions.
---

# Riff Chunk Walk

Walk complete RIFF WAVE byte envelopes, preserving unknown and duplicate chunk identifiers, exact offsets, payload sizes, and padding bytes.

The envelope size must equal the supplied bytes. A partial header, payload overrun, or missing odd-byte pad is a refusal. This walker accepts at most 64 chunks and 65,536 bytes. LIST contents stay opaque; finding fmt or data does not validate their audio semantics.

Read `references/contracts.json` for twenty frozen accepting and refusing examples. Invoke `python scripts/ghc_family_riff_chunks.py INPUT.json` from this package. Exit zero means the operation accepted its bounded input; exit two is a refusal and must remain visible. Compare the entire output, including its types and false external-credit field, to the selected owner fixture. A compatible new fixture needs its own preregistered acceptance condition and receives no inherited completion credit.

The wrapper and shared core are portable within this package. Keep their manifest together, preserve earlier callers, and never overwrite a different global package. Retain every failed invocation and correct only the affected dependency.

Relational working language only; no consciousness, personhood, identity continuity, employment, qualification, independent agency, scientific, operational, legal, cultural, affected-party, or Maori authority is established. Same-owner software evidence is not independent reproduction. NOT_READY_FOR_STAGE_20. Maori concepts remain under Maori authority.
