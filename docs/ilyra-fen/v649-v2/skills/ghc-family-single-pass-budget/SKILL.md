---
name: ghc-family-single-pass-budget
description: Enforce one successful canonical validation pass and no replay. Use when validating the repository-local v649-v2 transfusion handover fixture, its rejecting mutation, or its evidence boundary.
---

# ghc-family-single-pass-budget

Apply this bounded phase-local workflow only to Ilyra Fen v649-v2 owner artifacts.

## Workflow

1. Read `valid-fixture.json` and `rejecting-fixture.json` as UTF-8.
2. Invoke the matching family-current runner or reusable v649-v2 runtime.
3. Require the valid fixture to be accepted and the rejecting fixture to be refused.
4. Preserve every failure and zero gate; do not infer authority or empirical truth.
5. Record use as same-owner bounded evidence only.

## Boundaries

Do not use this skill to access real participants, patients, specimens, identity keys, tokens, empirical datasets, private archives, accounts, sibling lanes, or host-security controls. Do not claim professional, clinical, legal, cultural, Māori, production, accessibility-complete, security-complete, independent-reproduction, consciousness, personhood, Theory-of-Everything, or Stage 20 authority.
