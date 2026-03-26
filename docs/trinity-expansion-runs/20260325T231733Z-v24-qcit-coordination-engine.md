# Trinity Expansion Result: v24_qcit_coordination_engine

- generated_utc: `2026-03-25T23:17:33+00:00`
- pillar: `trinity`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | PASS | Wrote docs\trinity-expansion\v24-qcit-coordination-report.json |
| output_status | FAIL | path=docs/trinity-expansion/v24-qcit-coordination-report.json, status=FAIL |

## Metrics
```json
{
  "output_status": "FAIL",
  "returncode": 0,
  "runner_command": [
    "python3",
    "scripts/qcit_coordination_engine.py",
    "--out",
    "docs/trinity-expansion/v24-qcit-coordination-report.json"
  ],
  "timeout_sec": 60
}
```

## Repo targets touched
- `docs/trinity-expansion/v24-qcit-coordination-engine-latest.json`
- `docs/trinity-expansion/v24-qcit-coordination-report.json`
