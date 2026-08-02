# GHC Family Method Flow State

- Phase: v658-v8-2-remaster
- Owner: Lyren Moss
- Methods: 12
- Passing witnesses: 12
- Failed witnesses retained: 12

## Preferred methods

### V6588R2-X1-METHOD-001 — Bounded recovery for powershell-empty-pipe-element-during-skill-inventory

- Trigger: powershell-empty-pipe-element-during-skill-inventory
- Method: Materialize foreach rows before piping to ConvertTo-Json.
- Recurrence guard: Materialize foreach rows before piping to ConvertTo-Json.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6588R2-X1-METHOD-001-F, V6588R2-X1-METHOD-001-P

### V6588R2-X1-METHOD-002 — Bounded recovery for archive-container-guessed-as-git-root

- Trigger: archive-container-guessed-as-git-root
- Method: Resolve the repository from the verified Lyren worktree before Git probes.
- Recurrence guard: Resolve the repository from the verified Lyren worktree before Git probes.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6588R2-X1-METHOD-002-F, V6588R2-X1-METHOD-002-P

### V6588R2-X1-METHOD-003 — Bounded recovery for workflow-plan-safe-candidate-cap-too-high

- Trigger: workflow-plan-safe-candidate-cap-too-high
- Method: Correct only the declared cap from 2,000 to the schema maximum of 1,000.
- Recurrence guard: Correct only the declared cap from 2,000 to the schema maximum of 1,000.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6588R2-X1-METHOD-003-F, V6588R2-X1-METHOD-003-P

### V6588R2-X1-METHOD-004 — Bounded recovery for live-route-narrative-conflict-ilyra-next

- Trigger: live-route-narrative-conflict-ilyra-next
- Method: Use the explicit numbered Ilyra-to-Auren v659-v2 edge and retain the later Sable phrase as drift.
- Recurrence guard: Use the explicit numbered Ilyra-to-Auren v659-v2 edge and retain the later Sable phrase as drift.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6588R2-X1-METHOD-004-F, V6588R2-X1-METHOD-004-P

### V6588R2-X1-METHOD-005 — Bounded recovery for python-zoneinfo-tzdata-missing

- Trigger: python-zoneinfo-tzdata-missing
- Method: Use the verified New Zealand Windows host's offset-bearing local timezone conversion without adding a dependency.
- Recurrence guard: Use the verified New Zealand Windows host's offset-bearing local timezone conversion without adding a dependency.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6588R2-X1-METHOD-005-F, V6588R2-X1-METHOD-005-P

### V6588R2-X1-METHOD-006 — Bounded recovery for auth-validator-help-resolved-from-roster-skill-directory

- Trigger: auth-validator-help-resolved-from-roster-skill-directory
- Method: Resolve and invoke each family validator from its own exact skill directory.
- Recurrence guard: Resolve and invoke each family validator from its own exact skill directory.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6588R2-X1-METHOD-006-F, V6588R2-X1-METHOD-006-P

### V6588R2-X1-METHOD-007 — Bounded recovery for method-flow-derived-counts-stale-before-packet-refresh

- Trigger: method-flow-derived-counts-stale-before-packet-refresh
- Method: Regenerate the append-only ledger after recording the newest failure, then rerun only the isolated Method Flow validator.
- Recurrence guard: Regenerate the append-only ledger after recording the newest failure, then rerun only the isolated Method Flow validator.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6588R2-X1-METHOD-007-F, V6588R2-X1-METHOD-007-P

### V6588R2-X1-METHOD-008 — Bounded recovery for reflection-remaster-free-text-focus-matched-zero-surfaces

- Trigger: reflection-remaster-free-text-focus-matched-zero-surfaces
- Method: Rerun only the read-only selector with repeated exact family-current focus terms.
- Recurrence guard: Rerun only the read-only selector with repeated exact family-current focus terms.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6588R2-X1-METHOD-008-F, V6588R2-X1-METHOD-008-P

### V6588R2-X1-METHOD-009 — Bounded recovery for meta-tool-box-query-kind-script-unsupported

- Trigger: meta-tool-box-query-kind-script-unsupported
- Method: Use the catalogue's declared workflow kind and retain the rejected query as zero credit.
- Recurrence guard: Use the catalogue's declared workflow kind and retain the rejected query as zero credit.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6588R2-X1-METHOD-009-F, V6588R2-X1-METHOD-009-P

### V6588R2-X1-METHOD-010 — Bounded recovery for legacy-startup-builder-help-token-triggered-default-v640-write

- Trigger: legacy-startup-builder-help-token-triggered-default-v640-write
- Method: Remove only the three invocation-owned legacy outputs, preserve inherited bytes, and gate the legacy builder as inapplicable to the remaster lane.
- Recurrence guard: Remove only the three invocation-owned legacy outputs, preserve inherited bytes, and gate the legacy builder as inapplicable to the remaster lane.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6588R2-X1-METHOD-010-F, V6588R2-X1-METHOD-010-P

### V6588R2-X1-METHOD-011 — Bounded recovery for staged-byte-mojibake-regex-console-transcoding-error

- Trigger: staged-byte-mojibake-regex-console-transcoding-error
- Method: Use literal UTF-8 byte containment for mojibake sentinels and rerun the staged-byte validator from the beginning.
- Recurrence guard: Use literal UTF-8 byte containment for mojibake sentinels and rerun the staged-byte validator from the beginning.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6588R2-X1-METHOD-011-F, V6588R2-X1-METHOD-011-P

### V6588R2-X1-METHOD-012 — Bounded recovery for staged-manifest-line-ending-drift-and-unanchored-sk-prefix

- Trigger: staged-manifest-line-ending-drift-and-unanchored-sk-prefix
- Method: Normalize owner-packet text to LF before manifesting and anchor credential prefixes at a non-word boundary.
- Recurrence guard: Normalize owner-packet text to LF before manifesting and anchor credential prefixes at a non-word boundary.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6588R2-X1-METHOD-012-F, V6588R2-X1-METHOD-012-P

## Retained boundary

Same-owner workflow evidence only; no independent reproduction or protected-gate closure.
