---
name: ghc-family-credential-evidence-contract
description: Apply the credential evidence contracts when reviewing an owner-scoped phase artifact or teaching its valid and adverse fixtures.
---

# Credential evidence contract

Use this guide when the supplied artifact makes a claim involving credential. Read the named criterion and its source before selecting a fixture. The digital identity assurance reviewer lens is a learning practice, not a professional qualification.

## Procedure

1. Identify the current owner, exact source revision, and allowed output directory.
2. Read references/criteria.json. Select the criterion whose acceptance condition matches the actual claim.
3. Use the shared ghc_family_claim_evidence_lab.py interface in the owning repository. The family selector is credential. A current recipe is python -X utf8 scripts/ghc_family_claim_evidence_lab.py --families credential --output OWNED_RESULT.json.
4. Inspect both the accepted example and the adverse counterpart. A schema result does not verify the world described by the fields.
5. Keep completed local checks separate from represented claims, open gaps, and exact authority gates.
6. Preserve failed definitions and fixtures. Repair only the affected dependency and record a focused witness.
7. Link the result into the owner flashcard, its pillar, its practice lens, and the task card.

## Criteria

- RA6856R2-N151: Credential type is separate from credential validity.
- RA6856R2-N152: Issuer and subject are not interchanged.
- RA6856R2-N153: A holder role is not inferred from the subject.
- RA6856R2-N154: Credential context is pinned without remote retrieval.
- RA6856R2-N155: A proof field is not a verified signature.
- RA6856R2-N156: Credential status has an explicit observation time.
- RA6856R2-N157: Revocation and suspension have different meanings.
- RA6856R2-N158: A synthetic identifier is not a live DID.
- RA6856R2-N159: Interoperability requires an exercised protocol.
- RA6856R2-N160: Trust governance remains a separate authority gate.

## Failure handling

An unknown rule, malformed payload, unsupported evidence promotion, missing source, or contrary result is not a pass. Keep the original record and create a correction with its own content digest. Do not generate external observations, identities, approvals, or live messages to satisfy a local field.

## Reuse and rollback

The accepted and adverse fixtures are local examples. They supply no independent replication, scientific discovery, employment, consciousness, legal authority, or Stage 20 credit. The original source guide remains available after global promotion. Roll back by selecting the prior source package and preserving the new failed candidate as evidence.
