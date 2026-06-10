# Trinity Expansion Result: v21_body_compute_signal_refresh

- generated_utc: `2026-05-01T05:13:51+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | PASS | overall_status=PASS |
| output_status | PASS | path=docs/trinity-api-cache/body-signals-latest.json, status=PASS |

## Metrics
```json
{
  "output_status": "PASS",
  "returncode": 0,
  "runner_command": [
    "python3",
    "scripts/body_compute_signal_refresh.py"
  ],
  "timeout_sec": 240
}
```

## Repo targets touched
- `docs/trinity-api-cache/body-signals-latest.json`
- `docs/trinity-api-query-pack-v1.json`
- `docs/trinity-api-source-manifest-v1.json`
- `docs/trinity-expansion/v21-body-compute-signal-refresh-latest.json`
