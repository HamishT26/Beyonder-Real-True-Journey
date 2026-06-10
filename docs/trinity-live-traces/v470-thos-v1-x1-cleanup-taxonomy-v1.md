# v470 THOS v1 x1 Cleanup Taxonomy

Classification: `evidence`

This taxonomy defines what cleanup means in THOS before any cleanup is attempted. The phase performs inventory and governance work only.

## Cleanup Classes

| Class | Meaning | Current status |
| --- | --- | --- |
| `read_only_observation` | Inspect, list, count, compare, parse, and summarize | Allowed |
| `safe_local_hygiene` | Create curated manifests and candidate ledgers | Allowed |
| `reversible_cleanup_candidate` | Proposed move, quarantine, archive, or rename | Requires explicit approval |
| `destructive_cleanup` | Deletion, purge, branch pruning, history rewrite, worktree deletion | Blocked |
| `external_mutation` | Cloud, Drive, automation, account, or connector writes | Blocked |
| `forbidden_material_handling` | Raw logs, session JSONL, screenshots, or credential-bearing material | Not publishable |

## Candidate Fields

Every cleanup candidate must record target, reason, owner or phase, retention class, cleanup class, approval status, rollback plan, source evidence, and blocker. Without those fields, the candidate stays observation-only.

## Safe Tonight

The safe path is to inventory, classify, and propose. The unsafe path is to treat a dirty worktree or large file count as permission to delete. The current repo has a broad pre-existing dirty surface, so v470 keeps staging narrow and current-phase only.

## Fail-Closed Rule

If a candidate touches deletion, movement, recursive cleanup, cache purge, worktree removal, history rewrite, cloud write, connector mutation, or automation edit, it fails closed until Hamish gives separate explicit approval.
