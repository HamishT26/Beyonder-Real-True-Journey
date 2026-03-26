# Trinity Expansion Result: v24_aurelis_atomic_nz_clock

- generated_utc: `2026-03-25T20:59:13+00:00`
- pillar: `body`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | PASS | 09:59AM NZDT Thu 26 Mar 2026 |
| output_status | FAIL | path=docs/trinity-expansion/v24-aurelis-atomic-nz-clock-latest.json, status=FAIL |

## Metrics
```json
{
  "output_status": "FAIL",
  "returncode": 0,
  "runner_command": [
    "python3",
    "scripts/aurelis_atomic_nz_clock.py",
    "--stamp"
  ],
  "timeout_sec": 60
}
```

## Repo targets touched
- `docs/aurelis-nz-clock-sessions.jsonl`
- `docs/aurelis-nz-clock-state.json`
- `docs/trinity-expansion/v24-aurelis-atomic-nz-clock-latest.json`
