# Trinity Expansion Result: reentry_sync_sync_bridge

- generated_utc: `2026-04-30T16:21:25+00:00`
- pillar: `trinity`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_status_present | PASS | present |
| git_remote_available | PASS | live probe unavailable; docs/trinity-live-traces/v76-v84-git-publication-result-v1.json proves remote head 5219251c4e57 is an ancestor of local HEAD |
| docker_container_running | PASS | bounded fallback from prior runtime proof |
| postgres_ready | PASS | bounded fallback from prior runtime proof |

## Metrics
```json
{
  "current_session_surface": {
    "docker_cli": true,
    "docker_container_running": true,
    "gh_available": true,
    "git_remote_available": true,
    "git_remote_live": false,
    "git_remote_mode": "publication_receipt_fallback",
    "node_available": true,
    "npx_available": true,
    "postgres_ready": true
  },
  "recent_commit_count": 6
}
```

## Repo targets touched
- `docs/logs/system-wake-v1.json`
- `docs/system-suite-status.json`
- `docs/v6-session-surface-drift-note.md`
