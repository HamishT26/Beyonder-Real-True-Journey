#!/usr/bin/env python3
"""Final lifecycle constants for Neris v656-v7."""

from __future__ import annotations


SOURCE_COMMIT = "7d0954ea088c9957cdcc81a07ef2c8b2d88997b3"
X1_COMMIT = "f048a624daa5d6035cb01a485d74f43151cc4cd2"
EVIDENCE_COMMIT = "c91e45d9fcc7da6bb5160767c38cdd1167b3a88a"
CLOSEOUT_COMMIT = "91dbe7ec626e56483e77ecdc41608528a3b0a925"
CLOSEOUT_EFFECTIVE_NEGATIVES = 14891
CLOSEOUT_EFFECTIVE_METHODS = 1176
OPEN_GAPS = 103
EXACT_GATES = 102

# Append only final-preparation failures actually observed before the exact
# final candidate is committed.
FINAL_PREPARATION_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6567-X2-N12",
        "slug": "closeout-validation-receipt-omitted-from-seal",
        "failure_signature": (
            "The exact closeout commit passed its staged review and test selection "
            "but omitted the dedicated closeout-validation.json receipt expected "
            "by the final builder."
        ),
        "candidate_workaround": (
            "Retain the omission, generate the same-owner detailed validation "
            "receipt after closeout under the exact declared filename, and keep it "
            "inside the final delta rather than backdating it."
        ),
        "recurrence_guard": (
            "Resolve every direct-child builder prerequisite before constructing "
            "the parent lifecycle manifest and commit."
        ),
        "fail_procedure": (
            "Inspect the exact closeout tree for the final builder's declared "
            "closeout-validation receipt."
        ),
        "fail_observed": (
            "The receipt was absent from the immutable closeout tree and received "
            "zero closeout-receipt credit."
        ),
        "pass_procedure": (
            "Run the detailed validator after closeout, write "
            "validation/closeout-validation.json, and label it as a final-delta "
            "recovery while preserving the omission."
        ),
        "pass_observed": (
            "The post-closeout same-owner receipt passed all 322 detailed checks "
            "without rewriting the closeout commit."
        ),
        "scope_boundary": (
            "Final-preparation receipt recovery only; no independent reproduction "
            "or retroactive closeout credit."
        ),
    },
    {
        "negative_id": "V6567-X2-N13",
        "slug": "final-compile-script-prefix-omission",
        "failure_signature": (
            "The first final py_compile selection passed bare script filenames "
            "from the repository root and failed with file-not-found before "
            "compiling the final architecture."
        ),
        "candidate_workaround": (
            "Prefix each final script with scripts/ while leaving test paths "
            "repository-relative, then rerun the same bounded compile selection."
        ),
        "recurrence_guard": (
            "Normalize generated compile targets to explicit repository-relative "
            "paths and assert that every target exists before invocation."
        ),
        "fail_procedure": (
            "Invoke py_compile from the repository root with bare final script "
            "filenames."
        ),
        "fail_observed": (
            "Python returned file-not-found for build_ghc_family_v656_v7_final.py; "
            "the attempt received zero compile credit."
        ),
        "pass_procedure": (
            "Use explicit scripts/... targets and rerun py_compile over the same "
            "four scripts and two tests."
        ),
        "pass_observed": (
            "The corrected six-file compile selection completed without output."
        ),
        "scope_boundary": (
            "Owner-local compile target recovery only."
        ),
    },
    {
        "negative_id": "V6567-X2-N14",
        "slug": "final-tests-before-receipt-manifest",
        "failure_signature": (
            "The first final and successor test selection ran before the final "
            "receipt builder had created final-owner-manifest.json."
        ),
        "candidate_workaround": (
            "Retain the failed selection, build the final privacy, cap, and owner "
            "manifest receipts, then rerun the identical scoped tests."
        ),
        "recurrence_guard": (
            "Follow the declared final lifecycle order: candidate builder, receipt "
            "builder, scoped tests, exact staging, and staged review."
        ),
        "fail_procedure": (
            "Run the final artifact-existence test immediately after the candidate "
            "builder and before the final receipt builder."
        ),
        "fail_observed": (
            "One final test failed because validation/final-owner-manifest.json did "
            "not yet exist; the 13-test selection received zero success credit."
        ),
        "pass_procedure": (
            "Build the declared final receipts and rerun the same final and "
            "successor modules."
        ),
        "pass_observed": (
            "The final owner manifest existed and the artifact packet check passed."
        ),
        "scope_boundary": (
            "Final lifecycle ordering recovery only."
        ),
    },
    {
        "negative_id": "V6567-X2-N15",
        "slug": "successor-baton-brittle-substring",
        "failure_signature": (
            "The first successor-scope test required the exact substring "
            "'for v656-v8' even though the baton stated the stronger phrase "
            "'solo v656-v8 x1/x2 phase' and separately named Vesper."
        ),
        "candidate_workaround": (
            "Assert the exact recipient, phase header, solo x1/x2 phrase, and "
            "replacement prohibition instead of an incidental preposition."
        ),
        "recurrence_guard": (
            "Bind route tests to semantic state fields and stable exact-title or "
            "phase markers, not incidental prose fragments."
        ),
        "fail_procedure": (
            "Search the baton for the brittle literal substring 'for v656-v8'."
        ),
        "fail_observed": (
            "The successor test failed despite the baton correctly naming Vesper "
            "and v656-v8; the assertion earned zero route-contract credit."
        ),
        "pass_procedure": (
            "Require the VESPER ARLEN header, the solo v656-v8 x1/x2 phrase, the "
            "exact-title task marker, and the no-replacement instruction."
        ),
        "pass_observed": (
            "The revised assertion validated the same committed route semantics "
            "without changing the baton."
        ),
        "scope_boundary": (
            "Prepared-baton test precision only; no send or successor credit."
        ),
    },
]
