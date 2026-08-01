#!/usr/bin/env python3
"""Immutable x2 lifecycle configuration for Liora Venn v657-v7."""

from __future__ import annotations


SOURCE_COMMIT = "b7f207d4c354dfd2671cd0562a058ac69f83fe35"
FIRST_X1_COMMIT = "9219708f5a8d16f7faee010f9c7f219f804b59a2"
X1_COMMIT = "9219708f5a8d16f7faee010f9c7f219f804b59a2"
PHASE_ROOT = "docs/liora-venn/v657-v7"
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 16144
SOURCE_EFFECTIVE_NEGATIVES = 16145
X1_OPERATIONAL_NEGATIVES = 12
SOURCE_OPEN_GAPS = 110
SOURCE_EXACT_GATES = 109
SOURCE_METHODS = 2420
X1_METHODS = 12
MUTATIONS_PER_PROPOSAL = 5
EXPECTED_PROPOSALS = 30
EXPECTED_MUTATIONS = EXPECTED_PROPOSALS * MUTATIONS_PER_PROPOSAL
EXPECTED_DISTRIBUTION = {
    "completed": 23,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}


X2_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6577-X2-N01",
        "slug": "runtime-domain-multihunk-patch-unicode-context-rejection",
        "failure_signature": (
            "The first runtime-domain patch combined ASCII fixture-field changes with a "
            "PowerShell-mojibake rendering of a Māori boundary line and was atomically rejected."
        ),
        "candidate_workaround": (
            "Apply the ASCII-stable fixture, validator, and mutation hunks separately, then "
            "audit the exact UTF-8 boundary code points before proposing any Unicode edit."
        ),
        "recurrence_guard": (
            "Do not combine domain refactors with shell-rendered Unicode context in one patch."
        ),
        "fail_procedure": "Patch the runtime fields and shell-rendered boundary in one multi-hunk edit.",
        "fail_observed": "Apply-patch rejected the complete edit without changing the runtime; zero evidence credit was assigned.",
        "pass_procedure": "Apply only ASCII-stable hunks and compile the resulting runtime.",
        "pass_observed": "The split patch replaced the real-world fixture fields and mutation identifier while preserving the existing UTF-8 boundary.",
        "scope_boundary": "Owner-local x2 source-edit recovery only; no empirical, safety, route, or independent-reproduction credit.",
    },
    {
        "negative_id": "V6577-X2-N02",
        "slug": "shell-mojibake-misread-as-source-unicode-defect",
        "failure_signature": (
            "A follow-up patch tried to replace a shell-rendered M-mojibake sequence, but the "
            "UTF-8 source already contained the correct U+0101 character, so the patch was rejected."
        ),
        "candidate_workaround": (
            "Inspect the exact source with an ASCII representation and Unicode code-point list; "
            "leave already-correct bytes unchanged."
        ),
        "recurrence_guard": (
            "Treat legacy-console mojibake as a display fault until an exact UTF-8 code-point audit proves a file defect."
        ),
        "fail_procedure": "Infer a repository encoding defect solely from PowerShell display text.",
        "fail_observed": "The single-line patch found no matching malformed source and earned zero credit.",
        "pass_procedure": "Read the exact UTF-8 line and enumerate non-ASCII code points.",
        "pass_observed": "The audit found U+0101 in the source, proving the Māori boundary text was already correctly encoded.",
        "scope_boundary": "Read-only encoding diagnosis only; no repository, route, or authority-state credit.",
    },
    {
        "negative_id": "V6577-X2-N03",
        "slug": "combined-x2-prose-patch-nonexistent-context",
        "failure_signature": (
            "A combined x2 prose patch included an expected inert-template comment that had "
            "not yet been added, so apply-patch rejected every hunk atomically."
        ),
        "candidate_workaround": (
            "Split the skill, report, inert-template marker, and function-call edits into "
            "independent patches against exact current ASCII-stable context."
        ),
        "recurrence_guard": (
            "Verify every cross-region patch anchor before combining independent x2 edits."
        ),
        "fail_procedure": "Apply skill, report, template, and call changes with one unverified context anchor.",
        "fail_observed": "The patch found no inert-template comment and changed no file; zero evidence credit was assigned.",
        "pass_procedure": "Apply bounded exact-current patches separately and inspect each resulting region.",
        "pass_observed": "The split edits installed the optics skill boundaries, static-report boundary, inert marker, and v657-v7 overview call.",
        "scope_boundary": "Owner-local x2 prose-edit recovery only; no scientific, safety, route, or independent-reproduction credit.",
    },
]
