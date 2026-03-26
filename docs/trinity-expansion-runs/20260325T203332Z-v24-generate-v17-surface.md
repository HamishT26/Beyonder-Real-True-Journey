# Trinity Expansion Result: v24_generate_v17_surface

- generated_utc: `2026-03-25T20:33:32+00:00`
- pillar: `trinity`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | PASS | generated_v17_surface=PASS |
| output_status | FAIL | path=docs/trinity-expansion-system-manifest-v17.json, status=FAIL |

## Metrics
```json
{
  "output_status": "FAIL",
  "returncode": 0,
  "runner_command": [
    "python3",
    "scripts/generate_v17_surface.py"
  ],
  "timeout_sec": 120
}
```

## Repo targets touched
- `docs/trinity-expansion-system-manifest-v17.json`
- `docs/trinity-extension-catalog-v15.json`
- `docs/trinity-runtime-model-resolution-v1.json`
- `docs/v17-runtime-session-log-latest.json`
- `docs/v17-runtime-truth-resolution-board-v1.json`
