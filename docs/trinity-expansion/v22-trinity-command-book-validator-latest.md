# Trinity Expansion Result: v22_trinity_command_book_validator

- generated_utc: `2026-03-24T06:21:22+00:00`
- pillar: `heart`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | PASS | overall_status=PASS |
| output_status | PASS | path=docs/trinity-expansion/v22-trinity-command-book-validator-latest.json, status=PASS |

## Metrics
```json
{
  "output_status": "PASS",
  "returncode": 0,
  "runner_command": [
    "python3",
    "scripts/trinity_command_book_validator.py",
    "--fail-on-warn"
  ],
  "timeout_sec": 120
}
```

## Repo targets touched
- `docs/trinity-api-book-v6.json`
- `docs/trinity-api-source-manifest-v1.json`
- `docs/trinity-command-book-v11.json`
- `docs/trinity-expansion/v22-trinity-command-book-validator-latest.json`
- `docs/trinity-extension-catalog-v15.json`
