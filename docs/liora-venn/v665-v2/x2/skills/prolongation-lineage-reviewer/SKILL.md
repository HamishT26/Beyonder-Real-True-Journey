---
name: prolongation-lineage-reviewer
description: Trace order lifts and rank vacancies while refusing formal-solution or termination claims.
---

# Prolongation lineage reviewer

## Scope

Use only for Liora Venn v665-v2 owner-local synthetic or formal artifacts. This skill confers no professional, operational, legal, cultural, Māori, production, empirical, or Stage 20 authority.

## Required inputs

- UTF-8 JSON object using runner profile `prolongation_lineage`.
- Base boundary fields: `synthetic`, `real_rows`, `authority_events`, `claim_ceiling`, `terminal_verdict`, and `source_ids`.
- Profile fields: formal_solution_claim, prolongation_steps, rank_claim.

## Procedure

1. Read the complete input and preserve its digest.
2. Require `synthetic=true`, zero real rows, zero authority events, and `NOT_READY_FOR_STAGE_20`.
3. Invoke `scripts/ghc_family_prolongation_lineage.py` and retain every rejection before any recovery.
4. Report only the bounded runner decision and its exact claim ceiling.

## Fail-closed stops

Stop on real rows, real people, real vessels, chart cells, measurements, operational decisions, identity events, protected-gate promotion, source vacancy, malformed JSON, or an unexpected claim ceiling.

## Output boundary

An accepted fixture demonstrates only that this same-owner software contract accepted one synthetic structure and rejected its preregistered mutations. It is not conformance, navigation advice, professional validation, proof, production readiness, independent reproduction, or authority.

## Terminal boundary

The only terminal verdict allowed here is `NOT_READY_FOR_STAGE_20`.
