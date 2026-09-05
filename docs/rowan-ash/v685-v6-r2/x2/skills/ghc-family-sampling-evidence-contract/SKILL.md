---
name: ghc-family-sampling-evidence-contract
description: Apply the sampling evidence contracts when reviewing an owner-scoped phase artifact or teaching its valid and adverse fixtures.
---

# Sampling evidence contract

Use this guide when the supplied artifact makes a claim involving sampling. Read the named criterion and its source before selecting a fixture. The experimental design statistician lens is a learning practice, not a professional qualification.

## Procedure

1. Identify the current owner, exact source revision, and allowed output directory.
2. Read references/criteria.json. Select the criterion whose acceptance condition matches the actual claim.
3. Use the shared ghc_family_claim_evidence_lab.py interface in the owning repository. The family selector is sampling. A current recipe is python -X utf8 scripts/ghc_family_claim_evidence_lab.py --families sampling --output OWNED_RESULT.json.
4. Inspect both the accepted example and the adverse counterpart. A schema result does not verify the world described by the fields.
5. Keep completed local checks separate from represented claims, open gaps, and exact authority gates.
6. Preserve failed definitions and fixtures. Repair only the affected dependency and record a focused witness.
7. Link the result into the owner flashcard, its pillar, its practice lens, and the task card.

## Criteria

- RA6856R2-N111: Sample counts are nonnegative integers.
- RA6856R2-N112: Missing observations remain explicit.
- RA6856R2-N113: Duplicate observations do not increase sample size.
- RA6856R2-N114: Sampling frames limit generalization.
- RA6856R2-N115: Selection mechanisms are stated.
- RA6856R2-N116: Weights are finite and nonnegative.
- RA6856R2-N117: Clustered data retain their cluster structure.
- RA6856R2-N118: Train and evaluation partitions are disjoint.
- RA6856R2-N119: Bootstrap seeds do not create new participants.
- RA6856R2-N120: Zero real participants remains a real study gap.

## Failure handling

An unknown rule, malformed payload, unsupported evidence promotion, missing source, or contrary result is not a pass. Keep the original record and create a correction with its own content digest. Do not generate external observations, identities, approvals, or live messages to satisfy a local field.

## Reuse and rollback

The accepted and adverse fixtures are local examples. They supply no independent replication, scientific discovery, employment, consciousness, legal authority, or Stage 20 credit. The original source guide remains available after global promotion. Roll back by selecting the prior source package and preserving the new failed candidate as evidence.
