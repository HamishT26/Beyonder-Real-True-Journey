# Trinity Expansion Result: v21_body_compute_signal_refresh

- generated_utc: `2026-03-23T02:21:20+00:00`
- pillar: `body`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | PASS | overall_status=PASS |
| output_status | FAIL | path=docs/trinity-api-cache/body-signals-latest.json, status=FAIL |

## Metrics
```json
{
  "output_status": "FAIL",
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
