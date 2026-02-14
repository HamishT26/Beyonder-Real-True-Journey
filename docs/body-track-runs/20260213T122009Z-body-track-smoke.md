# Body Track Smoke Report

- generated_utc: `2026-02-13T12:20:09+00:00`
- overall_status: **PASS**

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | PASS | 0 | 0.030 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.028 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.068 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.05 0.1` |

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
Registered DID: did:freed:9a05802db32d42859a4d51eb4d7194f7
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'top_states': [{'state_index': 1, 'probability': 0.7448540522603362}, {'state_index': 0, 'probability': 0.2551459477396638}], 'entropy_bits': 0.819332842628254, 'expected_state_index': 0.7448540522603362, 'measurement_histogram': [131, 381]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'top_states': [{'state_index': 1, 'probability': 0.7448540522603362}, {'state_index': 0, 'probability': 0.2551459477396638}], 'entropy_bits': 0.819332842628254, 'expected_state_index': 0.7448540522603362, 'measurement_histogram': [131, 381]}, 'waste_energy': 7.5676465926786305, 'exotic_energy_generated': 1.711764395119087, 'total_exotic_energy': 1.711764395119087}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'top_states': [{'state_index': 1, 'probability': 0.5929343873595516}, {'state_index': 0, 'probability': 0.4070656126404483}], 'entropy_bits': 0.9749339524143232, 'expected_state_index': 0.5929343873595516, 'measurement_histogram': [208, 304]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'top_states': [{'state_index': 1, 'probability': 0.5929343873595516}, {'state_index': 0, 'probability': 0.4070656126404483}], 'entropy_bits': 0.9749339524143232, 'expected_state_index': 0.5929343873595516, 'measurement_histogram': [208, 304]}, 'waste_energy': 6.265109504851749, 'exotic_energy_generated': 0.8434063365678323, 'total_exotic_energy': 2.5551707316869194}
```

### stderr (trimmed)
```
(empty)
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.068`

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
