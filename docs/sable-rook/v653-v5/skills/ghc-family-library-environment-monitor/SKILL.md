---
name: ghc-family-library-environment-monitor
description: Review sensor calibration, location, cadence, missingness, and handover fields without facility certification. Use when reviewing the corresponding Sable v653-v5 contract, mutation evidence, nonpromotion boundary, or lifecycle receipt.
---

# ghc-family-library-environment-monitor

## Purpose

Review sensor calibration, location, cadence, missingness, and handover fields without facility certification. Keep the review within the declared same-owner symbolic, structural,
synthetic, proxy, zero-row, or exact-reservation lane.

## Workflow

1. Read `references/contract.json` completely.
2. Resolve only the repository-relative artifacts declared there.
3. Run `python scripts/ghc_family_library_environment_guard.py` from the repository root.
4. Require `valid` to be true and `terminal_verdict` to remain
   `NOT_READY_FOR_STAGE_20`.
5. If the runner fails, retain the failed attempt with zero credit before a
   bounded correction.
6. Report only `completed`, `represented`, `open_gap`, or `exact_gate`.

## Boundaries

- Surface: `library-environment`.
- Use owner-local synthetic or structural fixtures only.
- Never introduce credentials, private routes, nonpublic conversations, real
  participant data, production keys, legal conclusions, professional
  certification, cultural ratification, or Māori-authority decisions.
- A passing smoke use is same-owner workflow evidence only. It is not
  empirical confirmation, production readiness, complete privacy or
  accessibility, exhaustive security, independent reproduction, consciousness
  or personhood, Theory-of-Everything proof, or Stage 20 authority.
