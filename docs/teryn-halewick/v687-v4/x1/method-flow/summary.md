# GHC Family Method Flow State

- Phase: v687-v4
- Owner: Teryn Halewick
- Methods: 8
- Passing witnesses: 8
- Failed witnesses retained: 8

## Preferred methods

### TH6874-START-M001 — wrong-working-directory-git-probe

- Trigger: The calling settings directory is not a Git worktree.
- Method: Use the supplied immutable source worktree.
- Recurrence guard: Inspect actual filenames and result metadata; bound output before reading; retain failure before recovery.
- Rollback: Stop the affected read. Preserve source and existing records.
- Witnesses: TH6874-START-M001-F, TH6874-START-M001-P

### TH6874-START-M002 — first-activation-display-truncated

- Trigger: A combined readout exceeded its output budget.
- Method: Read all unique lines with source line numbers and recover truncated windows.
- Recurrence guard: Inspect actual filenames and result metadata; bound output before reading; retain failure before recovery.
- Rollback: Stop the affected read. Preserve source and existing records.
- Witnesses: TH6874-START-M002-F, TH6874-START-M002-P

### TH6874-START-M003 — deduplicated-activation-display-still-truncated

- Trigger: An oversized unique-line chunk exceeded the wrapper budget.
- Method: Set both output budgets and use bounded source-line windows.
- Recurrence guard: Inspect actual filenames and result metadata; bound output before reading; retain failure before recovery.
- Rollback: Stop the affected read. Preserve source and existing records.
- Witnesses: TH6874-START-M003-F, TH6874-START-M003-P

### TH6874-START-M004 — assumed-source-receipt-layout-absent

- Trigger: The guessed nested owner and phase receipt directory was absent.
- Method: Read the source final artifact pointers and verify exact observed paths.
- Recurrence guard: Inspect actual filenames and result metadata; bound output before reading; retain failure before recovery.
- Rollback: Stop the affected read. Preserve source and existing records.
- Witnesses: TH6874-START-M004-F, TH6874-START-M004-P

### TH6874-START-M005 — release-profile-reference-basename-absent

- Trigger: The addendum shorthand profile filename was absent in the index reference folder.
- Method: Enumerate only the two named reference folders and use the observed current profile.
- Recurrence guard: Inspect actual filenames and result metadata; bound output before reading; retain failure before recovery.
- Rollback: Stop the affected read. Preserve source and existing records.
- Witnesses: TH6874-START-M005-F, TH6874-START-M005-P

### TH6874-START-M006 — combined-historical-auth-read-truncated

- Trigger: A historical route state exceeded the combined read budget.
- Method: Read bounded slices and apply the newer explicit release for current ownership.
- Recurrence guard: Inspect actual filenames and result metadata; bound output before reading; retain failure before recovery.
- Rollback: Stop the affected read. Preserve source and existing records.
- Witnesses: TH6874-START-M006-F, TH6874-START-M006-P

### TH6874-START-M007 — running-search-envelope-not-projected

- Trigger: A search wrapper projected output without retaining a running-process handle.
- Method: Audit the bounded matching process and recover through exact source artifact pointers.
- Recurrence guard: Inspect actual filenames and result metadata; bound output before reading; retain failure before recovery.
- Rollback: Stop the affected read. Preserve source and existing records.
- Witnesses: TH6874-START-M007-F, TH6874-START-M007-P

### TH6874-START-M008 — source-task-readout-exceeded-budget

- Trigger: One source-task read included a large completed turn.
- Method: Keep its native envelope private and inspect only the final artifact pointers.
- Recurrence guard: Inspect actual filenames and result metadata; bound output before reading; retain failure before recovery.
- Rollback: Stop the affected read. Preserve source and existing records.
- Witnesses: TH6874-START-M008-F, TH6874-START-M008-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
