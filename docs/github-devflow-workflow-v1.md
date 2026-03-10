# GitHub Devflow Workflow v1

- pack: `github_devflow`
- pillar: `trinity`
- gating_class: `staged_setup_gate`
- sync_strategy: `staged_connector`

## Guardrails
- offline-safe by default
- no secrets in repo
- staged connector gate
- read-only handshake first


## Outputs
- cache: `docs/trinity-mcp-cache/github-devflow-latest.json `
- gate: `docs/trinity-expansion/github-devflow-gate-latest.json`

## Notes
- next_action: Promote GitHub only after token or gh auth detection and a safe read-only handshake.
