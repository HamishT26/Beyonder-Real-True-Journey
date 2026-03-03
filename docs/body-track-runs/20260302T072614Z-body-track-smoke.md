# Body Track Smoke Report

- generated_utc: `2026-03-02T07:26:14+00:00`
- overall_status: **FAIL**

## Summary metrics
- pass_rate: `0.666667`
- total_duration_seconds: `1.115044`
- body_health_score: `66.67`
- speed_band: `steady`

## Benchmark guardrail
- status: **WARN**
- profile: `standard`
- trend: `stable`
```json
{
  "min_pass_rate": 1.0,
  "max_duration_sec": 1.0,
  "min_health_score": 95.0
}
```

### check_results
```json
{
  "pass_rate": {
    "ok": false,
    "actual": 0.666667,
    "threshold": 1.0
  },
  "total_duration_seconds": {
    "ok": false,
    "actual": 1.115044,
    "threshold": 1.0
  },
  "body_health_score": {
    "ok": false,
    "actual": 66.67,
    "threshold": 95.0
  }
}
```

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | FAIL | 1 | 0.071 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.112 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.932 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.02 0.05` |

## compile_python_modules

- returncode: `1`
- duration_seconds: `0.071`

### stdout (trimmed)
```
(empty)
```

### stderr (trimmed)
```
[Errno 2] No such file or directory: 'Freed_id_registry.py'
```

## run_full_orchestrator_demo

- returncode: `0`
- duration_seconds: `0.112`

### stdout (trimmed)
```
Registered DID: did:freed:8e4c505cf0904e7c879023ccd64eec4c
Task 1 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.19152563958563296, 0.8084743604143672], 'counts': {'0': 104, '1': 408}, 'entropy_nats': 0.48842761103539023, 'entropy_bits': 0.704652092274001, 'mean_phase_rad': 0.6952681227642863, 'coherence': 1.7494687810552432, 'top_outcomes': [{'index': 1, 'count': 408, 'freq': 0.796875, 'p': 0.8084743604143672}, {'index': 0, 'count': 104, 'freq': 0.203125, 'p': 0.19152563958563296}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.19152563958563296, 0.8084743604143672], 'counts': {'0': 104, '1': 408}, 'entropy_nats': 0.48842761103539023, 'entropy_bits': 0.704652092274001, 'mean_phase_rad': 0.6952681227642863, 'coherence': 1.7494687810552432, 'top_outcomes': [{'index': 1, 'count': 408, 'freq': 0.796875, 'p': 0.8084743604143672}, {'index': 0, 'count': 104, 'freq': 0.203125, 'p': 0.19152563958563296}]}}, 'waste_energy': 8.831719928163778, 'exotic_energy_generated': 2.554479952109186, 'total_exotic_energy': 2.554479952109186}
Task 2 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.8091351868027415, 0.19086481319725848], 'counts': {'0': 422, '1': 90}, 'entropy_nats': 0.4874745255820647, 'entropy_bits': 0.7032770806169449, 'mean_phase_rad': 0.6037732381142206, 'coherence': 1.7103196007497594, 'top_outcomes': [{'index': 0, 'count': 422, 'freq': 0.82421875, 'p': 0.8091351868027415}, {'index': 1, 'count': 90, 'freq': 0.17578125, 'p': 0.19086481319725848}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.8091351868027415, 0.19086481319725848], 'counts': {'0': 422, '1': 90}, 'entropy_nats': 0.4874745255820647, 'entropy_bits': 0.7032770806169449, 'mean_phase_rad': 0.6037732381142206, 'coherence': 1.7103196007497594, 'top_outcomes': [{'index': 0, 'count': 422, 'freq': 0.82421875, 'p': 0.8091351868027415}, {'index': 1, 'count': 90, 'freq': 0.17578125, 'p': 0.19086481319725848}]}}, 'waste_energy': 6.953920422122893, 'exotic_energy_generated': 1.3026136147485956, 'total_exotic_energy': 3.8570935668577815}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.928547,
  "final_total_exotic_energy": 3.857094
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.932`

### stdout (trimmed)
```
Gamma=0.0000: energy density ratio = 1.00000
Gamma=0.0200: energy density ratio = 1.01986
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
    "0.0200": 1.01986,
    "0.0500": 1.04964
  },
  "ratio_min": 1.0,
  "ratio_max": 1.04964,
  "ratio_span": 0.04964
}
```
