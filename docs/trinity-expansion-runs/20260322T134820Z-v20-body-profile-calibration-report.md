# Trinity Expansion Result: v20_body_profile_calibration_report

- generated_utc: `2026-03-22T13:48:20+00:00`
- pillar: `body`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | FAIL | usage: body_profile_calibration_report.py [-h] |
| output_status | PASS | path=docs/body-track-calibration-latest.json, status=WARN |

## Metrics
```json
{
  "output_status": "WARN",
  "returncode": 2,
  "runner_command": [
    "python3",
    "scripts/body_profile_calibration_report.py",
    "--profile-context",
    "materialize"
  ],
  "timeout_sec": 120
}
```

## Repo targets touched
- `docs/body-profile-policy-v1.json`
- `docs/body-track-calibration-latest.json`
- `docs/trinity-expansion/v20-body-profile-calibration-report-latest.json`
