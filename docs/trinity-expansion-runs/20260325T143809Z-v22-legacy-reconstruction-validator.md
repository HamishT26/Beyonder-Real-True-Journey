# Trinity Expansion Result: v22_legacy_reconstruction_validator

- generated_utc: `2026-03-25T14:38:09+00:00`
- pillar: `mind`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | PASS | legacy_reconstruction_validation=PASS |
| output_status | PASS | path=docs/trinity-expansion/v22-legacy-reconstruction-validator-latest.json, status=PASS |

## Metrics
```json
{
  "output_status": "PASS",
  "returncode": 0,
  "runner_command": [
    "python3",
    "scripts/legacy_reconstruction_validator.py",
    "--fail-on-warn"
  ],
  "timeout_sec": 120
}
```

## Repo targets touched
- `docs/comparative-validation-grid-v1.md`
- `docs/mind-theory-signal-board-latest.json`
- `docs/trinity-expansion/v22-legacy-reconstruction-validator-latest.json`
- `docs/trinity-public-research-validation-latest.json`
- `docs/trinity-public-source-registry-v1.json`
