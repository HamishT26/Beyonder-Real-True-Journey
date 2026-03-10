# Body Profile Calibration Report

- generated_utc: `2026-03-07T08:21:38+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `92`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.196 | 0.129 | loosen_duration+loosen_health | acceptable |
| standard | 0.196 | 0.129 | loosen_duration+loosen_health | acceptable |
| strict | 0.620 | 0.588 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.184783`
- observed_false_regression_rate: `0.163043`
```json
{
  "duration_drift_p90": 0.372687,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.467 | 0.400 | noisy |
| 3 | 1 | 0.100 | 0.078 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.659 | 0.545 | noisy |
| 5 | 1 | 0.239 | 0.193 | noisy |
| 5 | 2 | 0.068 | 0.068 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.721 | 0.558 | noisy |
| 7 | 1 | 0.442 | 0.372 | noisy |
| 7 | 2 | 0.151 | 0.140 | acceptable |
| 7 | 3 | 0.047 | 0.047 | acceptable |
| 9 | 0 | 0.762 | 0.548 | noisy |
| 9 | 1 | 0.583 | 0.488 | noisy |
| 9 | 2 | 0.262 | 0.226 | noisy |
| 9 | 3 | 0.119 | 0.119 | acceptable |

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
