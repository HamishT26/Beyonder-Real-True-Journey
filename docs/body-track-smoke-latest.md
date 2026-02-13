# Body Track Smoke Report

- generated_utc: `2026-02-13T12:21:22+00:00`
- overall_status: **PASS**

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | PASS | 0 | 0.030 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.028 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.071 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.05 0.1` |

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
- duration_seconds: `0.028`

### stdout (trimmed)
```
Registered DID: did:freed:c050e45cdca74f0386dbb5aeb9f7c8bb
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'top_states': [{'state_index': 0, 'probability': 0.8660353365119554}, {'state_index': 1, 'probability': 0.1339646634880446}], 'entropy_bits': 0.56821189079877, 'expected_state_index': 0.1339646634880446, 'measurement_histogram': [443, 69]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'top_states': [{'state_index': 0, 'probability': 0.8660353365119554}, {'state_index': 1, 'probability': 0.1339646634880446}], 'entropy_bits': 0.56821189079877, 'expected_state_index': 0.1339646634880446, 'measurement_histogram': [443, 69]}, 'waste_energy': 8.400514937810417, 'exotic_energy_generated': 2.267009958540278, 'total_exotic_energy': 2.267009958540278}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'top_states': [{'state_index': 0, 'probability': 0.8802922905362414}, {'state_index': 1, 'probability': 0.11970770946375868}], 'entropy_bits': 0.5285201011646735, 'expected_state_index': 0.11970770946375868, 'measurement_histogram': [451, 61]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'top_states': [{'state_index': 0, 'probability': 0.8802922905362414}, {'state_index': 1, 'probability': 0.11970770946375868}], 'entropy_bits': 0.5285201011646735, 'expected_state_index': 0.11970770946375868, 'measurement_histogram': [451, 61]}, 'waste_energy': 6.570157009199451, 'exotic_energy_generated': 1.0467713394663003, 'total_exotic_energy': 3.313781298006578}
```

### stderr (trimmed)
```
(empty)
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.071`

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
