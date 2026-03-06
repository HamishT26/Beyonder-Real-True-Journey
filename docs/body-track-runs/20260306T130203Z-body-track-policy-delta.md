# Body Profile Policy Delta Report

- generated_utc: `2026-03-06T13:02:03+00:00`
- overall_status: **PASS**
- apply_mode: `True`
- policy_updated: `True`
- history_samples: `73`

## Benchmark profile deltas
| profile | before_warn | after_warn | before_false_alert | after_false_alert | action |
|---|---:|---:|---:|---:|---|
| quick | 0.151 | 0.137 | 0.061 | 0.045 | apply_recommended_thresholds |
| standard | 0.151 | 0.137 | 0.061 | 0.045 | apply_recommended_thresholds |
| strict | 0.151 | 0.137 | 0.061 | 0.045 | apply_recommended_thresholds |

## Regression window delta
| window_before | window_after | before_alert_rate | after_alert_rate | before_false_alert_rate | after_false_alert_rate | action |
|---|---|---:|---:|---:|---:|---|
| {'window_size': 3, 'max_regressions': 2} | {'window_size': 3, 'max_regressions': 2} | 0.000 | 0.000 | 0.000 | 0.000 | keep |

## Selected updates
```json
{
  "benchmark_profiles": {
    "quick": {
      "min_pass_rate": 1.0,
      "max_duration_sec": 3.183,
      "min_health_score": 66.17
    },
    "standard": {
      "min_pass_rate": 1.0,
      "max_duration_sec": 3.183,
      "min_health_score": 66.17
    },
    "strict": {
      "min_pass_rate": 1.0,
      "max_duration_sec": 3.183,
      "min_health_score": 66.17
    }
  },
  "regression_window_policy": null
}
```
