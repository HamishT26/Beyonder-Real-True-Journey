# Body Profile Calibration Report

- generated_utc: `2026-03-31T03:55:50+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `345`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.641 | 0.633 | loosen_duration+tighten_health | noisy |
| standard | 0.641 | 0.633 | loosen_duration+tighten_health | noisy |
| strict | 0.890 | 0.888 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.333333`
- observed_false_regression_rate: `0.327536`
```json
{
  "duration_drift_p90": 1.531964,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.743 | 0.726 | noisy |
| 3 | 1 | 0.242 | 0.236 | noisy |
| 3 | 2 | 0.017 | 0.017 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.880 | 0.850 | noisy |
| 5 | 1 | 0.584 | 0.572 | noisy |
| 5 | 2 | 0.194 | 0.194 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.920 | 0.879 | noisy |
| 7 | 1 | 0.770 | 0.752 | noisy |
| 7 | 2 | 0.487 | 0.484 | noisy |
| 7 | 3 | 0.147 | 0.147 | acceptable |
| 9 | 0 | 0.941 | 0.887 | noisy |
| 9 | 1 | 0.866 | 0.843 | noisy |
| 9 | 2 | 0.665 | 0.656 | noisy |
| 9 | 3 | 0.404 | 0.404 | noisy |

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
