# V61-V65 Runtime Health Gate

```json
{
  "generated_utc": "2026-04-30T00:54:48+00:00",
  "phase": "v61_v65_hybrid_omega",
  "kubernetes_readyz": "not_requested_local_kubernetes_retired",
  "local_kubernetes_state": "retired_by_operator_for_v61_v65",
  "kubernetes_probe": {
    "ok": false,
    "returncode": null,
    "stdout_excerpt": "",
    "stderr_excerpt": "Command '['kubectl', 'config', 'current-context']' timed out after 12 seconds",
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
  "host_pressure_state": "warm_cooldown_before_heavy_suites",
  "max_container_cpu_percent": 0.0,
  "free_physical_memory_kb": 388212,
  "containers": [],
  "load_gate": "closed",
  "load_gate_basis": "host_pressure_cool_required; Docker and local Kubernetes are not required for repo-only Deep/L5 but remain on operator hold"
}
```
