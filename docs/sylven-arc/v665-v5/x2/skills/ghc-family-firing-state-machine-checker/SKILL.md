---
name: ghc-family-firing-state-machine-checker
description: Check synthetic ramp, soak, cool, abort, and power-loss transitions without equipment action.
---

# Firing state machine checker

## Scope

Use only for Sylven Arc v665-v5 owner-local synthetic, zero-row, or typed-formal artifacts. This skill confers no professional, empirical, production, legal, cultural, Māori, affected-party, accessibility-complete, security-complete, or Stage 20 authority.

## Required inputs

- UTF-8 JSON object using runner profile `firing_state_machine`.
- Base boundary fields: `synthetic`, `real_rows`, `authority_events`, `claim_ceiling`, `terminal_verdict`, and `source_ids`.
- Profile fields: abort_dominant, real_actuation, restart_authorized, states, transitions.

## Procedure

1. Read the complete input and preserve its digest.
2. Require `synthetic=true`, zero real rows, zero authority events, and `NOT_READY_FOR_STAGE_20`.
3. Invoke `scripts/ghc_family_sylven_v665_v5_firing_state_machine.py` and retain every rejection before recovery.
4. Report only the bounded runner decision and exact claim ceiling.

## Fail-closed stops

Stop on real rows, real studios, kilns, firings, ware, cones, glazes, materials, images, people, keys, proofs, identity events, equipment action, professional decisions, protected-gate promotion, malformed JSON, source vacancy, or an unexpected claim ceiling.

## Output boundary

An accepted fixture demonstrates only that this same-owner software contract accepted one bounded structure and rejected preregistered mutations. It is not scientific confirmation, ceramics or kiln guidance, professional validation, production conformance, independent reproduction, proof, or authority.

## Terminal boundary

The only terminal verdict permitted here is `NOT_READY_FOR_STAGE_20`.
