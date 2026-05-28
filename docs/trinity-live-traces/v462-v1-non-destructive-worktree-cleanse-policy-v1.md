# v462 v1 Non-Destructive Worktree Cleanse Policy

Generated UTC: `2026-05-28T07:08:29.4627646Z`

Status: `non_destructive_cleanse_policy_recorded`

v462 cleanse means preserve-and-index, not deletion.

## Allowed
- Create new clean worktrees for new phases when useful.
- Index old worktrees and dirty data by path, branch, and purpose.
- Use curated staging only.
- Create future archive branches or archive worktrees only after explicit planning, path checks, and remote verification.

## Blocked
- No `git reset --hard`.
- No discard checkout of user changes.
- No recursive delete of worktrees or raw data.
- No force-push.
- No staging of raw logs, session JSONL, screenshots, secrets, or raw Downloads Journey source files.
