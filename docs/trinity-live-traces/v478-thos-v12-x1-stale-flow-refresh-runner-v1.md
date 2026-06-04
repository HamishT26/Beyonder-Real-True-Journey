# v478-thos-v12-x1 Stale Flow Refresh Runner

- generated_nz: `2026-06-05T02:17:37+12:00`
- overall_status: `STALE_FLOWS_DETECTED`
- notify_aletheon: `true`
- stale_flow_count: `3`
- policy: status-only; no live lane mutation; no new threads; no old-style spawning.
- claim boundary: stale-flow planning only; all GMUT gates remain open.

## Flow Rows
- `STALE-BACKGROUND-PARTIAL` / `partial_open`: background notifier completed app lanes while CLI final markers remained open Next action: preserve split app/CLI status and continue other approved work.
- `STALE-MULTIPLEX-CLI-OPEN` / `visible_open`: multiplex board displays app readiness with CLI lanes still open Next action: keep board active and route repair planning through Fix-Enhancement Updater.
- `STALE-FIX-ENHANCEMENT-OPEN-ISSUES` / `plan_ready_open`: fix-enhancement receipt retains open issue rows for approved repair planning Next action: convert repeated open rows into exact packet tasks or bounded runner changes.
- `READY-SKILL-EVOLUTION` / `ready_verified`: live skill evolution receipt verifies draft match and frontmatter Next action: use evolved skill rules for future sibling-lane orchestration.
