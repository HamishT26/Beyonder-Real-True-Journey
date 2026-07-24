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
    _negative(
        4,
        "inherited_test_symbol_inventory_overbroad",
        "A read-only multi-module test-symbol inventory emitted more inherited source text than the tool boundary could return and was truncated before a bounded selector was established.",
        "Retain the truncated inventory with zero selector credit and count test cases per file with a scalar AST probe before choosing dependency-justified modules.",
        "Inventory inherited tests as per-file scalar counts; never print broad matching source bodies.",
    ),
    _negative(
        5,
        "grouped_closeout_status_probe_timeout",
        "A grouped read-only closeout probe combining status, head, log, file count, and script inventory timed out before returning attributable output.",
        "Retain the timeout and split status, exact head, and inventories into isolated bounded probes.",
        "Run one cold Git or filesystem subsystem per bounded closeout probe.",
    ),
    _negative(
        6,
        "full_untracked_status_inventory_timeout",
        "A read-only full untracked-status inventory timed out before returning its projected path count and bounded sample.",
        "Retain the timeout and inspect tracked status separately from owner-scoped untracked paths before explicit staging.",
        "Do not enumerate the checkout-wide untracked surface during closeout; scope untracked inventory to owner paths.",
    ),
    _negative(
        7,
        "per_entry_manifest_replay_timeout",
        "The first exact staged review exceeded its time bound while replaying inherited manifest entries through one Git process per row and was terminated without a receipt.",
        "Retain the timed-out attempt and replay each commit through one exact tree map plus bounded batch object reads.",
        "Never validate a large commit-local manifest with one Git subprocess per entry.",
    ),
    _negative(
        8,
        "batch_cat_file_pipe_deadlock_timeout",
        "The second staged review exceeded its time bound because its helper wrote every batch request before reading large Git blob output, allowing the Windows stdout pipe to fill and deadlock.",
        "Retain the timeout, terminate only the owned helper processes, use communicate for concurrent pipe handling, and parse the bounded returned byte stream deterministically.",
        "Use subprocess communicate rather than write-then-read for multi-object Git batch protocols on Windows.",
    ),
    _negative(
        9,
        "inherited_scanner_definition_false_positive",
        "The third staged review failed closed on six private-route and session-stream scanner literals stored in earlier phase privacy receipts and the x1 builder, with zero payload evidence.",
        "Retain the failed scan and quarantine only the exact earlier scanner-definition files before rescanning the complete owner surface.",
        "Carry every phase-local scanner implementation and its own receipt in an explicit definition allowlist without exempting payload files.",
    ),
    _negative(
        10,
        "generated_markdown_trailing_space_diff_hygiene",
        "The first exact diff-hygiene review rejected thirty generated Markdown proposal headings that used trailing hard-break spaces.",
        "Retain the failed hygiene check, remove the hard-break spaces in the generator, rebuild the seal, and regenerate exact manifests.",
        "Generate wrapped proposal bullets with explicit newlines and indentation rather than trailing Markdown spaces.",
    ),
    _negative(
        11,
        "checkout_wide_unstaged_name_diff_timeout",
        "A read-only checkout-wide unstaged-name diff exceeded its time bound before returning a path inventory.",
        "Retain the timeout and prove index-to-worktree equality with git diff-files --quiet plus owner-scoped untracked checks.",
        "Use plumbing-level quiet equality for large worktrees; enumerate only the owner-scoped untracked surface.",
    ),
    _negative(
        12,
        "postpush_porcelain_clean_probe_timeout",
        "After the first closeout was pushed and four-way equal, a read-only porcelain clean-state probe exceeded its time bound before returning a result.",
        "Retain the timeout in one additive terminal correction and use tracked diff-files and diff-index equality plus owner-scoped untracked checks.",
        "Do not use checkout-wide porcelain status as the terminal clean-state primitive on this large Windows worktree.",
    ),
]
