#!/usr/bin/env python3
"""Immutable x2 lifecycle configuration for Sable Rook v657-v4."""

from __future__ import annotations


SOURCE_COMMIT = "e282db933e535759cc1f58975126d2bb0e1cf5fd"
X1_COMMIT = "d05c484a3324bab2f893d35ff4d10d7f0269c9e9"
PHASE_ROOT = "docs/sable-rook/v657-v4"
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 15608
SOURCE_EFFECTIVE_NEGATIVES = 15610
X1_OPERATIONAL_NEGATIVES = 15
SOURCE_OPEN_GAPS = 107
SOURCE_EXACT_GATES = 106
SOURCE_METHODS = 1890
X1_METHODS = 15
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
        "negative_id": "V6574-X2-N01",
        "slug": "x1-commit-wrapper-silent-success",
        "failure_signature": (
            "The x1 commit invocation completed without attributable stdout, so the wrapper "
            "alone could not establish that the commit existed or that the lane was clean."
        ),
        "candidate_workaround": (
            "Read the exact new HEAD, commit subject, and porcelain status separately before "
            "pushing or beginning x2."
        ),
        "recurrence_guard": (
            "Treat an empty mutating-wrapper response as zero evidence until exact durable Git "
            "state is reread."
        ),
        "fail_procedure": "Infer x1 commit success only from wrapper completion.",
        "fail_observed": (
            "The wrapper emitted no attributable commit result and earned zero commit-proof credit."
        ),
        "pass_procedure": (
            "Read HEAD, the exact commit subject, and clean status; then push and prove four-way equality."
        ),
        "pass_observed": (
            "HEAD d05c484a3324bab2f893d35ff4d10d7f0269c9e9 carried the frozen x1 subject, "
            "the lane was clean, and local, upstream, tracking, and fresh-live remote were equal."
        ),
        "scope_boundary": "Owner-local x1 durable-state verification only.",
    },
    {
        "negative_id": "V6574-X2-N02",
        "slug": "skill-quick-validator-unsupported-help-assumption",
        "failure_signature": (
            "The first quick-validator discovery call supplied --help, but the installed "
            "single-positional script treated it as a skill directory and returned SKILL.md not found."
        ),
        "candidate_workaround": (
            "Read the bounded validator entrypoint, then invoke it once per exact phase-local skill directory under Python UTF-8 mode."
        ),
        "recurrence_guard": (
            "Inspect a small local script's argument contract before assuming argparse-style help support."
        ),
        "fail_procedure": "Invoke quick_validate.py --help and infer a conventional help interface.",
        "fail_observed": (
            "The script returned SKILL.md not found, validated no skill, changed no state, and earned zero validation credit."
        ),
        "pass_procedure": (
            "Read the entrypoint and run python -X utf8 quick_validate.py against each of the ten exact skill directories."
        ),
        "pass_observed": (
            "All ten phase-local skills returned Skill is valid, and all ten separate smoke uses passed."
        ),
        "scope_boundary": "Owner-local phase-skill metadata validation recovery only.",
    },
    {
        "negative_id": "V6574-X2-N03",
        "slug": "advanced-tree-x1-absence-assertion",
        "failure_signature": (
            "The first combined x1 and x2 development run passed 51 tests but failed the "
            "x1 lifecycle-local assertion that the current advanced working tree contain no x2 artifacts."
        ),
        "candidate_workaround": (
            "Exclude only that exact current-tree absence assertion after x2, run every other x1 "
            "and x2 test unchanged, and separately verify the immutable x1 commit tree contains no x2 artifacts."
        ),
        "recurrence_guard": (
            "Bind lifecycle-local absence assertions to their immutable commit tree rather than an advanced successor working tree."
        ),
        "fail_procedure": "Run all eleven x1 tests against the advanced x2 working tree together with all x2 tests.",
        "fail_observed": (
            "Fifty-one tests passed and one x1 current-tree absence test failed; the aggregate earned zero pass credit."
        ),
        "pass_procedure": (
            "Run the ten context-valid x1 tests plus all forty-one x2 tests, while the x2 immutable-tree test inspects x1 directly."
        ),
        "pass_observed": (
            "The exact lifecycle exclusion is named, the immutable x1 tree remains x2-free, and no substantive x1 or x2 assertion is weakened."
        ),
        "scope_boundary": "Owner-local lifecycle-scoped test selection recovery only.",
    },
    {
        "negative_id": "V6574-X2-N04",
        "slug": "expired-staged-review-process-handle",
        "failure_signature": (
            "After context compaction, the first poll targeted the former staged-review process "
            "identifier and returned unknown process rather than new review evidence."
        ),
        "candidate_workaround": (
            "Inspect the durable staged-review receipt before deciding whether any review rerun is justified."
        ),
        "recurrence_guard": (
            "Treat an unavailable transient process handle as zero evidence and audit durable outputs first."
        ),
        "fail_procedure": "Poll the pre-compaction process handle for the staged evidence review.",
        "fail_observed": (
            "The process handle was unavailable; the poll changed no repository state and earned zero review credit."
        ),
        "pass_procedure": (
            "Read and adjudicate the durable evidence-staged-review receipt without rerunning the review."
        ),
        "pass_observed": (
            "The durable receipt was valid for 167 staged paths, 204 manifest entries, zero mismatches, "
            "zero scope or frozen-x1 violations, zero confirmed privacy hits, and clean diff hygiene."
        ),
        "scope_boundary": "Owner-local durable receipt recovery only.",
    },
    {
        "negative_id": "V6574-X2-N05",
        "slug": "combined-status-wrapper-empty-output",
        "failure_signature": (
            "A broad combined post-review Git and JSON status wrapper returned no attributable output."
        ),
        "candidate_workaround": (
            "Split the audit into narrow receipt, staged-state, and exact Git probes with bounded output."
        ),
        "recurrence_guard": (
            "Do not aggregate large status surfaces when independent scalar probes preserve better evidence."
        ),
        "fail_procedure": "Combine branch, status, staged names, and JSON review fields in one wrapper.",
        "fail_observed": (
            "The wrapper produced no durable claim evidence and changed no repository state."
        ),
        "pass_procedure": (
            "Read the review fields and Git state through separate bounded literal-path probes."
        ),
        "pass_observed": (
            "The narrow receipt probe established a valid review; separate Git probes remained available for exact state proof."
        ),
        "scope_boundary": "Owner-local inspection-wrapper recovery only.",
    },
    {
        "negative_id": "V6574-X2-N06",
        "slug": "overbroad-method-flow-search-output-truncation",
        "failure_signature": (
            "A recursive method and negative search included generated witness JSON and exceeded the output budget."
        ),
        "candidate_workaround": (
            "Restrict source inspection to the exact configuration and builder files needed for a patch."
        ),
        "recurrence_guard": (
            "Exclude generated high-cardinality Method Flow ledgers from source-code searches."
        ),
        "fail_procedure": "Search source and generated Method Flow JSON together for negative fields.",
        "fail_observed": (
            "The result was truncated, earned zero completeness credit, and changed no repository state."
        ),
        "pass_procedure": (
            "Read the exact x2 configuration source directly and patch the bounded operational ledger."
        ),
        "pass_observed": (
            "The source-only read exposed the complete three-entry ledger and supported an additive retained-failure update."
        ),
        "scope_boundary": "Owner-local source-inspection recovery only.",
    },
    {
        "negative_id": "V6574-X2-N07",
        "slug": "asynchronous-receipt-build-output-not-returned",
        "failure_signature": (
            "The evidence-receipt builder exceeded the initial yield, then completed without returning its promised summary payload."
        ),
        "candidate_workaround": (
            "Read the exact durable receipt artifacts and validate them instead of inferring success from the wrapper."
        ),
        "recurrence_guard": (
            "An asynchronous completion with no attributable payload earns zero receipt-proof credit until durable files are checked."
        ),
        "fail_procedure": "Treat the completed asynchronous wrapper as sufficient receipt evidence.",
        "fail_observed": (
            "No summary payload was returned; the invocation alone earned zero receipt-build credit."
        ),
        "pass_procedure": (
            "Read the generated manifest and then run the exact staged review against the rebuilt artifacts."
        ),
        "pass_observed": (
            "The durable manifest contained 204 entries, and the subsequent exact review was reserved as the acceptance witness."
        ),
        "scope_boundary": "Owner-local durable receipt verification only.",
    },
    {
        "negative_id": "V6574-X2-N08",
        "slug": "line-ending-warning-volume-truncated-stage-summary",
        "failure_signature": (
            "The first exact-scope Git add emitted enough line-ending warnings to truncate the bounded result summary."
        ),
        "candidate_workaround": (
            "Reread staged and unstaged counts independently, then suppress repetitive warning text on later exact-scope refreshes while preserving exit status."
        ),
        "recurrence_guard": (
            "Keep exact staging pathsets but separate warning-volume control from durable staged-state proof."
        ),
        "fail_procedure": "Infer exact staged state from a warning-truncated add wrapper.",
        "fail_observed": (
            "The path operation ran, but the intended count summary was truncated and earned zero exact-state credit."
        ),
        "pass_procedure": (
            "Refresh the same bounded pathset, check the native exit code, and read staged and unstaged counts separately."
        ),
        "pass_observed": (
            "The exact-scope staged surface remained recoverable without broadening the candidate or changing frozen x1 content."
        ),
        "scope_boundary": "Owner-local Git-index inspection recovery only.",
    },
]
