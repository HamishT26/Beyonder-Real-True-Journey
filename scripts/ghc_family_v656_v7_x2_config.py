#!/usr/bin/env python3
"""Immutable x2 lifecycle configuration for Neris v656-v7."""

from __future__ import annotations


SOURCE_COMMIT = "7d0954ea088c9957cdcc81a07ef2c8b2d88997b3"
X1_COMMIT = "f048a624daa5d6035cb01a485d74f43151cc4cd2"
PHASE_ROOT = "docs/neris-solane/v656-v7"
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 14729
SOURCE_EFFECTIVE_NEGATIVES = 14730
X1_OPERATIONAL_NEGATIVES = 10
SOURCE_OPEN_GAPS = 102
SOURCE_EXACT_GATES = 101
SOURCE_METHODS = 1015
X1_METHODS = 10
MUTATIONS_PER_PROPOSAL = 5
EXPECTED_PROPOSALS = 30
EXPECTED_MUTATIONS = EXPECTED_PROPOSALS * MUTATIONS_PER_PROPOSAL
EXPECTED_DISTRIBUTION = {
    "completed": 23,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}

# Phase-local x2 operational failures are appended only after they are actually
# observed. Inherited owner failures remain inherited evidence, not Neris credit.
X2_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6567-X2-N11",
        "slug": "evidence-validation-receipt-filename-drift",
        "failure_signature": (
            "The first detailed-validation invocation wrote a valid receipt under "
            "an undeclared evidence-detailed-validation filename rather than the "
            "declared evidence-validation lifecycle exclusion."
        ),
        "candidate_workaround": (
            "Remove only the misnamed uncommitted receipt, write the same validated "
            "payload to evidence-validation.json, and rebuild the candidate manifest."
        ),
        "recurrence_guard": (
            "Resolve lifecycle output names from the receipt builder's declared "
            "exclusions before invoking a validator."
        ),
        "fail_procedure": (
            "Invoke the detailed validator with an inferred descriptive filename."
        ),
        "fail_observed": (
            "The validation itself passed, but the output path drifted from the "
            "declared lifecycle contract and received zero lifecycle credit."
        ),
        "pass_procedure": (
            "Use validation/evidence-validation.json exactly and rebuild manifests "
            "after removing the misnamed uncommitted file."
        ),
        "pass_observed": (
            "The detailed receipt occupied the declared path and the regenerated "
            "manifest/exclusion set reconciled."
        ),
        "scope_boundary": (
            "Owner-local uncommitted lifecycle-filename recovery only."
        ),
    }
]
