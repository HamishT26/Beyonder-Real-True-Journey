# Body Profile Calibration Report

- generated_utc: `2026-03-17T23:55:47+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `205`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.463 | 0.444 | loosen_duration+tighten_health | noisy |
| standard | 0.463 | 0.444 | loosen_duration+tighten_health | noisy |
| strict | 0.815 | 0.808 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.282927`
- observed_false_regression_rate: `0.273171`
```json
{
  "duration_drift_p90": 1.106906,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.660 | 0.631 | noisy |
| 3 | 1 | 0.192 | 0.182 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.811 | 0.761 | noisy |
| 5 | 1 | 0.483 | 0.463 | noisy |
| 5 | 2 | 0.134 | 0.134 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.869 | 0.799 | noisy |
| 7 | 1 | 0.683 | 0.653 | noisy |
| 7 | 2 | 0.362 | 0.357 | noisy |
| 7 | 3 | 0.101 | 0.101 | acceptable |
| 9 | 0 | 0.898 | 0.807 | noisy |
| 9 | 1 | 0.802 | 0.761 | noisy |
| 9 | 2 | 0.548 | 0.533 | noisy |
| 9 | 3 | 0.289 | 0.289 | noisy |

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
