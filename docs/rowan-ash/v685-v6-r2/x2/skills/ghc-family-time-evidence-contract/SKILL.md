---
name: ghc-family-time-evidence-contract
description: Apply the time evidence contracts when reviewing an owner-scoped phase artifact or teaching its valid and adverse fixtures.
---

# Time evidence contract

Use this guide when the supplied artifact makes a claim involving time. Read the named criterion and its source before selecting a fixture. The metrologist lens is a learning practice, not a professional qualification.

## Procedure

1. Identify the current owner, exact source revision, and allowed output directory.
2. Read references/criteria.json. Select the criterion whose acceptance condition matches the actual claim.
3. Use the shared ghc_family_claim_evidence_lab.py interface in the owning repository. The family selector is time. A current recipe is python -X utf8 scripts/ghc_family_claim_evidence_lab.py --families time --output OWNED_RESULT.json.
4. Inspect both the accepted example and the adverse counterpart. A schema result does not verify the world described by the fields.
5. Keep completed local checks separate from represented claims, open gaps, and exact authority gates.
6. Preserve failed definitions and fixtures. Repair only the affected dependency and record a focused witness.
7. Link the result into the owner flashcard, its pillar, its practice lens, and the task card.

## Criteria

- RA6856R2-N021: Source timestamps require a timezone.
- RA6856R2-N022: Event time remains distinct from retrieval time.
- RA6856R2-N023: New Zealand dates retain their UTC anchor.
- RA6856R2-N024: Expiry is checked against the declared observation time.
- RA6856R2-N025: Intervals cannot have negative duration.
- RA6856R2-N026: Calendar dates do not imply precise instants.
- RA6856R2-N027: Monotonic elapsed time stays separate from civil time.
- RA6856R2-N028: Missing deadline fields remain missing.
- RA6856R2-N029: Correction timestamps preserve event order.
- RA6856R2-N030: Timezone conversion never changes the source event.

## Failure handling

An unknown rule, malformed payload, unsupported evidence promotion, missing source, or contrary result is not a pass. Keep the original record and create a correction with its own content digest. Do not generate external observations, identities, approvals, or live messages to satisfy a local field.

## Reuse and rollback

The accepted and adverse fixtures are local examples. They supply no independent replication, scientific discovery, employment, consciousness, legal authority, or Stage 20 credit. The original source guide remains available after global promotion. Roll back by selecting the prior source package and preserving the new failed candidate as evidence.
