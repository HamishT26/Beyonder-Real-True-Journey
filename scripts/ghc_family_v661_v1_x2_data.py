#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Sable Rook v661-v1."""

from __future__ import annotations

from ghc_family_v661_v1_data import *  # noqa: F401,F403
import ghc_family_v661_v1_data as x1


X1_FREEZE = "5a94096fb5e4a9243b16088e3488ddac355c6d94"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Append only failures actually observed after the immutable Sable x1 freeze.
# Expected rejecting mutations belong to the mutation register, not here.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6611-X2-N001",
        "signature": "first-current-x2-suite-passed-eighteen-of-nineteen-and-found-missing-skill-generated-method-flow-receipt-before-later-governance-reads",
        "recovery": "Retain the failed aggregate at zero credit, materialize only the preregistered bounded x2 workflow, governance, reflection, Method Flow, and meta-tool receipts, refresh the exact manifests, and rerun the scoped x2 suite once.",
    },
]
