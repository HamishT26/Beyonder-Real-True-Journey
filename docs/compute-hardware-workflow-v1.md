# Compute Hardware Workflow v1

- pack: `compute_hardware`
- pillar: `body`
- gating_class: `active`
- sync_strategy: `local_probe`

## Guardrails
- offline-safe by default
- no secrets in repo
- artifact-first recap
- promotion requires manual review


## Outputs
- cache: `docs/trinity-mcp-cache/compute-hardware-latest.json `
- gate: `docs/trinity-expansion/compute-hardware-gate-latest.json`

## Notes
- next_action: Map local tools and optional accelerators before widening compute assumptions.
