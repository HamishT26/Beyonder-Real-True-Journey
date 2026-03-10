# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-08T14:31:38+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=332.078 |
| reserve_tokens_positive | PASS | reserve_tokens=50510.365 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 54.428729,
    "covered_tokens": 50510.364604,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 101.571271,
    "uncovered_tokens": 105489.635396
  },
  "reserve_tokens": 50510.364604,
  "suite_duration_sec": 332.078
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
