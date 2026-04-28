# V61 Omega Plan Proposal

- Additions: helm_presence_probe, kustomize_presence_probe, stern_log_probe, kubectx_guard, one_node_restart_watch, host_cooldown_ledger, docker_compose_profile_guard, local_runtime_budget
- Validation: Deep plus Materialize L5 when runtime health gate is open.
- Audit: Standard and L4 every fifth phase or on any failure family; MCP refresh every third phase or on connector/cache changes.
