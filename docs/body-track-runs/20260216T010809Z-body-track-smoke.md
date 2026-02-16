# Body Track Smoke Report

- generated_utc: `2026-02-16T01:08:09+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.128429`
- body_health_score: `100.0`
- speed_band: `fast`

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | PASS | 0 | 0.035 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.027 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.067 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.035`

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
- duration_seconds: `0.027`

### stdout (trimmed)
```
Registered DID: did:freed:e892ba5606004e8b83cc07053e71bca1
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5731756426111559, 'entropy_bits': 0.9844940424728346, 'top_states': [{'state': 1, 'probability': 0.5731756426111559}, {'state': 0, 'probability': 0.42682435738884406}], 'empirical_top_states': [{'state': 1, 'count': 293, 'frequency': 0.572265625}, {'state': 0, 'count': 219, 'frequency': 0.427734375}], 'expected_state_index': 0.5731756426111559, 'measurement_histogram': [219, 293]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5731756426111559, 'entropy_bits': 0.9844940424728346, 'top_states': [{'state': 1, 'probability': 0.5731756426111559}, {'state': 0, 'probability': 0.42682435738884406}], 'empirical_top_states': [{'state': 1, 'count': 293, 'frequency': 0.572265625}, {'state': 0, 'count': 219, 'frequency': 0.427734375}], 'expected_state_index': 0.5731756426111559, 'measurement_histogram': [219, 293]}, 'waste_energy': 8.567074519635199, 'exotic_energy_generated': 2.378049679756799, 'total_exotic_energy': 2.378049679756799}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.8113788682877695, 'entropy_bits': 0.6985780462235057, 'top_states': [{'state': 0, 'probability': 0.8113788682877695}, {'state': 1, 'probability': 0.18862113171223044}], 'empirical_top_states': [{'state': 0, 'count': 415, 'frequency': 0.810546875}, {'state': 1, 'count': 97, 'frequency': 0.189453125}], 'expected_state_index': 0.18862113171223044, 'measurement_histogram': [415, 97]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.8113788682877695, 'entropy_bits': 0.6985780462235057, 'top_states': [{'state': 0, 'probability': 0.8113788682877695}, {'state': 1, 'probability': 0.18862113171223044}], 'empirical_top_states': [{'state': 0, 'count': 415, 'frequency': 0.810546875}, {'state': 1, 'count': 97, 'frequency': 0.189453125}], 'expected_state_index': 0.18862113171223044, 'measurement_histogram': [415, 97]}, 'waste_energy': 7.138138481801525, 'exotic_energy_generated': 1.42542565453435, 'total_exotic_energy': 3.803475334291149}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.901738,
  "final_total_exotic_energy": 3.803475
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.067`

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
