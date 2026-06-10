# v470 THOS v6 x3 to v6 x4 Handoff

v6 x3 adds the manifest/checksum layer and freezes the first shared snapshot, enum/null, and negative-fixture contracts around the v6 x2 package.

## v6 x4 Focus

The next pass should move from definition to enforcement. The cleanest next step is a verifier that can consume a manifest, reject checksum mismatch before trust propagation, reject snapshot contract drift, and execute the negative fixture set.

## Required Tests

- Corrupt one artifact byte and require deterministic failure.
- Feed a snapshot contract version mismatch and require deterministic failure or open gap.
- Preserve unknown enum values as unknown, not null.
- Block duplicate joins and missing provenance before visualization/synthesis trust.
- Reconcile visualization row counts against a declared row universe.

## Open Gates

All six GMUT gates remain open. This is THOS infrastructure only.
