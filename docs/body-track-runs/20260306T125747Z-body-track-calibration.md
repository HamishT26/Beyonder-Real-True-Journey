# Body Profile Calibration Report

- generated_utc: `2026-03-06T12:57:47+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `69`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.188 | 0.097 | loosen_duration+loosen_health | acceptable |
| standard | 0.188 | 0.097 | loosen_duration+loosen_health | acceptable |
| strict | 0.522 | 0.468 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.173913`
- observed_false_regression_rate: `0.144928`
```json
{
  "duration_drift_p90": 0.301154,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.418 | 0.328 | noisy |
| 3 | 1 | 0.119 | 0.090 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.569 | 0.415 | noisy |
| 5 | 1 | 0.246 | 0.185 | noisy |
| 5 | 2 | 0.092 | 0.092 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.619 | 0.397 | noisy |
| 7 | 1 | 0.397 | 0.302 | noisy |
| 7 | 2 | 0.206 | 0.190 | noisy |
| 7 | 3 | 0.063 | 0.063 | acceptable |
| 9 | 0 | 0.672 | 0.377 | noisy |
| 9 | 1 | 0.492 | 0.361 | noisy |
| 9 | 2 | 0.311 | 0.262 | noisy |
| 9 | 3 | 0.164 | 0.164 | noisy |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 3,
    "max_regressions": 2
  }
}
```
