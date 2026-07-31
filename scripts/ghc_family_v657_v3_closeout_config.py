#!/usr/bin/env python3
"""Closeout lifecycle constants for Auren Lark v657-v3."""

from __future__ import annotations


SOURCE_COMMIT = "67a5eaa17b2399d52bac5ba45d390d8659cc61cd"
X1_COMMIT = "b40c2f04cd7e51ed9bc5c1174255e9e3d06af4e1"
EVIDENCE_COMMIT = "ecd67debfa384f7d4224a2600cc23a4744f8b0b5"
EVIDENCE_EFFECTIVE_NEGATIVES = 15602
EVIDENCE_EFFECTIVE_METHODS = 1884
EVIDENCE_OPEN_GAPS = 107
EVIDENCE_EXACT_GATES = 106

# Append-only failures discovered after the evidence candidate was frozen and
# therefore not embedded in the immutable evidence commit. They remain
# zero-credit closeout witnesses and do not rewrite the evidence-layer totals.
CLOSEOUT_DISCOVERED_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6573-CLOSEOUT-N17",
        "slug": "staged-review-wrapper-timeout-after-valid-receipt",
        "failure_signature": (
            "The bounded shell wrapper exceeded 181 seconds after the evidence "
            "staged-review receipt had been written valid and staged."
        ),
        "candidate_workaround": (
            "Audit live processes, worktree locks, HEAD, stage state, and the exact "
            "written receipt before deciding whether any lifecycle work remains."
        ),
        "recurrence_guard": (
            "Treat a shell timeout after a potentially atomic receipt write as an "
            "ambiguous zero-credit outcome; inspect state before any replay."
        ),
        "fail_procedure": (
            "Run the evidence staged review and post-review staging inside one "
            "181-second outer shell bound."
        ),
        "fail_observed": (
            "The outer wrapper timed out after emitting a line-ending warning; no "
            "usable wrapper result was returned and the attempt earned zero credit."
        ),
        "pass_procedure": (
            "Confirm process and lock quiescence, read the receipt directly, then "
            "independently replay its staged manifest without rerunning review."
        ),
        "pass_observed": (
            "No Git or Python process or lock survived; the receipt was valid for "
            "166 reviewed paths, and 204 staged blobs replayed without mismatch."
        ),
        "scope_boundary": "Owner-local evidence-seal timeout recovery only.",
    },
    {
        "negative_id": "V6573-CLOSEOUT-N18",
        "slug": "combined-post-timeout-audit-ceiling",
        "failure_signature": (
            "A combined read-only audit of Git state, processes, locks, and receipt "
            "content exceeded its 60-second shell ceiling without returning output."
        ),
        "candidate_workaround": (
            "Split the audit into a no-Git process-and-lock probe, a direct receipt "
            "read, and a bounded scalar Git-and-blob replay."
        ),
        "recurrence_guard": (
            "After an ambiguous long-running operation, use small attributable "
            "recovery probes rather than one combined status traversal."
        ),
        "fail_procedure": (
            "Query repository status, staged paths, worktree locks, live processes, "
            "and the review JSON in one 60-second wrapper."
        ),
        "fail_observed": (
            "The read-only wrapper timed out with no output, changed no repository "
            "state, and earned zero diagnostic credit."
        ),
        "pass_procedure": (
            "Probe locks and processes without Git, read the receipt directly, then "
            "run one bounded staged-index and cat-file audit."
        ),
        "pass_observed": (
            "The split probes found no locks or surviving workers, preserved the x1 "
            "HEAD until seal, and validated the exact 167-path staged candidate."
        ),
        "scope_boundary": "Owner-local read-only post-timeout audit recovery only.",
    },
    {
        "negative_id": "V6573-CLOSEOUT-N19",
        "slug": "inherited-closeout-gap-gate-assertion",
        "failure_signature": (
            "The first 50-test closeout selection retained Ilyra's inherited "
            "106-open-gap and 105-exact-gate expectation instead of Auren's sealed "
            "107-open-gap and 106-exact-gate totals."
        ),
        "candidate_workaround": (
            "Correct only the two expected evidence-bound totals, rebuild the "
            "count-dependent closeout artifacts, and rerun the same eligible selection."
        ),
        "recurrence_guard": (
            "After mechanically copying lifecycle tests, compare every numeric truth "
            "assertion with the immutable current evidence receipts before execution."
        ),
        "fail_procedure": (
            "Run the 41 x2 tests and 9 closeout tests with the inherited 106/105 "
            "closeout assertion still present."
        ),
        "fail_observed": (
            "Forty-nine tests passed and one bounded-truth assertion failed; the "
            "50-test command received zero aggregate-pass credit."
        ),
        "pass_procedure": (
            "Bind the assertion to 107 open gaps and 106 exact gates, rebuild the "
            "closeout ledgers and receipts, then rerun the same selection."
        ),
        "pass_observed": (
            "The corrected assertion matches the immutable evidence totals and all "
            "eligible x2 plus closeout tests pass without broadening scope."
        ),
        "scope_boundary": "Owner-local closeout-test expectation recovery only.",
    },
]
