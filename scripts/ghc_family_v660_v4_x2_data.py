#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Neris Solane v660-v4."""

from __future__ import annotations

from ghc_family_v660_v4_data import *  # noqa: F401,F403
import ghc_family_v660_v4_data as x1


X1_FREEZE = "42124477d3610fd394830e4858feb099b585bfc1"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Only failures observed after the x1 freeze belong here. Expected rejecting
# mutations are recorded in the mutation register and Method Flow witnesses,
# not prefilled as tooling faults.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6604-X2-N001",
        "signature": "mechanical-x2-scaffold-retained-source-phase-anchors-owner-credit-labels-domain-vocabulary-and-eight-prefilled-operational-failures",
        "recovery": "Retain the scaffold audit at zero credit, bind the exact Neris x1 SHA, clear all inherited failure prefill, rewrite current-owner and ice-core contracts, and compile-review every generated runtime, builder, validator, and test before execution.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6604-X2-N002",
        "signature": "first-owner-x2-suite-passed-eighteen-of-nineteen-and-found-four-family-current-governance-and-reflection-receipt-groups-not-yet-materialized",
        "recovery": "Retain the 18-pass and one missing-receipt error at zero credit, invoke only the declared Method Flow, workflow refinement, reflection-remaster, and Meta Tool Box builders, refresh the x2 packet, and rerun the scoped owner suite.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6604-X2-N003",
        "signature": "first-reflection-remaster-command-resolved-the-repository-historical-compatibility-runner-with-the-same-filename-and-emitted-a-proposal-tribunal-instead-of-the-current-inventory",
        "recovery": "Retain the compatibility-runner artifacts at zero credit, resolve the selected family-current skill runner by its explicit skill path, and require the current inventory, issue, method, report, and validation receipts before promotion.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6604-X2-N004",
        "signature": "first-targeted-method-flow-regeneration-omitted-the-repository-scripts-directory-from-python-import-resolution",
        "recovery": "Retain the pre-mutation ModuleNotFoundError at zero credit, prepend the exact repository scripts directory to sys.path, and rerun only Method Flow generation and validation before the manifest refresh.",
        "recovery_passed": True,
    },
]
