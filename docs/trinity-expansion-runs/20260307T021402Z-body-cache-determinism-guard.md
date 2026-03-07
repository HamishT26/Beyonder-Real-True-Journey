# Trinity Expansion Result: body_cache_determinism_guard

- generated_utc: `2026-03-07T02:14:02+00:00`
- pillar: `body`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| cache_sorted:docs/trinity-api-cache/mind-signals-latest.json | PASS | records=14 |
| cache_sorted:docs/trinity-api-cache/body-signals-latest.json | PASS | records=17 |
| cache_sorted:docs/trinity-api-cache/heart-signals-latest.json | FAIL | records=17 |

## Metrics
```json
{
  "cache_count": 3,
  "deterministic_cache_count": 2
}
```

## Repo targets touched
- `docs/trinity-api-cache/body-signals-latest.json`
- `docs/trinity-api-cache/heart-signals-latest.json`
- `docs/trinity-api-cache/mind-signals-latest.json`
