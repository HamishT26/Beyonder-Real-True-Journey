# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-08T12:04:46+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=259.547 |
| reserve_tokens_positive | PASS | reserve_tokens=41276.900 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 45.195259,
    "covered_tokens": 41276.899604,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 110.804741,
    "uncovered_tokens": 114723.100396
  },
  "reserve_tokens": 41276.899604,
  "suite_duration_sec": 259.547
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
