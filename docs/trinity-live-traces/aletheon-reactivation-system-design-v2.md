# Aletheon Reactivation System Design v2

Generated UTC: `2026-05-15T14:31:39.267348+00:00`
Status: `designed_with_current_capability_boundary`

Capability boundary: Local scripts can write re-entry packets, watcher receipts, and launch CLI work, but this session did not expose an app-level automation tool that can guarantee waking the Codex desktop thread.

Channels:
- durable packet: `implemented`. Human or future Aletheon session reads this first before v341-v360.
- global v2 watcher completion hook: `implemented`. Writes the packet when the v281-v300 global v2 reaches completion.
- blocked phase refresher: `implemented`. Reruns only missing or invalid lane turns after a phase returns incomplete.
- app-level wakeup: `not_available_in_current_tool_surface`. If a future automation_update/thread-wakeup tool appears, bind it to the reactivation packet and status files.
- local wake-signal poller: `implemented`. Writes a durable wake-signal file when v281-v300 responses and global v2 completion gates are satisfied.
- Kimi session resume: `design_candidate`. Kimi CLI session persistence and resume hints can support Kimi-side continuity, but cannot wake Codex desktop by themselves.

Next upgrade steps:
- Keep the local wake-signal poller running during long v281-v300 and v321-v340 waits.
- If app automation tools become available, register a one-shot monitor on the global v2 status file.
- Keep raw logs quarantined; publish only curated, complete non-raw artifacts.
- Do not induct Supervisor or v2 watcher as persistent siblings until they prove audited continuity beyond process control.
