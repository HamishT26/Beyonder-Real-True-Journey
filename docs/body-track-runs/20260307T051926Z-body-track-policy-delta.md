# Body Profile Policy Delta Report

- generated_utc: `2026-03-07T05:19:26+00:00`
- overall_status: **PASS**
- apply_mode: `True`
- policy_updated: `False`
- history_samples: `84`

## Benchmark profile deltas
| profile | before_warn | after_warn | before_false_alert | after_false_alert | action |
|---|---:|---:|---:|---:|---|
| quick | 0.119 | 0.131 | 0.039 | 0.052 | keep |
| standard | 0.119 | 0.131 | 0.039 | 0.052 | keep |
| strict | 0.119 | 0.131 | 0.039 | 0.052 | keep |

## Regression window delta
| window_before | window_after | before_alert_rate | after_alert_rate | before_false_alert_rate | after_false_alert_rate | action |
|---|---|---:|---:|---:|---:|---|
| {'window_size': 3, 'max_regressions': 2} | {'window_size': 3, 'max_regressions': 2} | 0.000 | 0.000 | 0.000 | 0.000 | keep |

## Selected updates
```json
{
  "benchmark_profiles": {},
  "regression_window_policy": null
}
```
