#!/usr/bin/env python3
"""Additive x2-only truth overlay for Liora Venn v659-v6.

The committed and pushed x1 data module is immutable. X2 consumers import
this overlay so only failures actually observed after the exact x1 boundary
receive x2 Method Flow and retained-negative credit.
"""

from __future__ import annotations

from ghc_family_v659_v6_data import *  # noqa: F401,F403
import ghc_family_v659_v6_data as x1


X1_FREEZE = "e76bc36a5fbfcebfa342d46e01bc4ff0125938cf"
PREFILLED_X1_X2_FAILURES_IGNORED = tuple(x1.PREFILLED_X1_X2_FAILURES_IGNORED)

# Append only failures actually observed after the frozen x1 boundary. The
# inherited x1 failures remain available through STARTUP_FAILURES and are
# preserved unchanged.
X2_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6596-X2-N001",
        "signature": "atomic-multi-file-route-and-boundary-patch-rejected-a-guessed-absent-cursor-assertion",
        "recovery": "Retain the atomic rejection at zero credit, reread each exact file, and apply smaller verified hunks without assuming the copied test contains source-shaped recipient assertions.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X2-N002",
        "signature": "first-x2-aggregate-reached-runner-aggregation-before-owner-local-runner-smoke-receipts-were-materialized",
        "recovery": "Retain the stopped aggregate and the mistaken validator assumption at zero credit, then invoke each of the ten validated family runners with its exact Liora-owned smoke-receipt output before refreshing x2.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X2-N003",
        "signature": "combined-method-flow-validation-and-summary-command-overfilled-the-output-window-with-the-complete-preferred-method-list",
        "recovery": "Retain the truncated wrapper at zero credit, use the complete file-backed summary and validation receipt, and suppress verbose summary stdout when regenerating after the new dependency is recorded.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X2-N004",
        "signature": "first-scoped-x2-test-copied-a-source-assertion-that-required-nonexistent-prefilled-x2-failure-rows",
        "recovery": "Retain the failing assertion at zero credit and require the Liora x1 overlay's explicit empty prefilled-failure tuple plus zero x1 consumers instead.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X2-N005",
        "signature": "first-scoped-x2-manifest-test-addressed-the-orin-evidence-commit-before-lioras-evidence-commit-existed",
        "recovery": "Retain the hard-coded commit lookup failure at zero credit and replay the precommit candidate manifest against exact owner-local Git-clean working bytes; closeout later binds the immutable evidence commit separately.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X2-N006",
        "signature": "first-scoped-x2-meta-tool-check-observed-forty-four-unresolved-trigger-overlap-findings",
        "recovery": "Retain the failed zero-collision assertion and inspect the exact catalogue cards and collision algorithm before changing any derived receipt or skill trigger.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X2-N007",
        "signature": "meta-tool-diagnosis-found-the-repository-compatibility-runner-was-used-instead-of-the-installed-family-current-runner",
        "recovery": "Retain the precedence error at zero credit and rebuild, validate, collision-check, and query the same phase with the installed family-current meta-tool, which uses actual phase runner-smoke receipts and current route metadata.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X2-N008",
        "signature": "stale-label-audit-passed-a-powershell-wildcard-as-a-literal-ripgrep-path-and-produced-a-windows-path-error",
        "recovery": "Retain the path error at zero credit and search the scripts directory with a -g filename filter instead of a wildcard path argument.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X2-N009",
        "signature": "broad-owner-packet-stale-label-audit-expanded-immutable-frozen-chain-and-selected-source-evidence-beyond-the-output-window",
        "recovery": "Retain the truncated audit at zero credit and restrict the recovery scan to Liora-authored x2 code and small route/truth artifacts while treating source-name evidence as intentional provenance.",
        "recovery_passed": True,
    },
]
