#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Caelen Morrow v661-v8."""

from __future__ import annotations

from ghc_family_v661_v8_data import *  # noqa: F401,F403
import ghc_family_v661_v8_data as x1


X1_FREEZE = "1d999660e49a761e7484c171648b8b56d1d70ce3"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Append only failures actually observed after the immutable Caelen x1 freeze.
# Expected rejecting mutations belong to the mutation register, not here.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6618-X2-N001",
        "signature": "first_substantive_runtime_patch_used_an_already_normalized_version_token_context",
        "recovery": "Reread the exact current runtime lines and apply only the remaining basketry-domain substitutions; the rejected patch changed no repository byte.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6618-X2-N002",
        "signature": "mechanical_scaffolding_rewrite_added_utf8_bom_to_four_python_files",
        "recovery": "Remove only the leading BOM from the four new Caelen x2 Python files and repeat the AST and import probe before evidence generation.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6618-X2-N003",
        "signature": "first_bom_cleanup_wrapper_piped_directly_from_a_powershell_foreach_statement",
        "recovery": "Collect the four exact BOM-check rows in an explicit array before JSON projection; the parser fault executed no cleanup and changed no repository byte.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6618-X2-N004",
        "signature": "first_complete_x2_inventory_found_no_dedicated_current_phase_stale_label_review",
        "recovery": "Add a bounded evidence-delta stale-label scan, retain inherited Sylven source labels only as source evidence, and refresh only count and inventory dependent x2 receipts.",
        "completion_credit": 0,
    },
]
