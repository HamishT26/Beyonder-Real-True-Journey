# Body Track Smoke Report

- generated_utc: `2026-02-16T03:50:32+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.185337`
- body_health_score: `100.0`
- speed_band: `fast`

## Benchmark guardrail
- status: **PASS**
- trend: `stable`
```json
{
  "pass_rate": {
    "ok": true,
    "actual": 1.0,
    "threshold": 1.0
  },
  "total_duration_seconds": {
    "ok": true,
    "actual": 0.185337,
    "threshold": 1.0
  },
  "body_health_score": {
    "ok": true,
    "actual": 100.0,
    "threshold": 95.0
  }
}
```

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | PASS | 0 | 0.030 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.036 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.120 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.030`

### stdout (trimmed)
```
(empty)
```

### stderr (trimmed)
```
(empty)
```

## run_full_orchestrator_demo

- returncode: `0`
- duration_seconds: `0.036`

### stdout (trimmed)
```
Registered DID: did:freed:7ce03769846f4933b9cbdece915c806c
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.8308867680120214, 'entropy_bits': 0.6556722033188707, 'top_states': [{'state': 0, 'probability': 0.8308867680120214}, {'state': 1, 'probability': 0.16911323198797848}], 'empirical_top_states': [{'state': 0, 'count': 425, 'frequency': 0.830078125}, {'state': 1, 'count': 87, 'frequency': 0.169921875}], 'expected_state_index': 0.16911323198797848, 'measurement_histogram': [425, 87]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.8308867680120214, 'entropy_bits': 0.6556722033188707, 'top_states': [{'state': 0, 'probability': 0.8308867680120214}, {'state': 1, 'probability': 0.16911323198797848}], 'empirical_top_states': [{'state': 0, 'count': 425, 'frequency': 0.830078125}, {'state': 1, 'count': 87, 'frequency': 0.169921875}], 'expected_state_index': 0.16911323198797848, 'measurement_histogram': [425, 87]}, 'waste_energy': 8.450739139815479, 'exotic_energy_generated': 2.300492759876986, 'total_exotic_energy': 2.300492759876986}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.9185232865274079, 'entropy_bits': 0.40736122788864915, 'top_states': [{'state': 0, 'probability': 0.9185232865274079}, {'state': 1, 'probability': 0.0814767134725922}], 'empirical_top_states': [{'state': 0, 'count': 470, 'frequency': 0.91796875}, {'state': 1, 'count': 42, 'frequency': 0.08203125}], 'expected_state_index': 0.0814767134725922, 'measurement_histogram': [470, 42]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.9185232865274079, 'entropy_bits': 0.40736122788864915, 'top_states': [{'state': 0, 'probability': 0.9185232865274079}, {'state': 1, 'probability': 0.0814767134725922}], 'empirical_top_states': [{'state': 0, 'count': 470, 'frequency': 0.91796875}, {'state': 1, 'count': 42, 'frequency': 0.08203125}], 'expected_state_index': 0.0814767134725922, 'measurement_histogram': [470, 42]}, 'waste_energy': 6.6094578564079445, 'exotic_energy_generated': 1.072971904271963, 'total_exotic_energy': 3.373464664148949}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.686732,
  "final_total_exotic_energy": 3.373465
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.120`

### stdout (trimmed)
```
Gamma=0.0000: energy density ratio = 1.00000
Gamma=0.0100: energy density ratio = 1.00993
Gamma=0.0500: energy density ratio = 1.04964
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "gamma_count": 3,
  "gamma_ratios": {
    "0.0000": 1.0,
    "0.0100": 1.00993,
    "0.0500": 1.04964
  },
  "ratio_min": 1.0,
  "ratio_max": 1.04964,
  "ratio_span": 0.04964
}
```
