# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-07T02:24:53+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=183.906 |
| reserve_tokens_positive | PASS | reserve_tokens=26427.967 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 30.346318,
    "covered_tokens": 26427.967104,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 125.653682,
    "uncovered_tokens": 129572.032896
  },
  "reserve_tokens": 26427.967104,
  "suite_duration_sec": 183.906
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
