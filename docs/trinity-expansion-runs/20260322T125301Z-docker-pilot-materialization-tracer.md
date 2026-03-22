# Trinity Expansion Result: docker_pilot_materialization_tracer

- generated_utc: `2026-03-22T12:53:01+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| proof_written | PASS | docs/trinity-live-traces/docker-pilot-proof-v1.json |
| ledger_appended | PASS | docs/trinity-materialization-ledger.jsonl |
| write_scope | PASS | mode=preview_only |
| blockers_recorded | PASS | blockers=0 |

## Metrics
```json
{
  "actual_state": "active",
  "attempted_write": false,
  "blocker_count": 0,
  "connector_id": "",
  "desired_state": "active",
  "include_live_writes": false,
  "live_write_enabled": false,
  "materialization_level": "l2_persistent_dev",
  "mode": "preview_only",
  "pack": "docker_pilot",
  "profile_context": "deep",
  "tracer_result": "SKIP"
}
```

## Repo targets touched
- `docs/trinity-docker-pilot-report-v1.json`
- `docs/trinity-live-traces/docker-pilot-proof-v1.json`
- `docs/trinity-materialization-ledger.jsonl`
