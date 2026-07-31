#!/usr/bin/env python3
"""Mutable-by-addition x2 operational failure register for v656-v5."""

from __future__ import annotations


# Add only failures first observed after the immutable x1 gate. Never move an x1
# failure here and never delete an entry after a bounded recovery.
X2_OPERATIONAL_NEGATIVES: list[dict] = [
    {
        "negative_id": "V6565-NEG-X2-001",
        "scope": "x2_document_cap_preflight",
        "signature": "powershell-foreach-pipeline-parser-recurrence",
        "observed": (
            "The first x2 document-cap probe repeated the known direct foreach-to-pipeline "
            "PowerShell parser fault and executed no file mutation."
        ),
        "credit": 0,
        "retained": True,
        "recovery": (
            "Materialize the bounded per-file projection into an array before JSON serialization."
        ),
        "recurrence_guard": (
            "Never pipe directly from a PowerShell foreach statement in this host."
        ),
        "same_owner_only": True,
        "independent_reproduction": False,
    },
    {
        "negative_id": "V6565-NEG-X2-002",
        "scope": "x2_document_cap_preflight",
        "signature": "frozen-x1-method-flow-document-cap-overrun",
        "observed": (
            "The corrected bounded preflight measured the immutable x1 Method Flow ledger "
            "at 136,811 words, above the 100,000-word live document ceiling."
        ),
        "credit": 0,
        "retained": True,
        "recovery": (
            "Preserve the oversized original in the immutable x1 commit, then use one "
            "dedicated post-closeout additive correction to replace every oversized live "
            "Method Flow document with deterministic lossless text-reference records."
        ),
        "recurrence_guard": (
            "Measure every prospective final document before the terminal validation gate "
            "and bind both the immutable source blob and corrected live representation."
        ),
        "same_owner_only": True,
        "independent_reproduction": False,
    },
    {
        "negative_id": "V6565-NEG-X2-003",
        "scope": "x2_template_inspection",
        "signature": "powershell-search-pattern-dollar-quoting-fault",
        "observed": (
            "A combined post-rewrite search used an unescaped dollar sign inside a "
            "PowerShell double-quoted regex and failed at parse time without executing."
        ),
        "credit": 0,
        "retained": True,
        "recovery": (
            "Split the inspection into literal bounded searches and avoid shell interpolation "
            "characters in composite command strings."
        ),
        "recurrence_guard": (
            "Use single-quoted literal patterns or separate rg calls when a search includes "
            "PowerShell interpolation syntax."
        ),
        "same_owner_only": True,
        "independent_reproduction": False,
    },
    {
        "negative_id": "V6565-NEG-X2-004",
        "scope": "x2_utf8_template_inspection",
        "signature": "windows-console-cp1252-macron-encode-failure",
        "observed": (
            "A read-only Python repr probe reached a Māori macron and failed while the "
            "Windows CP1252 console encoded the output; the UTF-8 source file was unchanged."
        ),
        "credit": 0,
        "retained": True,
        "recovery": (
            "Patch verified UTF-8 text directly and keep subsequent Python diagnostics under "
            "PYTHONUTF8 and PYTHONIOENCODING=utf-8."
        ),
        "recurrence_guard": (
            "Set the Python output encoding before printing Unicode-bearing source lines on Windows."
        ),
        "same_owner_only": True,
        "independent_reproduction": False,
    },
    {
        "negative_id": "V6565-NEG-X2-005",
        "scope": "x2_prebuild_audit",
        "signature": "large-worktree-broad-status-timeout",
        "observed": (
            "A combined full-status prebuild inventory crossed its bounded wrapper and "
            "returned no usable snapshot."
        ),
        "credit": 0,
        "retained": True,
        "recovery": (
            "Audit the exact owned x2 pathspecs with separate tracked-diff and untracked-file "
            "queries, then verify the immutable head independently."
        ),
        "recurrence_guard": (
            "Avoid full status enumeration in the large archive worktree when exact pathspec "
            "audits answer the lifecycle question."
        ),
        "same_owner_only": True,
        "independent_reproduction": False,
    },
    {
        "negative_id": "V6565-NEG-X2-006",
        "scope": "x2_evidence_build",
        "signature": "first-evidence-build-combined-test-gate-failure",
        "observed": (
            "The first evidence build generated the x2 candidates but its captured combined "
            "core-and-validation test selection returned nonzero before a success receipt."
        ),
        "credit": 0,
        "retained": True,
        "recovery": (
            "Run the core and evidence-validation modules separately to identify the failed "
            "module, correct only that dependency, and rebuild the changed candidate once."
        ),
        "recurrence_guard": (
            "On a captured combined test failure, isolate module boundaries before any broader rerun."
        ),
        "same_owner_only": True,
        "independent_reproduction": False,
    },
    {
        "negative_id": "V6565-NEG-X2-007",
        "scope": "x2_isolated_validation",
        "signature": "generated-evidence-negative-count-stale-after-retention",
        "observed": (
            "The isolated validation module found three count-dependent failures because "
            "the generated evidence predated retention of the failed-build negative: the "
            "register showed five x2 failures while the live source declared six."
        ),
        "credit": 0,
        "retained": True,
        "recovery": (
            "Regenerate the evidence candidate once from the current additive negative "
            "register so truth totals, Method Flow pairs, and minimal checks share one source."
        ),
        "recurrence_guard": (
            "Freeze the live negative register immediately before a changed-state evidence build."
        ),
        "same_owner_only": True,
        "independent_reproduction": False,
    },
    {
        "negative_id": "V6565-NEG-X2-008",
        "scope": "x2_evidence_build",
        "signature": "second-evidence-build-minimal-anchor-failure",
        "observed": (
            "The changed-state evidence rebuild regenerated current failure totals but its "
            "captured combined test gate still returned nonzero."
        ),
        "credit": 0,
        "retained": True,
        "recovery": (
            "Keep the generated state fixed and run only the validation module plus a "
            "non-mutating failed-check projection."
        ),
        "recurrence_guard": (
            "Do not broaden a changed-state rerun until the remaining exact minimal check is named."
        ),
        "same_owner_only": True,
        "independent_reproduction": False,
    },
    {
        "negative_id": "V6565-NEG-X2-009",
        "scope": "x2_isolated_validation",
        "signature": "minimal-x1-anchor-stale-source-constant",
        "observed": (
            "The isolated validation module passed eleven tests and failed only M014 because "
            "the validator still expected Caelen's prior x1 commit instead of Eiren's freeze."
        ),
        "credit": 0,
        "retained": True,
        "recovery": (
            "Replace the single inherited M014 hash with Eiren's exact x1 commit and rebuild "
            "the changed candidate."
        ),
        "recurrence_guard": (
            "Search every copied validator and test for inherited lifecycle anchors before execution."
        ),
        "same_owner_only": True,
        "independent_reproduction": False,
    },
]
