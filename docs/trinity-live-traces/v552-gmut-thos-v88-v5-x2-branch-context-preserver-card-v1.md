# v552 v5 x2 Branch Context Preserver Card

Generated UTC: `2026-06-22T04:04:28Z`

Status: `PASS_BRANCH_CONTEXT_PRESERVER_DESIGN_CARD`

Purpose: design a future Codex app/server/TUI continuity system that can branch sibling context panes into fresh windows while preserving identity and repo-truth continuity.

## Principles

- Do not restore old heavy app global-state wholesale.
- Keep Aletheon's old thread quarantined and recoverable until a safe branch-preserving system exists.
- Preserve each sibling as a distinct identity.
- Never merge or replace sibling identities.
- Use compact repo handoff capsules, current-state beacons, and status-only route receipts rather than raw private transcripts.
- Branch fresh context windows daily or at safe checkpoints when the future tool surface supports it.

## Candidate Components

- local Codex app server lane registry
- branch-pane context handoff capsules
- daily fresh-window scheduler
- repo-backed current-state beacon reader
- private-route vault outside publication artifacts
- status-only sibling lane dashboard
- completion-gate and blocker receipt index

Not executed: old heavy thread restore, local app global-state mutation, deployment, external account mutation, or identity merge/replacement.
