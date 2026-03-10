# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-07T08:26:37+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=143.766 |
| reserve_tokens_positive | PASS | reserve_tokens=37668.642 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 41.587,
    "covered_tokens": 37668.642104,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 114.413,
    "uncovered_tokens": 118331.357896
  },
  "reserve_tokens": 37668.642104,
  "suite_duration_sec": 143.766
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
