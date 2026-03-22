# Body Profile Calibration Report

- generated_utc: `2026-03-22T05:12:19+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `234`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.521 | 0.507 | loosen_duration+tighten_health | noisy |
| standard | 0.521 | 0.507 | loosen_duration+tighten_health | noisy |
| strict | 0.838 | 0.833 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.311966`
- observed_false_regression_rate: `0.303419`
```json
{
  "duration_drift_p90": 1.116375,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.698 | 0.672 | noisy |
| 3 | 1 | 0.220 | 0.211 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.835 | 0.791 | noisy |
| 5 | 1 | 0.535 | 0.517 | noisy |
| 5 | 2 | 0.165 | 0.165 | noisy |
| 5 | 3 | 0.022 | 0.022 | acceptable |
| 7 | 0 | 0.886 | 0.825 | noisy |
| 7 | 1 | 0.724 | 0.697 | noisy |
| 7 | 2 | 0.421 | 0.417 | noisy |
| 7 | 3 | 0.136 | 0.136 | acceptable |
| 9 | 0 | 0.912 | 0.832 | noisy |
| 9 | 1 | 0.827 | 0.792 | noisy |
| 9 | 2 | 0.597 | 0.584 | noisy |
| 9 | 3 | 0.345 | 0.345 | noisy |

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
