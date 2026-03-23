# Trinity Expansion Result: v21_gmut_external_anchor_exclusion_note

- generated_utc: `2026-03-23T02:12:33+00:00`
- pillar: `mind`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | FAIL | overall_status=WARN |
| output_status | PASS | path=docs/mind-track-gmut-anchor-exclusion-latest.json, status=WARN |

## Metrics
```json
{
  "output_status": "WARN",
  "returncode": 1,
  "runner_command": [
    "python3",
    "scripts/gmut_external_anchor_exclusion_note.py",
    "--fail-on-warn"
  ],
  "timeout_sec": 120
}
```

## Repo targets touched
- `docs/mind-track-gmut-anchor-exclusion-latest.json`
- `docs/mind-track-gmut-comparator-latest.json`
- `docs/trinity-expansion/v21-gmut-external-anchor-exclusion-note-latest.json`
