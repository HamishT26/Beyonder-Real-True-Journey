# Body Track Smoke Report

- generated_utc: `2026-02-16T04:30:31+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.129804`
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
    "actual": 0.129804,
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
| run_full_orchestrator_demo | PASS | 0 | 0.035 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.065 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

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
- duration_seconds: `0.035`

### stdout (trimmed)
```
Registered DID: did:freed:139673cfffae4caca8b997319fcb4592
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.8892919660264381, 'entropy_bits': 0.502047915473534, 'top_states': [{'state': 0, 'probability': 0.8892919660264381}, {'state': 1, 'probability': 0.1107080339735618}], 'empirical_top_states': [{'state': 0, 'count': 455, 'frequency': 0.888671875}, {'state': 1, 'count': 57, 'frequency': 0.111328125}], 'expected_state_index': 0.1107080339735618, 'measurement_histogram': [455, 57]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.8892919660264381, 'entropy_bits': 0.502047915473534, 'top_states': [{'state': 0, 'probability': 0.8892919660264381}, {'state': 1, 'probability': 0.1107080339735618}], 'empirical_top_states': [{'state': 0, 'count': 455, 'frequency': 0.888671875}, {'state': 1, 'count': 57, 'frequency': 0.111328125}], 'expected_state_index': 0.1107080339735618, 'measurement_histogram': [455, 57]}, 'waste_energy': 7.747468547995331, 'exotic_energy_generated': 1.8316456986635543, 'total_exotic_energy': 1.8316456986635543}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.9692836877182321, 'entropy_bits': 0.1979715061995263, 'top_states': [{'state': 1, 'probability': 0.9692836877182321}, {'state': 0, 'probability': 0.03071631228176788}], 'empirical_top_states': [{'state': 1, 'count': 496, 'frequency': 0.96875}, {'state': 0, 'count': 16, 'frequency': 0.03125}], 'expected_state_index': 0.9692836877182321, 'measurement_histogram': [16, 496]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.9692836877182321, 'entropy_bits': 0.1979715061995263, 'top_states': [{'state': 1, 'probability': 0.9692836877182321}, {'state': 0, 'probability': 0.03071631228176788}], 'empirical_top_states': [{'state': 1, 'count': 496, 'frequency': 0.96875}, {'state': 0, 'count': 16, 'frequency': 0.03125}], 'expected_state_index': 0.9692836877182321, 'measurement_histogram': [16, 496]}, 'waste_energy': 7.485304993467346, 'exotic_energy_generated': 1.6568699956448973, 'total_exotic_energy': 3.4885156943084517}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.744258,
  "final_total_exotic_energy": 3.488516
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.065`

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
