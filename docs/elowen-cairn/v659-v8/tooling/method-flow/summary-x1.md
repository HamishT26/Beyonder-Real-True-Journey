# GHC Family Method Flow State

- Phase: v659-v8
- Owner: Elowen Cairn
- Methods: 27
- Passing witnesses: 27
- Failed witnesses retained: 27

## Preferred methods

### V6598-X1-METHOD-001 — Bounded recovery for activation-read-first-assumed-codex-metadata-root-was-a-git-worktree

- Trigger: activation-read-first-assumed-codex-metadata-root-was-a-git-worktree
- Method: Retain the fatal not-a-repository result and repeat only the activation read in Tamar's uniquely resolved source worktree.
- Recurrence guard: Retain the fatal not-a-repository result and repeat only the activation read in Tamar's uniquely resolved source worktree.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-001-F, V6598-X1-METHOD-001-P

### V6598-X1-METHOD-002 — Bounded recovery for first-complete-activation-display-exceeded-the-bounded-output-budget

- Trigger: first-complete-activation-display-exceeded-the-bounded-output-budget
- Method: Retain the truncated display and verify the exact line count, structured fields, and nonoverlapping bounded windows through EOF.
- Recurrence guard: Retain the truncated display and verify the exact line count, structured fields, and nonoverlapping bounded windows through EOF.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-002-F, V6598-X1-METHOD-002-P

### V6598-X1-METHOD-003 — Bounded recovery for first-activation-proposal-parser-reused-powershell-matches-inside-nested-loops

- Trigger: first-activation-proposal-parser-reused-powershell-matches-inside-nested-loops
- Method: Retain the null proposal identifiers and recover with separate exact heading extraction and independent template counts.
- Recurrence guard: Retain the null proposal identifiers and recover with separate exact heading extraction and independent template counts.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-003-F, V6598-X1-METHOD-003-P

### V6598-X1-METHOD-004 — Bounded recovery for historical-memory-rollout-full-read-exceeded-the-context-window

- Trigger: historical-memory-rollout-full-read-exceeded-the-context-window
- Method: Retain the truncated historical read and rely only on the bounded MEMORY registry pointer without importing stale route state.
- Recurrence guard: Retain the truncated historical read and rely only on the bounded MEMORY registry pointer without importing stale route state.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-004-F, V6598-X1-METHOD-004-P

### V6598-X1-METHOD-005 — Bounded recovery for first-source-ancestry-hash-literal-contained-an-invalid-command-separator-expression

- Trigger: first-source-ancestry-hash-literal-contained-an-invalid-command-separator-expression
- Method: Retain the pre-execution PowerShell parser fault and run each ancestry check as a separate scalar command.
- Recurrence guard: Retain the pre-execution PowerShell parser fault and run each ancestry check as a separate scalar command.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-005-F, V6598-X1-METHOD-005-P

### V6598-X1-METHOD-006 — Bounded recovery for combined-source-remote-probe-completed-without-attributable-output

- Trigger: combined-source-remote-probe-completed-without-attributable-output
- Method: Retain the empty wrapper and rerun only the local anchors and live remote as labelled scalar probes.
- Recurrence guard: Retain the empty wrapper and rerun only the local anchors and live remote as labelled scalar probes.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-006-F, V6598-X1-METHOD-006-P

### V6598-X1-METHOD-007 — Bounded recovery for combined-source-local-probe-completed-without-attributable-output

- Trigger: combined-source-local-probe-completed-without-attributable-output
- Method: Retain the empty wrapper and use bounded independent branch, head, tracking, history, parent, and divergence commands.
- Recurrence guard: Retain the empty wrapper and use bounded independent branch, head, tracking, history, parent, and divergence commands.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-007-F, V6598-X1-METHOD-007-P

### V6598-X1-METHOD-008 — Bounded recovery for commit-local-manifest-projection-piped-directly-from-a-powershell-foreach-block

- Trigger: commit-local-manifest-projection-piped-directly-from-a-powershell-foreach-block
- Method: Retain the empty-pipe parser fault and materialize the foreach rows before ConvertTo-Json.
- Recurrence guard: Retain the empty-pipe parser fault and materialize the foreach rows before ConvertTo-Json.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-008-F, V6598-X1-METHOD-008-P

### V6598-X1-METHOD-009 — Bounded recovery for source-data-import-omitted-the-repository-scripts-path

- Trigger: source-data-import-omitted-the-repository-scripts-path
- Method: Retain the ModuleNotFoundError and add only the exact scripts directory to the read-only inspection process.
- Recurrence guard: Retain the ModuleNotFoundError and add only the exact scripts directory to the read-only inspection process.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-009-F, V6598-X1-METHOD-009-P

### V6598-X1-METHOD-010 — Bounded recovery for source-data-inspection-assumed-a-proposals-symbol-that-the-module-does-not-export

- Trigger: source-data-inspection-assumed-a-proposals-symbol-that-the-module-does-not-export
- Method: Retain the ImportError, inspect declared constants, and use NEW_PROPOSAL_SPECS.
- Recurrence guard: Retain the ImportError, inspect declared constants, and use NEW_PROPOSAL_SPECS.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-010-F, V6598-X1-METHOD-010-P

### V6598-X1-METHOD-011 — Bounded recovery for installed-roster-and-auth-snapshots-stop-before-the-live-v659-v8-edge

- Trigger: installed-roster-and-auth-snapshots-stop-before-the-live-v659-v8-edge
- Method: Retain the snapshots as historical evidence and apply the acknowledged Tamar-to-Elowen activation phase-locally without rewriting global files.
- Recurrence guard: Retain the snapshots as historical evidence and apply the acknowledged Tamar-to-Elowen activation phase-locally without rewriting global files.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-011-F, V6598-X1-METHOD-011-P

### V6598-X1-METHOD-012 — Bounded recovery for external-post-route-receipt-exposes-one-more-failure-than-the-live-activation-baseline

- Trigger: external-post-route-receipt-exposes-one-more-failure-than-the-live-activation-baseline
- Method: Preserve the sealed counts and activation-stated baseline, then carry all five external route failures additively as 19541 negatives and 5815 methods.
- Recurrence guard: Preserve the sealed counts and activation-stated baseline, then carry all five external route failures additively as 19541 negatives and 5815 methods.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-012-F, V6598-X1-METHOD-012-P

### V6598-X1-METHOD-013 — Bounded recovery for first-full-source-data-display-exceeded-the-output-budget

- Trigger: first-full-source-data-display-exceeded-the-output-budget
- Method: Retain the truncated read and inspect nonoverlapping numbered windows through the exact final line.
- Recurrence guard: Retain the truncated read and inspect nonoverlapping numbered windows through the exact final line.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-013-F, V6598-X1-METHOD-013-P

### V6598-X1-METHOD-014 — Bounded recovery for combined-post-worktree-status-wrapper-completed-without-attributable-output

- Trigger: combined-post-worktree-status-wrapper-completed-without-attributable-output
- Method: Retain the empty wrapper and verify branch, head, staged diff, and unstaged diff as bounded scalar commands.
- Recurrence guard: Retain the empty wrapper and verify branch, head, staged diff, and unstaged diff as bounded scalar commands.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-014-F, V6598-X1-METHOD-014-P

### V6598-X1-METHOD-015 — Bounded recovery for first-novelty-wrapper-assumed-textencoder-existed-in-the-orchestration-isolate

- Trigger: first-novelty-wrapper-assumed-textencoder-existed-in-the-orchestration-isolate
- Method: Retain the pre-command ReferenceError and replace only the encoding mechanism.
- Recurrence guard: Retain the pre-command ReferenceError and replace only the encoding mechanism.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-015-F, V6598-X1-METHOD-015-P

### V6598-X1-METHOD-016 — Bounded recovery for second-novelty-wrapper-assumed-btoa-existed-in-the-orchestration-isolate

- Trigger: second-novelty-wrapper-assumed-btoa-existed-in-the-orchestration-isolate
- Method: Retain the pre-command ReferenceError and avoid isolate-specific encoding helpers.
- Recurrence guard: Retain the pre-command ReferenceError and avoid isolate-specific encoding helpers.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-016-F, V6598-X1-METHOD-016-P

### V6598-X1-METHOD-017 — Bounded recovery for third-novelty-wrapper-embedded-python-loop-quoting-that-powershell-parsed

- Trigger: third-novelty-wrapper-embedded-python-loop-quoting-that-powershell-parsed
- Method: Retain the PowerShell parser fault and remove nested inline-language quoting.
- Recurrence guard: Retain the PowerShell parser fault and remove nested inline-language quoting.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-017-F, V6598-X1-METHOD-017-P

### V6598-X1-METHOD-018 — Bounded recovery for first-powershell-novelty-recovery-materialized-forty-titles-as-one-nested-array

- Trigger: first-powershell-novelty-recovery-materialized-forty-titles-as-one-nested-array
- Method: Retain the invalid one-of-one result at zero credit and require an exact expected-count assertion.
- Recurrence guard: Retain the invalid one-of-one result at zero credit and require an exact expected-count assertion.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-018-F, V6598-X1-METHOD-018-P

### V6598-X1-METHOD-019 — Bounded recovery for second-powershell-novelty-recovery-returned-no-attributable-output

- Trigger: second-powershell-novelty-recovery-returned-no-attributable-output
- Method: Retain the empty wrapper and replace it with a narrow read-only Python probe.
- Recurrence guard: Retain the empty wrapper and replace it with a narrow read-only Python probe.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-019-F, V6598-X1-METHOD-019-P

### V6598-X1-METHOD-020 — Bounded recovery for dedicated-patch-surface-initially-wrote-the-novelty-probe-under-codex-metadata

- Trigger: dedicated-patch-surface-initially-wrote-the-novelty-probe-under-codex-metadata
- Method: Resolve both absolute paths and move only the newly created file into the unused D-first Elowen destination.
- Recurrence guard: Resolve both absolute paths and move only the newly created file into the unused D-first Elowen destination.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-020-F, V6598-X1-METHOD-020-P

### V6598-X1-METHOD-021 — Bounded recovery for first-d-first-novelty-probe-invocation-ran-before-the-misplaced-file-was-recovered

- Trigger: first-d-first-novelty-probe-invocation-ran-before-the-misplaced-file-was-recovered
- Method: Retain the file-not-found and null receipt; move the exact new file, then rerun only the read-only probe.
- Recurrence guard: Retain the file-not-found and null receipt; move the exact new file, then rerun only the read-only probe.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-021-F, V6598-X1-METHOD-021-P

### V6598-X1-METHOD-022 — Bounded recovery for first-valid-forty-title-novelty-screen-rejected-eleven-stale-pattern-drafts

- Trigger: first-valid-forty-title-novelty-screen-rejected-eleven-stale-pattern-drafts
- Method: Retain all eleven rejected drafts at zero credit, revise their mechanisms beyond noun substitution, and rerun the same forty-title screen.
- Recurrence guard: Retain all eleven rejected drafts at zero credit, revise their mechanisms beyond noun substitution, and rerun the same forty-title screen.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-022-F, V6598-X1-METHOD-022-P

### V6598-X1-METHOD-023 — Bounded recovery for shell-visible-apply-patch-wrapper-was-not-executable-from-the-d-worktree

- Trigger: shell-visible-apply-patch-wrapper-was-not-executable-from-the-d-worktree
- Method: Retain the access-denied result and use the dedicated patch surface with an absolute D-first path.
- Recurrence guard: Retain the access-denied result and use the dedicated patch surface with an absolute D-first path.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-023-F, V6598-X1-METHOD-023-P

### V6598-X1-METHOD-024 — Bounded recovery for first-official-source-patch-contained-an-empty-update-hunk

- Trigger: first-official-source-patch-contained-an-empty-update-hunk
- Method: Retain the patch verification failure, remove the empty hunk, and apply only the exact source-row replacement.
- Recurrence guard: Retain the patch verification failure, remove the empty hunk, and apply only the exact source-row replacement.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-024-F, V6598-X1-METHOD-024-P

### V6598-X1-METHOD-025 — Bounded recovery for first-startup-failure-ledger-patch-used-one-stale-mechanical-rewrite-context-line

- Trigger: first-startup-failure-ledger-patch-used-one-stale-mechanical-rewrite-context-line
- Method: Retain the patch verification failure, reread the exact block, and patch the current content only.
- Recurrence guard: Retain the patch verification failure, reread the exact block, and patch the current content only.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-025-F, V6598-X1-METHOD-025-P

### V6598-X1-METHOD-026 — Bounded recovery for combined-roster-auth-path-preflight-output-was-truncated

- Trigger: combined-roster-auth-path-preflight-output-was-truncated
- Method: Retain the truncated wrapper at zero credit and invoke each exact known validation entrypoint independently.
- Recurrence guard: Retain the truncated wrapper at zero credit and invoke each exact known validation entrypoint independently.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-026-F, V6598-X1-METHOD-026-P

### V6598-X1-METHOD-027 — Bounded recovery for first-workflow-plan-refinement-used-evidence-only-route-keys-outside-the-current-schema

- Trigger: first-workflow-plan-refinement-used-evidence-only-route-keys-outside-the-current-schema
- Method: Retain the complete needs-refinement output at zero credit; map the inherited cycle and topology into the required structural keys while keeping only the current phase assigned and every later edge unresolved.
- Recurrence guard: Retain the complete needs-refinement output at zero credit; map the inherited cycle and topology into the required structural keys while keeping only the current phase assigned and every later edge unresolved.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6598-X1-METHOD-027-F, V6598-X1-METHOD-027-P

## Retained boundary

Same-owner workflow evidence only; no independent reproduction or protected-gate closure.
