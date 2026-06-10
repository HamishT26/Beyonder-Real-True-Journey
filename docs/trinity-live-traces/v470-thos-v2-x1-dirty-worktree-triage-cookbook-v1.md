# v470 THOS v2 x1 Dirty Worktree Triage Cookbook

Classification: `evidence`

Dirty worktree handling is first-class schema data, not a vague warning.

## Triage Classes

| Class | Meaning |
| --- | --- |
| `clean` | No modified, staged, or untracked files. |
| `dirty_known_safe` | Changes exist but are understood and outside the publication slice. |
| `dirty_conflict_risk` | Changes overlap current artifacts or validation assets. |
| `dirty_unknown` | Provenance unclear; publication advice blocks until classified. |

## Read-Only Cookbook

Safe advisory examples include status, branch, head, diff names, cached diff names, untracked listing, recent log, remote listing, targeted text search, and directory listing.

Blocked patterns include staging, commit, push, hard reset, clean, destructive restore, recursive deletion, and unapproved file moves.

Recommended blocker codes: `BLOCKED_ENV_READ`, `BLOCKED_DIRTY_UNKNOWN`, `BLOCKED_OVERLAP_WITH_THOS`, `BLOCKED_WRITE_REQUIRED`, and `BLOCKED_SOURCE_UNVERIFIED`.
