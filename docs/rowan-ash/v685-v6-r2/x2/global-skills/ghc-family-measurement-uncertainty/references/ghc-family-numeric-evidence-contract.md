---
name: ghc-family-numeric-evidence-contract
description: Apply the numeric evidence contracts when reviewing an owner-scoped phase artifact or teaching its valid and adverse fixtures.
---

# Numeric evidence contract

Use this guide when the supplied artifact makes a claim involving numeric. Read the named criterion and its source before selecting a fixture. The metrologist lens is a learning practice, not a professional qualification.

## Procedure

1. Identify the current owner, exact source revision, and allowed output directory.
2. Read references/criteria.json. Select the criterion whose acceptance condition matches the actual claim.
3. Use the shared ghc_family_claim_evidence_lab.py interface in the owning repository. The family selector is numeric. A current recipe is python -X utf8 scripts/ghc_family_claim_evidence_lab.py --families numeric --output OWNED_RESULT.json.
4. Inspect both the accepted example and the adverse counterpart. A schema result does not verify the world described by the fields.
5. Keep completed local checks separate from represented claims, open gaps, and exact authority gates.
6. Preserve failed definitions and fixtures. Repair only the affected dependency and record a focused witness.
7. Link the result into the owner flashcard, its pillar, its practice lens, and the task card.

## Criteria

- RA6856R2-N041: Exact rational comparisons avoid float equality.
- RA6856R2-N042: Precision is declared for arbitrary precision arithmetic.
- RA6856R2-N043: Relative tolerance is paired with absolute tolerance.
- RA6856R2-N044: Nonfinite numeric values are refused.
- RA6856R2-N045: Cancellation is checked against an exact reference.
- RA6856R2-N046: Polynomial derivatives match symbolic references.
- RA6856R2-N047: Residual signs remain attached to their convention.
- RA6856R2-N048: Integer domain restrictions survive serialization.
- RA6856R2-N049: Repeated seeds do not imply independent replication.
- RA6856R2-N050: Numeric convergence retains a finite tested range.

## Failure handling

An unknown rule, malformed payload, unsupported evidence promotion, missing source, or contrary result is not a pass. Keep the original record and create a correction with its own content digest. Do not generate external observations, identities, approvals, or live messages to satisfy a local field.

## Reuse and rollback

The accepted and adverse fixtures are local examples. They supply no independent replication, scientific discovery, employment, consciousness, legal authority, or Stage 20 credit. The original source guide remains available after global promotion. Roll back by selecting the prior source package and preserving the new failed candidate as evidence.
