# V60-V67 Runtime Health Gate

```json
{
  "generated_utc": "2026-04-28T20:50:47+00:00",
  "phase": "v60_v67_hybrid_omega",
  "kubernetes_readyz": "ok",
  "kubernetes_probe": {
    "ok": true,
    "returncode": 0,
    "stderr_excerpt": ""
  },
  "host_pressure_state": "warm_cooldown_before_heavy_suites",
  "max_container_cpu_percent": 115.93,
  "free_physical_memory_kb": 415456,
  "containers": [
    {
      "name": "kind-cloud-provider",
      "cpu_percent": 1.88,
      "memory": "42.66MiB / 1.711GiB"
    },
    {
      "name": "kind-registry-mirror",
      "cpu_percent": 0.0,
      "memory": "8.375MiB / 1.711GiB"
    },
    {
      "name": "desktop-control-plane",
      "cpu_percent": 115.93,
      "memory": "676.7MiB / 1.711GiB"
    }
  ],
  "load_gate": "closed"
}
```
