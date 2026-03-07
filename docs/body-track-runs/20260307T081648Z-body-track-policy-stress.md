# Body Policy Stress-Window Delta Report

- generated_utc: `2026-03-07T08:16:48+00:00`
- overall_status: **PASS**
- history_samples: `91`
- stressed_samples: `12`

## Benchmark profile stressed deltas
| profile | before_warn | after_warn | before_false_alert | after_false_alert | false_alert_delta | warn_rate_delta |
|---|---:|---:|---:|---:|---:|---:|
| quick | 0.000 | 0.083 | 0.000 | 0.083 | 0.083 | 0.083 |
| standard | 0.000 | 0.083 | 0.000 | 0.083 | 0.083 | 0.083 |
| strict | 0.000 | 0.083 | 0.000 | 0.083 | 0.083 | 0.083 |

## Regression-window stressed delta
| before_window | after_window | before_alert_rate | after_alert_rate | before_false_alert_rate | after_false_alert_rate | false_alert_delta |
|---|---|---:|---:|---:|---:|---:|
| {'window_size': 3, 'max_regressions': 2} | {'window_size': 3, 'max_regressions': 2} | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## Scenario parameters
```json
{
  "scenario_length": 12,
  "duration_step": 0.08,
  "health_step": 0.35,
  "periodic_duration_spike": 0.55,
  "periodic_health_drop": 2.4
}
```
