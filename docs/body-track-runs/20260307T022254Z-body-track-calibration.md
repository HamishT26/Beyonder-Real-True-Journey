# Body Profile Calibration Report

- generated_utc: `2026-03-07T02:22:54+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `79`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.215 | 0.139 | loosen_duration+loosen_health | acceptable |
| standard | 0.215 | 0.139 | loosen_duration+loosen_health | acceptable |
| strict | 0.570 | 0.528 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.177215`
- observed_false_regression_rate: `0.151899`
```json
{
  "duration_drift_p90": 0.440562,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.429 | 0.351 | noisy |
| 3 | 1 | 0.104 | 0.078 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.600 | 0.467 | noisy |
| 5 | 1 | 0.213 | 0.160 | noisy |
| 5 | 2 | 0.080 | 0.080 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.671 | 0.479 | noisy |
| 7 | 1 | 0.370 | 0.288 | noisy |
| 7 | 2 | 0.178 | 0.164 | noisy |
| 7 | 3 | 0.055 | 0.055 | acceptable |
| 9 | 0 | 0.718 | 0.465 | noisy |
| 9 | 1 | 0.507 | 0.394 | noisy |
| 9 | 2 | 0.268 | 0.225 | noisy |
| 9 | 3 | 0.141 | 0.141 | acceptable |

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
