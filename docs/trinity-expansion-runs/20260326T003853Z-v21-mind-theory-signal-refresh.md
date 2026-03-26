# Trinity Expansion Result: v21_mind_theory_signal_refresh

- generated_utc: `2026-03-26T00:38:53+00:00`
- pillar: `mind`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | FAIL | Traceback (most recent call last): |
| output_status | PASS | path=docs/trinity-api-cache/mind-signals-latest.json, status=PASS |

## Metrics
```json
{
  "output_status": "PASS",
  "returncode": 1,
  "runner_command": [
    "python3",
    "scripts/mind_theory_signal_refresh.py"
  ],
  "timeout_sec": 240
}
```

## Repo targets touched
- `docs/trinity-api-cache/mind-signals-latest.json`
- `docs/trinity-api-query-pack-v1.json`
- `docs/trinity-api-source-manifest-v1.json`
- `docs/trinity-expansion/v21-mind-theory-signal-refresh-latest.json`
