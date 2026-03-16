# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-16T01:25:35+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=46.968 |
| reserve_tokens_positive | PASS | reserve_tokens=1427787.600 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 156.0,
    "covered_tokens": 156000.0,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 0.0,
    "uncovered_tokens": 0.0
  },
  "reserve_tokens": 1427787.599604,
  "suite_duration_sec": 46.968
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
