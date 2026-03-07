# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-07T02:14:03+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=32.656 |
| reserve_tokens_positive | PASS | reserve_tokens=9692.382 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 15.918351,
    "covered_tokens": 9692.381682,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 140.081649,
    "uncovered_tokens": 146307.618318
  },
  "reserve_tokens": 9692.381682,
  "suite_duration_sec": 32.656
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
