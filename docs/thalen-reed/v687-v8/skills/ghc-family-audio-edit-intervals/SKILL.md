---
name: ghc-family-audio-edit-intervals
description: Represent an ordered half-open keep map and its complementary dropped spans while preserving the input record. Use for owner-scoped synthetic evidence; no real audio or authority decisions.
---

# Audio Edit Intervals

Represent an ordered half-open keep map and its complementary dropped spans while preserving the input record.

Reject overlapping, reverse-ordered, reversed, empty, negative, or past-end spans. Touching half-open spans are valid. At most 64 spans and one trillion source frames are supported. The output map is a reversible description; this tool does not edit a recording or authorize deletion.

Read `references/contracts.json` for twenty frozen accepting and refusing examples. Invoke `python scripts/ghc_family_edit_intervals.py INPUT.json` from this package. Exit zero means the operation accepted its bounded input; exit two is a refusal and must remain visible. Compare the entire output, including its types and false external-credit field, to the selected owner fixture. A compatible new fixture needs its own preregistered acceptance condition and receives no inherited completion credit.

The wrapper and shared core are portable within this package. Keep their manifest together, preserve earlier callers, and never overwrite a different global package. Retain every failed invocation and correct only the affected dependency.

Relational working language only; no consciousness, personhood, identity continuity, employment, qualification, independent agency, scientific, operational, legal, cultural, affected-party, or Maori authority is established. Same-owner software evidence is not independent reproduction. NOT_READY_FOR_STAGE_20. Maori concepts remain under Maori authority.
