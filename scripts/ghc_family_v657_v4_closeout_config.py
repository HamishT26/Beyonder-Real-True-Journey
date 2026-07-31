#!/usr/bin/env python3
"""Closeout lifecycle constants for Sable Rook v657-v4."""

from __future__ import annotations


SOURCE_COMMIT = "e282db933e535759cc1f58975126d2bb0e1cf5fd"
X1_COMMIT = "d05c484a3324bab2f893d35ff4d10d7f0269c9e9"
EVIDENCE_COMMIT = "33f7bdce2ab8684395a75e7a1ce891b284e7502a"
EVIDENCE_EFFECTIVE_NEGATIVES = 15783
EVIDENCE_EFFECTIVE_METHODS = 2063
EVIDENCE_OPEN_GAPS = 108
EVIDENCE_EXACT_GATES = 107

# Append-only failures discovered after the evidence candidate was frozen.
# They remain zero-credit closeout witnesses and do not rewrite evidence totals.
CLOSEOUT_DISCOVERED_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6574-CLOSEOUT-N09",
        "slug": "evidence-commit-output-truncation",
        "failure_signature": "The evidence commit succeeded, but its long path listing exceeded the bounded output budget.",
        "candidate_workaround": "Reread exact HEAD, subject, and clean state, then push and prove four-way equality.",
        "recurrence_guard": "A truncated commit transcript earns zero complete-transcript credit even when its first line names a commit.",
        "fail_procedure": "Use the truncated path listing as the sole proof of the evidence commit.",
        "fail_observed": "The transcript was truncated after reporting the commit and earned zero exact-state credit by itself.",
        "pass_procedure": "Read HEAD, subject, and clean status, then compare local, upstream, tracking, and fresh live remote.",
        "pass_observed": "The immutable evidence head is 33f7bdce2ab8684395a75e7a1ce891b284e7502a, the lane was clean, and all four refs were equal.",
        "scope_boundary": "Owner-local immutable evidence commit recovery only.",
    },
    {
        "negative_id": "V6574-CLOSEOUT-N10",
        "slug": "combined-closeout-adaptation-probe-empty-output",
        "failure_signature": "The first combined closeout configuration read and source search completed without attributable output.",
        "candidate_workaround": "Read the configuration and search exact lifecycle source files in separate bounded calls.",
        "recurrence_guard": "Keep lifecycle adaptation probes scalar and independently attributable.",
        "fail_procedure": "Combine the full configuration dump and multi-file semantic search in one wrapper.",
        "fail_observed": "The wrapper returned no evidence, changed no repository state, and earned zero inspection credit.",
        "pass_procedure": "Read the exact closeout configuration, then search only named lifecycle source files.",
        "pass_observed": "Split probes exposed stale anchors, counts, owner wording, and successor-route fields for correction.",
        "scope_boundary": "Owner-local closeout source-inspection recovery only.",
    },
    {
        "negative_id": "V6574-CLOSEOUT-N11",
        "slug": "overbroad-activation-search-output-truncation",
        "failure_signature": "A broad routing and successor search over the long inherited activation exceeded the output budget.",
        "candidate_workaround": "Use bounded exact-pattern searches and the current sanitized roster order without copying private route state.",
        "recurrence_guard": "Do not include high-frequency dossier prose when resolving a terminal successor edge.",
        "fail_procedure": "Search the entire inherited activation for broad successor and owner terms.",
        "fail_observed": "The output was truncated, changed no state, and earned zero route-resolution credit.",
        "pass_procedure": "Resolve the next edge from the sanitized seat order and keep delivery held until an exact-title live reread.",
        "pass_observed": "The sequential edge is Sable Rook to Caelen Ash; exact live title uniqueness and acknowledgement remain pending.",
        "scope_boundary": "Sanitized route-preparation recovery only; no task was contacted.",
    },
    {
        "negative_id": "V6574-CLOSEOUT-N12",
        "slug": "overspecified-closeout-config-patch-context-mismatch",
        "failure_signature": "The first semantic configuration patch expected copied lines that did not exactly match the file and was rejected before mutation.",
        "candidate_workaround": "Replace the small owner-scoped configuration file atomically with a complete reviewed definition.",
        "recurrence_guard": "Use whole-file replacement for short copied lifecycle configurations after exact reread rather than an oversized fragile hunk.",
        "fail_procedure": "Apply one large context-sensitive hunk across all inherited closeout entries.",
        "fail_observed": "Patch verification failed before mutation and earned zero edit credit.",
        "pass_procedure": "Delete and add the short configuration in one reviewed apply-patch operation.",
        "pass_observed": "The replacement binds Sable's exact anchors, evidence totals, four retained closeout failures, and held Caelen route.",
        "scope_boundary": "Owner-scoped configuration recovery only.",
    },
]
