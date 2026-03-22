# Trinity Expansion Result: v20_gmut_anchor_trace_validator

- generated_utc: `2026-03-22T20:53:55+00:00`
- pillar: `mind`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | PASS | overall_status=PASS |
| output_status | PASS | path=docs/mind-track-gmut-trace-validation-latest.json, status=PASS |

## Metrics
```json
{
  "output_status": "PASS",
  "returncode": 0,
  "runner_command": [
    "python3",
    "scripts/gmut_anchor_trace_validator.py",
    "--fail-on-warn"
  ],
  "timeout_sec": 120
}
```

## Repo targets touched
- `docs/mind-track-external-anchor-canonical-inputs-v1.json`
- `docs/mind-track-gmut-trace-validation-latest.json`
- `docs/trinity-expansion/v20-gmut-anchor-trace-validator-latest.json`
