# Trinity Expansion Result: v24_validate_token_energy_reports

- generated_utc: `2026-03-26T03:02:18+00:00`
- pillar: `trinity`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | PASS | validated token-credit and energy-bank reports |

## Metrics
```json
{
  "returncode": 0,
  "runner_command": [
    "python3",
    "scripts/validate_token_energy_reports.py",
    "--token",
    "docs/trinity-expansion/v24-token-credit-bank-report.json",
    "--energy",
    "docs/trinity-expansion/v24-energy-bank-report.json"
  ],
  "timeout_sec": 60
}
```

## Repo targets touched
- `docs/trinity-expansion/v24-energy-bank-report.json`
- `docs/trinity-expansion/v24-token-credit-bank-report.json`
- `docs/trinity-expansion/v24-validate-token-energy-reports-latest.json`
