# V60-V67 Runtime Health Gate

```json
{
  "generated_utc": "2026-04-30T01:37:36+00:00",
  "phase": "v61_v65_hybrid_omega",
  "kubernetes_readyz": "not_requested_local_kubernetes_retired",
  "local_kubernetes_state": "retired_by_operator_for_v61_v65",
  "kubernetes_probe": {
    "ok": false,
    "returncode": 1,
    "stdout_excerpt": "",
    "stderr_excerpt": "error: current-context is not set",
    "policy": "do_not_reenable_local_kubernetes_in_v61_v65; use OCI/E2B read-only gates before cloud execution"
  },
  "docker_probe": {
    "state": "operator_hold_or_not_running",
    "policy": "operator_deactivated_hold; do_not_start_docker_desktop_in_v61_without_new_operator_confirmation",
    "info_ok": false,
    "ps_ok": false,
    "server_version_excerpt": "\"\"",
    "running_containers": []
  },
  "host_pressure_state": "cool",
  "max_container_cpu_percent": 0.0,
  "free_physical_memory_kb": 478928,
  "free_memory_cool_floor_kb": 400000,
  "containers": [],
  "load_gate": "open",
  "load_gate_basis": "host_pressure_cool_required; Docker and local Kubernetes are not required for repo-only Deep/L5 but remain on operator hold"
}
```
