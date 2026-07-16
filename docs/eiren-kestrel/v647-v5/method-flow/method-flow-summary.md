# GHC Family Method Flow State

- Phase: v647-gmut-thos-v5-x1-x2
- Owner: Eiren Kestrel
- Methods: 7
- Passing witnesses: 7
- Failed witnesses retained: 7

## Preferred methods

### V6475-M01 — Split slow multi-surface startup probes before composition

- Trigger: large Windows worktrees; multiple Git status probes; drive-capacity query; bounded wrapper
- Method: Split repository refs, clean-state, live-remote, and drive-capacity checks into separately bounded probes and preserve every result before composing the preflight receipt.
- Recurrence guard: Do not combine multiple slow Windows Git status and filesystem probes under one short wrapper; bound and capture each surface independently.
- Rollback: Give the timed-out aggregate probe zero state-verification credit and rerun only smaller read-only probes.
- Witnesses: V6475-M01-W-F, V6475-M01-W-P

### V6475-M02 — Use ripgrep directory roots with explicit Windows glob filters

- Trigger: Windows PowerShell; ripgrep; multiple directories; filename filter
- Method: Pass directories to ripgrep and express filename matching with repeated --glob filters instead of shell-style wildcard path operands on Windows.
- Recurrence guard: On Windows, give rg real directories and use --glob for selection; do not assume the shell expands wildcard path operands.
- Rollback: Give the invalid inspection zero discovery credit and rerun a bounded directory-plus-glob query.
- Witnesses: V6475-M02-W-F, V6475-M02-W-P

### V6475-M03 — Verify UTF-8 patch context before matching non-ASCII lines

- Trigger: non-ASCII repository text; inherited console display; apply_patch exact context
- Method: Inspect UTF-8 source text before patching and use smaller exact hunks or an explicit apply-patch replacement when inherited display encoding may differ.
- Recurrence guard: Read the exact UTF-8 lines before matching inherited non-ASCII text; treat display-layer corruption as untrusted patch context.
- Rollback: Retain the failed hunk, confirm that no partial change landed, and retry only with verified UTF-8 context through apply_patch.
- Witnesses: V6475-M03-W-F, V6475-M03-W-P

### V6475-M04 — Resolve bundled runner paths from the selected skill root

- Trigger: selected local skill; documented bundled runner; repository-local path assumption
- Method: Resolve the selected skill directory first and invoke its bundled runner from the exact discovered scripts path instead of assuming repository materialization.
- Recurrence guard: When a skill documents a bundled runner, resolve the skill root and scripts directory before constructing a repository-relative command.
- Rollback: Give the empty repository lookup zero runner-discovery credit and inspect only the selected skill package.
- Witnesses: V6475-M04-W-F, V6475-M04-W-P

### V6475-M05 — Fail closed on inherited portfolio-title collisions before materialization

- Trigger: expanded x1 portfolio; prior family portfolios; normalized exact-title audit
- Method: Retain the protected meaning while rewriting every exact-collision title into a phase-specific formulation, then rerun the complete prior-portfolio comparison before packet emission.
- Recurrence guard: Run exact normalized portfolio-title comparison before materialization and never waive a collision merely because the safety boundary is still required.
- Rollback: Emit no x1 packet, preserve the failed collision receipt in Method Flow, rename only the colliding entries, and rerun the full audit.
- Witnesses: V6475-M05-W-F, V6475-M05-W-P

### V6475-M06 — Parse porcelain status prefixes with anchored regular expressions

- Trigger: Git porcelain status rows; PowerShell status classification; exact staged review
- Method: Parse the two-character porcelain status prefix with anchored regular expressions, including an escaped literal question-mark pair for untracked rows.
- Recurrence guard: Use anchored regular expressions against the porcelain prefix and retain staged, unstaged, and untracked counts as separate fields.
- Rollback: Reject the wildcard-derived count, preserve the failed observation, and rerun the same immutable status rows through anchored prefix expressions.
- Witnesses: V6475-M06-W-F, V6475-M06-W-P

### V6475-M07 — Separate repository-wide status from constant-time identity probes

- Trigger: large inherited worktree; Git status inspection; bounded shell wrapper
- Method: Separate repository-wide status from constant-time branch and head probes and give the status process a measured bounded budget that includes shell startup overhead.
- Recurrence guard: Do not bundle repository-wide status with independent identity probes under a ten-second wrapper; measure status separately and retain timeout evidence.
- Rollback: Treat the combined wrapper as failed, perform no mutation, and rerun branch, head, and status as separate read-only probes.
- Witnesses: V6475-M07-W-F, V6475-M07-W-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
