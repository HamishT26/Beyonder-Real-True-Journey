# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-10T05:50:19+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=564.672 |
| reserve_tokens_positive | PASS | reserve_tokens=98204.355 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 102.122721,
    "covered_tokens": 98204.354604,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 53.877279,
    "uncovered_tokens": 57795.645396
  },
  "reserve_tokens": 98204.354604,
  "suite_duration_sec": 564.672
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
