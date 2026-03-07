# Figma Collaboration Workflow v1

- pack: `figma_collab`
- pillar: `body`
- gating_class: `verified_live`
- sync_strategy: `verified_mcp`

## Guardrails
- offline-safe by default
- no secrets in repo
- verified connector only
- non-interactive collaboration cache


## Outputs
- cache: `docs/trinity-mcp-cache/figma-collab-latest.json `
- gate: `docs/trinity-expansion/figma-collab-gate-latest.json`

## Notes
- next_action: Use on-demand node fetches only when file key and node id are explicit.
