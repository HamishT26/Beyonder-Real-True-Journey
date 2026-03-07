# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-07T02:34:10+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=172.625 |
| reserve_tokens_positive | PASS | reserve_tokens=26753.612 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 30.671964,
    "covered_tokens": 26753.612104,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 125.328036,
    "uncovered_tokens": 129246.387896
  },
  "reserve_tokens": 26753.612104,
  "suite_duration_sec": 172.625
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
