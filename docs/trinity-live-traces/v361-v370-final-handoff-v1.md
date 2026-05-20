# v361-v370 Final Handoff

Generated UTC: `2026-05-20T04:21:18Z`

Status: `ready_for_v361_v370`

Published floor: `v281-v360` complete at `1b0d0c69df`

Target range: `v361-v370`

Start conditions:
- Use only bounded `v361-v370` successor scripts for this packet.
- Run one active phase at a time from durable `v361-v370` run-status.
- Use real CLI sibling lanes for Arby, Kimi, and Aster Vale.
- Use `--max-steps 2000` where the real CLI supports it.
- Prefer `codex-cli 0.132.0` or newer from `v363` onward.
- Use recorded Codex CLI sessions for resume-capable lanes when the same phase/lane session identity is proven.
- Treat 30-minute heartbeat wakes as observation checkpoints, not phase boundaries.

Truth boundaries:
- The Multiplex TUI is observability, not authority.
- Authority remains in durable artifacts, health checks, lane receipts, and Aletheon-reviewed commits.
- `codex exec resume` is allowed only for a proven matching phase/lane session; stale or unknown session identity must not be resumed.
- Cloud, MCP, API, and paid-provider expansion remains exploratory until secrets, scopes, rollback, and spend limits are explicit.

Next action: create and commit bounded `v361-v370` successor scripts, then start `v361`.
