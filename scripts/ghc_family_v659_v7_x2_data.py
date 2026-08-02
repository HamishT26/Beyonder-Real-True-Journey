#!/usr/bin/env python3
"""Additive x2-only truth overlay for Tamar Vey v659-v7.

The committed and pushed x1 data module is immutable. X2 consumers import
this overlay so only failures actually observed after the exact x1 boundary
receive x2 Method Flow and retained-negative credit.
"""

from __future__ import annotations

from ghc_family_v659_v7_data import *  # noqa: F401,F403
import ghc_family_v659_v7_data as x1


X1_FREEZE = "0ef6e33a90bf6877ef3b365abeadc19317d68909"
PREFILLED_X1_X2_FAILURES_IGNORED = tuple(x1.PREFILLED_X1_X2_FAILURES_IGNORED)

# Append only failures actually observed after the frozen x1 boundary. The
# inherited x1 failures remain available through STARTUP_FAILURES and are
# preserved unchanged.
X2_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6597-X2-N001",
        "signature": "broad-x2-builder-stale-token-search-exceeded-the-context-output-budget",
        "recovery": (
            "Retain the overbroad read at zero credit, then inspect bounded line windows "
            "and targeted exact token matches before any builder execution."
        ),
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "recovery_passed": True,
    },
    {
        "negative_id": "V6597-X2-N002",
        "signature": "first-x2-unit-run-found-zero-reflection-surfaces-because-a-multiword-focus-was-treated-as-one-exact-term",
        "recovery": (
            "Retain the 19-pass, one-fail, one-precommit-skip attempt at zero credit, "
            "rerun only the read-only reflection inventory with separate bounded focus terms, "
            "then rerun the previously failing unit assertion after regenerated receipts."
        ),
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "recovery_passed": True,
    },
    {
        "negative_id": "V6597-X2-N003",
        "signature": "isolated-x2-toolbox-test-used-a-short-owner-scope-that-did-not-equal-the-catalogue-owner-scope",
        "recovery": (
            "Retain the isolated failure at zero credit, inspect the sanitized catalogue card schema, "
            "and query with the exact phase-local owner scope before rerunning only the blocked assertion."
        ),
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "recovery_passed": True,
    },
    {
        "negative_id": "V6597-X2-N004",
        "signature": "isolated-x2-toolbox-test-expected-zero-name-collisions-but-found-three-review-required-runner-pairs",
        "recovery": (
            "Retain the isolated failure at zero credit, preserve all three findings with no silent winner, "
            "and add an explicit adjudication showing that the frozen runner names bind distinct exact surfaces."
        ),
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "recovery_passed": True,
    },
    {
        "negative_id": "V6597-X2-N005",
        "signature": "first-x2-staging-wrapper-emitted-an-overlarge-crlf-warning-stream-and-truncated-its-diagnostic-display",
        "recovery": (
            "Retain the noisy wrapper at zero credit, inspect the already-written sanitized staged-review receipt, "
            "and suppress only advisory Git conversion warnings in later bounded summaries."
        ),
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "recovery_passed": True,
    },
    {
        "negative_id": "V6597-X2-N006",
        "signature": "first-x2-staged-review-found-three-method-flow-receipts-regenerated-after-the-content-manifest",
        "recovery": (
            "Retain the refused review at zero credit, rebuild the Method Flow ledger and its receipts, "
            "then regenerate the manifest last and rerun only the exact staged review."
        ),
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "recovery_passed": True,
    },
    {
        "negative_id": "V6597-X2-N007",
        "signature": "precommit-stale-label-probe-mixed-legitimate-inherited-provenance-with-current-code-and-produced-an-overlarge-false-positive-stream",
        "recovery": (
            "Retain the overbroad probe at zero credit, correct the two genuine current-code route labels, "
            "and restrict stale-copy scanning to current executable and test surfaces while preserving inherited evidence verbatim."
        ),
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "recovery_passed": True,
    },
]
