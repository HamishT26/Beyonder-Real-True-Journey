# Body Profile Calibration Report

- generated_utc: `2026-03-25T20:00:10+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `310`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.623 | 0.614 | loosen_duration+tighten_health | noisy |
| standard | 0.623 | 0.614 | loosen_duration+tighten_health | noisy |
| strict | 0.877 | 0.875 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.316129`
- observed_false_regression_rate: `0.309677`
```json
{
  "duration_drift_p90": 1.34251,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.721 | 0.701 | noisy |
| 3 | 1 | 0.221 | 0.214 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.866 | 0.833 | noisy |
| 5 | 1 | 0.546 | 0.533 | noisy |
| 5 | 2 | 0.167 | 0.167 | noisy |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.911 | 0.865 | noisy |
| 7 | 1 | 0.743 | 0.724 | noisy |
| 7 | 2 | 0.438 | 0.434 | noisy |
| 7 | 3 | 0.128 | 0.128 | acceptable |
| 9 | 0 | 0.934 | 0.874 | noisy |
| 9 | 1 | 0.851 | 0.825 | noisy |
| 9 | 2 | 0.626 | 0.616 | noisy |
| 9 | 3 | 0.348 | 0.348 | noisy |

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
