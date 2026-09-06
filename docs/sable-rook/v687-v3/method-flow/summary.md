# GHC Family Method Flow State

- Phase: v687-v3
- Owner: Sable Rook
- Methods: 7
- Passing witnesses: 7
- Failed witnesses retained: 7

## Preferred methods

### SR6873-START-M001 — PowerShell native-command sequencing

- Trigger: Windows PowerShell; fresh Sable-owned v687-v3 startup
- Method: Run the native command first, capture LASTEXITCODE, then construct the summary object.
- Recurrence guard: Run the native command first, capture LASTEXITCODE, then construct the summary object.
- Rollback: Stop in the owner lane; preserve source and sibling lanes read-only.
- Witnesses: SR6873-START-W001-F, SR6873-START-W001-P

### SR6873-START-M002 — Bounded collision scalar probes

- Trigger: Windows PowerShell; fresh Sable-owned v687-v3 startup
- Method: Split local branch, filesystem path, worktree registry, D capacity, and live remote into bounded scalar probes.
- Recurrence guard: Split local branch, filesystem path, worktree registry, D capacity, and live remote into bounded scalar probes.
- Rollback: Stop in the owner lane; preserve source and sibling lanes read-only.
- Witnesses: SR6873-START-W002-F, SR6873-START-W002-P

### SR6873-START-M003 — Fresh no-checkout index initialization

- Trigger: Windows PowerShell; fresh Sable-owned v687-v3 startup
- Method: After locks and processes quiesce, populate the fresh exact-source index with git read-tree -mu HEAD and reapply sparse rules.
- Recurrence guard: After locks and processes quiesce, populate the fresh exact-source index with git read-tree -mu HEAD and reapply sparse rules.
- Rollback: Stop in the owner lane; preserve source and sibling lanes read-only.
- Witnesses: SR6873-START-W003-F, SR6873-START-W003-P

### SR6873-START-M004 — Supported workflow messaging token

- Trigger: Windows PowerShell; fresh Sable-owned v687-v3 startup
- Method: Preserve the failed packet and replace only the unsupported token with declared_endpoint_only_after_terminal_gate.
- Recurrence guard: Preserve the failed packet and replace only the unsupported token with declared_endpoint_only_after_terminal_gate.
- Rollback: Stop in the owner lane; preserve source and sibling lanes read-only.
- Witnesses: SR6873-START-W004-F, SR6873-START-W004-P

### SR6873-START-M005 — Exact reflection-runner path

- Trigger: Windows PowerShell; fresh Sable-owned v687-v3 startup
- Method: Enumerate the installed skill scripts, select ghc_family_reflection_remaster.py, and rerun only the reflection audit.
- Recurrence guard: Enumerate the installed skill scripts, select ghc_family_reflection_remaster.py, and rerun only the reflection audit.
- Rollback: Stop in the owner lane; preserve source and sibling lanes read-only.
- Witnesses: SR6873-START-W005-F, SR6873-START-W005-P

### SR6873-START-M006 — Method Flow next-state inspection

- Trigger: Windows PowerShell; fresh Sable-owned v687-v3 startup
- Method: Inspect the append-only ledger after a passing witness and request only the remaining validated-to-preferred transition.
- Recurrence guard: Inspect the append-only ledger after a passing witness and request only the remaining validated-to-preferred transition.
- Rollback: Stop in the owner lane; preserve source and sibling lanes read-only.
- Witnesses: SR6873-START-W006-F, SR6873-START-W006-P

### SR6873-START-M007 — Normalized-LF staged manifest domain

- Trigger: Windows PowerShell; fresh Sable-owned v687-v3 startup
- Method: Declare normalized-LF bytes for text manifest entries and compare the staged Git blob in that same domain.
- Recurrence guard: Declare normalized-LF bytes for text manifest entries and compare the staged Git blob in that same domain.
- Rollback: Stop in the owner lane; preserve source and sibling lanes read-only.
- Witnesses: SR6873-START-W007-F, SR6873-START-W007-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
