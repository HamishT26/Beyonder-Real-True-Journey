# Trinity Expansion Result: v21_standards_bridge_validator

- generated_utc: `2026-03-31T03:55:57+00:00`
- pillar: `heart`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | PASS | overall_status=PASS |
| output_status | PASS | path=docs/v17-standards-bridge-validation-latest.json, status=PASS |

## Metrics
```json
{
  "output_status": "PASS",
  "returncode": 0,
  "runner_command": [
    "python3",
    "scripts/v17_standards_bridge_validator.py",
    "--fail-on-warn"
  ],
  "timeout_sec": 120
}
```

## Repo targets touched
- `docs/trinity-expansion/v21-standards-bridge-validator-latest.json`
- `docs/v17-standards-bridge-registry-v1.json`
- `docs/v17-standards-bridge-validation-latest.json`
