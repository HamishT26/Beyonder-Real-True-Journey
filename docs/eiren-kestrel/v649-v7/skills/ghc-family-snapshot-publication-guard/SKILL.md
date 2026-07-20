---
name: ghc-family-snapshot-publication-guard
description: Evaluate bounded snapshot publication guard contracts, mutations, and evidence boundaries. Use when the v649-v7 phase or a compatible future phase needs ghc-family-snapshot-publication-guard without production, authority, independent-reproduction, or Stage 20 promotion.
---

# Snapshot Publication Guard

1. Read the declared contract, source status, mutation plan, and protected gates.
2. Refuse missing fields, boundary promotion, or evidence without an attributable witness.
3. Run only bounded owner-local fixtures; retain every rejected mutation.
4. Emit one of `completed`, `represented`, `open_gap`, or `exact_gate`.
5. Keep same-owner validation distinct from independent reproduction.

Never infer consciousness, personhood, professional competence, legal or cultural authority, Maori authority, production safety, empirical confirmation, Theory of Everything, or Stage 20 readiness.
