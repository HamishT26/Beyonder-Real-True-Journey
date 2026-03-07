# Body Profile Calibration Report

- generated_utc: `2026-03-07T05:24:17+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `85`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.200 | 0.128 | loosen_duration+loosen_health | acceptable |
| standard | 0.200 | 0.128 | loosen_duration+loosen_health | acceptable |
| strict | 0.588 | 0.551 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.188235`
- observed_false_regression_rate: `0.164706`
```json
{
  "duration_drift_p90": 0.358545,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.446 | 0.373 | noisy |
| 3 | 1 | 0.108 | 0.084 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.630 | 0.506 | noisy |
| 5 | 1 | 0.235 | 0.185 | noisy |
| 5 | 2 | 0.074 | 0.074 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.696 | 0.519 | noisy |
| 7 | 1 | 0.418 | 0.342 | noisy |
| 7 | 2 | 0.165 | 0.152 | noisy |
| 7 | 3 | 0.051 | 0.051 | acceptable |
| 9 | 0 | 0.740 | 0.506 | noisy |
| 9 | 1 | 0.545 | 0.442 | noisy |
| 9 | 2 | 0.260 | 0.221 | noisy |
| 9 | 3 | 0.130 | 0.130 | acceptable |

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
