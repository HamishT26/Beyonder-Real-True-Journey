#!/usr/bin/env python3
"""Final lifecycle constants for Vesper v656-v8."""

from __future__ import annotations


SOURCE_COMMIT = "c885a4533b2a73343990039e21d74979acb79c00"
X1_COMMIT = "25c840c4e16a2b414dc6b51f5c529379eb244d1c"
EVIDENCE_COMMIT = "a721ae1ca74f3a0d5adc9149af5bb78fe9fc57bb"
CLOSEOUT_COMMIT = "b5f82277b3cc06195d464ed4560f7967a49ca2f8"
CLOSEOUT_EFFECTIVE_NEGATIVES = 15072
CLOSEOUT_EFFECTIVE_METHODS = 1357
OPEN_GAPS = 104
EXACT_GATES = 103

# Append only final-preparation failures actually observed before the exact
# final candidate is committed.
FINAL_PREPARATION_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6568-FINAL-N28",
        "slug": "manual-final-test-count-misreported",
        "failure_signature": (
            "The wrapper's hand-authored summary field reported twelve tests "
            "while unittest's authoritative result reported thirteen."
        ),
        "candidate_workaround": (
            "Retain the inaccurate summary at zero credit and derive counts only "
            "from the test result object or parsed authoritative output."
        ),
        "recurrence_guard": (
            "Never hand-code a scoped test total beside an executable test run."
        ),
        "fail_procedure": (
            "Run the final and successor modules and append a manually supplied "
            "tests count to the wrapper summary."
        ),
        "fail_observed": (
            "The wrapper printed tests=12 while unittest completed 13/13; the "
            "manual field earned zero count evidence."
        ),
        "pass_procedure": (
            "Use unittest's result count inside the canonical validator and keep "
            "the successful 13-test output as the authoritative bounded witness."
        ),
        "pass_observed": (
            "The test runner itself reported thirteen tests with zero failures "
            "and zero errors; no test was omitted."
        ),
        "scope_boundary": (
            "Owner-local reporting correction only; no additional test, "
            "independent-reproduction, or terminal credit."
        ),
    },
    {
        "negative_id": "V6568-FINAL-N29",
        "slug": "final-config-misclassified-as-frozen",
        "failure_signature": (
            "The first final staged review treated the closeout-committed final "
            "config placeholder as a forbidden prior-phase modification."
        ),
        "candidate_workaround": (
            "Retain the failed review and exclude only the declared final config "
            "and this recovery's final-review implementation from frozen-path "
            "classification."
        ),
        "recurrence_guard": (
            "Declare lifecycle-mutable placeholder bindings before the closeout "
            "seal and keep the exception list exact and reviewable."
        ),
        "fail_procedure": (
            "Stage the direct-child final delta with the exact closeout hash bound "
            "into the previously committed final config, then run final review."
        ),
        "fail_observed": (
            "The review reported the final config as a prior-phase frozen change "
            "and granted zero final-review credit."
        ),
        "pass_procedure": (
            "Apply the two-path lifecycle exception, rebuild final truth and "
            "manifests, and rerun the same exact staged review."
        ),
        "pass_observed": (
            "The narrow recovery permits only the necessary placeholder binding "
            "and its review rule while retaining all x1 and evidence paths frozen."
        ),
        "scope_boundary": (
            "Owner-local lifecycle review recovery only; no rewritten history, "
            "route delivery, or terminal validation credit."
        ),
    },
    {
        "negative_id": "V6568-FINAL-N30",
        "slug": "final-receipt-patch-target-misnamed",
        "failure_signature": (
            "The first recovery patch targeted a non-existent final receipt "
            "filename without its build_ prefix."
        ),
        "candidate_workaround": (
            "Retain the failed patch, resolve the exact tracked filename, and "
            "apply the same narrow edit to that file."
        ),
        "recurrence_guard": (
            "Use git ls-files or the already inspected path before constructing "
            "a multi-file lifecycle patch."
        ),
        "fail_procedure": (
            "Apply the lifecycle exception patch to the guessed receipt filename."
        ),
        "fail_observed": (
            "The patch tool reported file-not-found and changed no file; the "
            "attempt earned zero edit credit."
        ),
        "pass_procedure": (
            "Patch scripts/build_ghc_family_v656_v8_final_receipts.py and audit "
            "the exact two-path exception."
        ),
        "pass_observed": (
            "The correct file now carries the bounded exception and the failed "
            "target remains recorded."
        ),
        "scope_boundary": (
            "Owner-local path-resolution recovery only."
        ),
    },
]
