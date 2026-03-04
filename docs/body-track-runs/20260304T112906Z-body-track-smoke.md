# Body Track Smoke Report

- generated_utc: `2026-03-04T11:29:06+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `1.066998`
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
    "actual": 1.066998,
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
| compile_python_modules | PASS | 0 | 0.080 | `/usr/bin/python3 -m py_compile freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.098 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.889 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.02 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.080`

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
- duration_seconds: `0.098`

### stdout (trimmed)
```
Registered DID: did:freed:830bcab7f2ce48f18764da4414027d41
Task 1 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.7619706500188071, 0.23802934998119285], 'counts': {'0': 381, '1': 131}, 'entropy_nats': 0.5487977347054744, 'entropy_bits': 0.791747770310685, 'mean_phase_rad': 1.0165076845576146, 'coherence': 1.2766553864098529, 'top_outcomes': [{'index': 0, 'count': 381, 'freq': 0.744140625, 'p': 0.7619706500188071}, {'index': 1, 'count': 131, 'freq': 0.255859375, 'p': 0.23802934998119285}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.7619706500188071, 0.23802934998119285], 'counts': {'0': 381, '1': 131}, 'entropy_nats': 0.5487977347054744, 'entropy_bits': 0.791747770310685, 'mean_phase_rad': 1.0165076845576146, 'coherence': 1.2766553864098529, 'top_outcomes': [{'index': 0, 'count': 381, 'freq': 0.744140625, 'p': 0.7619706500188071}, {'index': 1, 'count': 131, 'freq': 0.255859375, 'p': 0.23802934998119285}]}}, 'waste_energy': 7.828472938429723, 'exotic_energy_generated': 1.885648625619815, 'total_exotic_energy': 1.885648625619815}
Task 2 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.8734563460102133, 0.12654365398978665], 'counts': {'0': 454, '1': 58}, 'entropy_nats': 0.37976311830611315, 'entropy_bits': 0.5478823674927582, 'mean_phase_rad': 0.09926634697462235, 'coherence': 1.5346549636275655, 'top_outcomes': [{'index': 0, 'count': 454, 'freq': 0.88671875, 'p': 0.8734563460102133}, {'index': 1, 'count': 58, 'freq': 0.11328125, 'p': 0.12654365398978665}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.8734563460102133, 0.12654365398978665], 'counts': {'0': 454, '1': 58}, 'entropy_nats': 0.37976311830611315, 'entropy_bits': 0.5478823674927582, 'mean_phase_rad': 0.09926634697462235, 'coherence': 1.5346549636275655, 'top_outcomes': [{'index': 0, 'count': 454, 'freq': 0.88671875, 'p': 0.8734563460102133}, {'index': 1, 'count': 58, 'freq': 0.11328125, 'p': 0.12654365398978665}]}}, 'waste_energy': 6.651048332933279, 'exotic_energy_generated': 1.1006988886221853, 'total_exotic_energy': 2.9863475142420004}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.493174,
  "final_total_exotic_energy": 2.986348
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.889`

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
