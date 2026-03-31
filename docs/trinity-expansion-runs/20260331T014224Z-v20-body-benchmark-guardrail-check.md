# Trinity Expansion Result: v20_body_benchmark_guardrail_check

- generated_utc: `2026-03-31T01:42:24+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| runner_command_exit | PASS | overall_status=PASS |
| output_status | PASS | path=docs/body-track-benchmark-latest.json, status=PASS |

## Metrics
```json
{
  "output_status": "PASS",
  "returncode": 0,
  "runner_command": [
    "python3",
    "body_track_runner.py",
    "--gammas",
    "0.0",
    "0.02",
    "0.05",
    "--benchmark-profile",
    "standard",
    "--profile-policy",
    "docs/body-profile-policy-v1.json",
    "--fail-on-benchmark"
  ],
  "timeout_sec": 120
}
```

## Repo targets touched
- `docs/body-profile-policy-v1.json`
- `docs/body-track-benchmark-latest.json`
- `docs/trinity-expansion/v20-body-benchmark-guardrail-check-latest.json`
