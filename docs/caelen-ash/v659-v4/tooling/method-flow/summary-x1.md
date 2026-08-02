# GHC Family Method Flow State

- Phase: v659-v4
- Owner: Caelen Ash
- Methods: 15
- Passing witnesses: 15
- Failed witnesses retained: 15

## Preferred methods

### V6594-X1-METHOD-001 — Bounded recovery for initial-memory-registry-probe-used-a-nonexistent-relative-memory-path

- Trigger: initial-memory-registry-probe-used-a-nonexistent-relative-memory-path
- Method: Use the documented literal memories/MEMORY.md path, retain the failed path assumption, and treat live v659 activation as authoritative over historical memory.
- Recurrence guard: Use the documented literal memories/MEMORY.md path, retain the failed path assumption, and treat live v659 activation as authoritative over historical memory.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6594-X1-METHOD-001-F, V6594-X1-METHOD-001-P

### V6594-X1-METHOD-002 — Bounded recovery for first-skill-inventory-piped-foreach-output-directly-and-triggered-an-empty-pipe-element

- Trigger: first-skill-inventory-piped-foreach-output-directly-and-triggered-an-empty-pipe-element
- Method: Materialize foreach output into a task-specific array before sorting, projecting, or JSON serialization.
- Recurrence guard: Materialize foreach output into a task-specific array before sorting, projecting, or JSON serialization.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6594-X1-METHOD-002-F, V6594-X1-METHOD-002-P

### V6594-X1-METHOD-003 — Bounded recovery for skill-inventory-repeated-the-known-direct-foreach-pipeline-parser-failure

- Trigger: skill-inventory-repeated-the-known-direct-foreach-pipeline-parser-failure
- Method: Retain the recurrence separately and apply the materialized-array guard before every later multi-row PowerShell projection.
- Recurrence guard: Retain the recurrence separately and apply the materialized-array guard before every later multi-row PowerShell projection.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6594-X1-METHOD-003-F, V6594-X1-METHOD-003-P

### V6594-X1-METHOD-004 — Bounded recovery for artifact-reference-search-used-an-invalid-optional-token-regex

- Trigger: artifact-reference-search-used-an-invalid-optional-token-regex
- Method: Use an ASCII-safe literal alternation without a bare repetition operator and preserve the failed search at zero credit.
- Recurrence guard: Use an ASCII-safe literal alternation without a bare repetition operator and preserve the failed search at zero credit.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6594-X1-METHOD-004-F, V6594-X1-METHOD-004-P

### V6594-X1-METHOD-005 — Bounded recovery for parallel-source-status-probe-outlived-its-wrapper-and-lost-the-original-session-handle

- Trigger: parallel-source-status-probe-outlived-its-wrapper-and-lost-the-original-session-handle
- Method: Confirm the original Git process terminated, then split tracked cleanliness and untracked-path checks into separate bounded scalar probes.
- Recurrence guard: Confirm the original Git process terminated, then split tracked cleanliness and untracked-path checks into separate bounded scalar probes.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6594-X1-METHOD-005-F, V6594-X1-METHOD-005-P

### V6594-X1-METHOD-006 — Bounded recovery for proposal-index-probe-assumed-a-nonexistent-rows-array

- Trigger: proposal-index-probe-assumed-a-nonexistent-rows-array
- Method: Inspect exact top-level JSON keys first, then combine prior_proposals and new_proposals according to the committed schema.
- Recurrence guard: Inspect exact top-level JSON keys first, then combine prior_proposals and new_proposals according to the committed schema.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6594-X1-METHOD-006-F, V6594-X1-METHOD-006-P

### V6594-X1-METHOD-007 — Bounded recovery for first-official-source-search-wrapper-assumed-a-content-array-and-rendered-no-usable-result

- Trigger: first-official-source-search-wrapper-assumed-a-content-array-and-rendered-no-usable-result
- Method: Serialize the installed web result directly, narrow to official domains, and retain the first empty rendering at zero credit.
- Recurrence guard: Serialize the installed web result directly, narrow to official domains, and retain the first empty rendering at zero credit.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6594-X1-METHOD-007-F, V6594-X1-METHOD-007-P

### V6594-X1-METHOD-008 — Bounded recovery for first-semantic-data-patch-failed-closed-on-an-inherited-unicode-byte-mismatch

- Trigger: first-semantic-data-patch-failed-closed-on-an-inherited-unicode-byte-mismatch
- Method: Split the change into smaller ASCII-anchored hunks and replace Unicode authority wording only against exact UTF-8 text.
- Recurrence guard: Split the change into smaller ASCII-anchored hunks and replace Unicode authority wording only against exact UTF-8 text.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6594-X1-METHOD-008-F, V6594-X1-METHOD-008-P

### V6594-X1-METHOD-009 — Bounded recovery for official-source-list-replacement-failed-closed-on-a-second-inherited-unicode-byte-mismatch

- Trigger: official-source-list-replacement-failed-closed-on-a-second-inherited-unicode-byte-mismatch
- Method: Preserve the inherited list under an explicit legacy name and add the verified Caelen source list separately without byte-sensitive replacement.
- Recurrence guard: Preserve the inherited list under an explicit legacy name and add the verified Caelen source list separately without byte-sensitive replacement.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6594-X1-METHOD-009-F, V6594-X1-METHOD-009-P

### V6594-X1-METHOD-010 — Bounded recovery for first-x1-test-update-failed-closed-on-the-same-inherited-unicode-byte-mismatch

- Trigger: first-x1-test-update-failed-closed-on-the-same-inherited-unicode-byte-mismatch
- Method: Separate ASCII-only assertions from the exact UTF-8 authority assertion and keep all three failed patches independently visible.
- Recurrence guard: Separate ASCII-only assertions from the exact UTF-8 authority assertion and keep all three failed patches independently visible.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6594-X1-METHOD-010-F, V6594-X1-METHOD-010-P

### V6594-X1-METHOD-011 — Bounded recovery for first-precommit-summary-typed-a-property-name-as-a-powershell-command-and-yielded-before-terminal-output

- Trigger: first-precommit-summary-typed-a-property-name-as-a-powershell-command-and-yielded-before-terminal-output
- Method: Follow the original process to completion, retain the typo at zero credit, and use direct property projection in later scalar summaries.
- Recurrence guard: Follow the original process to completion, retain the typo at zero credit, and use direct property projection in later scalar summaries.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6594-X1-METHOD-011-F, V6594-X1-METHOD-011-P

### V6594-X1-METHOD-012 — Bounded recovery for workflow-skill-fixture-validator-was-pointed-at-the-flat-phase-refinement-output

- Trigger: workflow-skill-fixture-validator-was-pointed-at-the-flat-phase-refinement-output
- Method: Retain the missing-fixture-path failure at zero credit, distinguish the skill-package fixture validator from the phase-plan runner, and run the bounded refinement only against the regenerated request that includes this failure.
- Recurrence guard: Retain the missing-fixture-path failure at zero credit, distinguish the skill-package fixture validator from the phase-plan runner, and run the bounded refinement only against the regenerated request that includes this failure.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6594-X1-METHOD-012-F, V6594-X1-METHOD-012-P

### V6594-X1-METHOD-013 — Bounded recovery for combined-prestage-status-wrapper-completed-without-a-scalar-receipt

- Trigger: combined-prestage-status-wrapper-completed-without-a-scalar-receipt
- Method: Retain the missing summary at zero credit and split the empty-index proof from later bounded status and allowlist checks.
- Recurrence guard: Retain the missing summary at zero credit and split the empty-index proof from later bounded status and allowlist checks.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6594-X1-METHOD-013-F, V6594-X1-METHOD-013-P

### V6594-X1-METHOD-014 — Bounded recovery for first-index-review-summary-projected-guessed-null-field-names-from-four-valid-receipts

- Trigger: first-index-review-summary-projected-guessed-null-field-names-from-four-valid-receipts
- Method: Retain the incomplete scalar projection at zero credit, inspect each exact top-level key set, and use only the committed schema fields in the corrected staged review.
- Recurrence guard: Retain the incomplete scalar projection at zero credit, inspect each exact top-level key set, and use only the committed schema fields in the corrected staged review.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6594-X1-METHOD-014-F, V6594-X1-METHOD-014-P

### V6594-X1-METHOD-015 — Bounded recovery for second-index-review-assumed-a-lowercase-route-state-value-in-two-valid-receipts

- Trigger: second-index-review-assumed-a-lowercase-route-state-value-in-two-valid-receipts
- Method: Retain the failed two-check review at zero credit, inspect the exact staged values, and compare the declared uppercase held-state literal without changing route state.
- Recurrence guard: Retain the failed two-check review at zero credit, inspect the exact staged values, and compare the declared uppercase held-state literal without changing route state.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6594-X1-METHOD-015-F, V6594-X1-METHOD-015-P

## Retained boundary

Same-owner workflow evidence only; no independent reproduction or protected-gate closure.
