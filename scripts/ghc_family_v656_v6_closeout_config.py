#!/usr/bin/env python3
"""Closeout lifecycle constants for Elaren v656-v6."""

from __future__ import annotations


SOURCE_COMMIT = "8a4bb8e8b6a649040c531e8d3dd36925fd0da301"
X1_COMMIT = "9c0227286b93672a4d98dba305e1c627a2300279"
EVIDENCE_COMMIT = "0744740cc17dfa57b0d151957d1edc7a2bb2c282"
EVIDENCE_EFFECTIVE_NEGATIVES = 14720
EVIDENCE_EFFECTIVE_METHODS = 1006
EVIDENCE_OPEN_GAPS = 102
EVIDENCE_EXACT_GATES = 101
POST_EVIDENCE_NEGATIVES = [
    {
        "negative_id": "V6566-X2-N22",
        "slug": "post-evidence-diff-index-timeout",
        "failure_signature": "The first post-evidence git diff-index cleanliness probe exceeded its thirty-second bound.",
        "candidate_workaround": "Separate tracked porcelain state from the untracked index query and allow a bounded large-worktree window.",
        "recurrence_guard": "Never infer clean state from a timed-out diff-index process.",
        "fail_procedure": "Run git diff-index --quiet HEAD over the large owner worktree.",
        "fail_observed": "The process timed out and received zero clean-state credit.",
        "pass_procedure": "Run porcelain tracked status with untracked traversal disabled, then query untracked paths separately.",
        "pass_observed": "Both bounded probes completed with empty results.",
        "scope_boundary": "Post-evidence local cleanliness recovery only.",
    },
    {
        "negative_id": "V6566-X2-N23",
        "slug": "post-evidence-diff-files-timeout",
        "failure_signature": "The scalar git diff-files cleanliness probe exceeded its forty-five-second bound.",
        "candidate_workaround": "Use bounded porcelain tracked status with explicit untracked exclusion.",
        "recurrence_guard": "Treat large-worktree diff-files latency as a tooling failure and preserve a distinct successful witness.",
        "fail_procedure": "Run git diff-files --quiet after the evidence commit.",
        "fail_observed": "The process timed out and received zero clean-state credit.",
        "pass_procedure": "Run git status --porcelain=v1 --untracked-files=no with a bounded large-worktree window.",
        "pass_observed": "The tracked porcelain result was empty.",
        "scope_boundary": "Post-evidence tracked-state recovery only.",
    },
    {
        "negative_id": "V6566-X2-N24",
        "slug": "guessed-closeout-directory-names",
        "failure_signature": "A closeout inventory guessed absent workflow-plan and meta-tool-box directories and returned nonzero.",
        "candidate_workaround": "List the exact top-level phase directories, then inspect only the discovered workflow, tooling, and orchestration paths.",
        "recurrence_guard": "Discover committed directory names before probing optional phase records.",
        "fail_procedure": "Probe guessed workflow-plan and meta-tool-box directories.",
        "fail_observed": "The command returned nonzero after the valid top-level list exposed the actual workflow directory.",
        "pass_procedure": "Inventory the discovered workflow, tooling, and orchestration directories by literal path.",
        "pass_observed": "The literal inventories returned the expected workflow, index, and route records.",
        "scope_boundary": "Repository artifact discovery only.",
    },
    {
        "negative_id": "V6566-X2-N25",
        "slug": "guessed-source-ledger-filename",
        "failure_signature": "A schema-inspection probe guessed a nonexistent official-primary-source-ledger filename after successfully reading the proposal ledger.",
        "candidate_workaround": "List the exact sources directory before loading the committed official-source-ledger file.",
        "recurrence_guard": "Resolve source-ledger filenames from a literal directory inventory rather than naming convention guesses.",
        "fail_procedure": "Read the guessed official-primary-source-ledger.json path.",
        "fail_observed": "The proposal schema printed, then the source read raised FileNotFoundError and received zero source-ledger credit.",
        "pass_procedure": "List the exact sources directory and read official-source-ledger.json.",
        "pass_observed": "The committed ledger parsed with twenty-three official or primary source rows.",
        "scope_boundary": "Repository source-ledger discovery only.",
    },
    {
        "negative_id": "V6566-X2-N26",
        "slug": "contextual-sent-token-test-false-positive",
        "failure_signature": "The first closeout test rejected a contextual prohibition sentence because it contained the future SENT token.",
        "candidate_workaround": "Reject only a standalone affirmative delivery declaration and separately require the committed PREPARED_NOT_SENT statement.",
        "recurrence_guard": "Distinguish delivery-state values from prose that explains why those values are forbidden before acknowledgement.",
        "fail_procedure": "Assert that the future SENT token is absent as a substring anywhere in the prepared baton.",
        "fail_observed": "Fifty-nine of sixty tests passed; the contextual-label assertion failed and the aggregate received zero credit.",
        "pass_procedure": "Require PREPARED_NOT_SENT and reject only a stripped line that affirmatively declares SENT true.",
        "pass_observed": "The corrected route-state test accepted the prohibition prose while preserving the unsent state.",
        "scope_boundary": "Prepared-baton delivery-state accounting only.",
    },
]
