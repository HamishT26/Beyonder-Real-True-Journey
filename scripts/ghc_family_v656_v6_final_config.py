#!/usr/bin/env python3
"""Final lifecycle constants for Elaren v656-v6."""

from __future__ import annotations


SOURCE_COMMIT = "8a4bb8e8b6a649040c531e8d3dd36925fd0da301"
X1_COMMIT = "9c0227286b93672a4d98dba305e1c627a2300279"
EVIDENCE_COMMIT = "0744740cc17dfa57b0d151957d1edc7a2bb2c282"
CLOSEOUT_COMMIT = "7fd248f8322e5d8a6c8d8b02bdaa8eab3d5139b1"
ORIGINAL_FINAL_COMMIT = "778e3ca49c25a8aced6701258733f5e11c1b3a82"
FAILED_CANONICAL_RECEIPT_SHA256 = (
    "6c04fda22f5097535271560df6a29353b8baedf040b4a0e54a3c4beee8939a42"
)
CLOSEOUT_EFFECTIVE_NEGATIVES = 14725
CLOSEOUT_EFFECTIVE_METHODS = 1011
OPEN_GAPS = 102
EXACT_GATES = 101
FINAL_PREPARATION_NEGATIVES = [
    {
        "negative_id": "V6566-X2-N27",
        "slug": "absent-successor-named-test-module",
        "failure_signature": "The bounded search found no existing Neris- or v656-v7-named test module and returned no matches.",
        "candidate_workaround": "Add one Elaren-owned successor-scope module that validates only the committed Neris baton, unsent route, and authority reservations.",
        "recurrence_guard": "Treat successor-scoped coverage as an explicit bounded route contract; never infer it from a nonexistent named module.",
        "fail_procedure": "Search existing test filenames for Neris or v656-v7 coverage.",
        "fail_observed": "No matching module existed, so the search returned nonzero and earned zero coverage credit.",
        "pass_procedure": "Run the additive Elaren successor-scope tests without contacting or acting for Neris.",
        "pass_observed": "The successor-scope module validated the prepared baton, unsent route, next edge, word cap, and protected authority boundaries.",
        "scope_boundary": "Elaren-owned route-contract coverage only; no Neris completion or authority credit.",
    },
    {
        "negative_id": "V6566-X2-N28",
        "slug": "self-referential-stale-label-token",
        "failure_signature": "The first postcommit canonical aggregate gave zero credit because the stale-label scanner found its three own literal rule tokens in the validator source.",
        "candidate_workaround": "Construct each stale-label token from semantic fragments so the validator still scans for the exact runtime values without embedding those values in its own source.",
        "recurrence_guard": "A scanner must not make its own rule declarations indistinguishable from findings; keep the runtime rule set exact while preventing self-matching source literals.",
        "fail_procedure": "Run the first postcommit canonical aggregate at the original final candidate.",
        "fail_observed": "Seventy-three tests, 322 detailed checks, 15 minimal checks, 195 JSON parses, 730 manifest entries, and a 258-file zero-hit privacy scan passed, but stale-label review failed on three literals in the validator itself, so the aggregate was invalid and earned zero credit.",
        "pass_procedure": "Run the isolated validator-source guard after fragmenting the three rule tokens, without replaying the aggregate.",
        "pass_observed": "The isolated guard found none of the three complete stale-label values in the validator source while reconstructing the exact runtime rule set.",
        "scope_boundary": "Stale-label scanner self-reference only; no canonical success, route, or external-authority credit.",
        "fail_expected": "All terminal checks, including stale-label review, must pass in the same exact-final aggregate.",
        "pass_expected": "The validator source contains no complete stale-label rule value, while runtime construction preserves all three values.",
        "approval_class": "safe_now_owner_local_validation_recovery",
        "rollback": "Retain the failed aggregate at zero credit and restore the scanner if fragment construction changes any runtime rule value.",
    },
    {
        "negative_id": "V6566-X2-N29",
        "slug": "powershell-token-array-cardinality",
        "failure_signature": "The first isolated PowerShell guard reported only one runtime token because an unparenthesized concatenation and comma expression did not materialize the intended three-element array.",
        "candidate_workaround": "Use an explicit three-element Python list for the isolated read-only guard.",
        "recurrence_guard": "Every scanner-rule guard must assert its expected rule cardinality before granting zero-hit credit.",
        "fail_procedure": "Run the first isolated PowerShell source-literal guard.",
        "fail_observed": "The command exited zero but reported runtime_token_count 1, so it earned zero isolated-guard credit.",
        "pass_procedure": "Run the same read-only source check with an explicit three-element Python list and a cardinality assertion.",
        "pass_observed": "The corrected isolated guard reported exactly three runtime tokens, zero source-literal hits, and valid true.",
        "scope_boundary": "Isolated scanner-rule cardinality only; no canonical aggregate, route, or external-authority credit.",
        "fail_expected": "The guard materializes exactly three rule values and fails closed on any other cardinality.",
        "pass_expected": "Exactly three runtime rule values are checked and none occurs literally in the validator source.",
        "approval_class": "safe_now_owner_local_validation_recovery",
        "rollback": "Retain the one-token guard at zero credit and reject the correction if the explicit list does not contain exactly three values.",
    },
    {
        "negative_id": "V6566-X2-N30",
        "slug": "stale-correction-plan-test-state",
        "failure_signature": "The first isolated correction test run kept the original final plan-state expectation and rejected the explicit post-correction state.",
        "candidate_workaround": "Update the lifecycle assertion to the exact retained correction state without weakening any route or canonical-success gate.",
        "recurrence_guard": "When a failed postcommit gate creates an additive correction lifecycle, update tests to the explicit correction state while preserving the failed predecessor in history.",
        "fail_procedure": "Run the isolated final and successor-scope modules after generating the correction records.",
        "fail_observed": "Fourteen tests ran with one failure because the test expected POSTCOMMIT_REQUIRED instead of POSTCORRECTION_COMMIT_REQUIRED.",
        "pass_procedure": "Rerun the same isolated modules after changing only the expected correction-plan state.",
        "pass_observed": "The same isolated selection passed with the failed aggregate still at zero credit and the route still PREPARED_NOT_SENT.",
        "scope_boundary": "Correction lifecycle assertion only; no canonical success, route, or external-authority credit.",
        "fail_expected": "The final test recognizes the explicit post-correction commit requirement.",
        "pass_expected": "The lifecycle assertion matches POSTCORRECTION_COMMIT_REQUIRED while completed and route-sent remain false.",
        "approval_class": "safe_now_owner_local_validation_recovery",
        "rollback": "Retain the failed isolated run and restore the earlier assertion if the correction plan does not explicitly declare its new state.",
    }
]
