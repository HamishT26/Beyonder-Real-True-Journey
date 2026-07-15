---
name: ghc-review-freed-id-state-machines
description: Review synthetic Freed ID credential state machines for deferred issuance, token scope, polling, expiry, notification idempotency, and replay. Use when testing identity-protocol structure without real credentials or production claims.
---

# Review Freed ID state machines

1. Freeze allowed states, events, token scopes, expiry rules, and terminal transitions from the cited specification.
2. Run valid and invalid synthetic sequences with no real key or credential material.
3. Reject unknown, consumed, expired, mis-scoped, replay-changing, or out-of-order transitions.
4. Preserve notification idempotency and failed-vector evidence.
5. Reserve real issuance, resolution, revocation, interoperability, privacy review, security review, and trust governance.

Structural conformance fixtures are not production identity assurance.
