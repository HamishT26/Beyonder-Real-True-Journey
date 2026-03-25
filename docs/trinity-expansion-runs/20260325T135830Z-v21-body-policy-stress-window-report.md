# Trinity Expansion Result: v21_body_policy_stress_window_report

- generated_utc: `2026-03-25T13:58:30+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | PASS | overall_status=PASS |
| output_status | PASS | path=docs/body-track-policy-stress-latest.json, status=PASS |

## Metrics
```json
{
  "output_status": "PASS",
  "returncode": 0,
  "runner_command": [
    "python3",
    "scripts/body_policy_stress_window_report.py",
    "--fail-on-warn"
  ],
  "timeout_sec": 180
}
```

## Repo targets touched
- `docs/body-profile-policy-v1.json`
- `docs/body-track-calibration-latest.json`
- `docs/body-track-policy-stress-latest.json`
- `docs/trinity-expansion/v21-body-policy-stress-window-report-latest.json`
