#!/usr/bin/env python3
"""Additive Elowen Cairn v654-v2 x2 operational negatives."""

from __future__ import annotations


def _negative(number, signature, failed, recovery, guard):
    return {
        "negative_id": f"V6542-X2-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


X2_OPERATIONAL_NEGATIVES = [
    _negative(
        1,
        "closeout_inspection_foreach_pipeline_parser_fault",
        "The first Tamar closeout inventory piped a PowerShell foreach block directly and failed at parse time before reading any template content.",
        "Materialize the inspection rows in an array before piping, and keep the subsequent source reads bounded.",
        "Never pipe a PowerShell foreach statement directly; collect its output before applying a pipeline.",
    ),
    _negative(
        2,
        "final_privacy_x1_builder_scanner_definition_false_positive",
        "The first final staged privacy review failed closed on two scanner-pattern literals in the committed x1 preregistration builder and earned zero privacy credit.",
        "Quarantine only the exact x1 scanner-definition builder, then rerun the complete owner-surface five-class scan without exempting payload files.",
        "Every owner-local scanner implementation and generator that embeds its patterns must be present in the exact definition allowlist.",
    ),
    _negative(
        3,
        "closeout_hardcoded_count_rg_alternation_quoting_fault",
        "A follow-up hardcoded-count search crossed the PowerShell quoting boundary and treated alternation fragments as filenames, so it earned zero search credit.",
        "Replace the compound alternation with bounded scalar searches whose patterns contain no shell metacharacter ambiguity.",
        "Use one literal or simple scalar pattern per Windows shell search when auditing generated hardcoded counts.",
    ),
]
