# Ilyra Fen v662-v6 exact-delta threat model

## Assets

Exact Git ancestry, owner attribution, immutable x1, sparse scope, changed-file
manifests, metadata budgets, path and URI boundaries, numeric and timestamp
contracts, attestation-shape boundaries, retained failures, privacy boundaries,
and successor-route truth.

## Threats and controls

- Decompression budgets inspect synthetic metadata only and invoke no decoder.
- Sparse logical and stored sizes remain distinct without materializing a file.
- Archive links, rooted Windows references, URI traversal, malformed numeric lexemes, and duplicate JSON Pointer targets fail closed.
- Media-type allowlisting never opens content or implies safety.
- DSSE PAE and in-toto checks validate bounded shape only; signature and provenance truth stay false.
- Wall-clock rollback, monotonic duration, and explicit-offset timestamps remain distinct and never become trusted time.
- Scope remains the exact owner delta and literal test dependencies.
- One canonical success is permitted and never replayed.
- Exact-title reread and acknowledgement are required for delivery.

## Residual risk

This is not exhaustive security, platform completeness, production assurance,
complete privacy or accessibility, independent reproduction, legal review,
cultural ratification, or Maori authority. Residual risks remain exact-gated.
