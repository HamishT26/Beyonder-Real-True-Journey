# GHC Family Method Flow State

- Phase: v659-v3
- Owner: Sable Rook
- Methods: 18
- Passing witnesses: 18
- Failed witnesses retained: 18

## Preferred methods

### V6593-X1-METHOD-001 — Bounded recovery for combined-source-equality-wrapper-completed-without-a-usable-receipt

- Trigger: combined-source-equality-wrapper-completed-without-a-usable-receipt
- Method: Split branch, local, upstream, tracking, live-remote, divergence, and cleanliness into bounded scalar probes.
- Recurrence guard: Split branch, local, upstream, tracking, live-remote, divergence, and cleanliness into bounded scalar probes.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-001-F, V6593-X1-METHOD-001-P

### V6593-X1-METHOD-002 — Bounded recovery for unquoted-divergence-revision-expression-returned-no-usable-scalar

- Trigger: unquoted-divergence-revision-expression-returned-no-usable-scalar
- Method: Quote the exact triple-dot revision expression and emit exit code plus a labelled divergence scalar.
- Recurrence guard: Quote the exact triple-dot revision expression and emit exit code plus a labelled divergence scalar.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-002-F, V6593-X1-METHOD-002-P

### V6593-X1-METHOD-003 — Bounded recovery for combined-commit-surface-counter-returned-no-usable-receipt

- Trigger: combined-commit-surface-counter-returned-no-usable-receipt
- Method: Count x1, evidence, final, and source-to-final surfaces with separate exact revision probes.
- Recurrence guard: Count x1, evidence, final, and source-to-final surfaces with separate exact revision probes.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-003-F, V6593-X1-METHOD-003-P

### V6593-X1-METHOD-004 — Bounded recovery for write-all-before-read-git-cat-file-batch-probe-deadlocked-and-left-a-helper

- Trigger: write-all-before-read-git-cat-file-batch-probe-deadlocked-and-left-a-helper
- Method: Stream one object query at a time through one cat-file process, drain each response immediately, and stop only the verified orphan helper.
- Recurrence guard: Stream one object query at a time through one cat-file process, drain each response immediately, and stop only the verified orphan helper.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-004-F, V6593-X1-METHOD-004-P

### V6593-X1-METHOD-005 — Bounded recovery for auth-validation-summary-selected-issues-while-the-schema-emits-errors

- Trigger: auth-validation-summary-selected-issues-while-the-schema-emits-errors
- Method: Inspect exact top-level keys and read the errors array without rerunning the already successful validator.
- Recurrence guard: Inspect exact top-level keys and read the errors array without rerunning the already successful validator.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-005-F, V6593-X1-METHOD-005-P

### V6593-X1-METHOD-006 — Bounded recovery for worktree-add-wrapper-yielded-before-the-original-checkout-reached-terminal-state

- Trigger: worktree-add-wrapper-yielded-before-the-original-checkout-reached-terminal-state
- Method: Do not duplicate checkout; monitor the exact original Git process and verify branch and head after it exits.
- Recurrence guard: Do not duplicate checkout; monitor the exact original Git process and verify branch and head after it exits.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-006-F, V6593-X1-METHOD-006-P

### V6593-X1-METHOD-007 — Bounded recovery for powershell-foreach-output-was-piped-directly-and-triggered-an-empty-pipe-element

- Trigger: powershell-foreach-output-was-piped-directly-and-triggered-an-empty-pipe-element
- Method: Materialize foreach output into an array before sorting, projecting, or serializing it.
- Recurrence guard: Materialize foreach output into an array before sorting, projecting, or serializing it.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-007-F, V6593-X1-METHOD-007-P

### V6593-X1-METHOD-008 — Bounded recovery for bounded-checkout-wait-wrapper-returned-no-scalar-while-the-original-process-remained-active

- Trigger: bounded-checkout-wait-wrapper-returned-no-scalar-while-the-original-process-remained-active
- Method: Use direct short PID probes, retain the wait-wrapper failure, and avoid a second checkout invocation.
- Recurrence guard: Use direct short PID probes, retain the wait-wrapper failure, and avoid a second checkout invocation.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-008-F, V6593-X1-METHOD-008-P

### V6593-X1-METHOD-009 — Bounded recovery for official-source-search-wrapper-assumed-an-mcp-content-array-and-rendered-no-evidence

- Trigger: official-source-search-wrapper-assumed-an-mcp-content-array-and-rendered-no-evidence
- Method: Serialize the installed web result object directly and keep the first wrapper failure at zero credit.
- Recurrence guard: Serialize the installed web result object directly and keep the first wrapper failure at zero credit.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-009-F, V6593-X1-METHOD-009-P

### V6593-X1-METHOD-010 — Bounded recovery for combined-post-check-mixed-full-untracked-status-file-count-and-worktree-registration-without-a-receipt

- Trigger: combined-post-check-mixed-full-untracked-status-file-count-and-worktree-registration-without-a-receipt
- Method: Split revision, tracked status, tracked-file count, untracked status, and worktree registration into bounded probes.
- Recurrence guard: Split revision, tracked status, tracked-file count, untracked status, and worktree registration into bounded probes.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-010-F, V6593-X1-METHOD-010-P

### V6593-X1-METHOD-011 — Bounded recovery for first-full-untracked-scan-wrapper-returned-before-its-read-only-git-process-reached-terminal-state

- Trigger: first-full-untracked-scan-wrapper-returned-before-its-read-only-git-process-reached-terminal-state
- Method: Retain the wrapper failure and inspect the exact Git process before any further untracked scan.
- Recurrence guard: Retain the wrapper failure and inspect the exact Git process before any further untracked scan.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-011-F, V6593-X1-METHOD-011-P

### V6593-X1-METHOD-012 — Bounded recovery for second-untracked-scan-was-launched-before-the-first-read-only-scan-was-confirmed-terminal

- Trigger: second-untracked-scan-was-launched-before-the-first-read-only-scan-was-confirmed-terminal
- Method: Do not launch a third scan; verify both exact processes terminate and use exact staged manifests for the x1 boundary.
- Recurrence guard: Do not launch a third scan; verify both exact processes terminate and use exact staged manifests for the x1 boundary.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-012-F, V6593-X1-METHOD-012-P

### V6593-X1-METHOD-013 — Bounded recovery for first-x1-materialization-failed-closed-on-two-title-neighbour-collisions

- Trigger: first-x1-materialization-failed-closed-on-two-title-neighbour-collisions
- Method: Retain the failed build, inspect exact nearest inherited titles, and revise only the two colliding titles before rerunning the same bounded novelty gate.
- Recurrence guard: Retain the failed build, inspect exact nearest inherited titles, and revise only the two colliding titles before rerunning the same bounded novelty gate.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-013-F, V6593-X1-METHOD-013-P

### V6593-X1-METHOD-014 — Bounded recovery for combined-process-and-staged-status-probe-completed-without-a-usable-receipt

- Trigger: combined-process-and-staged-status-probe-completed-without-a-usable-receipt
- Method: Retain the missing receipt at zero credit and split the exact staged-name query from any process inspection before continuing.
- Recurrence guard: Retain the missing receipt at zero credit and split the exact staged-name query from any process inspection before continuing.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-014-F, V6593-X1-METHOD-014-P

### V6593-X1-METHOD-015 — Bounded recovery for first-exact-index-reviewer-lost-embedded-python-quotes-through-windows-native-argument-handling

- Trigger: first-exact-index-reviewer-lost-embedded-python-quotes-through-windows-native-argument-handling
- Method: Retain the syntax failure at zero credit and pass the unchanged reviewer through standard input instead of a quote-bearing native argument.
- Recurrence guard: Retain the syntax failure at zero credit and pass the unchanged reviewer through standard input instead of a quote-bearing native argument.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-015-F, V6593-X1-METHOD-015-P

### V6593-X1-METHOD-016 — Bounded recovery for first-running-index-review-overclassified-public-drive-root-capacity-probes-as-private-local-paths

- Trigger: first-running-index-review-overclassified-public-drive-root-capacity-probes-as-private-local-paths
- Method: Inspect only the exact candidate line numbers, disclose no matched value, and distinguish root-only storage probes from paths carrying private suffixes.
- Recurrence guard: Inspect only the exact candidate line numbers, disclose no matched value, and distinguish root-only storage probes from paths carrying private suffixes.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-016-F, V6593-X1-METHOD-016-P

### V6593-X1-METHOD-017 — Bounded recovery for first-root-only-adjudicator-assumed-one-source-slash-and-missed-escaped-root-literals

- Trigger: first-root-only-adjudicator-assumed-one-source-slash-and-missed-escaped-root-literals
- Method: Accept one-or-more source escape slashes only when the complete quoted literal ends at the drive root, then rerun the unchanged five-class review.
- Recurrence guard: Accept one-or-more source escape slashes only when the complete quoted literal ends at the drive root, then rerun the unchanged five-class review.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-017-F, V6593-X1-METHOD-017-P

### V6593-X1-METHOD-018 — Bounded recovery for final-restage-wrapper-promoted-benign-git-line-ending-warnings-to-a-terminating-powershell-error

- Trigger: final-restage-wrapper-promoted-benign-git-line-ending-warnings-to-a-terminating-powershell-error
- Method: Inspect the existing index first, retain the wrapper failure, and use the native exit code rather than PowerShell stderr classification for any required idempotent restage.
- Recurrence guard: Inspect the existing index first, retain the wrapper failure, and use the native exit code rather than PowerShell stderr classification for any required idempotent restage.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6593-X1-METHOD-018-F, V6593-X1-METHOD-018-P

## Retained boundary

Same-owner workflow evidence only; no independent reproduction or protected-gate closure.
