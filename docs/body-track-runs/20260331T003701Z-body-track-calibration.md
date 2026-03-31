# Body Profile Calibration Report

- generated_utc: `2026-03-31T00:37:01+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `333`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.643 | 0.635 | loosen_duration+tighten_health | noisy |
| standard | 0.643 | 0.635 | loosen_duration+tighten_health | noisy |
| strict | 0.886 | 0.883 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.33033`
- observed_false_regression_rate: `0.324324`
```json
{
  "duration_drift_p90": 1.610777,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.734 | 0.716 | noisy |
| 3 | 1 | 0.239 | 0.233 | noisy |
| 3 | 2 | 0.018 | 0.018 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.875 | 0.845 | noisy |
| 5 | 1 | 0.574 | 0.562 | noisy |
| 5 | 2 | 0.191 | 0.191 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.917 | 0.875 | noisy |
| 7 | 1 | 0.761 | 0.743 | noisy |
| 7 | 2 | 0.471 | 0.468 | noisy |
| 7 | 3 | 0.153 | 0.153 | noisy |
| 9 | 0 | 0.938 | 0.883 | noisy |
| 9 | 1 | 0.862 | 0.837 | noisy |
| 9 | 2 | 0.652 | 0.643 | noisy |
| 9 | 3 | 0.388 | 0.388 | noisy |

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
