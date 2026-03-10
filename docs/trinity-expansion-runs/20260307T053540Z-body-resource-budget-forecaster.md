# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-07T05:35:40+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=121.391 |
| reserve_tokens_positive | PASS | reserve_tokens=30936.040 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 34.854395,
    "covered_tokens": 30936.039604,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 121.145605,
    "uncovered_tokens": 125063.960396
  },
  "reserve_tokens": 30936.039604,
  "suite_duration_sec": 121.391
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
