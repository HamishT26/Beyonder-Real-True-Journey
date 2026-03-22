# Body Profile Calibration Report

- generated_utc: `2026-03-21T03:39:51+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `232`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.517 | 0.502 | loosen_duration+tighten_health | noisy |
| standard | 0.517 | 0.502 | loosen_duration+tighten_health | noisy |
| strict | 0.836 | 0.831 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.306034`
- observed_false_regression_rate: `0.297414`
```json
{
  "duration_drift_p90": 1.116875,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.696 | 0.670 | noisy |
| 3 | 1 | 0.217 | 0.209 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.833 | 0.789 | noisy |
| 5 | 1 | 0.531 | 0.513 | noisy |
| 5 | 2 | 0.167 | 0.167 | noisy |
| 5 | 3 | 0.022 | 0.022 | acceptable |
| 7 | 0 | 0.885 | 0.823 | noisy |
| 7 | 1 | 0.721 | 0.695 | noisy |
| 7 | 2 | 0.416 | 0.412 | noisy |
| 7 | 3 | 0.137 | 0.137 | acceptable |
| 9 | 0 | 0.911 | 0.830 | noisy |
| 9 | 1 | 0.826 | 0.790 | noisy |
| 9 | 2 | 0.594 | 0.580 | noisy |
| 9 | 3 | 0.339 | 0.339 | noisy |

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
