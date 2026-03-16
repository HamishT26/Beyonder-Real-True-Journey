# Body Profile Calibration Report

- generated_utc: `2026-03-16T02:05:06+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `184`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.418 | 0.395 | loosen_duration+tighten_health | noisy |
| standard | 0.418 | 0.395 | loosen_duration+tighten_health | noisy |
| strict | 0.793 | 0.785 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.282609`
- observed_false_regression_rate: `0.271739`
```json
{
  "duration_drift_p90": 1.107951,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.659 | 0.626 | noisy |
| 3 | 1 | 0.192 | 0.181 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.806 | 0.750 | noisy |
| 5 | 1 | 0.483 | 0.461 | noisy |
| 5 | 2 | 0.144 | 0.144 | acceptable |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.860 | 0.781 | noisy |
| 7 | 1 | 0.680 | 0.646 | noisy |
| 7 | 2 | 0.376 | 0.371 | noisy |
| 7 | 3 | 0.112 | 0.112 | acceptable |
| 9 | 0 | 0.886 | 0.784 | noisy |
| 9 | 1 | 0.784 | 0.739 | noisy |
| 9 | 2 | 0.545 | 0.528 | noisy |
| 9 | 3 | 0.324 | 0.324 | noisy |

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
