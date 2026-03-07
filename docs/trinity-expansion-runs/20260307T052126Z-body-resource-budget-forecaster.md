# Trinity Expansion Result: body_resource_budget_forecaster

- generated_utc: `2026-03-07T05:21:26+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| suite_duration_recorded | PASS | duration=245.422 |
| reserve_tokens_positive | PASS | reserve_tokens=27956.850 |
| projection_summary_present | PASS | projection_keys=['sessions', 'planned_tokens', 'covered_tokens', 'uncovered_tokens', 'planned_credits', 'covered_credits', 'uncovered_credits'] |

## Metrics
```json
{
  "projection_summary": {
    "covered_credits": 31.875203,
    "covered_tokens": 27956.849604,
    "planned_credits": 156.0,
    "planned_tokens": 156000.0,
    "sessions": 10,
    "uncovered_credits": 124.124797,
    "uncovered_tokens": 128043.150396
  },
  "reserve_tokens": 27956.849604,
  "suite_duration_sec": 245.422
}
```

## Repo targets touched
- `docs/energy-bank-report.json`
- `docs/system-suite-status.json`
