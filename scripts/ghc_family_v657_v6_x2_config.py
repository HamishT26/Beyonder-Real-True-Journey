#!/usr/bin/env python3
"""Immutable x2 lifecycle configuration for Orin Thale v657-v6."""

from __future__ import annotations


SOURCE_COMMIT = "87815f96a372849dfb42a09d785515e858ea7925"
FIRST_X1_COMMIT = "40c25aeb884fadc96366847507ff79c53d4e95c5"
X1_COMMIT = "f7161b026d270a131cc8449e75a7562fe04f0f66"
PHASE_ROOT = "docs/orin-thale/v657-v6"
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 15966
SOURCE_EFFECTIVE_NEGATIVES = 15966
X1_OPERATIONAL_NEGATIVES = 16
SOURCE_OPEN_GAPS = 109
SOURCE_EXACT_GATES = 108
SOURCE_METHODS = 2242
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


X2_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6576-X2-N01",
        "slug": "guarded-commit-tree-wrapper-completion-unattributed",
        "failure_signature": (
            "The guarded write-tree, commit-tree, and update-ref wrapper returned without "
            "attributable output; the immediate audit still showed the first x1 commit, while "
            "the later post-interruption audit found the exact repair commit durable."
        ),
        "candidate_workaround": (
            "Do not launch a duplicate helper; audit exact HEAD, parent, changed paths, index, "
            "worktree, locks, and owner-started processes before any further mutation."
        ),
        "recurrence_guard": (
            "After any unattributed mutating wrapper, poll durable Git state before retrying, "
            "including across a user interruption."
        ),
        "fail_procedure": "Infer failure or retry the guarded commit path from missing wrapper output.",
        "fail_observed": "The wrapper produced no attributable completion and earned zero lifecycle credit.",
        "pass_procedure": "Reread the branch after interruption and verify the repair commit, parent, tree, exact delta, and clean state.",
        "pass_observed": (
            "The later audit found repair commit f7161b026d270a131cc8449e75a7562fe04f0f66 "
            "as the direct child of 40c25aeb884fadc96366847507ff79c53d4e95c5, with the "
            "reviewed sixteen-path x1-only delta, zero merges, 40/40 owner-manifest parity, "
            "and clean four-way-equal pushed state."
        ),
        "scope_boundary": "Owner-local x1 durable-state recovery only; no history rewrite or independent reproduction.",
    },
    {
        "negative_id": "V6576-X2-N02",
        "slug": "powershell-python-cp1252-skill-spec-diagnostic",
        "failure_signature": (
            "A read-only Python diagnostic computed the expected portfolio counts but failed "
            "while emitting a skill or runner specification containing Māori text through the "
            "default Windows CP1252 stream."
        ),
        "candidate_workaround": (
            "Pin PYTHONIOENCODING=utf-8 before Unicode-emitting diagnostics or emit an ASCII-safe "
            "summary when the exact Unicode payload is not needed."
        ),
        "recurrence_guard": "Set UTF-8 explicitly before repository diagnostics that may emit Māori text.",
        "fail_procedure": "Print the complete phase skill and runner specifications through the default PowerShell Python stream.",
        "fail_observed": "The counts printed, then UnicodeEncodeError stopped the remaining diagnostic; it earned zero completion credit.",
        "pass_procedure": "Repeat only the bounded read-only diagnostic with PYTHONIOENCODING=utf-8 and verify the declared counts.",
        "pass_observed": (
            "The UTF-8-pinned diagnostic completed and confirmed 30 proposals, 30 safe tasks, "
            "20 candidate tasks, 30 CLEAN tasks, 10 skill specifications, and 10 runner specifications."
        ),
        "scope_boundary": "Read-only encoding recovery only; no repository, route, sibling, or external state mutation.",
    },
    {
        "negative_id": "V6576-X2-N03",
        "slug": "powershell-array-injected-as-unquoted-python-modules",
        "failure_signature": (
            "A read-only unittest inventory embedded a PowerShell array into Python without "
            "JSON string quoting, so Python treated the first module prefix as an undefined name."
        ),
        "candidate_workaround": "Pass an explicit Python string list or serialize and parse valid JSON.",
        "recurrence_guard": "Never interpolate a PowerShell array directly into Python source.",
        "fail_procedure": "Inject the PowerShell module array directly into an inline Python assignment.",
        "fail_observed": "The inventory stopped with NameError before loading or running any test and earned zero validation credit.",
        "pass_procedure": "Load an explicit quoted module list and count test cases without executing them.",
        "pass_observed": (
            "The quoted inventory completed without executing tests and counted 11 current-x1, "
            "41 current-x2, 5 Caelen-successor, 8 Caelen-final, and 8 Sable-final cases."
        ),
        "scope_boundary": "Read-only test inventory recovery only; no test execution or repository mutation.",
    },
    {
        "negative_id": "V6576-X2-N04",
        "slug": "windows-ripgrep-literal-wildcard-operand",
        "failure_signature": (
            "A read-only ripgrep command passed scripts/*v657_v5*.py as a literal Windows path "
            "operand, which Windows rejected before content search."
        ),
        "candidate_workaround": "Enumerate paths with rg --files, filter the names, then pass exact literal paths.",
        "recurrence_guard": "Do not rely on POSIX wildcard expansion for Windows ripgrep path operands.",
        "fail_procedure": "Pass a wildcard-bearing Windows path directly as the ripgrep search operand.",
        "fail_observed": "Ripgrep reported Windows error 123 and the content search earned zero evidence credit.",
        "pass_procedure": "Filter rg --files output for exact v657_v5 validator paths and inspect those literal paths.",
        "pass_observed": (
            "The rg --files recovery identified the exact Caelen detailed, minimal, and final "
            "validator paths and inspected their check-count surfaces without error."
        ),
        "scope_boundary": "Read-only validator inventory recovery only; no repository mutation.",
    },
    {
        "negative_id": "V6576-X2-N05",
        "slug": "evidence-receipt-builder-partial-without-attributable-output",
        "failure_signature": (
            "The first isolated evidence-receipt builder returned no attributable console output; "
            "the durable audit found privacy, document-cap, and owner-cap receipts but no evidence manifest."
        ),
        "candidate_workaround": (
            "Retain the partial result, audit owned processes and exact artifacts, then rerun only "
            "the receipt builder with a bounded longer supervision window."
        ),
        "recurrence_guard": "Treat absent builder output as zero evidence until every required durable artifact is inspected.",
        "fail_procedure": "Infer complete receipt construction from the silent builder wrapper.",
        "fail_observed": "Three preliminary receipts existed, but evidence-content-manifest.json was absent; the attempt earned zero manifest credit.",
        "pass_procedure": "Wait for the original owned invocation, audit for duplicate processes, and inspect every exact artifact before considering any rerun.",
        "pass_observed": (
            "A later existence-gated audit found the manifest valid JSON and found no remaining owned "
            "builder process; no duplicate builder was launched for this recovery."
        ),
        "scope_boundary": "Owner-local evidence-receipt recovery only; no test, route, sibling, or external-state credit.",
    },
    {
        "negative_id": "V6576-X2-N06",
        "slug": "artifact-audit-unconditional-missing-manifest-read",
        "failure_signature": (
            "The first durable artifact audit correctly reported that the manifest was absent, "
            "then unconditionally attempted to read it and raised FileNotFoundError."
        ),
        "candidate_workaround": "Gate every JSON read on exact file existence and report absent artifacts as data.",
        "recurrence_guard": "Do not combine an existence probe with an unconditional later read.",
        "fail_procedure": "Read the manifest after the existence table has already reported it absent.",
        "fail_observed": "The audit ended in FileNotFoundError and earned zero manifest-validation credit.",
        "pass_procedure": "Run an existence-gated audit and inspect only artifacts that are present.",
        "pass_observed": (
            "The existence-gated audit completed and parsed all four required evidence receipt "
            "artifacts without reading an absent path."
        ),
        "scope_boundary": "Read-only artifact-audit recovery only; no repository mutation.",
    },
    {
        "negative_id": "V6576-X2-N07",
        "slug": "combined-git-status-inventory-lost-inner-session-attribution",
        "failure_signature": (
            "A combined tracked, untracked, and staged Git inventory exceeded the immediate wrapper "
            "and returned no attributable payload because the inner session identifier was not preserved."
        ),
        "candidate_workaround": "Split tracked status, untracked scope, owned process, and lock checks into scalar probes.",
        "recurrence_guard": "Preserve session identifiers or use bounded scalar Git state probes on large worktrees.",
        "fail_procedure": "Infer clean or staged state from the blank combined inventory wrapper.",
        "fail_observed": "The wrapper provided no state evidence and earned zero staging-gate credit.",
        "pass_procedure": "Run scalar tracked-status, untracked-scope, process, and lock probes.",
        "pass_observed": (
            "Tracked status was empty; 170 untracked paths were all inside the declared Orin evidence "
            "scope; no owned Git or Python process and no worktree lock remained."
        ),
        "scope_boundary": "Owner-local pre-staging state recovery only; no mutation or independent reproduction.",
    },
]
