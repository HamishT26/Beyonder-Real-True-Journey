#!/usr/bin/env python3
"""Closeout lifecycle constants for Caelen Ash v657-v5."""

from __future__ import annotations


SOURCE_COMMIT = "1ae8aa07d6b0d5f74dc3c5b29615c79b908e235f"
X1_COMMIT = "7fdae81a188decacbee20c2f2c283b7104c0e91a"
EVIDENCE_COMMIT = "e2f0f3535f968e26fab748385c950cf4b7de085a"
EVIDENCE_EFFECTIVE_NEGATIVES = 15964
EVIDENCE_EFFECTIVE_METHODS = 2240
EVIDENCE_OPEN_GAPS = 109
EVIDENCE_EXACT_GATES = 108


CLOSEOUT_DISCOVERED_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6575-CLOSEOUT-N01",
        "slug": "broad-closeout-narrative-patch-context-mismatch",
        "failure_signature": "The first broad closeout narrative patch was rejected at its heading context before changing the file.",
        "candidate_workaround": "Use short ASCII-stable semantic hunks and audit every owner, phase, count, pillar, and route field afterward.",
        "recurrence_guard": "Do not combine a long generated baton rewrite with a non-ASCII heading as one patch precondition.",
        "fail_procedure": "Apply one broad mixed-context patch to the inherited closeout narrative.",
        "fail_observed": "The patch did not apply, changed no repository content, and earned zero closeout credit.",
        "pass_procedure": "Patch bounded exact lines, compile, build, and scan the complete baton for stale labels and truth mismatches.",
        "pass_observed": "Acceptance is reserved for a valid bounded baton and exact closeout review; the rejected patch remains retained.",
        "scope_boundary": "Owner-local closeout-source correction only.",
    },
]
