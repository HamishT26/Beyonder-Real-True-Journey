# Trinity Expansion Result: v21_mind_theory_signal_board

- generated_utc: `2026-03-26T02:53:56+00:00`
- pillar: `mind`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | FAIL | overall_status=FAIL |
| output_status | FAIL | path=docs/mind-theory-signal-board-latest.json, status=FAIL |

## Metrics
```json
{
  "output_status": "FAIL",
  "returncode": 1,
  "runner_command": [
    "python3",
    "scripts/mind_theory_signal_board.py",
    "--fail-on-warn"
  ],
  "timeout_sec": 120
}
```

## Repo targets touched
- `docs/mind-theory-signal-board-latest.json`
- `docs/trinity-api-cache/mind-signals-latest.json`
- `docs/trinity-expansion/v21-mind-theory-signal-board-latest.json`
