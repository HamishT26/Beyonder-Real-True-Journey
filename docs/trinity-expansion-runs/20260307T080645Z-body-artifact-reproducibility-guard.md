# Trinity Expansion Result: body_artifact_reproducibility_guard

- generated_utc: `2026-03-07T08:06:45+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| dependency:docs/body-track-smoke-latest.json | PASS | status=PASS |
| dependency:docs/body-track-benchmark-latest.json | PASS | status=PASS |
| dependency:docs/body-track-trend-guard-latest.json | PASS | status=PASS |
| dependency:docs/body-track-calibration-latest.json | PASS | status=WARN |
| dependency:docs/body-track-policy-stress-latest.json | PASS | status=PASS |

## Metrics
```json
{
  "dependencies_checked": 5,
  "pass_like_dependencies": 5
}
```

## Repo targets touched
- `docs/body-track-benchmark-latest.json`
- `docs/body-track-calibration-latest.json`
- `docs/body-track-policy-stress-latest.json`
- `docs/body-track-smoke-latest.json`
- `docs/body-track-trend-guard-latest.json`
