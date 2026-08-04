# GHC Family Method Flow State

- Phase: v661-v2
- Owner: Caelen Ash
- Methods: 22
- Passing witnesses: 22
- Failed witnesses retained: 22

## Preferred methods

### V6612-X1-METHOD-001 — Bounded recovery for combined-activation-and-skill-probe-produced-no-attributable-output-before-recovery

- Trigger: combined-activation-and-skill-probe-produced-no-attributable-output-before-recovery
- Method: Retain the empty wrapper at zero credit and split activation, skill, and source reads into exact bounded probes.
- Recurrence guard: Retain the empty wrapper at zero credit and split activation, skill, and source reads into exact bounded probes.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-001-F, V6612-X1-METHOD-001-P

### V6612-X1-METHOD-002 — Bounded recovery for first-skill-inventory-foreach-pipeline-hit-powershell-empty-pipe-syntax-error

- Trigger: first-skill-inventory-foreach-pipeline-hit-powershell-empty-pipe-syntax-error
- Method: Retain the parser rejection at zero credit and materialize the array before JSON projection.
- Recurrence guard: Retain the parser rejection at zero credit and materialize the array before JSON projection.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-002-F, V6612-X1-METHOD-002-P

### V6612-X1-METHOD-003 — Bounded recovery for combined-skill-display-truncated-before-all-required-skill-eofs

- Trigger: combined-skill-display-truncated-before-all-required-skill-eofs
- Method: Retain the partial display at zero credit and reread each selected skill and reference individually through EOF.
- Recurrence guard: Retain the partial display at zero credit and reread each selected skill and reference individually through EOF.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-003-F, V6612-X1-METHOD-003-P

### V6612-X1-METHOD-004 — Bounded recovery for one-shot-authorization-state-display-truncated-before-eof

- Trigger: one-shot-authorization-state-display-truncated-before-eof
- Method: Retain the truncated projection at zero credit and read the exact current-state file in deterministic numbered windows.
- Recurrence guard: Retain the truncated projection at zero credit and read the exact current-state file in deterministic numbered windows.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-004-F, V6612-X1-METHOD-004-P

### V6612-X1-METHOD-005 — Bounded recovery for broad-d-drive-canonical-receipt-search-exceeded-the-bounded-time-window

- Trigger: broad-d-drive-canonical-receipt-search-exceeded-the-bounded-time-window
- Method: Retain the timed-out search at zero credit, stop only its verified read-only process, and use bounded top-level receipt discovery.
- Recurrence guard: Retain the timed-out search at zero credit, stop only its verified read-only process, and use bounded top-level receipt discovery.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-005-F, V6612-X1-METHOD-005-P

### V6612-X1-METHOD-006 — Bounded recovery for exec-session-cancel-attempt-used-an-unsupported-write-stdin-route

- Trigger: exec-session-cancel-attempt-used-an-unsupported-write-stdin-route
- Method: Retain the unsupported cancellation attempt at zero credit and stop only the exact verified read-only search process by process identifier.
- Recurrence guard: Retain the unsupported cancellation attempt at zero credit and stop only the exact verified read-only search process by process identifier.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-006-F, V6612-X1-METHOD-006-P

### V6612-X1-METHOD-007 — Bounded recovery for first-top-level-directory-projection-hit-powershell-empty-pipe-syntax-error

- Trigger: first-top-level-directory-projection-hit-powershell-empty-pipe-syntax-error
- Method: Retain the parser rejection at zero credit and materialize the directory rows before projection.
- Recurrence guard: Retain the parser rejection at zero credit and materialize the directory rows before projection.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-007-F, V6612-X1-METHOD-007-P

### V6612-X1-METHOD-008 — Bounded recovery for combined-local-git-probe-hit-powershell-parenthesized-command-parse-errors

- Trigger: combined-local-git-probe-hit-powershell-parenthesized-command-parse-errors
- Method: Retain the parser rejection at zero credit and recover with scalar head, branch, divergence, and cleanliness probes.
- Recurrence guard: Retain the parser rejection at zero credit and recover with scalar head, branch, divergence, and cleanliness probes.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-008-F, V6612-X1-METHOD-008-P

### V6612-X1-METHOD-009 — Bounded recovery for first-x2-manifest-replay-compared-the-evidence-manifest-against-the-later-final-tree

- Trigger: first-x2-manifest-replay-compared-the-evidence-manifest-against-the-later-final-tree
- Method: Retain the three expected lifecycle mismatches at zero credit and replay the x2 manifest at the immutable evidence commit, where all entries matched.
- Recurrence guard: Retain the three expected lifecycle mismatches at zero credit and replay the x2 manifest at the immutable evidence commit, where all entries matched.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-009-F, V6612-X1-METHOD-009-P

### V6612-X1-METHOD-010 — Bounded recovery for broad-worktree-proposal-index-search-exceeded-the-bounded-time-window

- Trigger: broad-worktree-proposal-index-search-exceeded-the-bounded-time-window
- Method: Retain the timed-out search at zero credit, stop only its verified read-only process, and resolve the exact index path with Git tree metadata.
- Recurrence guard: Retain the timed-out search at zero credit, stop only its verified read-only process, and resolve the exact index path with Git tree metadata.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-010-F, V6612-X1-METHOD-010-P

### V6612-X1-METHOD-011 — Bounded recovery for broad-domain-collision-projection-exceeded-the-output-budget

- Trigger: broad-domain-collision-projection-exceeded-the-output-budget
- Method: Retain the truncated projection at zero credit and use structured JSON counts plus bounded samples for each candidate domain.
- Recurrence guard: Retain the truncated projection at zero credit and use structured JSON counts plus bounded samples for each candidate domain.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-011-F, V6612-X1-METHOD-011-P

### V6612-X1-METHOD-012 — Bounded recovery for planetarium-lens-collided-with-seven-exact-frozen-proposals

- Trigger: planetarium-lens-collided-with-seven-exact-frozen-proposals
- Method: Retain the rejected lens at zero credit and choose no planetarium proposal.
- Recurrence guard: Retain the rejected lens at zero credit and choose no planetarium proposal.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-012-F, V6612-X1-METHOD-012-P

### V6612-X1-METHOD-013 — Bounded recovery for stained-glass-lens-collided-with-two-frozen-phase-families

- Trigger: stained-glass-lens-collided-with-two-frozen-phase-families
- Method: Retain the rejected lens at zero credit and choose no stained-glass proposal.
- Recurrence guard: Retain the rejected lens at zero credit and choose no stained-glass proposal.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-013-F, V6612-X1-METHOD-013-P

### V6612-X1-METHOD-014 — Bounded recovery for carillon-lens-collided-with-the-frozen-change-ringing-phase-family

- Trigger: carillon-lens-collided-with-the-frozen-change-ringing-phase-family
- Method: Retain the rejected lens at zero credit and choose no bell, carillon, or change-ringing proposal.
- Recurrence guard: Retain the rejected lens at zero credit and choose no bell, carillon, or change-ringing proposal.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-014-F, V6612-X1-METHOD-014-P

### V6612-X1-METHOD-015 — Bounded recovery for worktree-add-wrapper-yielded-before-its-authorized-child-checkout-finished

- Trigger: worktree-add-wrapper-yielded-before-its-authorized-child-checkout-finished
- Method: Retain the premature wrapper state at zero credit and wait for the exact authorized Git process tree to finish naturally.
- Recurrence guard: Retain the premature wrapper state at zero credit and wait for the exact authorized Git process tree to finish naturally.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-015-F, V6612-X1-METHOD-015-P

### V6612-X1-METHOD-016 — Bounded recovery for premature-status-probe-observed-in-progress-index-deletions-during-authorized-checkout

- Trigger: premature-status-probe-observed-in-progress-index-deletions-during-authorized-checkout
- Method: Retain the transient observation at zero credit, make no repair, and recheck only after the exact worktree-add process completed.
- Recurrence guard: Retain the transient observation at zero credit, make no repair, and recheck only after the exact worktree-add process completed.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-016-F, V6612-X1-METHOD-016-P

### V6612-X1-METHOD-017 — Bounded recovery for bounded-restore-preflight-refused-while-authorized-git-checkout-processes-were-live

- Trigger: bounded-restore-preflight-refused-while-authorized-git-checkout-processes-were-live
- Method: Retain the refused recovery at zero credit, perform no restore, wait for natural completion, and prove the resulting worktree clean.
- Recurrence guard: Retain the refused recovery at zero credit, perform no restore, wait for natural completion, and prove the resulting worktree clean.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-017-F, V6612-X1-METHOD-017-P

### V6612-X1-METHOD-018 — Bounded recovery for first-read-only-data-summary-wrapper-lost-python-raw-string-quotes-at-the-powershell-boundary

- Trigger: first-read-only-data-summary-wrapper-lost-python-raw-string-quotes-at-the-powershell-boundary
- Method: Retain the syntax rejection at zero credit and bind the module path process-locally with a quote-simple inspection command.
- Recurrence guard: Retain the syntax rejection at zero credit and bind the module path process-locally with a quote-simple inspection command.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-018-F, V6612-X1-METHOD-018-P

### V6612-X1-METHOD-019 — Bounded recovery for second-read-only-data-summary-wrapper-lost-python-subscript-quotes-in-native-argument-marshalling

- Trigger: second-read-only-data-summary-wrapper-lost-python-subscript-quotes-in-native-argument-marshalling
- Method: Retain the name-resolution rejection at zero credit and stream the bounded inspection program to Python standard input instead of using a native command-line code argument.
- Recurrence guard: Retain the name-resolution rejection at zero credit and stream the bounded inspection program to Python standard input instead of using a native command-line code argument.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-019-F, V6612-X1-METHOD-019-P

### V6612-X1-METHOD-020 — Bounded recovery for first-complete-novelty-screen-passed-eighteen-of-twenty-and-rejected-two-template-neighbour-titles

- Trigger: first-complete-novelty-screen-passed-eighteen-of-twenty-and-rejected-two-template-neighbour-titles
- Method: Retain the eighteen-of-twenty witness at zero credit, preserve the threshold, and replace the terminal-deficit, handover, comparison, and near-neighbour network formulations with domain-specific mechanisms.
- Recurrence guard: Retain the eighteen-of-twenty witness at zero credit, preserve the threshold, and replace the terminal-deficit, handover, comparison, and near-neighbour network formulations with domain-specific mechanisms.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-020-F, V6612-X1-METHOD-020-P

### V6612-X1-METHOD-021 — Bounded recovery for first-current-x1-suite-passed-twenty-one-of-twenty-three-and-found-two-missing-family-tool-receipt-families

- Trigger: first-current-x1-suite-passed-twenty-one-of-twenty-three-and-found-two-missing-family-tool-receipt-families
- Method: Retain the failed aggregate at zero credit, materialize only the declared workflow, governance, index, reflection, Method Flow, and meta-tool receipts, refresh manifests, and rerun the scoped x1 module once.
- Recurrence guard: Retain the failed aggregate at zero credit, materialize only the declared workflow, governance, index, reflection, Method Flow, and meta-tool receipts, refresh manifests, and rerun the scoped x1 module once.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-021-F, V6612-X1-METHOD-021-P

### V6612-X1-METHOD-022 — Bounded recovery for intentional-invalid-workflow-fixture-was-rejected-on-the-messaging-boundary

- Trigger: intentional-invalid-workflow-fixture-was-rejected-on-the-messaging-boundary
- Method: Retain the rejecting workflow witness at zero credit, preserve its issue packet, and use the separately corrected request without changing the authorized route.
- Recurrence guard: Retain the rejecting workflow witness at zero credit, preserve its issue packet, and use the separately corrected request without changing the authorized route.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6612-X1-METHOD-022-F, V6612-X1-METHOD-022-P

## Retained boundary

Same-owner workflow evidence only; no independent reproduction or protected-gate closure.
