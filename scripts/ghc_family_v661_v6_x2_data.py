#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Elowen Cairn v661-v6."""

from __future__ import annotations

from ghc_family_v661_v6_data import *  # noqa: F401,F403
import ghc_family_v661_v6_data as x1


X1_FREEZE = "2896abfb994093e547e6fb5b219026c25af1a21b"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Append only failures actually observed after the immutable Elowen x1 freeze.
# Expected rejecting mutations belong to the mutation register, not here.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6616-X2-N001",
        "signature": "first-x2-builder-template-transport-truncated-at-the-tool-output-budget",
        "recovery": "Retain the incomplete unexecuted file at zero credit, reconstruct it from bounded exact source chunks, then verify AST, line count, and required functions before any x2 build.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6616-X2-N002",
        "signature": "default-console-projection-could-not-encode-maori-text-even-though-the-utf8-file-was-correct",
        "recovery": "Retain the projection failure at zero credit and inspect the committed bytes with an ASCII-safe Unicode-escape projection; do not rewrite correct UTF-8 content to satisfy a legacy console encoding.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6616-X2-N003",
        "signature": "yaml-version-probe-returned-an-unbounded-truncated-tool-presentation",
        "recovery": "Retain the presentation failure at zero credit and replace it with a bounded JSON boolean import-availability probe before invoking the validator.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6616-X2-N004",
        "signature": "quick-validate-cp1252-decode-failure-ghc-family-gmut-piano-constraint-graph",
        "recovery": "Retain the failed invocation at zero credit and rerun only this validator with process-local PYTHONUTF8=1; the unchanged UTF-8 skill then passed.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6616-X2-N005",
        "signature": "quick-validate-cp1252-decode-failure-ghc-family-piano-accessibility-companion",
        "recovery": "Retain the failed invocation at zero credit and rerun only this validator with process-local PYTHONUTF8=1; the unchanged UTF-8 skill then passed.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6616-X2-N006",
        "signature": "quick-validate-cp1252-decode-failure-ghc-family-piano-action-topology",
        "recovery": "Retain the failed invocation at zero credit and rerun only this validator with process-local PYTHONUTF8=1; the unchanged UTF-8 skill then passed.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6616-X2-N007",
        "signature": "quick-validate-cp1252-decode-failure-ghc-family-piano-correction-lineage",
        "recovery": "Retain the failed invocation at zero credit and rerun only this validator with process-local PYTHONUTF8=1; the unchanged UTF-8 skill then passed.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6616-X2-N008",
        "signature": "quick-validate-cp1252-decode-failure-ghc-family-piano-intake-identity",
        "recovery": "Retain the failed invocation at zero credit and rerun only this validator with process-local PYTHONUTF8=1; the unchanged UTF-8 skill then passed.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6616-X2-N009",
        "signature": "quick-validate-cp1252-decode-failure-ghc-family-piano-keyframe-topology",
        "recovery": "Retain the failed invocation at zero credit and rerun only this validator with process-local PYTHONUTF8=1; the unchanged UTF-8 skill then passed.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6616-X2-N010",
        "signature": "quick-validate-cp1252-decode-failure-ghc-family-piano-material-claim-hold",
        "recovery": "Retain the failed invocation at zero credit and rerun only this validator with process-local PYTHONUTF8=1; the unchanged UTF-8 skill then passed.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6616-X2-N011",
        "signature": "quick-validate-cp1252-decode-failure-ghc-family-piano-measurement-envelope",
        "recovery": "Retain the failed invocation at zero credit and rerun only this validator with process-local PYTHONUTF8=1; the unchanged UTF-8 skill then passed.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6616-X2-N012",
        "signature": "quick-validate-cp1252-decode-failure-ghc-family-piano-privacy-minimization",
        "recovery": "Retain the failed invocation at zero credit and rerun only this validator with process-local PYTHONUTF8=1; the unchanged UTF-8 skill then passed.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6616-X2-N013",
        "signature": "quick-validate-cp1252-decode-failure-ghc-family-piano-rights-authority",
        "recovery": "Retain the failed invocation at zero credit and rerun only this validator with process-local PYTHONUTF8=1; the unchanged UTF-8 skill then passed.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6616-X2-N014",
        "signature": "direct-powershell-foreach-block-could-not-be-piped-without-an-enclosing-expression",
        "recovery": "Retain the parser fault at zero credit and collect the bounded read-only script inventory into an explicit array before JSON projection.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6616-X2-N015",
        "signature": "combined-meta-tool-box-wrapper-timed-out-after-catalogue-build-before-validation-and-collision-projection",
        "recovery": "Retain the aggregate timeout at zero credit, inspect the exact output directory, preserve the completed 20-card catalogue, and invoke only the two missing validation and collision subcommands separately.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6616-X2-N016",
        "signature": "final-truth-and-document-cap-summary-projection-guessed-nonexistent-receipt-property-names",
        "recovery": "Retain the null projection at zero credit, inspect each receipt's actual property names, and project effective_open_gaps, effective_exact_gates, terminal_verdict, cap_per_document, and passes explicitly.",
        "completion_credit": 0,
    },
]
