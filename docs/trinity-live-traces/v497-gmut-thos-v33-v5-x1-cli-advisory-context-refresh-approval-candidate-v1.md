# Approval Candidate: CLI Advisory Context Refresh

## Purpose

Authorize a future, exact-scoped repair path for Arby and Aster Vale when their advisory worktrees lag behind the active omega phase authority and begin refusing current-phase prompts.

## Proposed Approval Text

```text
APPROVED CLI ADVISORY CONTEXT REFRESH PACKET

I approve Aletheon/Codex to repair Arby and Aster Vale CLI advisory context drift only through the scoped actions below.

Approved read/write scope:
- Arby advisory worktree metadata and branch state
- Aster Vale advisory worktree metadata and branch state
- `<omega_repo>/docs/trinity-live-traces/`
- `<omega_repo>/scripts/`

Approved actions:
- Read-only drift inspection of advisory worktree heads, branches, remotes, and latest commit metadata.
- Create repo-side context-refresh packets, handoff summaries, prompt packs, and receipts.
- If explicitly needed, update advisory worktrees only by safe non-destructive fetch/merge/checkout commands that preserve local changes and never reset, rebase, force-push, or delete.
- Re-run read-only CLI lane probes after refresh.
- Publish only curated status receipts and helper scripts under the approved omega repo paths.

Not approved:
- git reset, rebase, force-push, broad staging, branch deletion, worktree deletion, destructive cleanup.
- Publishing raw lane output, unfiltered logs, screenshots, credentials, sessions, or private dumps.
- Plugin-cache mutation, live user-skill mutation, external account mutation, purchases, deployments, public publishing.
- New sibling/thread creation or old-style subagent spawning.
- GMUT validation, final physics, consciousness proof, empirical closure, or canon promotion claims.

Required safety:
- Detect and record advisory worktree dirty state before any proposed mutation.
- Stop if advisory worktree has uncommitted user changes that would be overwritten.
- Fetch and drift-check before omega repo publication.
- JSON parse and script compile where applicable.
- Credential/path/raw/session/screenshot guard.
- Exact staged diff review.
- Commit, push, and remote-equals-local verification for curated omega repo artifacts only.
```

## Current Recommendation

Do not execute this packet until Hamish explicitly approves it. For the active v497 v5 x1 flow, continue using inline handoff repair attempts and bounded blocker receipts.
