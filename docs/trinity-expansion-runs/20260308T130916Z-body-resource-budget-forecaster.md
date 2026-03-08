# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-08T13:09:16+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=502.391 |
| reserve_tokens_positive | PASS | reserve_tokens=42526.452 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 46.444812,
    "covered_tokens": 42526.452104,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 109.555188,
    "uncovered_tokens": 113473.547896
  },
  "reserve_tokens": 42526.452104,
  "suite_duration_sec": 502.391
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
