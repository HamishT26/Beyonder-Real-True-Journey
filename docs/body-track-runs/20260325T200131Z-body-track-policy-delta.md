# Body Profile Policy Delta Report

- generated_utc: `2026-03-25T20:01:31+00:00`
- overall_status: **PASS**
- apply_mode: `True`
- policy_updated: `False`
- history_samples: `312`

## Benchmark profile deltas
| profile | before_warn | after_warn | before_false_alert | after_false_alert | action |
|---|---:|---:|---:|---:|---|
| quick | 0.064 | 0.074 | 0.043 | 0.052 | keep |
| standard | 0.026 | 0.074 | 0.003 | 0.052 | keep |
| strict | 0.064 | 0.074 | 0.043 | 0.052 | keep |

## Regression window delta
| window_before | window_after | before_alert_rate | after_alert_rate | before_false_alert_rate | after_false_alert_rate | action |
|---|---|---:|---:|---:|---:|---|
| {'window_size': 3, 'max_regressions': 3} | {'window_size': 3, 'max_regressions': 3} | 0.000 | 0.000 | 0.000 | 0.000 | keep |

## Selected updates
```json
{
  "benchmark_profiles": {},
  "regression_window_policy": null
}
```
