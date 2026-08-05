#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Elaren Kestrel v662-v2."""

from __future__ import annotations

from ghc_family_v662_v2_data import *  # noqa: F401,F403
import ghc_family_v662_v2_data as x1


X1_FREEZE = "77f043266676075810fee3fa6d416282431a0c83"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Append only failures actually observed after the immutable Elaren x1 freeze.
# Expected rejecting mutations belong to the mutation register, not here.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6622-X2-N001",
        "signature": "first_large_x2_semantic_patch_was_rejected_atomically_after_a_prior_mechanical_source_rewrite",
        "recovery": "Retain the rejected patch at zero credit, inspect the current exact lines, and apply small semantic hunks for domain, source, route, and authority boundaries.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6622-X2-N002",
        "signature": "first_focused_x2_suite_passed_eighteen_of_twenty_but_found_unmaterialized_governance_receipts_and_a_self_dependent_stale_label_manifest_entry",
        "recovery": "Retain the 18-of-20 suite at zero aggregate credit, run only the required family-governance tools, exclude the self-dependent stale-label receipt from the exact content manifest, refresh count-dependent receipts without replaying surfaces or skill validators, and rerun the two affected tests before the focused suite.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6622-X2-N003",
        "signature": "first_isolated_governance_recovery_found_a_stale_forty_three_method_validation_receipt_after_the_ledger_advanced_to_forty_four",
        "recovery": "Retain the isolated one-of-two result at zero aggregate credit, treat the count-dependent Method Flow validation receipt as a declared manifest exclusion, refresh the ledger and counts once, then validate the final ledger after refresh.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6622-X2-N004",
        "signature": "pre_staging_inventory_found_three_untracked_future_closeout_and_final_templates_in_the_x2_evidence_delta",
        "recovery": "Retain the caught-before-staging scope error at zero credit, verify the templates were never executed or staged, delete only those three untracked Elaren-owned compatibility copies, and refresh the evidence manifest without rerunning surfaces.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6622-X2-N005",
        "signature": "first_post_receipt_index_audit_wrapper_contained_an_invisible_character_and_failed_at_python_parse_time",
        "recovery": "Retain the zero-credit wrapper failure, regenerate the derived x2 counts, use an ASCII-only audit identifier map, and require a complete post-receipt Git-index proof before commit.",
        "completion_credit": 0,
    },
]
