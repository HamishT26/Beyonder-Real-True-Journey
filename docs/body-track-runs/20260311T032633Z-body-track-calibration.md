# Body Profile Calibration Report

- generated_utc: `2026-03-11T03:26:33+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `139`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.331 | 0.295 | loosen_duration+tighten_health | noisy |
| standard | 0.331 | 0.295 | loosen_duration+tighten_health | noisy |
| strict | 0.734 | 0.720 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.266187`
- observed_false_regression_rate: `0.251799`
```json
{
  "duration_drift_p90": 1.01777,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.628 | 0.584 | noisy |
| 3 | 1 | 0.175 | 0.161 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.778 | 0.704 | noisy |
| 5 | 1 | 0.430 | 0.400 | noisy |
| 5 | 2 | 0.133 | 0.133 | acceptable |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.820 | 0.714 | noisy |
| 7 | 1 | 0.632 | 0.586 | noisy |
| 7 | 2 | 0.346 | 0.338 | noisy |
| 7 | 3 | 0.105 | 0.105 | acceptable |
| 9 | 0 | 0.847 | 0.710 | noisy |
| 9 | 1 | 0.733 | 0.672 | noisy |
| 9 | 2 | 0.519 | 0.496 | noisy |
| 9 | 3 | 0.298 | 0.298 | noisy |

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
