# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-10T06:21:46+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=286.703 |
| reserve_tokens_positive | PASS | reserve_tokens=175601.997 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 156.0,
    "covered_tokens": 156000.0,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 0.0,
    "uncovered_tokens": 0.0
  },
  "reserve_tokens": 175601.997104,
  "suite_duration_sec": 286.703
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
