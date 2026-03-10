# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-10T05:57:17+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=408.110 |
| reserve_tokens_positive | PASS | reserve_tokens=113683.067 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 117.601434,
    "covered_tokens": 113683.067104,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 38.398566,
    "uncovered_tokens": 42316.932896
  },
  "reserve_tokens": 113683.067104,
  "suite_duration_sec": 408.11
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
