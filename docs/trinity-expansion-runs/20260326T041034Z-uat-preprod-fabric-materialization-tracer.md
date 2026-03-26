# Trinity Expansion Result: uat_preprod_fabric_materialization_tracer

- generated_utc: `2026-03-26T04:10:34+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| proof_written | PASS | docs/trinity-live-traces/uat-preprod-fabric-proof-v1.json |
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
  "materialization_level": "l5_ha_prod",
  "mode": "not_applicable",
  "pack": "uat_preprod_fabric",
  "profile_context": "materialize",
  "tracer_result": "SKIP"
}
```

## Repo targets touched
- `docs/trinity-live-traces/uat-preprod-fabric-proof-v1.json`
- `docs/trinity-materialization-ladder-v1.json`
- `docs/trinity-materialization-ledger.jsonl`
- `docs/trinity-uat-preprod-targets-v1.json`
