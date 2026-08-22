---
name: ghc-family-mosaic-observation-diagnosis-firewall
description: Keep observation, uncertainty, diagnosis refusal, and manual-review vacancy distinct.
---

# Mosaic observation diagnosis firewall

## Scope

Use only for Elowen Cairn v665-v4 owner-local synthetic, zero-row, or typed-formal artifacts. This skill confers no professional, empirical, production, legal, cultural, Māori, affected-party, accessibility-complete, security-complete, or Stage 20 authority.

## Required inputs

- UTF-8 JSON object using runner profile `mosaic_observation`.
- Base boundary fields: `synthetic`, `real_rows`, `authority_events`, `claim_ceiling`, `terminal_verdict`, and `source_ids`.
- Profile fields: diagnosis_claim, manual_evaluation_present, observation_terms, treatment_claim, uncertainty_present.

## Procedure

1. Read the complete input and preserve its digest.
2. Require `synthetic=true`, zero real rows, zero authority events, and `NOT_READY_FOR_STAGE_20`.
3. Invoke `scripts/ghc_family_mosaic_observation_firewall.py` and retain every rejection before recovery.
4. Report only the bounded runner decision and exact claim ceiling.

## Fail-closed stops

Stop on real rows, real mosaics, tesserae, sites, images, people, keys, proofs, identity events, treatment or destructive action, professional decisions, protected-gate promotion, malformed JSON, source vacancy, or an unexpected claim ceiling.

## Output boundary

An accepted fixture demonstrates only that this same-owner software contract accepted one bounded structure and rejected preregistered mutations. It is not scientific confirmation, mosaic conservation guidance, professional validation, production conformance, independent reproduction, proof, or authority.

## Terminal boundary

The only terminal verdict permitted here is `NOT_READY_FOR_STAGE_20`.
