#!/usr/bin/env python3
"""Additive Tamar Vey v654-v1 x2 operational negatives."""

from __future__ import annotations


def _negative(number, signature, failed, recovery, guard):
    return {
        "negative_id": f"V6541-X2-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


X2_OPERATIONAL_NEGATIVES = [
    _negative(
        1,
        "evidence_builder_large_patch_context_mismatch",
        "The first large evidence-builder patch matched no bytes because an inherited Unicode line differed from the proposed context.",
        "Retain the failed patch, inspect exact bounded line windows, and apply small ASCII-anchored changes.",
        "Patch compact generated builders with exact small contexts and avoid spanning inherited non-ASCII text.",
    ),
    _negative(
        2,
        "evidence_manifest_unwritten_blob_lookup",
        "The first evidence validator computed a filtered blob identifier without writing the temporary object, then git cat-file correctly refused the absent object.",
        "Retain the failed validator, add hash-object -w for owner-local temporary blob materialization, and rerun the full bounded evidence validation.",
        "Any validator that reads a just-computed object through cat-file must write that object or hash the filtered bytes directly.",
    ),
    _negative(
        3,
        "porcelain_first_line_leading_space_trim",
        "The second evidence validator stripped the leading status space from the first modified path, then sliced away its first filename character and failed the scope gate.",
        "Retain the 17-of-18 result and read porcelain status directly without global string trimming before fixed-column parsing.",
        "Never apply strip to an entire porcelain status stream; preserve its two status columns exactly.",
    ),
]
