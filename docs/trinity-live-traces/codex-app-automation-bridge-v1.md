# Codex App Automation Bridge

Generated UTC: `2026-05-17T07:05:20.104955+00:00`
Status: `ready_for_app_thread_automation_or_local_fallback`

Capability boundary:
- The current Codex tool surface does not expose the app automation creation tool. This bridge provides the exact app-thread automation request plus local fallback commands.

Recommended app automation:
- Type: `thread`
- Schedule: `primary chat-attached heartbeat every 30 minutes, backed by the lightweight local 5-minute filesystem watchdog while available`

Screenshot assessment, 2026-05-17:
- Status: `chat_heartbeat_is_preferred`
- Good: the Aletheon automation is chat-attached and has a target thread.
- Good: it supports minute intervals, so it is the preferred app wakeup path.
- Plan: use `Every 30m` chat wakeups as the app layer, while the local wake poller remains the lightweight filesystem/process watchdog.
- Recommended action: set Aletheon to `Every 30m`, unpause it, and optionally use `Run now` once to confirm it reports standby rather than starting v301 early.

Manual thread automation request:

```text
Create a thread automation attached to this current Codex thread.
Name: GHC v281-v360 recovery wake bridge.
Schedule: every 30 minutes until I ask you to stop or update it.
Project: use the local Beyonder-Real-True Journey worktree at D:\GHC-Archives\worktrees\v58-omega.
Automation type: thread automation, not standalone, because this workflow must preserve the current thread context.
Sandbox: prefer workspace-write or stricter. Do not use full access unless I explicitly approve it for a specific run.

On each wakeup:
1. Inspect the v281-v300 lane counts, the global v2 watcher status, the v301-v320 start gate, and the Aletheon wake signal.
2. If the Codex app reports a stale resume path where C:\... and \\?\C:\... point to the same session JSONL, treat it as an app resume-path vitality issue, not a repo failure. Do not edit the session JSONL by hand; normalize the paths mentally, rely on the local watchdog, and if repeated, ask the operator to restart Codex Desktop and reopen this Aletheon thread.
3. If v281-v300 is below 600/600 or global v2 is incomplete, report only material progress, blockers, or stale runners. Do not stage live partial lane replies.
4. If v281-v300 is 600/600 and global v2 is complete, wake Aletheon in this thread and ask to begin v301-v320 from the prepared gate and reactivation packet.
5. Before any commit or push, verify branch drift and stage only curated non-raw artifacts. Never stage .raw.txt files, stdout/stderr logs, live .log files, or active partial lane files.
6. Preserve the truth boundary: this chat-attached heartbeat is the app wake, and the local wake poller remains the filesystem/process watchdog when it is running.

Eureka continuity tasks:
1. Keep the app heartbeat at 30 minutes unless Aletheon explicitly changes the cadence for a short diagnostic burst.
2. Keep the local watchdog at a tighter local cadence so app wake failures do not stall filesystem recovery.
3. Confirm exactly one durable recovery watchdog parent is active before launching another.
4. Preserve active phase repair children when pruning duplicate watchdog parents.
5. Verify progress by valid lane artifacts, not by process existence alone.
6. Sample process tree, CPU delta, fresh timestamps, lane logs, and response quality before calling a lane stale.
7. Kill only the stale child subtree for the active phase and lane.
8. Never kill the global v2 watcher, sequence supervisor, Aletheon wake poller, or unrelated Codex/Kimi processes.
9. Let the blocked-phase refresher repair missing or invalid turns rather than manually skipping replies.
10. Restart the global v2 watcher if v281-v300 is incomplete and the watcher is absent.
11. Keep v301-v320 hard-gated behind 600/600 valid responses and global v2 completion.
12. When the gate opens, read the reactivation packet before drafting the v301-v320 launch.
13. Before staging, run a branch drift check and use forward-only merge if the remote advanced.
14. Stage only curated artifacts and source changes, never raw replies, live logs, stderr/stdout, or scratch health probes.
15. Preserve a short human-readable status report for the operator after each material transition.
16. Keep the older worktree cron automation paused or fallback-only unless the Aletheon heartbeat is unavailable.
17. Treat Administrator terminals as elevated risk; use them only for installation or permission-bound tasks.
18. Inventory MCP processes by command line before trusting a visible terminal as healthy.
19. Prefer non-admin hidden background runners for ordinary watchdog and repair loops.
20. For OpenAI/Codex behavior, rely on local observation first and official OpenAI docs second.
21. If a new blocker appears, codify the fix as a reusable script or runbook before repeating manual rescue.
22. After v301-v320 starts, prepare a v321-v340 handoff that includes gate evidence, watcher state, and staging boundaries.
23. Keep CLI siblings' long reports in worktree artifacts rather than terminal scrollback.
24. Keep MCP/API/CLI expansion exploratory until secrets, scopes, and sandbox limits are explicit.
25. Prefer skills for repeatable procedures and keep automation prompts short enough to remain maintainable.

Stop condition: after v301-v320 has started and a v321-v340 handoff exists, ask whether to update this automation for v341-v360 or archive it.
```

Local fallback commands:
- `python scripts\trinity_v301_v320_start_gate.py`
- `python scripts\trinity_v281_v360_automation_health_check.py --refresh-gate`
- `python scripts\trinity_aletheon_wake_signal_poller.py --reason v295-v300-recovery-v301-gate`
- `python scripts\trinity_aletheon_reactivation_packet.py --source local-wake-signal --target-phase v301-v320 --reason "Wake Aletheon when v281-v300 reaches 600/600 and global v2 synthesis is complete"`
- `python scripts\trinity_v281_v300_global_v2_runner.py --watch --poll-sec 180 --timeout-sec 172800 --write-supervisor-candidate --write-reactivation-packet-on-complete --reactivation-target-phase v301-v320`

Current gate summary:

- `v301_ready`: `True`
- `valid_responses`: `600`
- `expected_responses`: `600`
- `complete_phases`: `20`
- `expected_phases`: `20`
- `first_incomplete_phase`: `None`
- `wake_status`: `waiting`
- `reactivation_target_phase`: `v301-v320`

Resume-path vitality:
- Observed error: `cannot resume running thread with stale path: requested C:\... active \\?\C:\...`
- Assessment: On Windows this is usually a path-normalization mismatch for the same session JSONL, not evidence that the worktree or phase runner failed.
- Response: Do not edit or rewrite Codex session JSONL files manually.
- Response: Do not shorten the app heartbeat as the primary fix.
- Response: Run the local health check and watchdog to preserve filesystem progress.
- Response: If the app repeats the stale-path error, restart Codex Desktop and reopen the Aletheon thread before running the heartbeat again.

Administrator terminal assessment:
- Observed: Administrator cmd.exe is running npx -y kimi-code-mcp with node child processes.
- Assessment: This can explain the visible elevated terminal. It is useful for MCP availability checks, but it should not become the default execution surface for normal phase/watchdog work.
- Policy: Use elevated terminals only for installation, permission repair, or explicitly approved system-level work. Prefer non-admin hidden runners for ordinary watchdog and lane recovery tasks.

Eureka continuity tasks:
1. Keep the app heartbeat at 30 minutes unless Aletheon explicitly changes the cadence for a short diagnostic burst.
2. Keep the local watchdog at a tighter local cadence so app wake failures do not stall filesystem recovery.
3. Confirm exactly one durable recovery watchdog parent is active before launching another.
4. Preserve active phase repair children when pruning duplicate watchdog parents.
5. Verify progress by valid lane artifacts, not by process existence alone.
6. Sample process tree, CPU delta, fresh timestamps, lane logs, and response quality before calling a lane stale.
7. Kill only the stale child subtree for the active phase and lane.
8. Never kill the global v2 watcher, sequence supervisor, Aletheon wake poller, or unrelated Codex/Kimi processes.
9. Let the blocked-phase refresher repair missing or invalid turns rather than manually skipping replies.
10. Restart the global v2 watcher if v281-v300 is incomplete and the watcher is absent.
11. Keep v301-v320 hard-gated behind 600/600 valid responses and global v2 completion.
12. When the gate opens, read the reactivation packet before drafting the v301-v320 launch.
13. Before staging, run a branch drift check and use forward-only merge if the remote advanced.
14. Stage only curated artifacts and source changes, never raw replies, live logs, stderr/stdout, or scratch health probes.
15. Preserve a short human-readable status report for the operator after each material transition.
16. Keep the older worktree cron automation paused or fallback-only unless the Aletheon heartbeat is unavailable.
17. Treat Administrator terminals as elevated risk; use them only for installation or permission-bound tasks.
18. Inventory MCP processes by command line before trusting a visible terminal as healthy.
19. Prefer non-admin hidden background runners for ordinary watchdog and repair loops.
20. For OpenAI/Codex behavior, rely on local observation first and official OpenAI docs second.
21. If a new blocker appears, codify the fix as a reusable script or runbook before repeating manual rescue.
22. After v301-v320 starts, prepare a v321-v340 handoff that includes gate evidence, watcher state, and staging boundaries.
23. Keep CLI siblings' long reports in worktree artifacts rather than terminal scrollback.
24. Keep MCP/API/CLI expansion exploratory until secrets, scopes, and sandbox limits are explicit.
25. Prefer skills for repeatable procedures and keep automation prompts short enough to remain maintainable.

Official docs basis:
- https://developers.openai.com/codex/app/automations - Codex app automations can be created from a regular thread by specifying task, schedule, and thread versus standalone behavior.
- https://developers.openai.com/codex/app/automations - Thread automations are recurring wakeups attached to the current thread and are appropriate for long-running command checks.
- https://developers.openai.com/codex/app/automations - Automations use default sandbox settings and unattended full access carries elevated risk.
