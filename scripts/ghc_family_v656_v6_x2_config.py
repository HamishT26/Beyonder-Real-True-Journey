#!/usr/bin/env python3
"""Immutable x2 lifecycle configuration for Elaren v656-v6."""

from __future__ import annotations


SOURCE_COMMIT = "8a4bb8e8b6a649040c531e8d3dd36925fd0da301"
X1_COMMIT = "9c0227286b93672a4d98dba305e1c627a2300279"
PHASE_ROOT = "docs/elaren-kestrel/v656-v6"
SOURCE_EFFECTIVE_NEGATIVES = 14549
X1_OPERATIONAL_NEGATIVES = 16
SOURCE_OPEN_GAPS = 101
SOURCE_EXACT_GATES = 100
SOURCE_METHODS = 835
X1_METHODS = 16
MUTATIONS_PER_PROPOSAL = 5
EXPECTED_PROPOSALS = 30
EXPECTED_MUTATIONS = EXPECTED_PROPOSALS * MUTATIONS_PER_PROPOSAL
EXPECTED_DISTRIBUTION = {
    "completed": 23,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}
X2_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6566-X2-N17",
        "slug": "combined-state-inventory-probe-timeout",
        "failure_signature": "A combined Git status, skill inventory, and runner inventory probe exceeded its thirty-second bound without yielding a trustworthy aggregate result.",
        "candidate_workaround": "Split the request into one scalar Git head probe and one literal-path inventory probe.",
        "recurrence_guard": "Do not combine broad Git worktree state with recursive or wildcard inventories in one cold Windows command.",
        "fail_procedure": "Request head, full short status, skill directories, and wetland runner files in one bounded shell process.",
        "fail_observed": "The wrapper timed out after thirty seconds and returned no usable aggregate output.",
        "pass_procedure": "Resolve the exact head separately, then enumerate the two literal directories without a Git status traversal.",
        "pass_observed": "The scalar head matched the frozen x1 commit and the literal inventories returned ten skill directories and ten runner modules.",
        "scope_boundary": "Bounded local state-discovery recovery only.",
    },
    {
        "negative_id": "V6566-X2-N18",
        "slug": "windows-console-unicode-encoding-failure",
        "failure_signature": "The first runner wrote its receipt but raised UnicodeEncodeError when the cp1252 console could not emit a macron-bearing character.",
        "candidate_workaround": "Set PYTHONUTF8=1 before process launch and rerun the unchanged runner inputs.",
        "recurrence_guard": "Pin UTF-8 before launching any Windows process that may emit te reo Māori or other non-ASCII text.",
        "fail_procedure": "Invoke the first family-current wetland runner under the inherited cp1252 console.",
        "fail_observed": "The process received zero invocation credit because console emission failed after receipt creation.",
        "pass_procedure": "Set PYTHONUTF8=1 in the child environment and invoke the complete unchanged ten-runner set.",
        "pass_observed": "All ten runners exited successfully, covering thirty valid fixtures and rejecting all one hundred fifty mutations.",
        "scope_boundary": "Console encoding and unchanged text only; no cultural authority or content approval is conferred.",
    },
    {
        "negative_id": "V6566-X2-N19",
        "slug": "windows-rg-literal-wildcard-scope-fault",
        "failure_signature": "A follow-up ripgrep command passed a Windows wildcard as a literal path and produced an oversized result before returning a path-syntax error.",
        "candidate_workaround": "Use narrow roots and ripgrep -g include/exclude filters rather than a wildcard path argument.",
        "recurrence_guard": "On Windows, pass wildcards to ripgrep through -g and keep large generated ledgers explicitly excluded.",
        "fail_procedure": "Search a literal scripts wildcard together with the complete generated phase tree.",
        "fail_observed": "The command returned nonzero because the wildcard path was invalid after emitting excessive output.",
        "pass_procedure": "Search only scripts, tests, and bounded phase paths with explicit -g filters and large ledgers excluded.",
        "pass_observed": "The scoped search returned the intended cardinality references with no path-syntax fault.",
        "scope_boundary": "Bounded repository text-discovery recovery only.",
    },
    {
        "negative_id": "V6566-X2-N20",
        "slug": "advanced-tree-historical-x1-assertion",
        "failure_signature": "The first combined x1 and x2 test run passed fifty tests but a frozen x1-only test inspected the advanced working tree and rejected legitimate x2 artifacts.",
        "candidate_workaround": "Evaluate the historical no-x2 invariant against the immutable x1 Git tree and exclude only the context-invalid working-tree assertion from the advanced-tree selection.",
        "recurrence_guard": "Bind historical lifecycle invariants to their exact commit object; use the current tree only for current lifecycle assertions.",
        "fail_procedure": "Run the frozen x1 no-x2 working-tree assertion after materializing the x2 evidence packet.",
        "fail_observed": "The aggregate received zero credit because one of fifty-one tests failed after detecting the intended x2 files.",
        "pass_procedure": "Inspect the exact frozen x1 Git tree for prohibited lifecycle paths, then run the remaining frozen x1 tests with the complete current x2 module.",
        "pass_observed": "The immutable x1 tree contained no x2 or outcome artifacts and the bounded advanced-tree selection passed.",
        "scope_boundary": "Historical x1 contract recovery only; no x2 evidence is backdated into x1.",
    },
    {
        "negative_id": "V6566-X2-N21",
        "slug": "combined-tracked-untracked-inventory-timeout",
        "failure_signature": "A combined tracked-diff and untracked-file inventory exceeded its thirty-second bound without yielding a trustworthy result.",
        "candidate_workaround": "Run index-backed tracked and untracked probes as separate bounded commands before staging.",
        "recurrence_guard": "Keep tracked and untracked large-worktree inventories in separate processes and never infer cleanliness from a timed-out wrapper.",
        "fail_procedure": "Run git diff --name-only and git ls-files --others in one bounded PowerShell command.",
        "fail_observed": "The combined process timed out and received zero clean-state credit.",
        "pass_procedure": "Run git diff-files --name-only and git ls-files --others --exclude-standard as separate scalar probes.",
        "pass_observed": "Both bounded inventories completed and exposed only the intended Elaren x2 candidate paths.",
        "scope_boundary": "Bounded local change-inventory recovery only.",
    },
]
