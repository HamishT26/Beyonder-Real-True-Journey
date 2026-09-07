---
name: ghc-family-audio-segment-binding
description: Verify source and segment SHA-256 claims against literal supplied bytes and explicit half-open endpoints. Use for owner-scoped synthetic evidence; no real audio or authority decisions.
---

# Audio Segment Binding

Verify source and segment SHA-256 claims against literal supplied bytes and explicit half-open endpoints.

Require lowercase hexadecimal, exact 64-character lowercase digests, and in-range integer endpoints. Empty segments are allowed and bind the empty byte string. A digest establishes only byte correspondence; it does not establish original custody, identity, consent, or rights.

Read `references/contracts.json` for twenty frozen accepting and refusing examples. Invoke `python scripts/ghc_family_segment_binding.py INPUT.json` from this package. Exit zero means the operation accepted its bounded input; exit two is a refusal and must remain visible. Compare the entire output, including its types and false external-credit field, to the selected owner fixture. A compatible new fixture needs its own preregistered acceptance condition and receives no inherited completion credit.

The wrapper and shared core are portable within this package. Keep their manifest together, preserve earlier callers, and never overwrite a different global package. Retain every failed invocation and correct only the affected dependency.

Relational working language only; no consciousness, personhood, identity continuity, employment, qualification, independent agency, scientific, operational, legal, cultural, affected-party, or Maori authority is established. Same-owner software evidence is not independent reproduction. NOT_READY_FOR_STAGE_20. Maori concepts remain under Maori authority.
