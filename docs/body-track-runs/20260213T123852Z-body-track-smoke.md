# Body Track Smoke Report

- generated_utc: `2026-02-13T12:38:52+00:00`
- overall_status: **PASS**

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | PASS | 0 | 0.029 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.028 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.144 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.029`

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
Registered DID: did:freed:b3b563be56fb489982f332d01c5fd57d
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.6044060389520888, 'entropy_bits': 0.9683148060203997, 'top_states': [{'state': 0, 'probability': 0.6044060389520888}, {'state': 1, 'probability': 0.3955939610479113}], 'empirical_top_states': [{'state': 0, 'count': 320, 'frequency': 0.625}, {'state': 1, 'count': 192, 'frequency': 0.375}]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.6044060389520888, 'entropy_bits': 0.9683148060203997, 'top_states': [{'state': 0, 'probability': 0.6044060389520888}, {'state': 1, 'probability': 0.3955939610479113}], 'empirical_top_states': [{'state': 0, 'count': 320, 'frequency': 0.625}, {'state': 1, 'count': 192, 'frequency': 0.375}]}, 'waste_energy': 7.450000207331747, 'exotic_energy_generated': 1.6333334715544978, 'total_exotic_energy': 1.6333334715544978}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.7048466765039113, 'entropy_bits': 0.8752854188190595, 'top_states': [{'state': 1, 'probability': 0.7048466765039113}, {'state': 0, 'probability': 0.2951533234960886}], 'empirical_top_states': [{'state': 1, 'count': 356, 'frequency': 0.6953125}, {'state': 0, 'count': 156, 'frequency': 0.3046875}]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.7048466765039113, 'entropy_bits': 0.8752854188190595, 'top_states': [{'state': 1, 'probability': 0.7048466765039113}, {'state': 0, 'probability': 0.2951533234960886}], 'empirical_top_states': [{'state': 1, 'count': 356, 'frequency': 0.6953125}, {'state': 0, 'count': 156, 'frequency': 0.3046875}]}, 'waste_energy': 6.799046395006771, 'exotic_energy_generated': 1.199364263337847, 'total_exotic_energy': 2.8326977348923448}
```

### stderr (trimmed)
```
(empty)
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.144`

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
