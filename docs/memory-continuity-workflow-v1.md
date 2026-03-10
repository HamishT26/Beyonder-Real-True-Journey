# Memory Continuity Workflow v1

- pack: `memory_continuity`
- pillar: `mind`
- gating_class: `active`
- sync_strategy: `local_repo`

## Guardrails
- offline-safe by default
- no secrets in repo
- artifact-first recap
- promotion requires manual review


## Outputs
- cache: `docs/trinity-mcp-cache/memory-continuity-latest.json `
- gate: `docs/trinity-expansion/memory-continuity-gate-latest.json`

## Notes
- next_action: Refresh recap state from commits, suite status, and capability audit before narrative updates.
