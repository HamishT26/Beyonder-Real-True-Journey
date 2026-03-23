# Body Profile Calibration Report

- generated_utc: `2026-03-23T03:53:50+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `271`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.583 | 0.572 | loosen_duration+tighten_health | noisy |
| standard | 0.583 | 0.572 | loosen_duration+tighten_health | noisy |
| strict | 0.860 | 0.856 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.313653`
- observed_false_regression_rate: `0.306273`
```json
{
  "duration_drift_p90": 1.315038,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.710 | 0.688 | noisy |
| 3 | 1 | 0.223 | 0.216 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.858 | 0.820 | noisy |
| 5 | 1 | 0.543 | 0.528 | noisy |
| 5 | 2 | 0.169 | 0.169 | noisy |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.902 | 0.849 | noisy |
| 7 | 1 | 0.743 | 0.721 | noisy |
| 7 | 2 | 0.430 | 0.426 | noisy |
| 7 | 3 | 0.132 | 0.132 | acceptable |
| 9 | 0 | 0.924 | 0.856 | noisy |
| 9 | 1 | 0.848 | 0.817 | noisy |
| 9 | 2 | 0.624 | 0.612 | noisy |
| 9 | 3 | 0.350 | 0.350 | noisy |

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
