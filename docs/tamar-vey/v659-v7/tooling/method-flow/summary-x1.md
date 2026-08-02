# GHC Family Method Flow State

- Phase: v659-v7
- Owner: Tamar Vey
- Methods: 22
- Passing witnesses: 22
- Failed witnesses retained: 22

## Preferred methods

### V6597-X1-METHOD-001 — Bounded recovery for concurrent-startup-probes-yielded-without-attributable-output

- Trigger: concurrent-startup-probes-yielded-without-attributable-output
- Method: Retain the empty aggregate result and rerun only exact source, memory, and worktree projections as bounded scalar reads.
- Recurrence guard: Retain the empty aggregate result and rerun only exact source, memory, and worktree projections as bounded scalar reads.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-001-F, V6597-X1-METHOD-001-P

### V6597-X1-METHOD-002 — Bounded recovery for d-drive-worktree-directory-read-exceeded-the-first-output-window

- Trigger: d-drive-worktree-directory-read-exceeded-the-first-output-window
- Method: Retain the initial yield and collect the exact attributable session once without broadening the directory scope.
- Recurrence guard: Retain the initial yield and collect the exact attributable session once without broadening the directory scope.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-002-F, V6597-X1-METHOD-002-P

### V6597-X1-METHOD-003 — Bounded recovery for source-git-status-wrapper-ended-after-its-opening-marker

- Trigger: source-git-status-wrapper-ended-after-its-opening-marker
- Method: Retain both incomplete wrappers and rely on hashed canonical receipts plus later exact diff, index, untracked, and clean-status probes.
- Recurrence guard: Retain both incomplete wrappers and rely on hashed canonical receipts plus later exact diff, index, untracked, and clean-status probes.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-003-F, V6597-X1-METHOD-003-P

### V6597-X1-METHOD-004 — Bounded recovery for skill-creator-broad-read-exceeded-the-context-output-budget

- Trigger: skill-creator-broad-read-exceeded-the-context-output-budget
- Method: Retain the truncated read and reread the complete 416-line skill in four bounded line windows through EOF.
- Recurrence guard: Retain the truncated read and reread the complete 416-line skill in four bounded line windows through EOF.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-004-F, V6597-X1-METHOD-004-P

### V6597-X1-METHOD-005 — Bounded recovery for powershell-format-table-suppressed-following-source-uniqueness-scalars

- Trigger: powershell-format-table-suppressed-following-source-uniqueness-scalars
- Method: Retain the presentation loss and emit each path, local-branch, and live-remote result as a labelled scalar.
- Recurrence guard: Retain the presentation loss and emit each path, local-branch, and live-remote result as a labelled scalar.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-005-F, V6597-X1-METHOD-005-P

### V6597-X1-METHOD-006 — Bounded recovery for post-worktree-probe-ran-while-the-original-checkout-was-still-materializing

- Trigger: post-worktree-probe-ran-while-the-original-checkout-was-still-materializing
- Method: Retain the transient empty-index, partial-tree, untracked, and lock observations; wait for only the attributable Git process tree and inspect final state.
- Recurrence guard: Retain the transient empty-index, partial-tree, untracked, and lock observations; wait for only the attributable Git process tree and inspect final state.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-006-F, V6597-X1-METHOD-006-P

### V6597-X1-METHOD-007 — Bounded recovery for premature-cached-diff-diagnostic-projected-an-overbroad-partial-tree-deletion-list

- Trigger: premature-cached-diff-diagnostic-projected-an-overbroad-partial-tree-deletion-list
- Method: Retain the truncated 1.3-million-token diagnostic at zero credit and never rerun it; use bounded process, lock, exact-head, and clean-status probes after checkout.
- Recurrence guard: Retain the truncated 1.3-million-token diagnostic at zero credit and never rerun it; use bounded process, lock, exact-head, and clean-status probes after checkout.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-007-F, V6597-X1-METHOD-007-P

### V6597-X1-METHOD-008 — Bounded recovery for worktree-post-create-wrapper-launched-an-expensive-full-untracked-enumeration

- Trigger: worktree-post-create-wrapper-launched-an-expensive-full-untracked-enumeration
- Method: Retain the delayed wrapper and wait for its exact ls-files processes before one final clean status check.
- Recurrence guard: Retain the delayed wrapper and wait for its exact ls-files processes before one final clean status check.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-008-F, V6597-X1-METHOD-008-P

### V6597-X1-METHOD-009 — Bounded recovery for javascript-template-literal-collided-with-a-powershell-tab-escape

- Trigger: javascript-template-literal-collided-with-a-powershell-tab-escape
- Method: Retain the pre-execution parser fault and build the PowerShell equality probe from ordinary strings with a character-code tab split.
- Recurrence guard: Retain the pre-execution parser fault and build the PowerShell equality probe from ordinary strings with a character-code tab split.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-009-F, V6597-X1-METHOD-009-P

### V6597-X1-METHOD-010 — Bounded recovery for javascript-template-literal-collided-with-powershell-output-formatting-in-a-file-size-probe

- Trigger: javascript-template-literal-collided-with-powershell-output-formatting-in-a-file-size-probe
- Method: Retain the pre-execution parser fault and use concatenated scalar output without embedded template backticks.
- Recurrence guard: Retain the pre-execution parser fault and use concatenated scalar output without embedded template backticks.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-010-F, V6597-X1-METHOD-010-P

### V6597-X1-METHOD-011 — Bounded recovery for first-data-patch-assumed-the-copied-module-imported-v659-v6-directly

- Trigger: first-data-patch-assumed-the-copied-module-imported-v659-v6-directly
- Method: Retain the failed patch application, reread the exact header, and patch the actual inherited v659-v5 import to Liora v659-v6.
- Recurrence guard: Retain the failed patch application, reread the exact header, and patch the actual inherited v659-v5 import to Liora v659-v6.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-011-F, V6597-X1-METHOD-011-P

### V6597-X1-METHOD-012 — Bounded recovery for installed-roster-and-auth-snapshots-stopped-at-an-older-v659-route-edge

- Trigger: installed-roster-and-auth-snapshots-stopped-at-an-older-v659-route-edge
- Method: Retain the stale snapshots as historical evidence and apply the acknowledged live Liora-to-Tamar-to-Elowen edge phase-locally without silently rewriting global state.
- Recurrence guard: Retain the stale snapshots as historical evidence and apply the acknowledged live Liora-to-Tamar-to-Elowen edge phase-locally without silently rewriting global state.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-012-F, V6597-X1-METHOD-012-P

### V6597-X1-METHOD-013 — Bounded recovery for first-x1-build-looked-for-forty-selected-source-specs-in-only-the-immediate-liora-ledger

- Trigger: first-x1-build-looked-for-forty-selected-source-specs-in-only-the-immediate-liora-ledger
- Method: Retain the stopped build at zero credit and join the immutable Liora and Orin proposal ledgers while keeping the Liora frozen-chain index authoritative.
- Recurrence guard: Retain the stopped build at zero credit and join the immutable Liora and Orin proposal ledgers while keeping the Liora frozen-chain index authoritative.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-013-F, V6597-X1-METHOD-013-P

### V6597-X1-METHOD-014 — Bounded recovery for second-x1-build-rejected-two-proposal-titles-at-or-above-the-declared-token-overlap-threshold

- Trigger: second-x1-build-rejected-two-proposal-titles-at-or-above-the-declared-token-overlap-threshold
- Method: Retain the stopped build, inspect the exact nearest inherited titles, and revise only the two titles toward textile-specific byte-profile and equal-budget view-comparison language.
- Recurrence guard: Retain the stopped build, inspect the exact nearest inherited titles, and revise only the two titles toward textile-specific byte-profile and equal-budget view-comparison language.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-014-F, V6597-X1-METHOD-014-P

### V6597-X1-METHOD-015 — Bounded recovery for first-x1-test-run-passed-twenty-of-twenty-one-checks-but-found-family-current-tool-receipts-not-yet-materialized

- Trigger: first-x1-test-run-passed-twenty-of-twenty-one-checks-but-found-family-current-tool-receipts-not-yet-materialized
- Method: Retain the incomplete suite at zero credit, invoke the required phase-local workflow, index, reflection, and Method Flow tools, refresh x1, and rerun only the bounded x1 suite.
- Recurrence guard: Retain the incomplete suite at zero credit, invoke the required phase-local workflow, index, reflection, and Method Flow tools, refresh x1, and rerun only the bounded x1 suite.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-015-F, V6597-X1-METHOD-015-P

### V6597-X1-METHOD-016 — Bounded recovery for guessed-a-nonexistent-generic-auth-permission-runner-name

- Trigger: guessed-a-nonexistent-generic-auth-permission-runner-name
- Method: Retain the read-only path error and inspect the exact skill inventory before using its present validate_auth_permission_state.py entry point.
- Recurrence guard: Retain the read-only path error and inspect the exact skill inventory before using its present validate_auth_permission_state.py entry point.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-016-F, V6597-X1-METHOD-016-P

### V6597-X1-METHOD-017 — Bounded recovery for repository-local-phase-specific-reflection-runner-was-invoked-instead-of-the-current-installed-skill-runner

- Trigger: repository-local-phase-specific-reflection-runner-was-invoked-instead-of-the-current-installed-skill-runner
- Method: Retain its bounded tribunal fixture and basename collision at zero credit, then invoke the exact installed ghc-family-reflection-remaster runner for the current inventory.
- Recurrence guard: Retain its bounded tribunal fixture and basename collision at zero credit, then invoke the exact installed ghc-family-reflection-remaster runner for the current inventory.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-017-F, V6597-X1-METHOD-017-P

### V6597-X1-METHOD-018 — Bounded recovery for method-flow-summary-stdout-exceeded-the-bounded-display-budget-after-writing-complete-files

- Trigger: method-flow-summary-stdout-exceeded-the-bounded-display-budget-after-writing-complete-files
- Method: Retain the truncated presentation at zero credit and suppress verbose stdout on later validation while checking the complete phase-local JSON receipt directly.
- Recurrence guard: Retain the truncated presentation at zero credit and suppress verbose stdout on later validation while checking the complete phase-local JSON receipt directly.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-018-F, V6597-X1-METHOD-018-P

### V6597-X1-METHOD-019 — Bounded recovery for supplemental-stale-label-scan-used-the-repository-root-and-exceeded-two-bounded-polls

- Trigger: supplemental-stale-label-scan-used-the-repository-root-and-exceeded-two-bounded-polls
- Method: Retain and stop only the attributable read-only process tree, then scan the three explicit Tamar owner roots without repository-wide traversal.
- Recurrence guard: Retain and stop only the attributable read-only process tree, then scan the three explicit Tamar owner roots without repository-wide traversal.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-019-F, V6597-X1-METHOD-019-P

### V6597-X1-METHOD-020 — Bounded recovery for unified-session-interrupt-was-unsupported-for-the-long-read-only-stale-scan

- Trigger: unified-session-interrupt-was-unsupported-for-the-long-read-only-stale-scan
- Method: Retain the unsupported interrupt at zero credit and resolve the exact PowerShell process plus descendants before stopping only that attributable tree.
- Recurrence guard: Retain the unsupported interrupt at zero credit and resolve the exact PowerShell process plus descendants before stopping only that attributable tree.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-020-F, V6597-X1-METHOD-020-P

### V6597-X1-METHOD-021 — Bounded recovery for powershell-process-stop-loop-used-the-reserved-pid-variable-name

- Trigger: powershell-process-stop-loop-used-the-reserved-pid-variable-name
- Method: Retain the parser and binding fault, rename the loop variable to processId, and stop only the two exact attributable process identifiers.
- Recurrence guard: Retain the parser and binding fault, rename the loop variable to processId, and stop only the two exact attributable process identifiers.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-021-F, V6597-X1-METHOD-021-P

### V6597-X1-METHOD-022 — Bounded recovery for explicit-root-ripgrep-stale-label-scan-still-exceeded-two-bounded-polls

- Trigger: explicit-root-ripgrep-stale-label-scan-still-exceeded-two-bounded-polls
- Method: Retain and stop only its exact read-only process tree, then scan the already enumerated staged paths once with a bounded Python UTF-8 pass.
- Recurrence guard: Retain and stop only its exact read-only process tree, then scan the already enumerated staged paths once with a bounded Python UTF-8 pass.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6597-X1-METHOD-022-F, V6597-X1-METHOD-022-P

## Retained boundary

Same-owner workflow evidence only; no independent reproduction or protected-gate closure.
