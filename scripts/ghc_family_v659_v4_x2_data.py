#!/usr/bin/env python3
"""Additive x2-only truth overlay for Caelen Ash v659-v4.

The frozen x1 data module remains immutable. Its unused, template-prefilled
``X2_FAILURES`` constant was never consumed by an x1 builder, test, receipt,
or truth artifact and is not evidence. X2 consumers import this overlay so
only failures actually observed after the pushed x1 boundary receive credit.
"""

from __future__ import annotations

from ghc_family_v659_v4_data import *  # noqa: F401,F403
import ghc_family_v659_v4_data as x1


X1_FREEZE = "8f1d7f05d3e79ede4b6579a68f1e0d901eba8669"
PREFILLED_X1_X2_FAILURES_IGNORED = tuple(x1.X2_FAILURES)

X2_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6594-X2-N001",
        "signature": "x1-commit-wrapper-returned-no-prose-receipt-after-the-git-process-completed",
        "recovery": "Retain the missing wrapper receipt at zero credit, inspect the exact new commit, parent, and subject, and never duplicate or amend the successful x1 commit.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6594-X2-N002",
        "signature": "frozen-x1-data-contained-an-unused-template-prefilled-x2-failure-constant",
        "recovery": "Prove that no x1 builder, test, receipt, or generated artifact consumed the prefilled rows; reject them as non-evidence and use this additive overlay for observed x2 failures only.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6594-X2-N003",
        "signature": "initial-x2-build-wrapper-returned-before-the-original-python-child-reached-terminal-state",
        "recovery": "Do not launch a duplicate build; retain the wrapper failure, follow the exact original Python process to exit, and inspect the declared scan and truth artifacts before rebuilding against changed failure data.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6594-X2-N004",
        "signature": "first-combined-x2-process-and-artifact-probe-completed-without-a-scalar-receipt",
        "recovery": "Retain the missing probe at zero credit, split exact PID checks from exact artifact checks, and continue monitoring the original build without replay while it remains active.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6594-X2-N005",
        "signature": "first-x2-reflection-remaster-passed-comma-joined-focus-terms-as-one-literal-and-scoped-zero-surfaces",
        "recovery": "Retain the zero-scope receipt at zero credit, inspect the append-style focus contract, and rerun against changed arguments with one explicit focus option per bounded family surface group.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6594-X2-N006",
        "signature": "first-x2-prestage-untracked-versus-manifest-inventory-returned-no-attributable-scalar-receipt",
        "recovery": "Retain the missing inventory at zero credit, derive the exact evidence allowlist from the manifest minus the immutable x1 tree, and defer the residue check until those paths are staged.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6594-X2-N007",
        "signature": "combined-process-query-after-the-missing-inventory-also-returned-no-usable-receipt",
        "recovery": "Retain the second wrapper loss, use a direct bounded Git-or-Python process query, and require zero matching processes before staging the manifest-derived allowlist.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6594-X2-N008",
        "signature": "first-valid-x2-evidence-index-review-lost-its-scalar-stdout-after-writing-the-complete-receipt",
        "recovery": "Retain the wrapper loss at zero credit, inspect the exact valid receipt without replaying its old input, and regenerate the ledger and index once against this newly retained failure.",
        "recovery_passed": True,
    },
]
