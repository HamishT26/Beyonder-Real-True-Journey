# Vesper v662-v4 exact-delta threat model

## Assets

Exact Git ancestry, owner attribution, x1 separation, changed-file manifests,
validation receipts, retained failures, privacy boundaries, and successor-route
truth.

## Threats and controls

- Duplicate JSON keys: strict ordered-pair parsing refuses ambiguity.
- Unicode or case-fold path collisions: the exact path audit fails closed.
- Bidi or control-character deception: explicit controls are rejected.
- Symlink, gitlink, or type confusion: only regular blob modes are accepted.
- Manifest tampering: per-file Git blob hashes, SHA-256, canonical commitment,
  and a deterministic Merkle root bind the delta.
- Stale baton substitution: relative path, committed blob, digest, and word
  range must all match.
- Scope creep: only exact-delta files and literal test dependencies execute.
- Validation laundering: one canonical success is permitted and never replayed.
- Route substitution: explicit current and next owners plus exact-title reread
  and acknowledgement are required.

## Residual risk

This is not exhaustive security, production assurance, complete privacy,
independent reproduction, legal review, cultural ratification, or Maori
authority. Residual risks remain exact-gated.
