# Trinity Expansion Result: v20_trinity_public_research_validator

- generated_utc: `2026-03-31T00:59:21+00:00`
- pillar: `mind`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | PASS | overall_status=PASS |
| output_status | PASS | path=docs/trinity-public-research-validation-latest.json, status=PASS |

## Metrics
```json
{
  "output_status": "PASS",
  "returncode": 0,
  "runner_command": [
    "python3",
    "scripts/validate_trinity_public_research.py",
    "--fail-on-warn"
  ],
  "timeout_sec": 120
}
```

## Repo targets touched
- `docs/trinity-expansion/v20-trinity-public-research-validator-latest.json`
- `docs/trinity-public-research-validation-latest.json`
- `docs/trinity-public-source-registry-v1.json`
