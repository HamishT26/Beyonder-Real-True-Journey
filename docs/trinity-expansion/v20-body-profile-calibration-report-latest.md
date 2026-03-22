# Trinity Expansion Result: v20_body_profile_calibration_report

- generated_utc: `2026-03-22T21:23:07+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | PASS | overall_status=WARN |
| output_status | PASS | path=docs/body-track-calibration-latest.json, status=WARN |

## Metrics
```json
{
  "output_status": "WARN",
  "returncode": 0,
  "runner_command": [
    "python3",
    "scripts/body_profile_calibration_report.py",
    "--profile-context",
    "deep"
  ],
  "timeout_sec": 120
}
```

## Repo targets touched
- `docs/body-profile-policy-v1.json`
- `docs/body-track-calibration-latest.json`
- `docs/trinity-expansion/v20-body-profile-calibration-report-latest.json`
