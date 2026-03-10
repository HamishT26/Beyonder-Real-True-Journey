# Playwright Operations Workflow v1

- pack: `playwright_ops`
- pillar: `body`
- gating_class: `skill_only`
- sync_strategy: `skill_only`

## Guardrails
- offline-safe by default
- no secrets in repo
- skill-only fallback
- no MCP assumption


## Outputs
- cache: `docs/trinity-mcp-cache/playwright-ops-latest.json `
- gate: `docs/trinity-expansion/playwright-ops-gate-latest.json`

## Notes
- next_action: Use the local Playwright skill until a direct MCP surface exists.
