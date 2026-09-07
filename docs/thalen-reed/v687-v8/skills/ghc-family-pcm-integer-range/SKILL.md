---
name: ghc-family-pcm-integer-range
description: Classify signed or unsigned integer sample values against exact one-through-thirty-two-bit numeric bounds. Use for owner-scoped synthetic evidence; no real audio or authority decisions.
---

# Pcm Integer Range

Classify signed or unsigned integer sample values against exact one-through-thirty-two-bit numeric bounds.

Accept at most 64 integer samples and Boolean signedness. Report out-of-range positions separately from positions equal to an endpoint. An endpoint value alone never establishes clipping, distortion, audibility, instrument behavior, or restoration quality.

Read `references/contracts.json` for twenty frozen accepting and refusing examples. Invoke `python scripts/ghc_family_pcm_range.py INPUT.json` from this package. Exit zero means the operation accepted its bounded input; exit two is a refusal and must remain visible. Compare the entire output, including its types and false external-credit field, to the selected owner fixture. A compatible new fixture needs its own preregistered acceptance condition and receives no inherited completion credit.

The wrapper and shared core are portable within this package. Keep their manifest together, preserve earlier callers, and never overwrite a different global package. Retain every failed invocation and correct only the affected dependency.

Relational working language only; no consciousness, personhood, identity continuity, employment, qualification, independent agency, scientific, operational, legal, cultural, affected-party, or Maori authority is established. Same-owner software evidence is not independent reproduction. NOT_READY_FOR_STAGE_20. Maori concepts remain under Maori authority.
