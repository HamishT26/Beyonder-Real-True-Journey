# GHC Family Method Flow State

- Phase: v659-v2
- Owner: Auren Lark
- Methods: 8
- Passing witnesses: 8
- Failed witnesses retained: 8

## Preferred methods

### V6592-X1-METHOD-001 — Bounded recovery for first-tool-call-assumed-unavailable-shell-command-surface

- Trigger: first-tool-call-assumed-unavailable-shell-command-surface
- Method: Use the installed exec-command surface and keep subsequent repository probes bounded and literal.
- Recurrence guard: Use the installed exec-command surface and keep subsequent repository probes bounded and literal.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6592-X1-METHOD-001-F, V6592-X1-METHOD-001-P

### V6592-X1-METHOD-002 — Bounded recovery for first-activation-baton-read-truncated-after-line-180

- Trigger: first-activation-baton-read-truncated-after-line-180
- Method: Read the exact Git object contiguously in bounded forty-line windows through EOF and verify total line and word counts.
- Recurrence guard: Read the exact Git object contiguously in bounded forty-line windows through EOF and verify total line and word counts.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6592-X1-METHOD-002-F, V6592-X1-METHOD-002-P

### V6592-X1-METHOD-003 — Bounded recovery for parallel-three-window-baton-render-exceeded-model-context

- Trigger: parallel-three-window-baton-render-exceeded-model-context
- Method: Stop parallel rendering and complete the same immutable baton sequentially with nonoverlapping bounded windows.
- Recurrence guard: Stop parallel rendering and complete the same immutable baton sequentially with nonoverlapping bounded windows.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6592-X1-METHOD-003-F, V6592-X1-METHOD-003-P

### V6592-X1-METHOD-004 — Bounded recovery for broad-repository-path-discovery-returned-truncated-historical-listing

- Trigger: broad-repository-path-discovery-returned-truncated-historical-listing
- Method: Restrict path discovery to the current v659 source owner, exact phase, and named activation artifacts.
- Recurrence guard: Restrict path discovery to the current v659 source owner, exact phase, and named activation artifacts.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6592-X1-METHOD-004-F, V6592-X1-METHOD-004-P

### V6592-X1-METHOD-005 — Bounded recovery for backend-rejected-write-stdin-control-c-on-noninteractive-session

- Trigger: backend-rejected-write-stdin-control-c-on-noninteractive-session
- Method: Do not inject control bytes; poll the yielded command with the supported wait surface and inspect its terminal result.
- Recurrence guard: Do not inject control bytes; poll the yielded command with the supported wait surface and inspect its terminal result.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6592-X1-METHOD-005-F, V6592-X1-METHOD-005-P

### V6592-X1-METHOD-006 — Bounded recovery for powershell-materialized-statistics-probe-used-an-empty-pipe-element

- Trigger: powershell-materialized-statistics-probe-used-an-empty-pipe-element
- Method: Materialize the foreach results into a task-specific variable before sorting and projecting bounded scalar output.
- Recurrence guard: Materialize the foreach results into a task-specific variable before sorting and projecting bounded scalar output.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6592-X1-METHOD-006-F, V6592-X1-METHOD-006-P

### V6592-X1-METHOD-007 — Bounded recovery for broad-receipt-filename-search-exceeded-useful-owner-local-bound

- Trigger: broad-receipt-filename-search-exceeded-useful-owner-local-bound
- Method: Stop the broad search, inspect the exact owner and phase receipt directory, and verify the successful receipt by supplied SHA-256.
- Recurrence guard: Stop the broad search, inspect the exact owner and phase receipt directory, and verify the successful receipt by supplied SHA-256.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6592-X1-METHOD-007-F, V6592-X1-METHOD-007-P

### V6592-X1-METHOD-008 — Bounded recovery for first-owned-lane-absence-preflight-had-powershell-cast-and-semicolon-parse-error

- Trigger: first-owned-lane-absence-preflight-had-powershell-cast-and-semicolon-parse-error
- Method: Capture each Git exit code separately, resolve literal branch and path targets, then create one additive Auren-owned worktree from the verified immutable source.
- Recurrence guard: Capture each Git exit code separately, resolve literal branch and path targets, then create one additive Auren-owned worktree from the verified immutable source.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6592-X1-METHOD-008-F, V6592-X1-METHOD-008-P

## Retained boundary

Same-owner workflow evidence only; no independent reproduction or protected-gate closure.
