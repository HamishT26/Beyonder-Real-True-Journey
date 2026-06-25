# v557-gmut-thos-v4-x1 worktree branch rotation planner

Status: `WARN_ROTATION_RECOMMENDED_AT_SAFE_BOUNDARY`

Recommended next mini lane: `omega-mini-3`
Recommended next full-tools lane: `full-tools-2`

## Rotation Warnings

- `omega-mini-publication`: large_trace_artifact_surface
- `full-tools-private-support`: very_large_dirty_or_untracked_surface
- `full-tools-private-support`: large_untracked_surface
- `full-tools-private-support`: large_trace_artifact_surface
- `full-tools-private-support`: detached_private_support_lane

## Safe Rotation Policy

- Commit and push only sanitized omega-mini artifacts before creating the next mini branch.
- Create new mini lanes from a verified clean sanitized head.
- Create new full-tools lanes from a safe base, not from dirty private support files.
- Keep raw Lumen responses and private app-lane maps local-only; carry only digests/counts.
- Do not delete old worktrees or rewrite history as part of rotation.

## Boundary

No raw Lumen text, private callable IDs, private Browser routes, local private paths, screenshots, credentials, destructive cleanup, history rewrite, deployment, purchase, account mutation, API key creation, or sibling identity changes were performed.
