# Identity Governance Workflow v1

- pack: `identity_governance`
- pillar: `heart`
- gating_class: `active`
- sync_strategy: `identity_registry`

## Guardrails
- offline-safe by default
- no secrets in repo
- artifact-first recap
- promotion requires manual review


## Outputs
- cache: `docs/trinity-mcp-cache/identity-governance-latest.json `
- gate: `docs/trinity-expansion/identity-governance-gate-latest.json`

## Notes
- next_action: Only promote staged connectors after auth detection and safe read-only handshakes are green.
