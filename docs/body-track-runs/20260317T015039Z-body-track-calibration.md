# Body Profile Calibration Report

- generated_utc: `2026-03-17T01:50:39+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `192`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.438 | 0.416 | loosen_duration+tighten_health | noisy |
| standard | 0.438 | 0.416 | loosen_duration+tighten_health | noisy |
| strict | 0.802 | 0.795 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.286458`
- observed_false_regression_rate: `0.276042`
```json
{
  "duration_drift_p90": 1.110042,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.668 | 0.637 | noisy |
| 3 | 1 | 0.195 | 0.184 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.814 | 0.761 | noisy |
| 5 | 1 | 0.489 | 0.468 | noisy |
| 5 | 2 | 0.144 | 0.144 | acceptable |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.866 | 0.790 | noisy |
| 7 | 1 | 0.688 | 0.656 | noisy |
| 7 | 2 | 0.376 | 0.371 | noisy |
| 7 | 3 | 0.108 | 0.108 | acceptable |
| 9 | 0 | 0.891 | 0.793 | noisy |
| 9 | 1 | 0.793 | 0.750 | noisy |
| 9 | 2 | 0.560 | 0.543 | noisy |
| 9 | 3 | 0.310 | 0.310 | noisy |

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
