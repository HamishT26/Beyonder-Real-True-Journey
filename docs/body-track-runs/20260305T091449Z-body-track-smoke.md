# Body Track Smoke Report

- generated_utc: `2026-03-05T09:14:49+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.536139`
- body_health_score: `100.0`
- speed_band: `steady`

## Benchmark guardrail
- status: **PASS**
- profile: `standard`
- trend: `improvement`
```json
{
  "min_pass_rate": 1.0,
  "max_duration_sec": 1.274,
  "min_health_score": 32.83
}
```

### check_results
```json
{
  "pass_rate": {
    "ok": true,
    "actual": 1.0,
    "threshold": 1.0
  },
  "total_duration_seconds": {
    "ok": true,
    "actual": 0.536139,
    "threshold": 1.274
  },
  "body_health_score": {
    "ok": true,
    "actual": 100.0,
    "threshold": 32.83
  }
}
```

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | PASS | 0 | 0.104 | `/usr/bin/python3 -m py_compile freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.143 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.289 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.02 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.104`

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
- duration_seconds: `0.143`

### stdout (trimmed)
```
Registered DID: did:freed:e80f4a2dc355483aab9bf63d5920c883
Task 1 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.7664135359134324, 0.23358646408656766], 'counts': {'0': 395, '1': 117}, 'entropy_nats': 0.5435737226006955, 'entropy_bits': 0.7842111139535765, 'mean_phase_rad': 0.8254847960275689, 'coherence': 1.6326093098016514, 'top_outcomes': [{'index': 0, 'count': 395, 'freq': 0.771484375, 'p': 0.7664135359134324}, {'index': 1, 'count': 117, 'freq': 0.228515625, 'p': 0.23358646408656766}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.7664135359134324, 0.23358646408656766], 'counts': {'0': 395, '1': 117}, 'entropy_nats': 0.5435737226006955, 'entropy_bits': 0.7842111139535765, 'mean_phase_rad': 0.8254847960275689, 'coherence': 1.6326093098016514, 'top_outcomes': [{'index': 0, 'count': 395, 'freq': 0.771484375, 'p': 0.7664135359134324}, {'index': 1, 'count': 117, 'freq': 0.228515625, 'p': 0.23358646408656766}]}}, 'waste_energy': 8.628566961811726, 'exotic_energy_generated': 2.419044641207817, 'total_exotic_energy': 2.419044641207817}
Task 2 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.5989993924618761, 0.401000607538124], 'counts': {'0': 302, '1': 210}, 'entropy_nats': 0.6734152931654331, 'entropy_bits': 0.9715329039085578, 'mean_phase_rad': 0.3641157629189105, 'coherence': 1.9756681873143305, 'top_outcomes': [{'index': 0, 'count': 302, 'freq': 0.58984375, 'p': 0.5989993924618761}, {'index': 1, 'count': 210, 'freq': 0.41015625, 'p': 0.401000607538124}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.5989993924618761, 0.401000607538124], 'counts': {'0': 302, '1': 210}, 'entropy_nats': 0.6734152931654331, 'entropy_bits': 0.9715329039085578, 'mean_phase_rad': 0.3641157629189105, 'coherence': 1.9756681873143305, 'top_outcomes': [{'index': 0, 'count': 302, 'freq': 0.58984375, 'p': 0.5989993924618761}, {'index': 1, 'count': 210, 'freq': 0.41015625, 'p': 0.401000607538124}]}}, 'waste_energy': 7.164169531940227, 'exotic_energy_generated': 1.4427796879601515, 'total_exotic_energy': 3.861824329167969}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.930912,
  "final_total_exotic_energy": 3.861824
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.289`

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
