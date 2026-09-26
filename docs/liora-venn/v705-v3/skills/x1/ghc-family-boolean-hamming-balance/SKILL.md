---
name: ghc-family-boolean-hamming-balance
description: Count finite truth-table weight and report exact balance. Use only for bounded public synthetic Boolean-function records in the Liora v705-v3 owner lane.
---

# ghc-family-boolean-hamming-balance

Read one frozen `ghc.family.boolean-function.request.v1` record and its saved owner result for `hamming_weight_balance`.

1. Require a binary truth table of length exactly `2^variables` and purpose `public_synthetic`.
2. Preserve the original truth table and declared variable order.
3. Check only the exact finite invariant named by `hamming_weight_balance`.
4. Refuse authority-bearing, participant, production, empirical, or private-data envelopes.
5. Retain a malformed subject as failed even when its separate refusal witness passes.

The result is same-owner finite software evidence only. It is not independent reproduction, cryptographic suitability, empirical GMUT evidence, production validation, professional authority, complete accessibility or security, or Stage 20 readiness.
