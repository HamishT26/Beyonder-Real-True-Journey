# Body Profile Calibration Report

- generated_utc: `2026-03-10T09:28:36+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `127`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.339 | 0.300 | loosen_duration+loosen_health | noisy |
| standard | 0.339 | 0.300 | loosen_duration+loosen_health | noisy |
| strict | 0.717 | 0.700 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.259843`
- observed_false_regression_rate: `0.244094`
```json
{
  "duration_drift_p90": 0.997187,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.608 | 0.560 | noisy |
| 3 | 1 | 0.176 | 0.160 | noisy |
| 3 | 2 | 0.008 | 0.008 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.756 | 0.675 | noisy |
| 5 | 1 | 0.415 | 0.382 | noisy |
| 5 | 2 | 0.138 | 0.138 | acceptable |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.802 | 0.686 | noisy |
| 7 | 1 | 0.603 | 0.554 | noisy |
| 7 | 2 | 0.322 | 0.314 | noisy |
| 7 | 3 | 0.116 | 0.116 | acceptable |
| 9 | 0 | 0.832 | 0.681 | noisy |
| 9 | 1 | 0.706 | 0.639 | noisy |
| 9 | 2 | 0.471 | 0.445 | noisy |
| 9 | 3 | 0.303 | 0.303 | noisy |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 3,
    "max_regressions": 3
  }
}
```
