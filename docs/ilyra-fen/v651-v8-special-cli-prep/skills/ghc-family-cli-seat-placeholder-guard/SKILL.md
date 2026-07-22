---
name: ghc-family-cli-seat-placeholder-guard
description: Apply the bounded cli seat placeholder guard contract for GHC Family CLI preparation. Use only when the matching trigger is present and preserve launch, identity, authority, privacy, production, and Stage 20 gates.
---

# ghc-family-cli-seat-placeholder-guard

## Trigger

Use this phase-local skill only for `cli seat placeholder guard` inside an owner-scoped preparation or validation lane.

## Procedure

1. Read the current phase truth and the exact frozen proposal linked to this guard.
2. Run the corresponding family-current runner on one accepting fixture and one rejecting fixture.
3. Credit only the declared bounded invariant. Preserve each rejection and tooling failure.
4. Stop before any task creation, CLI launch, account change, credential read, sibling mutation, destructive action, or authority substitution.
5. Record the result in the skill-use ledger and Method Flow when recovery was needed.

## Truth boundary

This skill is repository-local same-owner workflow guidance. It is not independent reproduction, production certification, exhaustive security, complete privacy or accessibility, professional validation, legal or cultural authority, Maori authority, consciousness or personhood evidence, or Stage 20 authority.
