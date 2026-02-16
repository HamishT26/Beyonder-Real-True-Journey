# Body Track Smoke Report

- generated_utc: `2026-02-16T03:35:48+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.133402`
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
    "actual": 0.133402,
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
| run_full_orchestrator_demo | PASS | 0 | 0.037 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.066 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

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
- duration_seconds: `0.037`

### stdout (trimmed)
```
Registered DID: did:freed:f55d6a1836674f878c583da98b5908e4
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.6191086904109386, 'entropy_bits': 0.9586690947599799, 'top_states': [{'state': 0, 'probability': 0.6191086904109386}, {'state': 1, 'probability': 0.38089130958906126}], 'empirical_top_states': [{'state': 0, 'count': 317, 'frequency': 0.619140625}, {'state': 1, 'count': 195, 'frequency': 0.380859375}], 'expected_state_index': 0.38089130958906126, 'measurement_histogram': [317, 195]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.6191086904109386, 'entropy_bits': 0.9586690947599799, 'top_states': [{'state': 0, 'probability': 0.6191086904109386}, {'state': 1, 'probability': 0.38089130958906126}], 'empirical_top_states': [{'state': 0, 'count': 317, 'frequency': 0.619140625}, {'state': 1, 'count': 195, 'frequency': 0.380859375}], 'expected_state_index': 0.38089130958906126, 'measurement_histogram': [317, 195]}, 'waste_energy': 7.418599328581331, 'exotic_energy_generated': 1.612399552387554, 'total_exotic_energy': 1.612399552387554}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.7905408526173037, 'entropy_bits': 0.7404476472770836, 'top_states': [{'state': 0, 'probability': 0.7905408526173037}, {'state': 1, 'probability': 0.20945914738269633}], 'empirical_top_states': [{'state': 0, 'count': 405, 'frequency': 0.791015625}, {'state': 1, 'count': 107, 'frequency': 0.208984375}], 'expected_state_index': 0.20945914738269633, 'measurement_histogram': [405, 107]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.7905408526173037, 'entropy_bits': 0.7404476472770836, 'top_states': [{'state': 0, 'probability': 0.7905408526173037}, {'state': 1, 'probability': 0.20945914738269633}], 'empirical_top_states': [{'state': 0, 'count': 405, 'frequency': 0.791015625}, {'state': 1, 'count': 107, 'frequency': 0.208984375}], 'expected_state_index': 0.20945914738269633, 'measurement_histogram': [405, 107]}, 'waste_energy': 6.7063744719216825, 'exotic_energy_generated': 1.1375829812811213, 'total_exotic_energy': 2.7499825336686756}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.374991,
  "final_total_exotic_energy": 2.749983
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.066`

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
