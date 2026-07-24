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


def _closeout_negative(number, signature, failed, recovery, guard):
    row = _negative(number, signature, failed, recovery, guard)
    row["negative_id"] = f"V6543-CLOSEOUT-N{number:02d}"
    return row


CLOSEOUT_OPERATIONAL_NEGATIVES = [
    _closeout_negative(
        1,
        "combined_closeout_state_probe_timeout",
        "A combined status, head, branch, line-count, and source-tail probe exceeded its bound before yielding attributable output and earned zero review credit.",
        "Audit repository status first, then split scalar Git and bounded file reads into separate commands.",
        "Do not combine cold Git state probes with source-file reads in one closeout command.",
    ),
    _closeout_negative(
        2,
        "assumed_x1_final_manifest_filename",
        "A manifest count probe successfully read the evidence manifest but then assumed a nonexistent x1-final-manifest filename and earned no x1-manifest review credit.",
        "Inventory the exact phase validation filenames before selecting the committed x1 staged manifest.",
        "Resolve manifest filenames from the phase directory before projecting their schemas or counts.",
    ),
    _closeout_negative(
        3,
        "assumed_x1_proposal_ledger_directory",
        "A proposal-title probe assumed an x1 proposal-ledger path that does not exist and therefore produced no proposal-review evidence.",
        "Inventory the exact owner packet paths and read the committed proposal ledger from its actual directory.",
        "Resolve phase artifact paths before projecting their fields.",
    ),
    _closeout_negative(
        4,
        "assumed_runner_plan_filename",
        "A runner-plan probe assumed a preregistration filename that is not present and therefore earned no runner-inventory credit.",
        "Use the committed phase-data runner declarations and exact tooling inventory files discovered from the owner packet.",
        "Inventory exact runner artifacts before reading them.",
    ),
    _closeout_negative(
        5,
        "closeout_method_parity_omitted_inherited_external_witnesses",
        "The first closeout build reconstructed and validated Method Flow but stopped before seal output because its operational-parity assertion omitted five inherited external witness pairs.",
        "Include the five inherited external negative records with x1, x2, and closeout failures in the parity domain, then rebuild from immutable evidence.",
        "Define Method Flow parity over every inherited-external and owner-phase failure represented by the ledger.",
    ),
    _closeout_negative(
        6,
        "staged_baton_heading_case_assertion",
        "The first staged current-phase aggregate passed 25 of 26 tests but failed a case-sensitive assertion that expected a lower-case baton heading phrase while the committed heading correctly begins with an upper-case word.",
        "Bind the structural test to the exact heading capitalization without changing the sanitized baton meaning.",
        "Use exact normalized headings for case-sensitive document assertions.",
    ),
]
