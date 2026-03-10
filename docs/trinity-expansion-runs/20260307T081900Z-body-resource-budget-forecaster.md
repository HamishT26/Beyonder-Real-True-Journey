# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-07T08:19:00+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=279.406 |
| reserve_tokens_positive | PASS | reserve_tokens=36191.817 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 40.110174,
    "covered_tokens": 36191.817104,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 115.889826,
    "uncovered_tokens": 119808.182896
  },
  "reserve_tokens": 36191.817104,
  "suite_duration_sec": 279.406
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
