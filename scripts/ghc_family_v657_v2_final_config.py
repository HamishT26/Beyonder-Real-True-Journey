#!/usr/bin/env python3
"""Final lifecycle constants for Ilyra Fen v657-v2."""

from __future__ import annotations


SOURCE_COMMIT = "4d888c1387c4203bd21acd7156bed2b0a13f2bee"
X1_COMMIT = "3f79c72723f927c03045091266431b9adf11dff3"
EVIDENCE_COMMIT = "ceb6316d97551f376d853eb27e0590ae9efae9bd"
CLOSEOUT_COMMIT = "3be6573ebebd1111f9762b77a93c90f0a1c627f0"
CLOSEOUT_EFFECTIVE_NEGATIVES = 15432
CLOSEOUT_EFFECTIVE_METHODS = 1716
OPEN_GAPS = 106
EXACT_GATES = 105

# Append only final-preparation failures actually observed before the exact
# final candidate is committed.
FINAL_PREPARATION_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6572-FINAL-N35",
        "slug": "combined-final-semantic-patch-context-mismatch",
        "failure_signature": (
            "A combined final-layer semantic patch expected an exact overview sentence "
            "that differed from the mechanically copied source text."
        ),
        "candidate_workaround": (
            "Apply exact lifecycle, route, validator, and overview edits as separate "
            "observed-text hunks."
        ),
        "recurrence_guard": (
            "Inspect each inherited final symbol before combining semantic patches; "
            "one unmatched optional prose line must not obscure all intended edits."
        ),
        "fail_procedure": (
            "Apply one patch spanning the builder header, closeout validation receipt, "
            "route records, scope list, checklist, and overview pronouns."
        ),
        "fail_observed": (
            "Patch verification rejected the complete operation before any file "
            "changed, so it earned zero final-preparation credit."
        ),
        "pass_procedure": (
            "Patch each exact observed lifecycle surface independently and compile "
            "the complete final tool set before execution."
        ),
        "pass_observed": (
            "The corrected final tools bind the exact closeout, preserve the held "
            "route, and retain this failure in Method Flow."
        ),
        "scope_boundary": "Owner-local final-tool editing recovery only.",
    },
    {
        "negative_id": "V6572-FINAL-N36",
        "slug": "successor-test-literal-clause-mismatch",
        "failure_signature": (
            "The first 73-test final precommit selection passed 72 tests but one "
            "successor-scope test required a standalone sentence not present in the "
            "sealed baton, despite its longer clause preserving the same prohibition."
        ),
        "candidate_workaround": (
            "Leave the closeout-sealed baton immutable and bind the final test to its "
            "exact committed no-inference and no-replacement wording."
        ),
        "recurrence_guard": (
            "Derive lifecycle wording assertions from the immutable Git blob instead "
            "of paraphrasing a semantically equivalent sentence."
        ),
        "fail_procedure": (
            "Run the 73-test selection with a successor assertion for the exact text "
            "Do not create a replacement."
        ),
        "fail_observed": (
            "Seventy-two tests passed and the one literal substring assertion failed; "
            "the aggregate received zero pass credit."
        ),
        "pass_procedure": (
            "Assert the frozen baton phrases Do not infer a recipient from this file "
            "and create a replacement, or send a second confirmation."
        ),
        "pass_observed": (
            "The unchanged baton and corrected exact-text successor test pass together "
            "without weakening the route boundary."
        ),
        "scope_boundary": "Owner-local immutable-baton test-alignment recovery only.",
    },
]
