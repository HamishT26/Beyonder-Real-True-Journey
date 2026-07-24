#!/usr/bin/env python3
"""Additive Sylven Arc v654-v3 x2 operational negatives."""

from __future__ import annotations


def _negative(number, signature, failed, recovery, guard):
    return {
        "negative_id": f"V6543-X2-N{number:02d}",
        "signature": signature,
        "failed": failed,
        "recovery": recovery,
        "recurrence_guard": guard,
        "credit": "retained_negative_zero_initial_pass_credit",
    }


X2_OPERATIONAL_NEGATIVES = [
    _negative(
        1,
        "broad_evidence_patch_unicode_context_mismatch",
        "The first broad x2 evidence patch matched the structural sections but failed atomically on one Unicode-sensitive boundary line, so it changed no file and earned zero credit.",
        "Split runner, skill, test, and truth edits into smaller exact-context patches.",
        "Do not combine Unicode-sensitive prose with independent structural edits in one patch.",
    ),
    _negative(
        2,
        "stale_label_search_quoting_fault",
        "A compound stale-label search crossed the PowerShell quoting boundary before ripgrep executed and earned zero review credit.",
        "Use a single-quoted bounded pattern without shell-sensitive Unicode fragments.",
        "Keep Windows stale-label review patterns simple and shell-literal.",
    ),
    _negative(
        3,
        "windows_rg_wildcard_path_assumption",
        "A stale-label review passed a wildcard as a literal Windows path to ripgrep and failed before scanning any file.",
        "Search the literal scripts directory with an explicit file glob.",
        "Never pass an unresolved Windows wildcard path as a ripgrep path operand.",
    ),
    _negative(
        4,
        "x1_test_live_method_flow_lifecycle_assumption",
        "The first current-phase aggregate passed 15 tests but failed one x1 lifecycle assertion because the x1 test read the live 34-method ledger instead of the immutable 31-method x1 ledger.",
        "Read the Method Flow ledger from the frozen x1 commit for x1-specific assertions, while leaving x2 evidence tests on the live ledger.",
        "Every lifecycle-specific test must bind immutable phase artifacts rather than mutable successor files.",
    ),
    _negative(
        5,
        "x1_commit_message_selector_initial_freeze_collision",
        "The second current-phase aggregate found the initial x1 freeze commit by message and read 30 methods instead of the repaired final x1 commit's 31 methods.",
        "Bind the already verified exact final x1 anchor directly in the lifecycle test.",
        "Use exact lifecycle anchors when a phase contains more than one x1 commit.",
    ),
]
