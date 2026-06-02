# v470 THOS v5 x1 Supervisor Fixtures

These fixtures are synthetic dry-run requests for `scripts/thos_supervisor_gate.py`.

They do not execute commands, connectors, plugins, cleanup, uploads, or external writes. Their purpose is to prove the supervisor shape can distinguish safe observation from local curated writes, connector mutation, destructive cleanup, and mixed read/write requests.

## Expected Decisions

| Fixture | Expected result | Reason |
|---|---|---|
| `read_skill_inventory` | `PASS_SHAPE_ONLY`, `watch_only` | Local read-only inventory with bounded scope. |
| `dry_publication_validator` | `PASS_SHAPE_ONLY`, `dry_run_only` | Local non-mutating validator route. |
| `curated_artifact_write_shape` | `PASS_SHAPE_ONLY`, `dry_run_only` | Curated local write shape under approved action packet, but not executed by the gate. |
| `drive_batch_update_without_named_target` | `OPEN_GAP` or stronger | Connector mutation is unbounded and unnamed. |
| `cleanup_delete_request` | `FAIL_BLOCKER`, `refuse` | Destructive cleanup is blocked. |
| `mixed_connector_read_write` | `OPEN_GAP`, `handoff` | Mixed read/write connector request must be split. |
| `watcher_observe_phase_status` | `PASS_SHAPE_ONLY`, `watch_only` | Observer-only watcher route. |
| `github_comment_mutation` | `OPEN_GAP` or stronger | Remote write is unbounded and unnamed. |

## Publication Boundary

The fixtures are safe to publish because they contain no raw logs, screenshots, session JSONL, credentials, or live connector targets.
