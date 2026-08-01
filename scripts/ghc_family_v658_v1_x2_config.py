#!/usr/bin/env python3
"""Immutable x2 lifecycle configuration for Elowen Cairn v658-v1."""

from __future__ import annotations


SOURCE_COMMIT = "15857de0afd21f7432196bf71b2f53ab2f5504c9"
FIRST_X1_COMMIT = "6f42b9dc6fca6ffed17438030ce8c36bc2535846"
X1_COMMIT = FIRST_X1_COMMIT
PHASE_ROOT = "docs/elowen-cairn/v658-v1"
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 16491
SOURCE_EFFECTIVE_NEGATIVES = 16492
X1_OPERATIONAL_NEGATIVES = 10
SOURCE_OPEN_GAPS = 112
SOURCE_EXACT_GATES = 111
SOURCE_METHODS = 2765
X1_METHODS = 11
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
        "negative_id": "V6581-X2-N01",
        "slug": "combined-x2-template-read-truncated",
        "failure_signature": (
            "A combined read of the inherited runtime and several large x2 builder windows "
            "exceeded the useful output envelope, so the truncated builder portion earned zero credit."
        ),
        "candidate_workaround": (
            "Read the runtime completely and inspect only active builder functions and bounded "
            "regions before adapting the current owner-local engine."
        ),
        "recurrence_guard": (
            "Map large lifecycle tools by declarations, then read one required function or bounded "
            "region at a time instead of aggregating several long templates."
        ),
        "fail_procedure": "Render the runtime and multiple large builder regions in one grouped result.",
        "fail_observed": (
            "The grouped result was truncated; no repository byte or external state was changed "
            "by the failed read and it received no evidence credit."
        ),
        "pass_procedure": (
            "Read the runtime through EOF, select active builder regions by function boundary, "
            "and adapt only the exact owner, domain, route, and count contracts."
        ),
        "pass_observed": (
            "The reusable contract, mutation, skill, runner, truth, Method Flow, and report "
            "functions were bounded without replaying Tamar's successful aggregate."
        ),
        "scope_boundary": (
            "Owner-local read and workflow recovery only; no structural, scientific, professional, "
            "production, route, authority, or independent-reproduction credit."
        ),
    },
    {
        "negative_id": "V6581-X2-N02",
        "slug": "console-rendered-unicode-used-as-whole-file-patch-context",
        "failure_signature": (
            "A whole-file patch was built from PowerShell-rendered source text whose Māori spelling "
            "was displayed as mojibake, so apply-patch atomically rejected the context."
        ),
        "candidate_workaround": (
            "Replace the owner-local uncommitted configuration with apply-patch using exact UTF-8 "
            "source text and retain the rejected attempt at zero credit."
        ),
        "recurrence_guard": (
            "Never use console-rendered Unicode as whole-file patch context; patch bounded exact "
            "UTF-8 lines or replace only an owner-created uncommitted template copy."
        ),
        "fail_procedure": "Construct a whole-file apply-patch from console-rendered Unicode output.",
        "fail_observed": "The patch context did not match and no repository byte changed.",
        "pass_procedure": (
            "Use apply-patch to replace the exact owner-local template copy with a clean UTF-8 "
            "configuration containing only observed Elowen failures."
        ),
        "pass_observed": "The immutable x2 configuration was installed with correct Māori spelling.",
        "scope_boundary": (
            "Owner-local source-edit recovery only; no cultural, scientific, route, authority, or "
            "completion credit."
        ),
    },
    {
        "negative_id": "V6581-X2-N03",
        "slug": "v8-isolate-base64-decoder-assumption",
        "failure_signature": (
            "A patch-orchestration attempt assumed the fresh V8 isolate exposed atob for a "
            "base64-encoded exact UTF-8 source region, but atob was undefined."
        ),
        "candidate_workaround": (
            "Have Python emit the exact source region as ensure_ascii JSON and decode it with "
            "JSON.parse before composing the apply-patch hunk."
        ),
        "recurrence_guard": (
            "Use only documented isolate helpers or self-contained JSON encoding; do not assume "
            "browser base64 globals exist in tool-orchestration isolates."
        ),
        "fail_procedure": "Decode an exact patch region with the unavailable atob global.",
        "fail_observed": "The orchestration script raised ReferenceError before apply-patch and changed no file.",
        "pass_procedure": "Round-trip the exact UTF-8 region through Python ensure_ascii JSON and JSON.parse.",
        "pass_observed": "The bounded owner-local function region was replaced with exact Unicode preserved.",
        "scope_boundary": "Owner-local patch-orchestration recovery only; no completion or authority credit.",
    },
]
