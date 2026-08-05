#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Sylven Arc v661-v7."""

from __future__ import annotations

from ghc_family_v661_v7_data import *  # noqa: F401,F403
import ghc_family_v661_v7_data as x1


X1_FREEZE = "7b14e314d4e16cf18a1726c8988cd5e11843f410"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Append only failures actually observed after the immutable Sylven x1 freeze.
# Expected rejecting mutations belong to the mutation register, not here.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6617-X2-N001",
        "signature": "direct-powershell-foreach-block-could-not-be-piped-without-an-enclosing-expression",
        "recovery": "Retain the parser fault at zero credit and collect the bounded read-only script inventory into an explicit array before JSON projection.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6617-X2-N002",
        "signature": "first-skill-creator-read-was-over-serialized-and-truncated-before-eof",
        "recovery": "Retain the incomplete read at zero credit and reread the exact skill in bounded line windows through EOF before creating any phase-local package.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6617-X2-N003",
        "signature": "quick-validate-help-probe-treated-the-help-flag-as-a-skill-directory-and-returned-skill-md-not-found",
        "recovery": "Retain the harmless usage-probe failure at zero credit, use the skill-documented positional folder invocation, and validate only initialized phase-local packages.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6617-X2-N004",
        "signature": "mechanical-scaffolding-copy-materialized-three-future-closeout-files-before-the-x2-evidence-boundary",
        "recovery": "Retain the lifecycle false assumption at zero credit, remove only the untracked and unexecuted Sylven-owned future scaffolds, refresh the exact x2 delta, and rematerialize them only after the pushed evidence gate.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6617-X2-N005",
        "signature": "first-exact-x2-staged-manifest-review-timed-out-while-spawning-one-git-show-process-per-entry",
        "recovery": "Retain the read-only aggregate at zero credit and replay all staged blobs through one git cat-file batch process while consuming stdout and stderr together.",
        "completion_credit": 0,
    },
]
