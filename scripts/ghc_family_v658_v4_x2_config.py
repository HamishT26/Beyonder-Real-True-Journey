#!/usr/bin/env python3
"""Immutable x2 lifecycle configuration for Eiren Kestrel v658-v4."""

from __future__ import annotations


SOURCE_COMMIT = "9c5f4c935d728f68b2ac612fa0affb4dfd389e05"
X1_COMMIT = "1e1d8bf1368c5f8304ad732a8a904834dd215adf"
PHASE_ROOT = "docs/eiren-kestrel/v658-v4"
SOURCE_EFFECTIVE_NEGATIVES = 17001
X1_OPERATIONAL_NEGATIVES = 17
SOURCE_OPEN_GAPS = 115
SOURCE_EXACT_GATES = 114
SOURCE_METHODS = 3275
X1_METHODS = 17
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
        "negative_id": "V6584-X2-N01",
        "slug": "js-template-literal-placeholder-interpolation",
        "failure_signature": "An apply-patch orchestration string treated a literal skill-template placeholder as a JavaScript interpolation and raised ReferenceError before any patch was applied.",
        "zero_credit": "The failed orchestration attempt earns zero implementation or validation credit.",
        "candidate_workaround": "Split the patch into bounded operations and transmit it through a non-template JavaScript string so the literal placeholder remains data.",
        "recurrence_guard": "When a patch contains placeholder syntax, use a plain quoted orchestration string or escape the placeholder before invoking apply_patch.",
        "scope_boundary": "Same-owner patch orchestration recovery only.",
        "fail_procedure": "Transmit a patch containing a literal skill placeholder through an interpolating orchestration string.",
        "fail_observed": "The orchestration layer raised ReferenceError before apply_patch received the patch.",
        "pass_procedure": "Retransmit the bounded patch through a non-interpolating string and inspect the exact target lines.",
        "pass_observed": "The intended owner-local lines changed and no unrelated file was modified.",
    },
    {
        "negative_id": "V6584-X2-N02",
        "slug": "broad-stale-label-scan-output-truncated",
        "failure_signature": "A combined stale-label probe traversed retained inherited ledgers and produced output beyond the bounded tool context, so its rendered result was truncated and unusable as validation evidence.",
        "zero_credit": "The truncated probe earns zero stale-label or privacy-validation credit.",
        "candidate_workaround": "Replace the probe with exact current-owner path classification plus bounded file-scoped summaries while retaining immutable inherited evidence.",
        "recurrence_guard": "Do not render complete inherited ledgers during a current-label audit; classify immutable evidence explicitly and cap diagnostic output.",
        "scope_boundary": "Same-owner diagnostic-output recovery only.",
        "fail_procedure": "Render every matching line from current and inherited owner documents in one stale-label probe.",
        "fail_observed": "The output exceeded the tool context and was truncated before it could support an attributable conclusion.",
        "pass_procedure": "Classify exact current-owner paths, exclude only declared immutable evidence, and record counts plus bounded path lists.",
        "pass_observed": "The replacement audit yields a complete machine-readable current-label receipt without rendering inherited ledgers.",
    },
    {
        "negative_id": "V6584-X2-N03",
        "slug": "repeated-recursive-label-probe-output-truncated",
        "failure_signature": "A follow-up recursive encoding-and-label probe again included the full phase document tree and exceeded the bounded output budget, so the diagnostic stream was truncated.",
        "zero_credit": "The repeated truncated diagnostic earns zero validation credit and does not supersede the first failure.",
        "candidate_workaround": "Limit subsequent probes to named implementation files or machine-count summaries with no recursive document rendering.",
        "recurrence_guard": "Never combine a recursive owner-document scan with rendered matching lines; use count-only classification and inspect at most one named file at a time.",
        "scope_boundary": "Same-owner bounded diagnostic recovery only.",
        "fail_procedure": "Recursively render encoding and label matches from the complete phase document tree.",
        "fail_observed": "The follow-up output was truncated again and could not receive validation credit.",
        "pass_procedure": "Use named-file reads and count-only scans, inspecting individual paths only when a count is nonzero.",
        "pass_observed": "Bounded probes complete with attributable output and retained evidence remains unchanged.",
    },
    {
        "negative_id": "V6584-X2-N04",
        "slug": "operational-negative-schema-key-mismatch",
        "failure_signature": "The first x2 builder invocation stopped with a KeyError after partial owner-local artifacts were emitted because the operational-negative records used field names incompatible with the Method Flow constructor.",
        "zero_credit": "The failed builder invocation and its partial files earn zero x2 build or test credit.",
        "candidate_workaround": "Inspect the constructor's exact record schema, add every required field, and deterministically rebuild the owner-local x2 artifacts.",
        "recurrence_guard": "Validate operational-negative record keys before invoking a phase builder and retain the failing invocation when schema drift is detected.",
        "scope_boundary": "Same-owner deterministic builder-schema recovery only.",
        "fail_procedure": "Invoke the x2 builder with operational-negative records that omit the constructor's required keys.",
        "fail_observed": "The builder raised KeyError at Method Flow construction after writing only a partial owner-local candidate.",
        "pass_procedure": "Conform each record to the frozen constructor schema, rerun the builder, and validate the complete artifact set.",
        "pass_observed": "The deterministic rebuild completes while the failed invocation remains retained at zero credit.",
    },
    {
        "negative_id": "V6584-X2-N05",
        "slug": "future-closeout-template-entered-x2-label-scan",
        "failure_signature": "The second x2 builder invocation failed closed because an uncommitted future-closeout template remained in the worktree and still contained an inherited-domain label.",
        "zero_credit": "The failed builder invocation earns zero x2 build or stale-label credit.",
        "candidate_workaround": "Park every future-closeout template in the D-drive scratch bank until the immutable x2 evidence commit is sealed, then patch it in the closeout lifecycle.",
        "recurrence_guard": "Keep future-lifecycle templates outside the active worktree until their lifecycle begins, even when they are untracked and intended only as scaffolding.",
        "scope_boundary": "Same-owner lifecycle-separation recovery only.",
        "fail_procedure": "Run the x2 current-label audit while a future-closeout template is present in the owner worktree.",
        "fail_observed": "The audit reported the future template and the builder stopped before validation credit.",
        "pass_procedure": "Move the exact future-closeout template set to the verified D-drive scratch directory and rebuild only the x2 lifecycle.",
        "pass_observed": "The x2 audit sees only current or immutable evidence paths; future templates remain preserved for the next lifecycle.",
    },
    {
        "negative_id": "V6584-X2-N06",
        "slug": "git-add-line-ending-warning-stream-truncated",
        "failure_signature": "The exact x2 staging command succeeded but emitted one line-ending warning per new file, causing the displayed warning stream to be truncated before it could serve as a complete staged-path review.",
        "zero_credit": "The truncated warning stream earns zero exact-review credit even though Git reported a successful staging exit code.",
        "candidate_workaround": "Ignore the non-fatal display stream for review purposes and compare the complete cached path set against the committed expected-delta list with a bounded machine summary.",
        "recurrence_guard": "For large additive stages, suppress or redirect repetitive conversion warnings and always perform an independent exact cached-path comparison.",
        "scope_boundary": "Same-owner staged-path review recovery only.",
        "fail_procedure": "Use the raw Git add warning stream as if it were a complete inventory of staged files.",
        "fail_observed": "The command exited successfully, but the warning display was truncated and therefore was not an exact path receipt.",
        "pass_procedure": "Read the cached name-status set directly, compare it to the builder's expected delta, and report only counts plus bounded mismatches.",
        "pass_observed": "The exact cached-path comparison supplies attributable staged-review evidence independently of warning rendering.",
    },
]
