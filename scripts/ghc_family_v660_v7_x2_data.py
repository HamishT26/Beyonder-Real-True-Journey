#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Ilyra Fen v660-v7."""

from __future__ import annotations

from ghc_family_v660_v7_data import *  # noqa: F401,F403
import ghc_family_v660_v7_data as x1


X1_FREEZE = "ae06de953f21db197bb7a57a5a5e70cc7e97da0a"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Only failures observed after the x1 freeze belong here. Expected rejecting
# mutations are recorded in the mutation register and Method Flow witnesses,
# not prefilled as tooling faults.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6607-X2-N001",
        "signature": "first-post-x1-four-way-proof-wrapper-failed-javascript-parsing-before-any-shell-or-git-command-because-a-powershell-backtick-entered-a-javascript-template-literal",
        "recovery": "Retain the wrapper failure at zero credit, replace the PowerShell backtick delimiter with the explicit character expression [char]9, and rerun only the bounded four-way equality probe; local, upstream, tracking, and fresh-live remote then matched the immutable Ilyra x1 with zero divergence and a clean lane.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N002",
        "signature": "first-seven-file-x2-scaffold-stale-token-audit-used-one-broad-line-emitting-search-and-its-output-was-truncated-before-an-attributable-complete-review",
        "recovery": "Retain the truncated display at zero credit, inventory exact token counts per file, then inspect only bounded matching lines and complete each file review before any x2 builder executes.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N003",
        "signature": "first-bounded-file-count-wrapper-used-an-invalid-grouped-powershell-foreach-expression-and-failed-with-unexpected-token-and-empty-pipe-parser-errors",
        "recovery": "Retain the parser failure at zero credit and use a bounded UTF-8 Python projection over the seven declared files; it reported exact byte and line counts without repository mutation.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N004",
        "signature": "first-method-flow-summary-command-printed-the-complete-large-ledger-summary-and-its-console-display-was-truncated-despite-successfully-writing-the-declared-json-and-markdown-files",
        "recovery": "Retain the truncated console display at zero credit and parse only the declared JSON output to project its schema, owner, phase, counts, preferred-method count, retained-failure count, and validity; after any additive ledger change, regenerate the changed summary once with console output suppressed and recheck the same bounded projection.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N005",
        "signature": "first-x2-reflection-remaster-invocation-resolved-the-repository-local-historical-compatibility-runner-instead-of-the-selected-family-skill-script-and-produced-unrelated-nested-tribunal-receipts",
        "recovery": "Retain the wrong-runner invocation and its bounded incidental receipts at zero credit, invoke the exact selected ghc-family-reflection-remaster skill script into the declared x2 output root, and verify its four expected inventory, issue, method, and report files before test credit.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N006",
        "signature": "first-owner-x2-test-selection-passed-eighteen-of-nineteen-tests-and-errored-on-the-missing-family-current-reflection-remaster-inventory-file",
        "recovery": "Retain the 18-pass and one-error aggregate at zero clean-pass credit, recover only the missing family-current reflection-remaster dependency, then rerun only the isolated failing governance-and-reflection test.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N007",
        "signature": "x2-preflight-falsely-assumed-the-meta-tool-box-receipts-existed-after-building-phase-local-skills-and-runners-even-though-the-declared-meta-tool-build-validate-and-collision-commands-had-not-run",
        "recovery": "Retain the false assumption at zero credit, enumerate the exact expected meta-tool paths, then run the family-current build, validate, and collision commands in dependency order against the declared Ilyra phase root.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N008",
        "signature": "first-isolated-governance-and-reflection-recovery-test-still-errored-after-reflection-recovery-because-the-meta-tool-box-validation-file-was-absent",
        "recovery": "Retain the isolated error at zero credit, materialize and validate only the missing meta-tool-box dependency, refresh count-dependent receipts, and rerun only the same isolated test.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N009",
        "signature": "first-exact-evidence-staging-wrapper-emitted-one-line-ending-advisory-per-declared-path-and-the-console-display-was-truncated-before-a-bounded-attributable-summary",
        "recovery": "Retain the truncated advisory display at zero credit, do not repeat the broad staging operation, compare the Git index directly with the frozen 191-path allowlist, and stage only later count-dependent receipt changes through a captured bounded Git process.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N010",
        "signature": "post-staging-count-refresh-repeated-the-line-ending-advisory-storm-through-internal-changed-path-probes-and-produced-multiple-truncated-displays-before-the-same-process-returned-success",
        "recovery": "Retain the repeated warning storm and every truncated display at zero credit, preserve the successful builder result, capture Git helper stderr for later bounded probes, refresh only count-dependent outputs, and verify the final index directly without another broad display.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N011",
        "signature": "post-staging-builder-refresh-collapsed-the-frozen-evidence-domain-from-one-hundred-ninety-one-indexed-paths-to-nine-unstaged-paths-and-an-eight-entry-content-manifest",
        "recovery": "Retain the collapsed staged-review and manifest outputs at zero credit, bind evidence enumeration to the exact Git index whenever staged paths exist, reconstruct the intended allowlist from the still-intact 191-path index, and regenerate privacy, document-cap, manifest, and staged-review receipts before commit.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N012",
        "signature": "first-post-builder-manifest-inspection-returned-an-application-level-output-overflow-instead-of-the-requested-compact-manifest-projection",
        "recovery": "Retain the overflowed inspection at zero credit and split the audit into scalar manifest-count, staged-count, unstaged-count, and exact-key probes with bounded output; those probes exposed the domain collapse without mutation.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N013",
        "signature": "first-scalar-recovery-probe-guessed-the-content-manifest-subdirectory-and-treated-an-unknown-staged-review-list-field-as-authoritative-before-discovering-the-real-files-and-schema",
        "recovery": "Retain the path and field-assumption fault at zero credit, discover exact repository-relative filenames with rg, print only the staged-review keys and list cardinalities, and then read the actual validation manifest and intended_allowlist fields.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N014",
        "signature": "first-post-recovery-multi-field-python-verification-process-exited-cleanly-but-returned-no-captured-standard-output-so-it-earned-no-verification-credit",
        "recovery": "Retain the empty-output witness at zero credit and split the verification into bounded native scalar reads; those reads confirmed the 191-path allowlist, 187 manifest entries, 190 privacy-scanned files, zero confirmed hits, and the count-dependent truth fields.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N015",
        "signature": "captured-bounded-git-add-wrapper-staged-the-intended-receipt-refreshes-but-returned-no-attributable-standard-output-summary",
        "recovery": "Retain the empty wrapper result at zero credit and inspect the index through a separate read-only scalar probe; it confirmed 191 staged paths, zero unstaged paths, and zero untracked paths before exact set comparison.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N016",
        "signature": "first-index-byte-manifest-replay-launched-one-git-show-process-per-entry-exceeded-the-bounded-wrapper-window-and-lost-its-session-handle-before-returning-evidence",
        "recovery": "Retain the slow replay and missing handle at zero credit, replace per-entry Git processes with one git-ls-files index projection and one git-cat-file batch object read, and verify all 187 normalized blob hashes and byte counts without checkout conversion.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N017",
        "signature": "first-validator-discovery-search-matched-large-compressed-json-lines-and-truncated-its-display-before-providing-a-bounded-attributable-inventory",
        "recovery": "Retain the broad search at zero credit, inspect only the exact final-validator line windows and the exact Method Flow skill directory, and use the declared phase-scoped validator rather than inferring commands from compressed evidence files.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N018",
        "signature": "first-post-summary-scalar-projection-guessed-four-top-level-method-flow-count-keys-and-returned-empty-values-despite-valid-summary-files",
        "recovery": "Retain the empty count projection at zero credit, enumerate the exact summary keys first, then read methods, witnesses, states, and witness-results from the declared counts object; the recovered projection confirmed 53 methods and 186 witnesses before this additive failure was appended.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N019",
        "signature": "final-compound-precommit-scalar-audit-crossed-its-wrapper-window-after-the-path-set-and-x1-overlap-checks-and-lost-the-unreported-later-fields",
        "recovery": "Retain the partial compound audit at zero credit, split worktree status and diff hygiene into independent session-aware probes, and poll the exact status process until it reported zero unstaged and zero untracked paths; the separate diff check returned zero issues.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6607-X2-N020",
        "signature": "first-final-truth-scalar-projection-used-the-default-short-wrapper-window-and-returned-no-output-before-the-read-only-json-projection-completed",
        "recovery": "Retain the empty projection at zero credit and rerun only the same bounded native JSON reads with an explicit 30-second wrapper window; the recovery reported aligned negative, method, privacy, document-cap, and recovery counts.",
        "recovery_passed": True,
    },
]
