#!/usr/bin/env python3
"""Final lifecycle constants for Lyren v657-v1."""

from __future__ import annotations


SOURCE_COMMIT = "a033d1318920de1beec288f9c5b27e7f73a8ff3b"
X1_COMMIT = "2e3d51c838caa01d05b0713b6c165bef0be882d5"
EVIDENCE_COMMIT = "91c36c44b6ccecbf73892792e07525cc7577d0c8"
CLOSEOUT_COMMIT = "8ff8a0658e10e2ddec8db77bf1edb2fe9047fedb"
CLOSEOUT_EFFECTIVE_NEGATIVES = 15246
CLOSEOUT_EFFECTIVE_METHODS = 1530
OPEN_GAPS = 105
EXACT_GATES = 104

# Append only final-preparation failures actually observed before the exact
# final candidate is committed.
FINAL_PREPARATION_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6571-FINAL-N21",
        "slug": "final-suite-before-owner-manifest",
        "failure_signature": (
            "The first bounded final and successor-scope suite ran after the final "
            "record builder but before the final receipt builder, so the required "
            "final owner manifest was absent and one of thirteen checks failed."
        ),
        "candidate_workaround": (
            "Build the final privacy, cap, and owner-manifest receipts before rerunning "
            "the same bounded final and successor-scope suite."
        ),
        "recurrence_guard": (
            "Treat the prospective final owner manifest as a declared prerequisite of "
            "the final artifact-packet test."
        ),
        "fail_procedure": (
            "Run the final and successor-scope unit modules immediately after the "
            "final record builder and before the final receipt builder."
        ),
        "fail_observed": (
            "Twelve of thirteen checks passed; the artifact-packet check failed because "
            "validation/final-owner-manifest.json did not yet exist."
        ),
        "pass_procedure": (
            "Generate the final receipts at the exact closeout head, then rerun the "
            "same thirteen checks without changing their scope."
        ),
        "pass_observed": (
            "The final owner manifest was present and the unchanged bounded final and "
            "successor-scope suite passed all thirteen checks."
        ),
        "scope_boundary": "Owner-local final artifact dependency-order recovery only.",
    },
    {
        "negative_id": "V6571-FINAL-N22",
        "slug": "selected-tests-package-import-path",
        "failure_signature": (
            "A read-only selected-test probe imported the final validator through the "
            "scripts package without adding that directory to Python's module path, "
            "so a sibling absolute import failed before any selected test ran."
        ),
        "candidate_workaround": (
            "Insert the repository-local scripts directory into the probe's module "
            "path before importing the final validator and calling selected_tests."
        ),
        "recurrence_guard": (
            "Invoke lifecycle modules that use sibling absolute imports from their "
            "script context or bind the scripts directory explicitly."
        ),
        "fail_procedure": (
            "Import scripts.ghc_family_v657_v1_final_validator directly from a root-"
            "level Python command and call selected_tests."
        ),
        "fail_observed": (
            "Python raised ModuleNotFoundError for the sibling evidence-receipt module "
            "before running any selected tests, so the probe earned zero test credit."
        ),
        "pass_procedure": (
            "Add the local scripts directory to sys.path, import the same final "
            "validator module, and call the unchanged selected_tests function."
        ),
        "pass_observed": (
            "The unchanged selected scope ran all seventy-three tests with zero "
            "failures, errors, or skips."
        ),
        "scope_boundary": "Owner-local read-only Python import-context recovery only.",
    },
]
