#!/usr/bin/env python3
"""Immutable x2 lifecycle configuration for Lyren v657-v1."""

from __future__ import annotations


SOURCE_COMMIT = "a033d1318920de1beec288f9c5b27e7f73a8ff3b"
X1_COMMIT = "2e3d51c838caa01d05b0713b6c165bef0be882d5"
PHASE_ROOT = "docs/lyren-moss/v657-v1"
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 15075
SOURCE_EFFECTIVE_NEGATIVES = 15076
X1_OPERATIONAL_NEGATIVES = 13
SOURCE_OPEN_GAPS = 104
SOURCE_EXACT_GATES = 103
SOURCE_METHODS = 1360
X1_METHODS = 13
MUTATIONS_PER_PROPOSAL = 5
EXPECTED_PROPOSALS = 30
EXPECTED_MUTATIONS = EXPECTED_PROPOSALS * MUTATIONS_PER_PROPOSAL
EXPECTED_DISTRIBUTION = {
    "completed": 23,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}

# Append only phase-local x2 operational failures actually observed before the
# immutable evidence commit. Inherited and x1 failures remain retained evidence,
# not new x2 credit.
X2_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6571-X2-N14",
        "slug": "sequential-rg-no-match-wrapper-recurrence",
        "failure_signature": (
            "A multi-file x2 stale-label audit repeated the known composition error: "
            "an expected ripgrep no-match exit stopped the wrapper after its first file."
        ),
        "candidate_workaround": (
            "Search all declared files in one bounded ripgrep invocation and explicitly "
            "normalize exit code one as a valid no-match result."
        ),
        "recurrence_guard": (
            "Never place raw ripgrep calls that may return no-match inside sequential "
            "tool orchestration without documented exit normalization."
        ),
        "fail_procedure": (
            "Run one ripgrep tool call per x2 file inside a sequential orchestration script."
        ),
        "fail_observed": (
            "The wrapper returned the first file's matches, then stopped on the next "
            "file's expected no-match result and earned zero complete-audit credit."
        ),
        "pass_procedure": (
            "Run one declared-file-set search and treat exit code one as successful "
            "evidence that no requested stale label was present."
        ),
        "pass_observed": (
            "The bounded combined search completed over all declared x2 files and "
            "returned the exact remaining stale-label inventory."
        ),
        "scope_boundary": "Owner-local read-only stale-label inspection recovery only.",
    },
    {
        "negative_id": "V6571-X2-N15",
        "slug": "mixed-unicode-runtime-patch-context-mismatch",
        "failure_signature": (
            "A mixed runtime-field and Unicode-boundary patch did not match the "
            "copied scaffold and changed nothing."
        ),
        "candidate_workaround": (
            "Apply the machine-field changes with ASCII-safe hunks, inspect the exact "
            "UTF-8 boundary lines, then patch that human-readable string separately."
        ),
        "recurrence_guard": (
            "Keep structural field edits separate from inherited Unicode prose when "
            "adapting lifecycle scaffolding."
        ),
        "fail_procedure": (
            "Submit one patch containing both ASCII field names and terminal-rendered "
            "Unicode prose context."
        ),
        "fail_observed": (
            "Patch verification rejected the mixed context before mutation and granted "
            "zero edit credit."
        ),
        "pass_procedure": (
            "Patch structural fields first, inspect the exact Unicode line with ripgrep, "
            "then apply a narrow text-only hunk."
        ),
        "pass_observed": (
            "The runtime now uses repair-specific synthetic fixture fields and a correct "
            "UTF-8 repair boundary without changing unrelated logic."
        ),
        "scope_boundary": "Owner-local runtime scaffold adaptation recovery only.",
    },
    {
        "negative_id": "V6571-X2-N16",
        "slug": "sequential-rg-no-match-wrapper-second-recurrence",
        "failure_signature": (
            "A later x2 validator inspection again stopped when the final declared "
            "file had no requested matches."
        ),
        "candidate_workaround": (
            "Discontinue sequential per-file ripgrep orchestration and use one literal "
            "file-set invocation with explicit no-match normalization."
        ),
        "recurrence_guard": (
            "Treat this second recurrence as a hard phase-local ban on raw sequential "
            "ripgrep calls."
        ),
        "fail_procedure": (
            "Inspect each validator in separate nested ripgrep calls without normalizing "
            "exit code one."
        ),
        "fail_observed": (
            "Three inventories returned, then the wrapper failed on a valid no-match "
            "result and earned zero complete-set credit."
        ),
        "pass_procedure": (
            "Search the complete declared validator set in one command and explicitly "
            "accept exit code one."
        ),
        "pass_observed": (
            "The single bounded file-set audit completed and exposed the exact stale "
            "route and lifecycle constants."
        ),
        "scope_boundary": "Owner-local read-only validator inspection recovery only.",
    },
]
