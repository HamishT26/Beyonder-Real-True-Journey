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
CLOSEOUT_OPERATIONAL_NEGATIVES = [
    _closeout_negative(
        1,
        "closeout_baton_multiline_fstring_syntax_error",
        "The first closeout preflight found an unterminated fallback string inside a multiline f-string expression, so the builder did not compile and earned zero closeout credit.",
        "Keep the inherited-witness fallback string on one syntactically complete line and repeat only the bounded compile preflight.",
        "Do not split quoted fallback literals across physical lines inside f-string expressions.",
    ),
    _closeout_negative(
        2,
        "prepared_baton_inherited_route_stale_label",
        "The first content build reached the stale-route guard and stopped because a verbatim inherited Method Flow summary surfaced an obsolete new-task phrase inside the prepared Eiren baton, so the build earned zero terminal credit.",
        "Render inherited methods as bounded ledger references without replaying their phase-specific route prose, while retaining every exact inherited method and witness in the committed Method Flow ledger.",
        "Do not quote superseded phase-specific routing instructions in a successor activation baton.",
    ),
    _closeout_negative(
        3,
        "final_owner_privacy_scanner_definition_quarantine_omission",
        "The first staged owner scan passed 12 of 13 checks but classified two literal privacy-pattern definitions in the committed x1 preregistration builder as payload hits, so the staged review earned zero credit.",
        "Add the exact preregistration builder to the scanner-definition quarantine and rerun the complete staged review after rebuilding Method Flow.",
        "Classify known scanner source files by exact path before treating their literal detection patterns as payload.",
    ),
]
