# Operator Release Workflow v1

- pack: `operator_release`
- pillar: `trinity`
- gating_class: `active`
- sync_strategy: `local_repo`

## Guardrails
- offline-safe by default
- no secrets in repo
- artifact-first recap
- promotion requires manual review


## Outputs
- cache: `docs/trinity-mcp-cache/operator-release-latest.json `
- gate: `docs/trinity-expansion/operator-release-gate-latest.json`

## Notes
- next_action: Capture branch and worktree state before any release recommendation.
