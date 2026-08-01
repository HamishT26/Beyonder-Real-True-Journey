#!/usr/bin/env python3
"""Immutable x2 lifecycle configuration for Caelen Ash v657-v5."""

from __future__ import annotations


SOURCE_COMMIT = "1ae8aa07d6b0d5f74dc3c5b29615c79b908e235f"
X1_COMMIT = "7fdae81a188decacbee20c2f2c283b7104c0e91a"
PHASE_ROOT = "docs/caelen-ash/v657-v5"
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 15787
SOURCE_EFFECTIVE_NEGATIVES = 15791
X1_OPERATIONAL_NEGATIVES = 18
SOURCE_OPEN_GAPS = 108
SOURCE_EXACT_GATES = 107
SOURCE_METHODS = 2067
X1_METHODS = 18
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
        "negative_id": "V6575-X2-N01",
        "slug": "x1-commit-wrapper-no-attributable-output",
        "failure_signature": (
            "The x1 diff-check and commit wrapper returned no attributable output, so the "
            "wrapper alone could not establish whether a commit existed."
        ),
        "candidate_workaround": (
            "Do not retry the mutation; audit exact HEAD, parent, subject, index, worktree, and lock state through scalar reads."
        ),
        "recurrence_guard": (
            "Treat a silent mutating wrapper as zero evidence until durable Git state is reread."
        ),
        "fail_procedure": "Infer commit success or failure from a silent wrapper.",
        "fail_observed": "No attributable commit result was returned; the invocation earned zero commit-proof credit.",
        "pass_procedure": "Read exact HEAD, parent, subject, and clean status before push.",
        "pass_observed": (
            "HEAD 7fdae81a188decacbee20c2f2c283b7104c0e91a is the direct child of the immutable source, carries the x1 freeze subject, and was subsequently pushed and proved clean and four-way equal."
        ),
        "scope_boundary": "Owner-local x1 durable-state verification only.",
    },
    {
        "negative_id": "V6575-X2-N02",
        "slug": "combined-postcommit-audit-no-attributable-output",
        "failure_signature": (
            "The first combined postcommit HEAD, log, index, worktree, lock, and status audit completed without attributable output."
        ),
        "candidate_workaround": (
            "Split HEAD, commit metadata, cleanliness, and equality into bounded scalar probes before x2."
        ),
        "recurrence_guard": (
            "Use scalar probes for durable lifecycle gates instead of coupling slow large-worktree status to every claim."
        ),
        "fail_procedure": "Treat the empty combined audit as proof of a clean x1 boundary.",
        "fail_observed": "The audit produced no claim evidence and earned zero lifecycle-gate credit.",
        "pass_procedure": "Read HEAD and commit metadata separately, then prove clean 0/0 four-way equality after push.",
        "pass_observed": (
            "The scalar probes established exact x1 HEAD, direct ancestry, clean state, zero divergence, and equality across local, upstream, tracking, and fresh live remote."
        ),
        "scope_boundary": "Owner-local x1 boundary recovery only.",
    },
    {
        "negative_id": "V6575-X2-N03",
        "slug": "combined-validation-receipt-wrapper-incomplete-output",
        "failure_signature": (
            "The detailed and minimal validators returned passing summaries, but the combined wrapper returned no receipt-builder summary and left the evidence manifest absent."
        ),
        "candidate_workaround": (
            "Inspect every durable validation artifact, retain the partial builder result, then rerun only the receipt builder with enough time for bounded Git-blob hashing."
        ),
        "recurrence_guard": (
            "Run validators and manifest construction as separate attributable lifecycle commands."
        ),
        "fail_procedure": "Infer that all evidence receipts exist from the two validator summaries.",
        "fail_observed": (
            "Detailed validation passed 322 checks and minimal validation passed 15 checks, but the final builder summary was absent and evidence-content-manifest.json did not exist."
        ),
        "pass_procedure": (
            "Regenerate x2 truth with this retained failure, rerun scoped validators, and execute the receipt builder alone before exact staging."
        ),
        "pass_observed": (
            "The isolated recovery is accepted only when the durable manifest, privacy, document-cap, owner-cap, detailed, and minimal receipts all exist and pass exact staged review."
        ),
        "scope_boundary": "Owner-local evidence-receipt construction recovery only.",
    },
    {
        "negative_id": "V6575-X2-N04",
        "slug": "combined-evidence-stage-review-no-output",
        "failure_signature": (
            "The exact evidence staging completed with 166 index paths, but the combined wrapper returned no review summary and produced no staged-review receipt."
        ),
        "candidate_workaround": (
            "Retain the staged index, update the operational ledger, refresh dependent evidence artifacts, then invoke the staged review alone."
        ),
        "recurrence_guard": (
            "Keep potentially slow exact staged review separate from Git add and poll its process explicitly."
        ),
        "fail_procedure": "Infer review success from the fact that evidence paths reached the index.",
        "fail_observed": (
            "The index contained 166 candidate paths but evidence-staged-review.json was absent, so the wrapper earned zero review credit."
        ),
        "pass_procedure": (
            "Refresh truth and manifests for this retained failure, stage the exact candidate, then run the review as a standalone attributable command."
        ),
        "pass_observed": (
            "Acceptance requires a durable valid review with no deletions, scope violations, frozen-x1 changes, unstaged or untracked paths, privacy hits, manifest mismatches, or diff-hygiene errors."
        ),
        "scope_boundary": "Owner-local exact staged-review recovery only.",
    },
    {
        "negative_id": "V6575-X2-N05",
        "slug": "frozen-x1-stale-owner-labels",
        "failure_signature": (
            "The pre-evidence stale-label audit found ten predecessor-owner/current-phase compound labels across three generated x1 Markdown headings and seven inherited helper lines in the immutable pushed x1 commit."
        ),
        "candidate_workaround": (
            "Do not rewrite frozen x1; add an x2 correction overlay that enumerates every occurrence and require zero such labels in mutable x2 additions."
        ),
        "recurrence_guard": (
            "Run exact current-owner label scans before freezing x1 and keep inherited helper functions out of copied builders."
        ),
        "fail_procedure": "Treat the stale x1 labels as current owner attribution or silently edit the frozen x1 tree.",
        "fail_observed": (
            "Ten stale occurrences were confirmed at the exact x1 commit and receive zero label-hygiene credit."
        ),
        "pass_procedure": (
            "Preserve x1 bytes, publish an exact correction overlay, and scan all mutable x2 additions for zero undeclared current-phase owner-label hits."
        ),
        "pass_observed": (
            "The correction overlay maps all ten frozen occurrences to Caelen Ash, while mutable x2 artifacts contain no undeclared predecessor-owner/current-phase compound label."
        ),
        "scope_boundary": "Owner-local provenance correction only; no history rewrite or identity-continuity claim.",
    },
]
