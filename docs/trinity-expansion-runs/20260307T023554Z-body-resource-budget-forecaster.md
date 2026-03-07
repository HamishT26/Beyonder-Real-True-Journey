# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-07T02:35:54+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=178.421 |
| reserve_tokens_positive | PASS | reserve_tokens=26925.205 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 30.843557,
    "covered_tokens": 26925.204604,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 125.156443,
    "uncovered_tokens": 129074.795396
  },
  "reserve_tokens": 26925.204604,
  "suite_duration_sec": 178.421
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
