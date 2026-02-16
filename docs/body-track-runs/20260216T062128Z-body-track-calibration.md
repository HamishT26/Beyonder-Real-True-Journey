# Body Profile Calibration Report

- generated_utc: `2026-02-16T06:21:28+00:00`
- profile_context: `quick`
- overall_status: **PASS**
- history_samples: `18`

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
  "duration_drift_p90": 0.070488,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.000 | 0.000 | acceptable |
| 3 | 1 | 0.000 | 0.000 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.000 | 0.000 | acceptable |
| 5 | 1 | 0.000 | 0.000 | acceptable |
| 5 | 2 | 0.000 | 0.000 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.000 | 0.000 | acceptable |
| 7 | 1 | 0.000 | 0.000 | acceptable |
| 7 | 2 | 0.000 | 0.000 | acceptable |
| 7 | 3 | 0.000 | 0.000 | acceptable |
| 9 | 0 | 0.000 | 0.000 | acceptable |
| 9 | 1 | 0.000 | 0.000 | acceptable |
| 9 | 2 | 0.000 | 0.000 | acceptable |
| 9 | 3 | 0.000 | 0.000 | acceptable |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 3,
    "max_regressions": 0
  }
}
```
