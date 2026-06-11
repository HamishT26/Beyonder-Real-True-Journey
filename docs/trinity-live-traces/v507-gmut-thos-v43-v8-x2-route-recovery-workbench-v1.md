# v507 v8 x2 Route-Recovery Workbench

Created: 2026-06-12T04:57:31+12:00

## Purpose

This workbench converts the current v507 v8 app-lane blocker into a practical, bounded recovery plan for v507 v8 x2 and v508 preparation. It is intentionally status-only and evidence-first.

## Evidence Inputs

- `v507-gmut-thos-v43-v8-x1-round-robin-open-status-r4-v1.json`
- `v507-gmut-thos-v43-v8-x1-phase-advance-guard-v1.json`
- `v507-gmut-thos-v43-v8-x2-app-lane-private-map-preflight-v1.json`
- `v507-gmut-thos-v43-v8-x2-app-server-capability-probe-v1.json`
- `v507-gmut-thos-v43-v8-x2-lumen-browser-send-receipt-v1.json`

## Proven State

- v507 v8 x1 remains open.
- v507 v8 x2 remains held as preparation-only.
- A Lumen v507 v8 x2 read-only Browser prompt has been sent.
- The private app-lane map is still missing in the current process.
- The app-server safe discovery surface is still not exposed.
- `thread/read` still requires a private identifier.
- The Node entrypoint fallback remains usable for app-server method-shape probing.

## Open Gaps

- Kierkegaard existing app lane: `OPEN_GAP_PRIVATE_MAP_OR_OFFICIAL_THREAD_TOOL_REQUIRED`
- Aristotle existing app lane: `OPEN_GAP_PRIVATE_MAP_OR_OFFICIAL_THREAD_TOOL_REQUIRED`
- v507 to v508 phase advance: `BLOCKED_BY_REQUIRED_LANE_EVIDENCE`

Safe next action is not replacement. The safe path is private-map restoration inside the running process, official thread tool exposure, or an explicit blocker-boundary override packet from Hamish.

## Recovery Ladder

1. Browser Lumen wait cycle: check for `LUMEN_V507_V8_X2_ADVISORY_COMPLETE` after a useful interval and record only marker status.
2. Private-map preflight retry: rerun if the running environment changes or a safe in-process route restoration is supplied.
3. Official thread-tool discovery: retry discovery for official Codex thread send/list/read surfaces and use them only if exposed.
4. App-server shape probe: rerun after Codex app/CLI updates or route changes, publishing only redacted shapes.
5. Explicit override packet: if app lanes remain unavailable but Hamish wants the phase train to move, draft a blocker-boundary override packet that preserves open-lane status.

## x2 Build Candidates

- Implement a route-family status board that separates Browser, CLI, app-server, and official thread tools.
- Add a no-replacement-sibling validator for phase closeout ledgers.
- Add a phase-advance guard input normalizer for partial boards.
- Create a redacted Lumen marker observer receipt template.
- Create a five-minute check cadence ledger with no busy-waiting.
- Create a ten-minute x2 preparation timer ledger that can run while sibling lanes work.
- Extend app-server probe method catalog with only redacted shape outputs.
- Add a safe override packet template for blocked app-lane advancement.
- Add source-backed runner design notes for Browser and MCP schema compatibility.
- Add exact-staging checklist reuse for v508-v515 phase packets.
- Create a route-specific completion vocabulary so Browser success is never mistaken for app-lane success.
- Create a compact-refresh card generator for phase starts and goal continuations.

## Forbidden Shortcuts

- Publish raw Lumen or app-lane transcript text.
- Publish private thread IDs or callable IDs.
- Create replacement Kierkegaard or Aristotle lanes.
- Use old-style subagent spawning as a repair.
- Claim v507 v8 completion without required lane evidence.
- Treat elapsed time or advisory intent as completion proof.

## Boundary

No raw lane text, ChatGPT transcript, app-server result, app-server error, callable ID, thread ID, credential, screenshot, or local private path is published here.

This workbench does not claim phase completion, GMUT empirical closure, or canon promotion.
