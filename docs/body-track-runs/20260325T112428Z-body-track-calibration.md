# Body Profile Calibration Report

- generated_utc: `2026-03-25T11:24:28+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `297`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.606 | 0.597 | loosen_duration+tighten_health | noisy |
| standard | 0.606 | 0.597 | loosen_duration+tighten_health | noisy |
| strict | 0.872 | 0.869 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.316498`
- observed_false_regression_rate: `0.309764`
```json
{
  "duration_drift_p90": 1.424924,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.715 | 0.695 | noisy |
| 3 | 1 | 0.224 | 0.217 | noisy |
| 3 | 2 | 0.014 | 0.014 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.860 | 0.826 | noisy |
| 5 | 1 | 0.546 | 0.532 | noisy |
| 5 | 2 | 0.171 | 0.171 | noisy |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.907 | 0.859 | noisy |
| 7 | 1 | 0.739 | 0.718 | noisy |
| 7 | 2 | 0.440 | 0.436 | noisy |
| 7 | 3 | 0.134 | 0.134 | acceptable |
| 9 | 0 | 0.931 | 0.869 | noisy |
| 9 | 1 | 0.844 | 0.817 | noisy |
| 9 | 2 | 0.623 | 0.612 | noisy |
| 9 | 3 | 0.356 | 0.356 | noisy |

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
