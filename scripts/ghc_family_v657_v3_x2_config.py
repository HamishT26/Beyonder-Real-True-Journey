#!/usr/bin/env python3
"""Immutable x2 lifecycle configuration for Auren Lark v657-v3."""

from __future__ import annotations


SOURCE_COMMIT = "67a5eaa17b2399d52bac5ba45d390d8659cc61cd"
X1_COMMIT = "b40c2f04cd7e51ed9bc5c1174255e9e3d06af4e1"
PHASE_ROOT = "docs/auren-lark/v657-v3"
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 15434
SOURCE_EFFECTIVE_NEGATIVES = 15436
X1_OPERATIONAL_NEGATIVES = 12
SOURCE_OPEN_GAPS = 106
SOURCE_EXACT_GATES = 105
SOURCE_METHODS = 1718
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


# Append only phase-local x2 operational failures actually observed before the
# immutable evidence commit. Inherited and x1 failures remain retained evidence,
# not new x2 credit.
X2_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6573-X2-N21",
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
            "Enumerate v657-v3 paths with rg --files, filter the exact list, and pass "
            "that bounded set to the inspection step."
        ),
        "pass_observed": (
            "The enumerated v657-v3 scaffold inventory completed and exposed the exact "
            "source, count, domain, and route fields requiring adaptation."
        ),
        "scope_boundary": "Owner-local read-only x2 scaffold inventory recovery only.",
    },
    {
        "negative_id": "V6573-X2-N22",
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
            "Ten premature Auren-only untracked files existed with predecessor anchors "
            "and had no evidence or lifecycle credit."
        ),
        "pass_procedure": (
            "Delete only those ten untracked Auren copies, retain all committed and "
            "sibling files untouched, and keep only evidence-layer scaffolds."
        ),
        "pass_observed": (
            "The evidence candidate contains no closeout or final scaffold; those layers "
            "remain deferred until their exact anchors exist."
        ),
        "scope_boundary": "Owner-local untracked lifecycle-order recovery only.",
    },
    {
        "negative_id": "V6573-X2-N23",
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
            "The runtime now uses typewriter-domain fixture fields and exact UTF-8 authority "
            "prose while preserving unrelated validation logic."
        ),
        "scope_boundary": "Owner-local runtime scaffold adaptation recovery only.",
    },
    {
        "negative_id": "V6573-X2-N24",
        "slug": "runtime-fixture-key-loop-not-renamed",
        "failure_signature": (
            "The first x2 build stopped on the first valid fixture because the schema "
            "used typewriter-domain keys while a separate fail-closed boolean loop still "
            "indexed the predecessor software-domain keys."
        ),
        "candidate_workaround": (
            "Align the boolean-key loop with the already frozen typewriter-domain fixture "
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
            "Replace all three stale loop keys with their typewriter-domain counterparts and "
            "run the same thirty-surface builder."
        ),
        "pass_observed": (
            "All valid fixtures completed the aligned fail-closed key checks before "
            "surface evidence was written."
        ),
        "scope_boundary": "Owner-local synthetic runtime schema recovery only.",
    },
    {
        "negative_id": "V6573-X2-N25",
        "slug": "evidence-detailed-receipt-filename-mismatch",
        "failure_signature": (
            "The first detailed validator receipt used evidence-detailed-validation.json "
            "while the lifecycle manifest declared evidence-validation.json as the "
            "post-manifest validation receipt."
        ),
        "candidate_workaround": (
            "Remove only the uncommitted misnamed Auren receipt, write the same detailed "
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


# Append only failures actually observed before the immutable evidence commit.
X2_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6573-X2-N13",
        "slug": "runtime-unicode-context-patch-mismatch",
        "failure_signature": (
            "The first runtime adaptation combined ASCII fixture-key changes with a "
            "terminal-rendered Māori boundary line and the patch was rejected unchanged."
        ),
        "candidate_workaround": (
            "Apply fixture-key and mutation hunks at ASCII-only anchors, then patch the "
            "plain ASCII boundary segment separately."
        ),
        "recurrence_guard": (
            "Do not combine structural schema changes with terminal-rendered Unicode "
            "context in one patch."
        ),
        "fail_procedure": "Patch runtime fixture keys and the complete Unicode boundary together.",
        "fail_observed": "Patch verification failed before mutation and earned zero evidence credit.",
        "pass_procedure": "Patch structural keys first, then replace the ASCII-only boundary prefix.",
        "pass_observed": "All runtime fixture keys and the typewriter object boundary are aligned.",
        "scope_boundary": "Owner-local synthetic runtime adaptation only.",
    },
    {
        "negative_id": "V6573-X2-N14",
        "slug": "skill-init-javascript-template-interpolation-fault",
        "failure_signature": (
            "The first skill-initialization orchestration embedded a Python dollar-brace "
            "expression inside a JavaScript template and failed with ReferenceError before dispatch."
        ),
        "candidate_workaround": (
            "Construct the skill default prompt in Python with chr(36) and concatenation, "
            "leaving no dollar-brace sequence for JavaScript to interpolate."
        ),
        "recurrence_guard": (
            "Keep nested-language interpolation markers out of JavaScript template literals."
        ),
        "fail_procedure": "Compose a nested Python f-string containing a JavaScript-visible interpolation marker.",
        "fail_observed": "JavaScript parsing reached an undefined name and no skill directory was created.",
        "pass_procedure": "Build the dollar-prefixed skill name with chr(36) inside Python and rerun the same ten initializations.",
        "pass_observed": "All ten phase-local skill directories initialized inside the Auren packet.",
        "scope_boundary": "Owner-local phase-skill initialization only; no global installation.",
    },
    {
        "negative_id": "V6573-X2-N15",
        "slug": "skill-validator-default-cp1252-batch-failure",
        "failure_signature": (
            "The first skill-creator quick-validation batch used Python's Windows CP1252 "
            "default; all ten UTF-8 SKILL.md reads raised UnicodeDecodeError."
        ),
        "candidate_workaround": (
            "Run the unchanged validator with Python UTF-8 mode enabled."
        ),
        "recurrence_guard": (
            "Use Python -X utf8 for validators that call Path.read_text without an explicit encoding."
        ),
        "fail_procedure": "Validate all ten UTF-8 phase-local skills under the platform default text encoding.",
        "fail_observed": "Ten of ten validator processes failed before metadata checks; no skill content changed.",
        "pass_procedure": "Run each same validator command with -X utf8.",
        "pass_observed": "All ten skills returned Skill is valid.",
        "scope_boundary": "Owner-local skill metadata validation only.",
    },
    {
        "negative_id": "V6573-X2-N16",
        "slug": "readiness-refresh-timeout-before-write",
        "failure_signature": (
            "The post-skill readiness refresh exceeded its command bound while checking "
            "frozen x1 paths and returned no completed refresh receipt."
        ),
        "candidate_workaround": (
            "Audit Python and Git processes, locks, HEAD, tracked status, and readiness "
            "timestamps; then split index and working-tree x1 comparisons before one retry."
        ),
        "recurrence_guard": (
            "Compare the frozen x1 index and working tree in separate bounded Git calls "
            "instead of one combined commit-to-working-tree diff."
        ),
        "fail_procedure": "Refresh all evidence records using one combined x1 commit-to-working-tree diff.",
        "fail_observed": (
            "The command timed out; no Python process or lock remained, short-lived Git "
            "children quiesced, HEAD stayed at x1, tracked status stayed clean, and the "
            "readiness file retained its pre-refresh timestamp and zero receipt counts."
        ),
        "pass_procedure": (
            "Use separate cached-index and working-tree comparisons for the exact frozen "
            "path list, then rerun the same readiness refresh once."
        ),
        "pass_observed": (
            "All 42 frozen x1 paths passed separate cached-index and working-tree "
            "comparisons in a bounded read-only check."
        ),
        "scope_boundary": "Owner-local x1 immutability and evidence-readiness refresh only.",
    },
]
