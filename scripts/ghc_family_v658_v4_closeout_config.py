#!/usr/bin/env python3
"""Closeout constants for Eiren Kestrel v658-v4."""

from __future__ import annotations


SOURCE_COMMIT = "9c5f4c935d728f68b2ac612fa0affb4dfd389e05"
X1_COMMIT = "1e1d8bf1368c5f8304ad732a8a904834dd215adf"
EVIDENCE_COMMIT = "f9000a0ac35ea632070570fddd93e9ba4364a4e2"
BRANCH = "codex/GHC-Family/eiren-kestrel-v658-v4-full-tools"
PHASE_ROOT = "docs/eiren-kestrel/v658-v4"
FROZEN_PROPOSALS = 2770
EFFECTIVE_NEGATIVES_EVIDENCE = 17174
EFFECTIVE_OPEN_GAPS = 116
EFFECTIVE_EXACT_GATES = 115
EFFECTIVE_METHODS_EVIDENCE = 3448
EXPECTED_OUTCOMES = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}


CLOSEOUT_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6584-CLOSEOUT-N01",
        "slug": "post-rebuild-restage-warning-stream-truncated",
        "failure_signature": "The post-rebuild restaging command succeeded but again emitted a warning per generated path, so its displayed stream was truncated and could not prove the exact cached set.",
        "candidate_workaround": "Treat the warning stream as non-evidence and compare the complete cached path set with the frozen expected-delta list using a bounded machine summary.",
        "recurrence_guard": "Suppress repetitive line-ending warnings for large additive stages and always bind staged review to cached path data rather than console rendering.",
        "scope_boundary": "Same-owner exact staged-set recovery only.",
        "fail_procedure": "Rely on the repeated restaging warning stream as the path inventory.",
        "fail_observed": "Git exited successfully, but the displayed warning stream was truncated and earned zero exact-review credit.",
        "pass_procedure": "Compare all cached paths with the 226-path expected x2 delta and separately count deletions, unstaged paths, and untracked paths.",
        "pass_observed": "The bounded comparison returned 226 expected and 226 actual paths, zero missing, zero extra, zero deletions, zero unstaged, and zero untracked.",
    },
    {
        "negative_id": "V6584-CLOSEOUT-N02",
        "slug": "evidence-commit-file-list-output-truncated",
        "failure_signature": "The evidence commit succeeded, but its verbose 226-file creation list exceeded the display budget and was truncated after the commit object had been written.",
        "candidate_workaround": "Give no inventory credit to the truncated stream and verify the immutable commit ID, direct x1 parent, clean state, push acknowledgement, and fresh four-way equality through bounded Git queries.",
        "recurrence_guard": "Use quiet commit output for large additive commits and verify commit identity and topology with separate bounded commands.",
        "scope_boundary": "Same-owner immutable-commit verification recovery only.",
        "fail_procedure": "Use the truncated verbose commit stream as complete evidence of the evidence commit.",
        "fail_observed": "The commit completed, but its displayed per-file list was truncated and earned zero manifest or topology credit.",
        "pass_procedure": "Resolve the exact commit and parent, push, then compare local, upstream, tracking, and fresh-live hashes plus divergence and clean state.",
        "pass_observed": "Evidence resolved to f9000a0ac35ea632070570fddd93e9ba4364a4e2 with direct x1 parent, 0/0 divergence, clean state, and exact four-way equality.",
    },
]
