#!/usr/bin/env python3
"""Immutable closeout configuration for Orin Thale v657-v6."""

from __future__ import annotations


SOURCE_COMMIT = "87815f96a372849dfb42a09d785515e858ea7925"
FIRST_X1_COMMIT = "40c25aeb884fadc96366847507ff79c53d4e95c5"
X1_COMMIT = "f7161b026d270a131cc8449e75a7562fe04f0f66"
EVIDENCE_COMMIT = "a8b76a81a588e0cb7b64c3ec17f508151e349b7e"
PHASE_ROOT = "docs/orin-thale/v657-v6"
BRANCH = "codex/GHC-Family/orin-thale-v657-v6-full-tools"
EVIDENCE_EFFECTIVE_NEGATIVES = 16139
EVIDENCE_EFFECTIVE_METHODS = 2415
OPEN_GAPS = 110
EXACT_GATES = 109


CLOSEOUT_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6576-CLOSEOUT-N01",
        "slug": "powershell-null-empty-status-comparison",
        "failure_signature": (
            "A post-evidence scalar audit assigned empty git-status output to a PowerShell variable; "
            "$null -eq '' evaluated false and incorrectly reported TrackedClean=false."
        ),
        "candidate_workaround": "Materialize status output as an array and require its Count to equal zero.",
        "recurrence_guard": "Use @(...).Count for commands whose successful empty output becomes PowerShell $null.",
        "fail_procedure": "Compare a scalar variable containing empty native-command output directly with an empty string.",
        "fail_observed": "The summary reported a dirty tracked state although direct porcelain, unstaged, and staged reads were empty; zero gate credit was assigned.",
        "pass_procedure": "Read status, unstaged diff, and staged diff directly, then use array counts for the four-way equality audit.",
        "pass_observed": (
            "Direct reads were empty, and the later array-count audit proved zero tracked and untracked "
            "rows with evidence HEAD equal across local, upstream, tracking, and fresh live remote."
        ),
        "scope_boundary": "Owner-local evidence-boundary status recovery only; no route or independent-reproduction credit.",
    },
    {
        "negative_id": "V6576-CLOSEOUT-N02",
        "slug": "blank-composite-readonly-audit-wrapper",
        "failure_signature": (
            "The first composite read-only closeout audit wrapper completed without returning attributable "
            "JSON or scalar output, so it could not support any state or gate claim."
        ),
        "candidate_workaround": "Split the audit into explicit no-profile scalar probes and poll the long-running Git status separately.",
        "recurrence_guard": "Require a labelled output line for every read-only audit field and treat empty wrapper output as zero credit.",
        "fail_procedure": "Run branch, head, status, and file-existence checks through one composite wrapper and accept wrapper completion alone.",
        "fail_observed": "The wrapper returned no attributable evidence; it changed no repository state and received zero credit.",
        "pass_procedure": "Run labelled HEAD, branch, builder-existence, byte-count, and status probes with a no-profile shell and bounded polling.",
        "pass_observed": (
            "The recovery proved evidence HEAD a8b76a81a588e0cb7b64c3ec17f508151e349b7e, the exact Orin branch, "
            "a 35,112-byte builder, and only the two expected untracked closeout files."
        ),
        "scope_boundary": "Owner-local read-only closeout audit transport only; no test, route, or independent-reproduction credit.",
    },
    {
        "negative_id": "V6576-CLOSEOUT-N03",
        "slug": "composite-allowlist-audit-result-loss",
        "failure_signature": (
            "A composite read-only candidate-path allowlist wrapper yielded without returning its labelled counts "
            "or a resumable session identifier, so it could not support staged-path credit."
        ),
        "candidate_workaround": "Run Git path enumerations as isolated commands and poll every returned session identifier through completion.",
        "recurrence_guard": "Never treat a blank yielded wrapper as completion; require an exit code or a resumable session plus exact path output.",
        "fail_procedure": "Combine status enumeration, substring parsing, allowlist filtering, and count reporting in one wrapper.",
        "fail_observed": "No attributable count or path evidence returned; no repository mutation occurred and the probe received zero credit.",
        "pass_procedure": "Run git ls-files --others --exclude-standard alone and poll the returned session until its exit code and exact paths arrive.",
        "pass_observed": (
            "The isolated recovery returned 31 exact paths: 26 under docs/orin-thale/v657-v6, four v657-v6 scripts, "
            "and one v657-v6 closeout test, with no sibling or shared-lane path."
        ),
        "scope_boundary": "Owner-local candidate-path enumeration only; no staged-review, test, route, or independent-reproduction credit.",
    },
    {
        "negative_id": "V6576-CLOSEOUT-N04",
        "slug": "closeout-staged-diff-hygiene-blank-eof",
        "failure_signature": (
            "The first exact closeout staged review returned invalid because git diff --cached --check found "
            "a new blank line at EOF in the mechanically derived closeout-receipt builder."
        ),
        "candidate_workaround": "Remove only the trailing blank EOF line, rebuild dependent receipts, and rerun the bounded staged review.",
        "recurrence_guard": "Run git diff --cached --check and inspect its exact stdout before assigning staged-review credit.",
        "fail_procedure": "Accept a mechanically transformed script without verifying its terminal newline surface in the staged index.",
        "fail_observed": (
            "The staged review received zero credit with diff_check_returncode nonzero; all deletion, scope, "
            "frozen-x1, unstaged, untracked, privacy, and manifest issue lists were otherwise empty."
        ),
        "pass_procedure": "Normalize the single file ending, regenerate all dependent closeout artifacts and manifest, restage, and rerun exact review.",
        "pass_observed": (
            "After the one-line EOF correction was staged, git diff --cached --check returned zero with no finding; "
            "the full dependent staged review was then required separately."
        ),
        "scope_boundary": "Owner-local staged diff hygiene only; no scientific, route, or independent-reproduction credit.",
    },
    {
        "negative_id": "V6576-CLOSEOUT-N05",
        "slug": "stale-closeout-json-count-floor",
        "failure_signature": (
            "The first bounded closeout lifecycle suite passed nine of ten checks but rejected the truthful 188-JSON "
            "packet because its locally chosen lower-bound assertion required at least 190 files."
        ),
        "candidate_workaround": "Replace the unsupported 190 threshold with the preregistered bounded packet floor of 180 and rerun only the failed test first.",
        "recurrence_guard": "Derive file-count gates from declared packet contracts or exact manifests, never from speculative round-number growth assumptions.",
        "fail_procedure": "Assert an ungrounded minimum of 190 phase JSON files in the closeout lifecycle suite.",
        "fail_observed": "The suite ran ten tests with one assertion failure at 188 versus 190; all JSON parsing itself succeeded and the run received zero aggregate credit.",
        "pass_procedure": "Set the declared lower bound to 180 and rerun the formerly failing JSON-parse-and-word-cap test in isolation.",
        "pass_observed": "The isolated corrected test passed 1 of 1 after parsing every phase JSON document and enforcing the 100,000-word cap.",
        "scope_boundary": "Owner-local test-count contract correction only; no full-suite, route, or independent-reproduction credit.",
    },
]
