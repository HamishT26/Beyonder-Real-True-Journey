# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-07T08:34:31+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=151.563 |
| reserve_tokens_positive | PASS | reserve_tokens=40074.147 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 43.992506,
    "covered_tokens": 40074.147104,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 112.007494,
    "uncovered_tokens": 115925.852896
  },
  "reserve_tokens": 40074.147104,
  "suite_duration_sec": 151.563
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
