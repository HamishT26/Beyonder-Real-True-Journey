# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-10T05:34:20+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=516.313 |
| reserve_tokens_positive | PASS | reserve_tokens=51779.677 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 55.698042,
    "covered_tokens": 51779.677104,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 100.301958,
    "uncovered_tokens": 104220.322896
  },
  "reserve_tokens": 51779.677104,
  "suite_duration_sec": 516.313
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
