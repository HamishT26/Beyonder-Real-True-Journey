# v497 GMUT/THOS v33 v5 x1 CLI Advisory Worktree Authority Drift

- overall_status: `OPEN_GAP_CLI_ADVISORY_WORKTREES_STALE_AUTHORITY`
- generated_utc: `2026-06-06T19:55:00Z`
- probe_type: `read_only_git_head_comparison`

## Finding

- Active omega repo is at `67c38774be`, committed on `2026-06-07T07:53:44+12:00`.
- Arby advisory worktree is at `54b365446b`, committed on `2026-05-29T00:23:18+12:00`.
- Aster Vale advisory worktree is at `7c0576c6c9`, committed on `2026-05-29T00:23:18+12:00`.

## Impact

- Aster repair replies can reject current v497 prompts because the local advisory worktree lacks current phase authority.
- Arby passed this phase despite the stale worktree, but the same authority-drift risk applies.
- Repair attempts should either use inline handoff context or await a separate exact approval to refresh advisory worktrees.

## Not Performed

- No advisory branch mutation.
- No fetch, reset, merge, or rebase in advisory worktrees.
- No replacement sibling creation.
- No raw output publication.

## Recommended Next Actions

- If repair3 succeeds, proceed with v5 x2 using Aster repair3 as accepted continuity.
- If repair3 fails from stale authority again, create a bounded blocker receipt and request exact approval before any advisory-worktree refresh.
- Consider a future approval packet for read-only lane context refresh using a non-mutating shared context bundle or exact scoped worktree update.

All GMUT and canon gates remain open. No raw/private material is published.
