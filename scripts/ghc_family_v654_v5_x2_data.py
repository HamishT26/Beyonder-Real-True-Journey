#!/usr/bin/env python3
"""Additive Eiren Kestrel v654-v5 x2 and closeout operational negatives."""

from __future__ import annotations


def _negative(number, signature, failed, recovery, guard):
    return {
        "negative_id": f"V6545-X2-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


def _closeout_negative(number, signature, failed, recovery, guard):
    row = _negative(number, signature, failed, recovery, guard)
    row["negative_id"] = f"V6545-CLOSEOUT-N{number:02d}"
    return row


# Append only after an attributable x2 attempt fails. A later recovery never
# rewrites or removes the failed witness.
X2_OPERATIONAL_NEGATIVES = []


# Append only after an attributable closeout attempt fails. These rows are
# rebuilt into Method Flow before content seal.
CLOSEOUT_OPERATIONAL_NEGATIVES = [
    _closeout_negative(
        1,
        "combined closeout inspection timeout",
        "A combined status, branch, head, and multi-file search command exceeded its bounded timeout and returned no usable inspection output.",
        "Split the audit into scalar Git state checks and narrowly scoped file inspections; both completed without mutating tracked state.",
        "Keep closeout state probes scalar and avoid combining Git inspection with repository text searches in one bounded command.",
    ),
    _closeout_negative(
        2,
        "broad JSON contract body search timeout",
        "A recursive body search across documentation JSON files exceeded its bounded timeout before identifying newer full-suite contracts.",
        "Use a filename-only tracked-file inventory, then open only the exact candidate contract needed for the phase.",
        "Inventory candidate filenames before searching large documentation bodies.",
    ),
    _closeout_negative(
        3,
        "indexed wildcard contract search timeout",
        "A Git-indexed content search with broad recursive wildcard domains still exceeded its bounded timeout and earned no result credit.",
        "Use git ls-files with a filename suffix filter; the bounded inventory completed and identified the available full-suite contracts.",
        "Prefer filename-only Git inventories over broad indexed content searches when the target artifact has a stable suffix.",
    ),
    _closeout_negative(
        4,
        "single-file pattern probe timeout",
        "A single-file multi-pattern rg probe exceeded a short timeout on the archive-backed worktree and returned no usable navigation output.",
        "Read the known closeout-builder regions directly in bounded line windows and patch the exact protocol block.",
        "On a slow archive-backed lane, prefer direct known-range reads over exploratory pattern probes during closeout.",
    ),
    _closeout_negative(
        5,
        "staged-review wrapper timeout with late child completion",
        "The staged-review wrapper exceeded its two-minute wait bound and returned no immediate receipt, while the child process continued in the archive-backed lane.",
        "Audit the exact process and five expected receipt paths before retrying; the child later exited and all five receipts existed, preserving the passing witness without claiming the wrapper succeeded.",
        "After a validator wrapper timeout, inspect process state and exact receipt artifacts before any retry or termination.",
    ),
    _closeout_negative(
        6,
        "validator process termination race",
        "A targeted stop command found that the known validator process had exited between the preceding process audit and the termination attempt.",
        "Treat the stop error as zero-credit tooling evidence, then inspect the completed receipt set and retain the already-finished staged-review result.",
        "Recheck the exact process identifier immediately before termination and tolerate a clean already-exited state without retrying the validator.",
    ),
]
