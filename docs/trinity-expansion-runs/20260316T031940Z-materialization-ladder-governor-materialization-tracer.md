# Trinity Expansion Result: materialization_ladder_governor_materialization_tracer

- generated_utc: `2026-03-16T03:19:40+00:00`
- pillar: `trinity`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| proof_written | PASS | docs/trinity-live-traces/materialization-ladder-governor-proof-v1.json |
| ledger_appended | PASS | docs/trinity-materialization-ledger.jsonl |
| write_scope | PASS | mode=not_applicable |
| blockers_recorded | PASS | blockers=0 |

## Metrics
```json
{
  "actual_state": "active",
  "attempted_write": false,
  "blocker_count": 0,
  "connector_id": "",
  "desired_state": "active",
  "include_live_writes": true,
  "live_write_enabled": false,
  "materialization_level": "l4_standard_prod",
  "mode": "not_applicable",
  "pack": "materialization_ladder_governor",
  "profile_context": "materialize",
  "tracer_result": "SKIP"
}
```

## Repo targets touched
- `docs/trinity-live-traces/materialization-ladder-governor-proof-v1.json`
- `docs/trinity-materialization-ladder-board-latest.json`
- `docs/trinity-materialization-ladder-v1.json`
- `docs/trinity-materialization-ledger.jsonl`
