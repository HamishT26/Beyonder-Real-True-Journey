#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Caelen Ash v661-v2."""

from __future__ import annotations

from ghc_family_v661_v2_data import *  # noqa: F401,F403
import ghc_family_v661_v2_data as x1


X1_FREEZE = "d62c0c856df45aec5d828a2da1212be9e8e55718"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Append only failures actually observed after the immutable Caelen x1 freeze.
# Expected rejecting mutations belong to the mutation register, not here.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6612-X2-N001",
        "signature": "first-current-x2-suite-passed-eighteen-of-nineteen-and-found-the-declared-family-governance-receipt-set-absent",
        "recovery": "Retain the failed aggregate at zero credit, materialize only the declared workflow, Method Flow, reflection-remaster, and meta-tool-box x2 receipts, refresh the owner-scoped manifests, and rerun the scoped x2 module once.",
        "completion_credit": 0,
    }
]
