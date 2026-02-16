# Body Track Smoke Report

- generated_utc: `2026-02-16T03:18:54+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.132077`
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
    "actual": 0.132077,
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
| run_full_orchestrator_demo | PASS | 0 | 0.034 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.069 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

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
- duration_seconds: `0.034`

### stdout (trimmed)
```
Registered DID: did:freed:06408759aaf74ef99f5f90f0982b68b5
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5451346830721482, 'entropy_bits': 0.9941140486303253, 'top_states': [{'state': 1, 'probability': 0.5451346830721482}, {'state': 0, 'probability': 0.4548653169278518}], 'empirical_top_states': [{'state': 1, 'count': 279, 'frequency': 0.544921875}, {'state': 0, 'count': 233, 'frequency': 0.455078125}], 'expected_state_index': 0.5451346830721482, 'measurement_histogram': [233, 279]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5451346830721482, 'entropy_bits': 0.9941140486303253, 'top_states': [{'state': 1, 'probability': 0.5451346830721482}, {'state': 0, 'probability': 0.4548653169278518}], 'empirical_top_states': [{'state': 1, 'count': 279, 'frequency': 0.544921875}, {'state': 0, 'count': 233, 'frequency': 0.455078125}], 'expected_state_index': 0.5451346830721482, 'measurement_histogram': [233, 279]}, 'waste_energy': 8.494940312343626, 'exotic_energy_generated': 2.3299602082290845, 'total_exotic_energy': 2.3299602082290845}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.7092421699096327, 'entropy_bits': 0.8696981745950747, 'top_states': [{'state': 0, 'probability': 0.7092421699096327}, {'state': 1, 'probability': 0.29075783009036726}], 'empirical_top_states': [{'state': 0, 'count': 363, 'frequency': 0.708984375}, {'state': 1, 'count': 149, 'frequency': 0.291015625}], 'expected_state_index': 0.29075783009036726, 'measurement_histogram': [363, 149]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.7092421699096327, 'entropy_bits': 0.8696981745950747, 'top_states': [{'state': 0, 'probability': 0.7092421699096327}, {'state': 1, 'probability': 0.29075783009036726}], 'empirical_top_states': [{'state': 0, 'count': 363, 'frequency': 0.708984375}, {'state': 1, 'count': 149, 'frequency': 0.291015625}], 'expected_state_index': 0.29075783009036726, 'measurement_histogram': [363, 149]}, 'waste_energy': 8.193440147879432, 'exotic_energy_generated': 2.1289600985862873, 'total_exotic_energy': 4.458920306815372}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 2.22946,
  "final_total_exotic_energy": 4.45892
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.069`

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
