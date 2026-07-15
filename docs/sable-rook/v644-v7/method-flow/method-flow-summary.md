# GHC Family Method Flow State

- Phase: v644-gmut-thos-v7-x1-x2
- Owner: Sable Rook
- Methods: 8
- Passing witnesses: 7
- Failed witnesses retained: 0

## Preferred methods

### V6447-M02 — Standalone complete reads for mandatory skills and references

- Trigger: multiple full instruction files; repository discovery; one shared orchestration envelope
- Method: Read every mandatory skill and directly required reference completely in its own bounded command before task actions, then run discovery separately.
- Recurrence guard: Never infer a complete instruction read from a timed-out batch; preserve the timeout and obtain one end-to-end witness per mandatory file.
- Rollback: Discard only the incomplete batch result, retain its negative, and reread each authoritative instruction source directly.
- Witnesses: V6447-M02-W01

### V6447-M03 — Newest-task-group and same-day-note memory fallback

- Trigger: exact keyword query; registry summaries; newest same-day extension note
- Method: Treat exit 1 as a no-match result, inspect the current exact-head task group in the registry, and read only the newest directly relevant same-day note.
- Recurrence guard: A no-match query cannot establish absence; use the newest indexed task group and bounded ad-hoc note before stopping.
- Rollback: Retain the no-match receipt and avoid broad rollout scans unless the bounded fallback remains insufficient.
- Witnesses: V6447-M03-W01

### V6447-M04 — Separated network, ancestry, equality, and cleanliness witnesses

- Trigger: network fetch; large-worktree status; live remote lookup; anchor ancestry; parallel parent envelope
- Method: Run fetch, local anchor ancestry, live-remote equality, owner ancestry, and named-lane cleanliness as separate exact witnesses with measured envelopes.
- Recurrence guard: Do not combine network and large-status operations under a shorter parent ceiling; record exact hashes from each completed witness.
- Rollback: Retain the timed-out batch, make no mutation from it, and require all standalone witnesses before fast-forward.
- Witnesses: V6447-M04-W01

### V6447-M05 — Explicit no-match normalization for semantic novelty probes

- Trigger: absence is an expected semantic result; ripgrep exit code 1; orchestrated multi-query sequence
- Method: Map exit 1 to an explicit NO_MATCH witness, keep other nonzero codes as faults, and audit the exact 29 proposal files covering all 290 frozen proposals.
- Recurrence guard: State no-match semantics explicitly and never let one expected absence suppress later collision categories.
- Rollback: Retain the interrupted batch and rerun the full bounded category set before freezing any proposal.
- Witnesses: V6447-M05-W01

### V6447-M06 — Non-elevating Windows Sandbox availability audit

- Trigger: DISM-backed optional feature query; non-elevated process; read-only sandbox audit
- Method: Stop at the privilege refusal, query only executable and command presence without elevation, and record Sandbox unavailable rather than enabling a feature or rebooting.
- Recurrence guard: Never elevate or change Windows features for an availability audit; a privilege refusal is a bounded negative, not a retry invitation.
- Rollback: Make no host change, retain the refusal, and use the canonical and named repository lanes for bounded tests.
- Witnesses: V6447-M06-W01

### V6447-M07 — Case-sensitive ordered-pair compatibility rewrite

- Trigger: mechanical compatibility copy; tokens differing only by case; PowerShell hash literal
- Method: Use an ordered array of explicit replacement pairs with case-sensitive String.Replace, require destination absence before creation, then inspect exact diffs for semantic leftovers.
- Recurrence guard: Never use a case-insensitive map when replacement keys differ only by case; separate mechanical copies from semantic apply-patch review.
- Rollback: If parsing or inspection fails, retain the negative, remove no history, and do not promote the generated file until exact diff review passes.
- Witnesses: V6447-M07-W01

### V6447-M08 — Uncollapsed untracked and staged exact-file comparison

- Trigger: new untracked directory tree; exact file-set audit; default git status untracked mode
- Method: Use git status --porcelain -uall before staging, direct expected-path existence checks, and git diff --cached --name-only after staging.
- Recurrence guard: An exact file-set receipt must enumerate leaf paths, not a collapsed directory placeholder.
- Rollback: Retain the inaccurate comparison, make no commit from it, and rerun against uncollapsed or staged leaf paths.
- Witnesses: V6447-M08-W01

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
