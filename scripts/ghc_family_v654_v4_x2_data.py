#!/usr/bin/env python3
"""Additive Caelen Morrow v654-v4 x2 and closeout operational negatives."""

from __future__ import annotations


def _negative(number, signature, failed, recovery, guard):
    return {
        "negative_id": f"V6544-X2-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


def _closeout_negative(number, signature, failed, recovery, guard):
    row = _negative(number, signature, failed, recovery, guard)
    row["negative_id"] = f"V6544-CLOSEOUT-N{number:02d}"
    return row


# Append only after an attributable x2 attempt fails. A later recovery never
# rewrites or removes the failed witness.
X2_OPERATIONAL_NEGATIVES = []


# Append only after an attributable closeout attempt fails. These rows are
# rebuilt into Method Flow before content seal.
CLOSEOUT_OPERATIONAL_NEGATIVES = []
