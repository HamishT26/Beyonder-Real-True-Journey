#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Lyren Moss v660-v6."""

from __future__ import annotations

from ghc_family_v660_v6_data import *  # noqa: F401,F403
import ghc_family_v660_v6_data as x1


X1_FREEZE = "ec19bf7f868be7a040b5305f1f8f113062674fb6"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Only failures observed after the x1 freeze belong here. Expected rejecting
# mutations are recorded in the mutation register and Method Flow witnesses,
# not prefilled as tooling faults.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6606-X2-N001",
        "signature": "mechanical-x2-scaffold-retained-source-owner-credit-route-and-meteorite-domain-text-across-the-runtime-builder-closeout-validator-and-tests",
        "recovery": "Retain the scaffold audit at zero credit, bind Lyren's exact pushed x1 SHA, clear every inherited operational-failure prefill, rewrite the seven generated x2 files to current origami and authorized terminal-gated route contracts, and compile-review each file before executing any x2 builder.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6606-X2-N002",
        "signature": "first-owner-x2-suite-passed-eighteen-of-nineteen-and-found-the-family-current-method-workflow-reflection-and-meta-tool-receipt-group-unmaterialized",
        "recovery": "Retain the 18-pass and one missing-path error at zero credit, invoke only the declared family-current Method Flow, workflow refinement, reflection-remaster, roster and authorization, and Meta Tool Box builders, refresh the evidence manifest, and rerun only the isolated owner suite.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6606-X2-N003",
        "signature": "first-evidence-staging-wrapper-truncated-its-line-ending-advisory-display-while-staging-the-exact-one-hundred-eighty-two-path-allowlist",
        "recovery": "Retain the truncated wrapper at zero credit, restore only the exact evidence paths from the Git index, verify the index is empty and the complete working delta remains, refresh affected receipts, and restage the same allowlist with advisory output captured rather than displayed.",
        "recovery_passed": True,
    },
]
