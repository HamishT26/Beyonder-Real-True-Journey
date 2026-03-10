# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-10T06:09:19+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=306.375 |
| reserve_tokens_positive | PASS | reserve_tokens=144641.852 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 148.56022,
    "covered_tokens": 144641.852104,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 7.43978,
    "uncovered_tokens": 11358.147896
  },
  "reserve_tokens": 144641.852104,
  "suite_duration_sec": 306.375
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
