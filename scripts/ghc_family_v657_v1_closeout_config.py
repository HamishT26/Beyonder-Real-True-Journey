#!/usr/bin/env python3
"""Closeout lifecycle constants for Lyren v657-v1."""

from __future__ import annotations


SOURCE_COMMIT = "a033d1318920de1beec288f9c5b27e7f73a8ff3b"
X1_COMMIT = "2e3d51c838caa01d05b0713b6c165bef0be882d5"
EVIDENCE_COMMIT = "91c36c44b6ccecbf73892792e07525cc7577d0c8"
EVIDENCE_EFFECTIVE_NEGATIVES = 15242
EVIDENCE_EFFECTIVE_METHODS = 1526
EVIDENCE_OPEN_GAPS = 105
EVIDENCE_EXACT_GATES = 104

# Append only failures discovered after the immutable evidence commit and
# before the closeout/content-seal commit.
CLOSEOUT_DISCOVERED_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6571-CLOSEOUT-N17",
        "slug": "combined-closeout-audit-timeout",
        "failure_signature": (
            "A combined PowerShell audit of Git state and two durable validator "
            "receipts exceeded its bounded runtime before returning scalar output."
        ),
        "candidate_workaround": (
            "Split durable JSON inspection from Git inspection and run both through "
            "bounded Node filesystem and child-process calls."
        ),
        "recurrence_guard": (
            "Do not combine repository status traversal and multiple JSON parses in "
            "one PowerShell probe for this large owner lane."
        ),
        "fail_procedure": (
            "Request branch, head, full short status, and both closeout validator "
            "summaries in one PowerShell invocation."
        ),
        "fail_observed": (
            "The invocation timed out without a usable scalar result and earned zero "
            "audit credit."
        ),
        "pass_procedure": (
            "Parse the two durable receipts directly with bounded Node filesystem "
            "calls, then inspect Git head, branch, and status separately."
        ),
        "pass_observed": (
            "The receipts reported 322 of 322 detailed checks and 15 of 15 minimal "
            "checks, while the separate Git inspection identified the immutable "
            "evidence head and the intended untracked closeout candidate."
        ),
        "scope_boundary": "Owner-local read-only closeout-state inspection recovery only.",
    },
    {
        "negative_id": "V6571-CLOSEOUT-N18",
        "slug": "powershell-process-lock-audit-timeout",
        "failure_signature": (
            "The immediate PowerShell recovery probe for Git processes, worktree "
            "existence, Git-dir resolution, and lock files also exceeded its bound "
            "without returning scalar output."
        ),
        "candidate_workaround": (
            "Bypass the unresponsive shell transport, inspect durable files directly, "
            "and use bounded Node child-process calls for isolated Git commands."
        ),
        "recurrence_guard": (
            "After a shell-level timeout with no output, avoid adding Git-dir and "
            "process enumeration to the same recovery surface."
        ),
        "fail_procedure": (
            "Combine process enumeration, worktree existence, Git-dir discovery, and "
            "four lock checks in one second PowerShell invocation."
        ),
        "fail_observed": (
            "The diagnostic itself timed out with no usable evidence and earned zero "
            "recovery credit."
        ),
        "pass_procedure": (
            "Use a bounded Node child process to prove the Git runtime responds, then "
            "issue only the exact Git query needed for each gate."
        ),
        "pass_observed": (
            "The isolated Git version probe completed, and later bounded Git head, "
            "branch, and status calls returned normally."
        ),
        "scope_boundary": "Owner-local read-only process and Git responsiveness recovery only.",
    },
    {
        "negative_id": "V6571-CLOSEOUT-N19",
        "slug": "powershell-scalar-probe-timeout",
        "failure_signature": (
            "A reduced PowerShell probe limited to a marker, worktree existence, and "
            "Git-process count still timed out without output."
        ),
        "candidate_workaround": (
            "Treat the shell surface as temporarily unavailable and use direct bounded "
            "filesystem reads without process enumeration."
        ),
        "recurrence_guard": (
            "Do not infer repository corruption from a shell transport that cannot "
            "return even a scalar marker."
        ),
        "fail_procedure": (
            "Retry the same shell transport with only marker output, path existence, "
            "and process counting."
        ),
        "fail_observed": (
            "The scalar-only diagnostic timed out, so it established no postcondition "
            "and earned zero credit."
        ),
        "pass_procedure": (
            "Read and parse each declared validator receipt directly through the "
            "bounded Node filesystem interface."
        ),
        "pass_observed": (
            "Both closeout validator receipts parsed successfully with valid true and "
            "zero detailed issues."
        ),
        "scope_boundary": "Owner-local read-only scalar diagnostic recovery only.",
    },
    {
        "negative_id": "V6571-CLOSEOUT-N20",
        "slug": "no-login-shell-marker-timeout",
        "failure_signature": (
            "A final no-login PowerShell invocation containing only a literal marker "
            "also exceeded its bound without returning output."
        ),
        "candidate_workaround": (
            "Stop retrying the failed shell transport and continue through bounded "
            "Node child-process calls with explicit executable, arguments, timeout, "
            "and output cap."
        ),
        "recurrence_guard": (
            "One failed no-login literal-marker probe is the terminal diagnostic for "
            "this shell surface; do not replay it during the phase."
        ),
        "fail_procedure": (
            "Invoke the shell without login semantics and request one literal output "
            "marker."
        ),
        "fail_observed": (
            "Even the literal marker did not return before timeout, and the attempt "
            "earned zero credit."
        ),
        "pass_procedure": (
            "Run Git through a bounded Node child process and retain the explicit "
            "stdout and stderr result."
        ),
        "pass_observed": (
            "The Git runtime and subsequent repository queries completed with bounded "
            "output, allowing closeout inspection to continue without replaying the "
            "failed shell probes."
        ),
        "scope_boundary": "Owner-local read-only command-transport recovery only.",
    },
]
