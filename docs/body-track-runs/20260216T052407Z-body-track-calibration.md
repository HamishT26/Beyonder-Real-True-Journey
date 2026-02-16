# Body Profile Calibration Report

- generated_utc: `2026-02-16T05:24:07+00:00`
- profile_context: `quick`
- overall_status: **PASS**
- history_samples: `15`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.000 | 0.000 | tighten_duration+tighten_health | acceptable |
| standard | 0.000 | 0.000 | tighten_duration+tighten_health | acceptable |
| strict | 0.000 | 0.000 | tighten_duration+tighten_health | acceptable |

## Trend alert analysis
- observed_regression_rate: `0.0`
- observed_false_regression_rate: `0.0`
```json
{
  "duration_drift_p90": 0.05772,
  "health_drop_p90": 0.0
}
```

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick"
}
```
