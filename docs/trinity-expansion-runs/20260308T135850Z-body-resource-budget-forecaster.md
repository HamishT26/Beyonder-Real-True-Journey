# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-08T13:58:50+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=553.922 |
| reserve_tokens_positive | PASS | reserve_tokens=46384.955 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 50.303317,
    "covered_tokens": 46384.954604,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 105.696683,
    "uncovered_tokens": 109615.045396
  },
  "reserve_tokens": 46384.954604,
  "suite_duration_sec": 553.922
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
