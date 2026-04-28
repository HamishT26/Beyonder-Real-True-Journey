# V60-V67 Runtime Health Gate

```json
{
  "generated_utc": "2026-04-28T23:07:46+00:00",
  "phase": "v60_v67_hybrid_omega",
  "kubernetes_readyz": "not_ok",
  "kubernetes_probe": {
    "ok": false,
    "returncode": 1,
    "stderr_excerpt": "Unable to connect to the server: net/http: TLS handshake timeout"
  },
  "host_pressure_state": "hot_pause_heavy_suites",
  "max_container_cpu_percent": 181.54,
  "free_physical_memory_kb": 157080,
  "containers": [
    {
      "name": "kind-cloud-provider",
      "cpu_percent": 48.18,
      "memory": "42.8MiB / 1.711GiB"
    },
    {
      "name": "kind-registry-mirror",
      "cpu_percent": 0.0,
      "memory": "7.973MiB / 1.711GiB"
    },
    {
      "name": "desktop-control-plane",
      "cpu_percent": 181.54,
      "memory": "710.3MiB / 1.711GiB"
    }
  ],
  "load_gate": "closed"
}
```
