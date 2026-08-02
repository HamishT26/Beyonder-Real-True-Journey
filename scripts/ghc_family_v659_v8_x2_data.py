#!/usr/bin/env python3
"""Additive x2-only truth overlay for Elowen Cairn v659-v8.

The committed and pushed x1 data module is immutable. X2 consumers import
this overlay so only failures actually observed after the exact x1 boundary
receive x2 Method Flow and retained-negative credit.
"""

from __future__ import annotations

from ghc_family_v659_v8_data import *  # noqa: F401,F403
import ghc_family_v659_v8_data as x1


X1_FREEZE = "045abaa3dd4486e7b4a9e5ca1404ff8297963c8d"
PREFILLED_X1_X2_FAILURES_IGNORED = tuple(x1.PREFILLED_X1_X2_FAILURES_IGNORED)

# Append only failures actually observed after the frozen x1 boundary. The
# inherited x1 failures remain available through STARTUP_FAILURES and are
# preserved unchanged. Never prefill prospective failures.
X2_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6598-X2-N001",
        "signature": "first-runtime-domain-patch-used-a-console-mojibake-boundary-context-line",
        "recovery": (
            "Retain the atomically rejected patch at zero credit, reread the UTF-8 source explicitly, "
            "and apply smaller ASCII-safe hunks plus the exact decoded boundary text."
        ),
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "recovery_passed": True,
    },
    {
        "negative_id": "V6598-X2-N002",
        "signature": "first-x2-method-flow-summary-stdout-exceeded-the-bounded-output-budget",
        "recovery": (
            "Retain the truncated display at zero credit, preserve the complete written summary artifacts, "
            "and suppress only stdout when regenerating the summary against the updated ledger."
        ),
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "recovery_passed": True,
    },
    {
        "negative_id": "V6598-X2-N003",
        "signature": "successful-x2-test-output-exposed-a-stale-v659-v7-class-label",
        "recovery": (
            "Retain the stale label as a zero-credit hygiene issue, rename only the test class to v659-v8, "
            "and compile the changed module without replaying the successful scoped suite."
        ),
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "recovery_passed": True,
    },
]
