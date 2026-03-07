# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-07T08:29:49+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=265.172 |
| reserve_tokens_positive | PASS | reserve_tokens=38871.395 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 42.789753,
    "covered_tokens": 38871.394604,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 113.210247,
    "uncovered_tokens": 117128.605396
  },
  "reserve_tokens": 38871.394604,
  "suite_duration_sec": 265.172
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
