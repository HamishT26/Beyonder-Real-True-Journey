#!/usr/bin/env python3
"""Immutable x2 lifecycle configuration for Ilyra Fen v657-v2."""

from __future__ import annotations


SOURCE_COMMIT = "4d888c1387c4203bd21acd7156bed2b0a13f2bee"
X1_COMMIT = "3f79c72723f927c03045091266431b9adf11dff3"
PHASE_ROOT = "docs/ilyra-fen/v657-v2"
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 15248
SOURCE_EFFECTIVE_NEGATIVES = 15248
X1_OPERATIONAL_NEGATIVES = 20
SOURCE_OPEN_GAPS = 105
SOURCE_EXACT_GATES = 104
SOURCE_METHODS = 1532
X1_METHODS = 20
MUTATIONS_PER_PROPOSAL = 5
EXPECTED_PROPOSALS = 30
EXPECTED_MUTATIONS = EXPECTED_PROPOSALS * MUTATIONS_PER_PROPOSAL
EXPECTED_DISTRIBUTION = {
    "completed": 23,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}


# Append only phase-local x2 operational failures actually observed before the
# immutable evidence commit. Inherited and x1 failures remain retained evidence,
# not new x2 credit.
X2_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6572-X2-N21",
        "slug": "windows-ripgrep-wildcard-literal-recurrence",
        "failure_signature": (
            "The first x2 scaffold inventory passed Windows wildcard filenames as "
            "positional ripgrep paths, which returned invalid-path syntax after only "
            "the exact config preview."
        ),
        "candidate_workaround": (
            "Use ripgrep glob options or enumerate exact repository paths before one "
            "bounded multi-file search."
        ),
        "recurrence_guard": (
            "Never pass an unexpanded Windows wildcard as a positional filename to "
            "ripgrep; bind -g patterns or exact paths."
        ),
        "fail_procedure": (
            "Search mechanically copied x2 scripts and tests using positional star "
            "patterns in PowerShell."
        ),
        "fail_observed": (
            "Ripgrep returned operating-system error 123 for each wildcard path and "
            "the inventory earned zero complete-set credit."
        ),
        "pass_procedure": (
            "Enumerate v657-v2 paths with rg --files, filter the exact list, and pass "
            "that bounded set to the inspection step."
        ),
        "pass_observed": (
            "The enumerated v657-v2 scaffold inventory completed and exposed the exact "
            "source, count, domain, and route fields requiring adaptation."
        ),
        "scope_boundary": "Owner-local read-only x2 scaffold inventory recovery only.",
    },
    {
        "negative_id": "V6572-X2-N22",
        "slug": "premature-closeout-final-scaffold-materialization",
        "failure_signature": (
            "The first mechanical x2 scaffold copy also created untracked closeout and "
            "final files before their immutable evidence and closeout anchors existed."
        ),
        "candidate_workaround": (
            "Remove only the newly created untracked lifecycle copies and rematerialize "
            "each layer after its required predecessor commit is immutable."
        ),
        "recurrence_guard": (
            "Copy lifecycle scaffolds just in time: evidence surfaces after x1, closeout "
            "after evidence, and final surfaces after closeout."
        ),
        "fail_procedure": (
            "Mechanically copy all predecessor lifecycle files immediately after the x1 "
            "gate without first partitioning them by immutable-anchor dependency."
        ),
        "fail_observed": (
            "Ten premature Ilyra-only untracked files existed with predecessor anchors "
            "and had no evidence or lifecycle credit."
        ),
        "pass_procedure": (
            "Delete only those ten untracked Ilyra copies, retain all committed and "
            "sibling files untouched, and keep only evidence-layer scaffolds."
        ),
        "pass_observed": (
            "The evidence candidate contains no closeout or final scaffold; those layers "
            "remain deferred until their exact anchors exist."
        ),
        "scope_boundary": "Owner-local untracked lifecycle-order recovery only.",
    },
    {
        "negative_id": "V6572-X2-N23",
        "slug": "mixed-runtime-unicode-context-mismatch",
        "failure_signature": (
            "A mixed structural-field and human-readable runtime patch did not match "
            "the inherited UTF-8 boundary line and changed nothing."
        ),
        "candidate_workaround": (
            "Apply ASCII-safe fixture-field hunks first, inspect the exact UTF-8 line, "
            "then patch the boundary prose separately."
        ),
        "recurrence_guard": (
            "Do not combine structural fields with terminal-rendered Unicode context "
            "when adapting lifecycle scaffolds."
        ),
        "fail_procedure": (
            "Submit one patch containing fixture keys and a terminal-rendered Māori "
            "boundary line."
        ),
        "fail_observed": (
            "Patch verification rejected the mixed hunk before mutation and granted "
            "zero edit credit."
        ),
        "pass_procedure": (
            "Patch machine fields at ASCII anchors, inspect the UTF-8 source through "
            "Python, and apply a narrow exact-text hunk."
        ),
        "pass_observed": (
            "The runtime now uses lift-domain fixture fields and exact UTF-8 authority "
            "prose while preserving unrelated validation logic."
        ),
        "scope_boundary": "Owner-local runtime scaffold adaptation recovery only.",
    },
    {
        "negative_id": "V6572-X2-N24",
        "slug": "runtime-fixture-key-loop-not-renamed",
        "failure_signature": (
            "The first x2 build stopped on the first valid fixture because the schema "
            "used lift-domain keys while a separate fail-closed boolean loop still "
            "indexed the predecessor software-domain keys."
        ),
        "candidate_workaround": (
            "Align the boolean-key loop with the already frozen lift-domain fixture "
            "schema and rerun the unchanged all-surface build."
        ),
        "recurrence_guard": (
            "Search every schema key across constructors, required-key sets, validation "
            "loops, mutations, and tests after a domain rename."
        ),
        "fail_procedure": (
            "Compile and run the x2 builder after changing constructor and required-key "
            "sets but before checking the independent boolean-key loop."
        ),
        "fail_observed": (
            "Python raised KeyError on real_systems_or_artifacts_used before writing "
            "the first surface; the attempt earned zero evidence credit."
        ),
        "pass_procedure": (
            "Replace all three stale loop keys with their lift-domain counterparts and "
            "run the same thirty-surface builder."
        ),
        "pass_observed": (
            "All valid fixtures completed the aligned fail-closed key checks before "
            "surface evidence was written."
        ),
        "scope_boundary": "Owner-local synthetic runtime schema recovery only.",
    },
    {
        "negative_id": "V6572-X2-N25",
        "slug": "evidence-detailed-receipt-filename-mismatch",
        "failure_signature": (
            "The first detailed validator receipt used evidence-detailed-validation.json "
            "while the lifecycle manifest declared evidence-validation.json as the "
            "post-manifest validation receipt."
        ),
        "candidate_workaround": (
            "Remove only the uncommitted misnamed Ilyra receipt, write the same detailed "
            "result to the declared path, and refresh manifest and staged review."
        ),
        "recurrence_guard": (
            "Inspect the lifecycle exclusion contract before selecting validator output "
            "filenames."
        ),
        "fail_procedure": (
            "Invoke the detailed validator with an improvised evidence-detailed filename."
        ),
        "fail_observed": (
            "The validator itself passed, but its receipt did not occupy the declared "
            "lifecycle path and earned no exact receipt-name credit."
        ),
        "pass_procedure": (
            "Write the unchanged detailed validator result to evidence-validation.json, "
            "rebuild the content contract, and rerun exact staged review."
        ),
        "pass_observed": (
            "The declared evidence-validation receipt is present and the refreshed "
            "manifest and staged review cover the corrected candidate."
        ),
        "scope_boundary": "Owner-local evidence-receipt naming recovery only.",
    },
]
