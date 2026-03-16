# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-16T00:12:53+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=6.141 |
| reserve_tokens_positive | PASS | reserve_tokens=1371891.975 |
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
  "reserve_tokens": 1371891.974604,
  "suite_duration_sec": 6.141
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
