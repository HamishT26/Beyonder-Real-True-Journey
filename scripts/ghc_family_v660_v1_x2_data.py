#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Sylven Arc v660-v1."""

from __future__ import annotations

from ghc_family_v660_v1_data import *  # noqa: F401,F403
import ghc_family_v660_v1_data as x1


X1_FREEZE = "d18cbd8bc001e51997e0b5c772ad6dddbb5c7c32"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Only failures observed after the x1 freeze belong here. Expected rejecting
# mutations are recorded in the mutation register and Method Flow witnesses,
# not prefilled as tooling faults.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6601-X2-N001",
        "signature": "first-x2-test-aggregate-found-the-overview-at-779-words-below-the-900-word-three-page-equivalent-floor",
        "recovery": "Retain the 16-of-17 aggregate at zero aggregate credit, expand only the overview with evidence-semantics and falsifier detail, and rerun the document dependency plus affected truth and manifest checks.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6601-X2-N002",
        "signature": "meta-tool-box-validation-used-the-undeclared-receipt-flag-and-exited-before-validation",
        "recovery": "Retain the argparse rejection at zero credit, inspect the exact subcommand help, and rerun only validation with the declared --output flag; require a valid bounded receipt before catalogue use.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6601-X2-N003",
        "signature": "isolated-x2-recovery-found-two-tests-hard-coded-the-prior-operational-failure-total",
        "recovery": "Retain the two failed assertions at zero credit, derive operational, Method Flow, witness, and cumulative totals from the immutable failure lists, then rerun only the two affected tests and their manifest dependencies.",
        "recovery_passed": True,
    },
]
