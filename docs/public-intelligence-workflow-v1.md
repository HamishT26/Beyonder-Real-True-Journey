# Public Intelligence Workflow v1

- pack: `public_intelligence`
- pillar: `trinity`
- gating_class: `active`
- sync_strategy: `public_feeds`

## Guardrails
- offline-safe by default
- no secrets in repo
- artifact-first recap
- promotion requires manual review


## Outputs
- cache: `docs/trinity-mcp-cache/public-intelligence-latest.json `
- gate: `docs/trinity-expansion/public-intelligence-gate-latest.json`

## Notes
- next_action: Refresh public feeds on demand and promote only manually reviewed records into curated docs.
