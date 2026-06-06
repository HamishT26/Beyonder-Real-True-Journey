# v497 GMUT/THOS v33 v6 x1 CLI Context Refresh Bundle Spec

- overall_status: `PASS_NON_MUTATING_CONTEXT_REFRESH_SPEC_READY`
- generated_utc: `2026-06-06T21:02:33Z`
- purpose: give stale CLI advisory worktrees current phase context without mutating their branches.

## Bundle Fields

- `phase_slug`
- `current_head_short`
- `previous_x2_summary`
- `lane_state_carry_forward`
- `exact_heading_contract`
- `open_repair_state`
- `blocked_live_mutations`
- `claim_boundary`

## Approved Current Use

- Inline prompt handoff for current-phase advisory output.
- Published status-only spec for future x2 builder use.
- No advisory branch mutation.

## Requires Future Exact Approval

- Fetching, merging, checking out, rebasing, or otherwise updating advisory worktrees.
- Writing files inside Arby or Aster Vale advisory worktrees.
- Changing Codex app, account, connector, plugin-cache, or user-skill state.

All GMUT and canon gates remain open. No raw/private material is published.
