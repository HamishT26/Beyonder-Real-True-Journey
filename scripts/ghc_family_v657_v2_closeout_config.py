#!/usr/bin/env python3
"""Closeout lifecycle constants for Ilyra Fen v657-v2."""

from __future__ import annotations


SOURCE_COMMIT = "4d888c1387c4203bd21acd7156bed2b0a13f2bee"
X1_COMMIT = "3f79c72723f927c03045091266431b9adf11dff3"
EVIDENCE_COMMIT = "ceb6316d97551f376d853eb27e0590ae9efae9bd"
EVIDENCE_EFFECTIVE_NEGATIVES = 15423
EVIDENCE_EFFECTIVE_METHODS = 1707
EVIDENCE_OPEN_GAPS = 106
EVIDENCE_EXACT_GATES = 105

# Append only failures discovered after the immutable evidence commit and
# before the closeout/content-seal commit.
CLOSEOUT_DISCOVERED_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6572-CLOSEOUT-N26",
        "slug": "powershell-unquoted-upstream-revision-parser-fault",
        "failure_signature": (
            "A read-only four-way equality wrapper passed @{upstream} unquoted to "
            "Windows PowerShell, which parsed it as an incomplete hash literal."
        ),
        "candidate_workaround": (
            "Run upstream, tracking, live-remote, divergence, and status checks as "
            "separate scalar probes and quote revision selectors literally."
        ),
        "recurrence_guard": (
            "Always spell the PowerShell argument as '@{upstream}' and quote any "
            "revision expression containing the selector."
        ),
        "fail_procedure": (
            "Invoke git rev-parse @{upstream} inside one PowerShell-backed wrapper."
        ),
        "fail_observed": (
            "PowerShell stopped at parse time before Git ran; no repository state "
            "changed and the command received zero evidence credit."
        ),
        "pass_procedure": (
            "Repeat only the read-only scalar gates with '@{upstream}' and "
            "'HEAD...@{upstream}' quoted."
        ),
        "pass_observed": (
            "Local, upstream, tracking, and fresh live remote all resolved to the "
            "immutable evidence head, divergence was 0/0, and the lane stayed clean."
        ),
        "scope_boundary": "Owner-local read-only evidence-head equality recovery only.",
    },
    {
        "negative_id": "V6572-CLOSEOUT-N27",
        "slug": "inherited-closeout-docstring-context-mismatch",
        "failure_signature": (
            "The first additive config patch expected the mechanically copied "
            "docstring to say Ilyra Fen, while the exact inherited text still said "
            "Lyren without a surname."
        ),
        "candidate_workaround": (
            "Read the exact copied file header, then replace the compact config "
            "through a complete apply-patch edit against observed text."
        ),
        "recurrence_guard": (
            "Inspect the exact copied header after bulk token replacement before "
            "constructing semantic patch context."
        ),
        "fail_procedure": (
            "Apply a semantic patch whose first context line assumes the owner token "
            "had already changed from Lyren to Ilyra Fen."
        ),
        "fail_observed": (
            "Patch verification rejected the context before any file changed, so the "
            "attempt earned zero completion credit."
        ),
        "pass_procedure": (
            "Re-read the exact UTF-8 header and replace the config with the verified "
            "Ilyra anchors, counts, and retained closeout witnesses."
        ),
        "pass_observed": (
            "The corrected config names Ilyra Fen, binds the immutable source, x1, "
            "and evidence commits, and preserves both closeout failures."
        ),
        "scope_boundary": "Owner-local closeout-config editing recovery only.",
    },
    {
        "negative_id": "V6572-CLOSEOUT-N28",
        "slug": "broad-closeout-source-slice-timeout",
        "failure_signature": (
            "One PowerShell command requested two large closeout source slices and "
            "exceeded 30 seconds without returning usable output."
        ),
        "candidate_workaround": (
            "Read only named symbols through one bounded direct runtime probe with a "
            "ceiling sized for the observed Windows transport latency."
        ),
        "recurrence_guard": (
            "Do not request multiple large inherited source slices in one short "
            "PowerShell wrapper on this owner lane."
        ),
        "fail_procedure": (
            "Read two broad sections of the copied closeout builder in one command."
        ),
        "fail_observed": (
            "The wrapper timed out before yielding reviewable text and earned zero "
            "inspection credit."
        ),
        "pass_procedure": (
            "Use one direct Node UTF-8 read and emit only lines around declared "
            "lifecycle symbols under a 120-second ceiling."
        ),
        "pass_observed": (
            "The bounded direct read returned the activation, route, checklist, and "
            "builder sections without modifying the repository."
        ),
        "scope_boundary": "Owner-local read-only closeout-source inspection only.",
    },
    {
        "negative_id": "V6572-CLOSEOUT-N29",
        "slug": "short-rg-context-inspection-timeout",
        "failure_signature": (
            "A symbol-scoped ripgrep context read still exceeded the same 30-second "
            "transport ceiling without usable output."
        ),
        "candidate_workaround": (
            "Avoid a second search process and read the already known file directly "
            "with a single runtime process."
        ),
        "recurrence_guard": (
            "After one context-search timeout, change the command surface rather than "
            "replaying another short search wrapper."
        ),
        "fail_procedure": (
            "Search the copied closeout builder for lifecycle symbols with context."
        ),
        "fail_observed": (
            "The search returned no reviewable result before timeout and earned zero "
            "evidence credit."
        ),
        "pass_procedure": (
            "Read the exact UTF-8 file once in Node and select the known lifecycle "
            "symbols in memory."
        ),
        "pass_observed": (
            "The direct read exposed every required semantic replacement surface."
        ),
        "scope_boundary": "Owner-local read-only symbol discovery recovery only.",
    },
    {
        "negative_id": "V6572-CLOSEOUT-N30",
        "slug": "direct-node-read-short-ceiling-timeout",
        "failure_signature": (
            "The first direct Node symbol read also exceeded a 30-second shell ceiling "
            "despite requiring no repository traversal."
        ),
        "candidate_workaround": (
            "Keep the direct read unchanged, raise only the bounded transport ceiling "
            "to 120 seconds, and do not add work."
        ),
        "recurrence_guard": (
            "Use the measured command-startup latency when sizing owner-local Windows "
            "read-only probes; never mistake wrapper latency for repository damage."
        ),
        "fail_procedure": (
            "Run the direct Node UTF-8 symbol read with a 30-second outer timeout."
        ),
        "fail_observed": (
            "The outer wrapper timed out without output and earned zero inspection "
            "credit."
        ),
        "pass_procedure": (
            "Run the same bounded direct read once with a 120-second ceiling."
        ),
        "pass_observed": (
            "The command completed in 29 seconds and returned the exact lifecycle "
            "sections needed for semantic editing."
        ),
        "scope_boundary": "Owner-local read-only command-ceiling recovery only.",
    },
    {
        "negative_id": "V6572-CLOSEOUT-N31",
        "slug": "short-owner-token-semantic-patch-mismatch",
        "failure_signature": (
            "A combined semantic patch assumed mechanical replacement had changed "
            "the inherited short owner token Lyren, but only the full name token had "
            "been replaced."
        ),
        "candidate_workaround": (
            "Patch the observed short-token text in small independently reviewable "
            "hunks before changing anchors, domain truth, and route records."
        ),
        "recurrence_guard": (
            "After mechanical token rewriting, enumerate both full-name and short-name "
            "forms before composing a semantic patch."
        ),
        "fail_procedure": (
            "Apply one multi-section patch whose anchor block expects Ilyra Fen where "
            "the copied source still says Lyren."
        ),
        "fail_observed": (
            "Patch verification rejected the entire operation before any file changed; "
            "the attempt earned zero completion credit."
        ),
        "pass_procedure": (
            "Apply exact-text patches separately for the header, anchor block, bounded "
            "truth, successor boundary, and held route."
        ),
        "pass_observed": (
            "Every semantic section now reflects Ilyra v657-v2 and the unresolved "
            "terminal-route contract without mutating evidence files."
        ),
        "scope_boundary": "Owner-local closeout-builder editing recovery only.",
    },
    {
        "negative_id": "V6572-CLOSEOUT-N32",
        "slug": "closeout-receipt-mode-omission",
        "failure_signature": (
            "The closeout receipt utility was invoked without its required build or "
            "review mode and argparse rejected the command before work began."
        ),
        "candidate_workaround": (
            "Invoke the declared build mode first, validate the generated surfaces, "
            "then invoke review explicitly."
        ),
        "recurrence_guard": (
            "Read the receipt CLI usage contract and always pass one exact lifecycle "
            "mode; never rely on an implicit default."
        ),
        "fail_procedure": (
            "Run build_ghc_family_v657_v2_closeout_receipts.py with no positional mode."
        ),
        "fail_observed": (
            "Argparse returned exit code 2, no receipt step ran, and the attempt "
            "received zero lifecycle credit."
        ),
        "pass_procedure": (
            "Refresh count-dependent closeout artifacts, then run the receipt utility "
            "with build and review as separate bounded commands."
        ),
        "pass_observed": (
            "The explicit lifecycle modes produce and verify the closeout receipts "
            "without concealing the omitted-mode failure."
        ),
        "scope_boundary": "Owner-local closeout receipt CLI recovery only.",
    },
    {
        "negative_id": "V6572-CLOSEOUT-N33",
        "slug": "unstaged-closeout-index-review",
        "failure_signature": (
            "The closeout receipt review attempted to resolve manifest paths from the "
            "Git index before the exact closeout candidate had been staged."
        ),
        "candidate_workaround": (
            "Refresh count-dependent artifacts, build receipts, stage only the exact "
            "closeout allowlist, then run the unchanged index review."
        ),
        "recurrence_guard": (
            "For index-domain staged review, require an explicit exact staging step "
            "between receipt build and receipt review."
        ),
        "fail_procedure": (
            "Run closeout receipt review immediately after build while all closeout "
            "paths remain untracked."
        ),
        "fail_observed": (
            "git rev-parse could not resolve the first closeout path from the index; "
            "review stopped with zero pass credit."
        ),
        "pass_procedure": (
            "Stage the bounded closeout scripts, test, and generated owner paths, then "
            "run the same review against index blobs."
        ),
        "pass_observed": (
            "The corrected review validates exact staged coverage, manifests, privacy, "
            "x1 immutability, and diff hygiene."
        ),
        "scope_boundary": "Owner-local closeout index-order recovery only.",
    },
    {
        "negative_id": "V6572-CLOSEOUT-N34",
        "slug": "historical-x1-absence-assertion-on-advanced-tree",
        "failure_signature": (
            "The combined closeout test selection ran the frozen x1 absence assertion "
            "against an advanced x2 and closeout worktree, where later artifacts "
            "truthfully exist."
        ),
        "candidate_workaround": (
            "Declare that one exact historical-state test ineligible on the descendant "
            "tree, validate its invariant against the immutable x1 commit, and run all "
            "other current-tree tests unchanged."
        ),
        "recurrence_guard": (
            "Bind lifecycle absence assertions to their immutable Git tree and never "
            "apply them to a later descendant worktree."
        ),
        "fail_procedure": (
            "Run x1, x2, and closeout unittest modules together in the advanced "
            "closeout worktree without lifecycle eligibility filtering."
        ),
        "fail_observed": (
            "Sixty tests passed and the one x1-only absence assertion failed; the "
            "61-test command received zero aggregate-pass credit."
        ),
        "pass_procedure": (
            "Verify x1 absence with Git-tree queries at the x1 commit, then run the "
            "60 eligible current-tree tests with the exact exclusion declared."
        ),
        "pass_observed": (
            "The immutable x1 tree contains no x2 or closeout paths, and every eligible "
            "current-tree test passes without broadening the exclusion set."
        ),
        "scope_boundary": "Owner-local lifecycle-test eligibility recovery only.",
    },
]
