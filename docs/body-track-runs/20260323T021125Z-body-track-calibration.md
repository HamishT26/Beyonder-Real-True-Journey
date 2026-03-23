# Body Profile Calibration Report

- generated_utc: `2026-03-23T02:11:25+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `267`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.577 | 0.565 | loosen_duration+tighten_health | noisy |
| standard | 0.577 | 0.565 | loosen_duration+tighten_health | noisy |
| strict | 0.858 | 0.854 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.314607`
- observed_false_regression_rate: `0.307116`
```json
{
  "duration_drift_p90": 1.256138,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.709 | 0.687 | noisy |
| 3 | 1 | 0.219 | 0.211 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.856 | 0.817 | noisy |
| 5 | 1 | 0.536 | 0.521 | noisy |
| 5 | 2 | 0.171 | 0.171 | noisy |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.900 | 0.847 | noisy |
| 7 | 1 | 0.739 | 0.716 | noisy |
| 7 | 2 | 0.433 | 0.429 | noisy |
| 7 | 3 | 0.134 | 0.134 | acceptable |
| 9 | 0 | 0.923 | 0.853 | noisy |
| 9 | 1 | 0.846 | 0.815 | noisy |
| 9 | 2 | 0.622 | 0.610 | noisy |
| 9 | 3 | 0.355 | 0.355 | noisy |

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
