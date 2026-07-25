#!/usr/bin/env python3
"""Additive Tavian Sol v654-v6 x2 and closeout operational negatives."""

from __future__ import annotations


def _negative(number, signature, failed, recovery, guard):
    return {
        "negative_id": f"V6546-X2-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


def _closeout_negative(number, signature, failed, recovery, guard):
    row = _negative(number, signature, failed, recovery, guard)
    row["negative_id"] = f"V6546-CLOSEOUT-N{number:02d}"
    return row


# Append only after an attributable x2 attempt fails. A later recovery never
# rewrites or removes the failed witness.
X2_OPERATIONAL_NEGATIVES = [
    _negative(
        1,
        "PowerShell foreach output piped without materialization during template inventory",
        "A compact foreach expression was piped directly to ConvertTo-Json and failed with an empty-pipe-element parser error before returning any inventory.",
        "Materialize the foreach results into an array, then pipe the completed array to ConvertTo-Json; the bounded inventory completed.",
        "On Windows PowerShell, assign foreach output to a scalar or array before passing it into a pipeline.",
    ),
    _negative(
        2,
        "Windows rg wildcard path syntax rejected during copied-template audit",
        "A recursive text search passed shell-style wildcard path arguments to rg on Windows and failed with invalid filename syntax.",
        "Use literal file lists or search stable parent directories and filter filenames separately.",
        "Do not pass unexpanded shell wildcard path arguments to rg on Windows.",
    ),
    _negative(
        3,
        "broad copied-template text audit timeout",
        "The recovery search across broad scripts and tests parents exceeded its bounded timeout and produced no usable audit output.",
        "Inspect the exact copied files with literal paths and narrowly scoped patterns or direct bounded reads.",
        "After a broad archive-backed search fails, narrow immediately to explicit files and known semantic regions.",
    ),
    _negative(
        4,
        "background evidence launcher omitted its expected process receipt",
        "The hidden Start-Process launcher returned success but emitted no planned JSON process receipt, so the launch wrapper itself earned no receipt credit.",
        "Resolve the one exact evidence-builder process by its literal command line and audit the fixed stdout and stderr paths without starting another child.",
        "After a background launcher omits its receipt, audit the exact child and fixed logs before considering any relaunch.",
    ),
    _negative(
        5,
        "combined evidence-process monitor probe timeout",
        "A combined sleep, broad process query, and log-tail monitor exceeded its bounded wrapper timeout and returned no usable state.",
        "Probe the already-known process identifier directly and read the fixed logs in a separate scalar check; the child had exited and its bounded success receipt was present.",
        "Keep background-process monitoring scalar: known process identifier first, then bounded log reads without a broad CIM query.",
    ),
    _negative(
        6,
        "first bounded evidence validation retained inherited successor-state label",
        "The first 18-check bounded evidence validation passed 17 checks but rejected the stale inherited successor-contact-prohibited expectation against Tavian's frozen Elaren-prepared terminal-gate state; the aggregate earned zero credit.",
        "Patch the phase-local builder, tests, and validator to require the exact frozen Elaren-prepared terminal-gate state, then rebuild the additive Method Flow and evidence before a new bounded validation.",
        "Anchor successor-state assertions to the current phase x1 receipt instead of copying a predecessor phase label.",
    ),
]


# Append only after an attributable closeout attempt fails. These rows are
# rebuilt into Method Flow before content seal.
CLOSEOUT_OPERATIONAL_NEGATIVES = [
    _closeout_negative(
        1,
        "first current-phase closeout test aggregate read mutable Method Flow state",
        "The first 31-test current-phase closeout aggregate passed 30 tests but the x1 lifecycle test compared the current 89-method ledger with the frozen x1 expectation of 83, so the aggregate earned zero credit.",
        "Make the x1 lifecycle test read the Method Flow ledger from the exact frozen x1 commit, then rebuild the closeout ledger and rerun the bounded current-phase aggregate.",
        "Lifecycle tests for frozen phase state must read exact committed blobs rather than mutable descendant worktree paths.",
    ),
]
