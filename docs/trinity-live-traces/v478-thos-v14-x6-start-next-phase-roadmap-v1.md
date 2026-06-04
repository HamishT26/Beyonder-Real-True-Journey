# v478 THOS v14 x6 Start Next-Phase Roadmap

- generated_nz: `2026-06-05T10:08:00+12:00`
- overall_status: `PASS_ROADMAP_PREP_WHILE_CLI_LANES_RUNNING`
- claim boundary: x6 start wait-time roadmap only; x6 lane completion is not claimed here; all GMUT gates remain open.

## Timing Policy

- Soft wait baseline: `312.832` seconds.
- Baseline role: first check-in point only.
- Observation window: `1800` seconds.
- Completion requirement: true app completion, CLI final marker, or blocker receipt.

## Roadmap Items

- `x6-closeout-five-lane-foldback`: fold app completion and CLI final-marker receipts into x6 start synthesis.
- `x6-closeout-command-compatibility`: carry the command-index v6 compatibility gap as a known open gap rather than rediscovering it.
- `x6-closeout-source-security`: map official OpenAI, MCP, OWASP, Microsoft, and NVIDIA source notes into runner and skill-governance implications.
- `x7-start-roster-discipline`: use every-second-session roster discipline for x7 only if the cadence demands it; otherwise keep five-lane state warm for the next required boundary.
- `x7-stale-flow-guard`: if CLI final markers are slow again, record the delay as a stale-watch item only after evidence repeats; avoid premature repair.
- `x7-publication-readiness`: keep validation and exact-staging packet small enough to publish without touching unrelated dirty worktree files.
