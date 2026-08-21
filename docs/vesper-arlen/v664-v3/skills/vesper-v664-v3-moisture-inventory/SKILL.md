---
name: vesper-v664-v3-moisture-inventory
description: Validate unit, uncertainty, inventory, and quarantine ledgers while refusing measurement, stock, availability, and conservation claims.
---

# vesper-v664-v3-moisture-inventory

Use this skill only for bounded owner-local synthetic seed-bank evidence matching the profile `moisture-inventory`.

## Workflow

1. Confirm the record declares `synthetic=true`, zero real-world rows, no authority, one frozen outcome, and every protected refusal.
2. Invoke the family-current `moisture-inventory` profile in `ghc_family_seed_bank_evidence.py`.
3. Preserve the positive witness and every rejecting mutation with zero mutation completion credit.
4. Stop on any schema, source, uncertainty, privacy, rights, authority, production, empirical, or Stage 20 promotion.

Covered surfaces:

- `moisture-unit-registry`
- `inventory-quarantine-ledger`

## Output boundary

Return only the bounded fixture result, rejected-mutation count, frozen outcome, and still-open gates. This skill does not authorize real accessions, seeds, packets, lots, storage, calibration, viability or germination tests, regeneration, distribution, transfers, people, identity operations, stewardship or benefit-sharing decisions, legal or cultural interpretation, Māori authority, privacy or accessibility completeness, production, empirical confirmation, independent reproduction, proof, canon, or Stage 20 readiness.
