# Body Track Smoke Report

- generated_utc: `2026-02-13T12:54:19+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.208063`
- body_health_score: `100.0`
- speed_band: `fast`

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | PASS | 0 | 0.030 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.030 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.148 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.05 0.1` |

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
- duration_seconds: `0.030`

### stdout (trimmed)
```
Registered DID: did:freed:50dd1074da2947d787b1215f32b49bd3
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'top_states': [{'state_index': 1, 'probability': 0.6528500564120033}, {'state_index': 0, 'probability': 0.3471499435879967}], 'entropy_bits': 0.9314969253413328, 'expected_state_index': 0.6528500564120033, 'measurement_histogram': [178, 334]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'top_states': [{'state_index': 1, 'probability': 0.6528500564120033}, {'state_index': 0, 'probability': 0.3471499435879967}], 'entropy_bits': 0.9314969253413328, 'expected_state_index': 0.6528500564120033, 'measurement_histogram': [178, 334]}, 'waste_energy': 8.039410856981968, 'exotic_energy_generated': 2.0262739046546447, 'total_exotic_energy': 2.0262739046546447}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'top_states': [{'state_index': 0, 'probability': 0.8072814113695888}, {'state_index': 1, 'probability': 0.1927185886304112}], 'entropy_bits': 0.7071240208830577, 'expected_state_index': 0.1927185886304112, 'measurement_histogram': [413, 99]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'top_states': [{'state_index': 0, 'probability': 0.8072814113695888}, {'state_index': 1, 'probability': 0.1927185886304112}], 'entropy_bits': 0.7071240208830577, 'expected_state_index': 0.1927185886304112, 'measurement_histogram': [413, 99]}, 'waste_energy': 6.344536499812291, 'exotic_energy_generated': 0.8963576665415274, 'total_exotic_energy': 2.922631571196172}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.461316,
  "final_total_exotic_energy": 2.922632
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.148`

### stdout (trimmed)
```
Gamma=0.0000: energy density ratio = 1.00000
Gamma=0.0500: energy density ratio = 1.04964
Gamma=0.1000: energy density ratio = 1.09928
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
    "0.0500": 1.04964,
    "0.1000": 1.09928
  },
  "ratio_min": 1.0,
  "ratio_max": 1.09928,
  "ratio_span": 0.09928
}
```
