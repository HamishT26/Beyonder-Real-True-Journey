# Body Track Smoke Report

- generated_utc: `2026-03-04T11:22:39+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `1.144342`
- body_health_score: `100.0`
- speed_band: `steady`

## Benchmark guardrail
- status: **PASS**
- profile: `standard`
- trend: `stable`
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
    "actual": 1.144342,
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
| compile_python_modules | PASS | 0 | 0.127 | `/usr/bin/python3 -m py_compile freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.123 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.895 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.02 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.127`

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
- duration_seconds: `0.123`

### stdout (trimmed)
```
Registered DID: did:freed:cec3baa654e64300ab0beb186047da8a
Task 1 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.16889659997501394, 0.8311034000249862], 'counts': {'0': 84, '1': 428}, 'entropy_nats': 0.4541323101308117, 'entropy_bits': 0.6551744317331708, 'mean_phase_rad': 0.877674190357867, 'coherence': 1.5626325399089938, 'top_outcomes': [{'index': 1, 'count': 428, 'freq': 0.8359375, 'p': 0.8311034000249862}, {'index': 0, 'count': 84, 'freq': 0.1640625, 'p': 0.16889659997501394}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.16889659997501394, 0.8311034000249862], 'counts': {'0': 84, '1': 428}, 'entropy_nats': 0.4541323101308117, 'entropy_bits': 0.6551744317331708, 'mean_phase_rad': 0.877674190357867, 'coherence': 1.5626325399089938, 'top_outcomes': [{'index': 1, 'count': 428, 'freq': 0.8359375, 'p': 0.8311034000249862}, {'index': 0, 'count': 84, 'freq': 0.1640625, 'p': 0.16889659997501394}]}}, 'waste_energy': 8.347734386859239, 'exotic_energy_generated': 2.231822924572825, 'total_exotic_energy': 2.231822924572825}
Task 2 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.6438503955057548, 0.35614960449424515], 'counts': {'0': 320, '1': 192}, 'entropy_nats': 0.6511705911351593, 'entropy_bits': 0.9394405826034291, 'mean_phase_rad': 0.41596999994273676, 'coherence': 1.9527273278167059, 'top_outcomes': [{'index': 0, 'count': 320, 'freq': 0.625, 'p': 0.6438503955057548}, {'index': 1, 'count': 192, 'freq': 0.375, 'p': 0.35614960449424515}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.6438503955057548, 0.35614960449424515], 'counts': {'0': 320, '1': 192}, 'entropy_nats': 0.6511705911351593, 'entropy_bits': 0.9394405826034291, 'mean_phase_rad': 0.41596999994273676, 'coherence': 1.9527273278167059, 'top_outcomes': [{'index': 0, 'count': 320, 'freq': 0.625, 'p': 0.6438503955057548}, {'index': 1, 'count': 192, 'freq': 0.375, 'p': 0.35614960449424515}]}}, 'waste_energy': 7.16975932948764, 'exotic_energy_generated': 1.4465062196584262, 'total_exotic_energy': 3.6783291442312516}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.839165,
  "final_total_exotic_energy": 3.678329
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.895`

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
