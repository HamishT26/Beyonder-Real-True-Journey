# Codex App Automation Bridge

Generated UTC: `2026-05-16T11:25:53.351953+00:00`
Status: `ready_for_app_thread_automation_or_local_fallback`

Capability boundary:
- The current Codex tool surface does not expose the app automation creation tool. This bridge provides the exact app-thread automation request plus local fallback commands.

Recommended app automation:
- Type: `thread`
- Schedule: `every 5 minutes until v301-v320 starts or the user updates the automation`

Manual thread automation request:

```text
Create a thread automation attached to this current Codex thread.
Name: GHC v281-v360 recovery wake bridge.
Schedule: every 5 minutes until I ask you to stop or update it.
Project: use the local Beyonder-Real-True Journey worktree at D:\GHC-Archives\worktrees\v58-omega.
Automation type: thread automation, not standalone, because this workflow must preserve the current thread context.
Sandbox: prefer workspace-write or stricter. Do not use full access unless I explicitly approve it for a specific run.

On each wakeup:
1. Inspect the v281-v300 lane counts, the global v2 watcher status, the v301-v320 start gate, and the Aletheon wake signal.
2. If v281-v300 is below 600/600 or global v2 is incomplete, report only material progress, blockers, or stale runners. Do not stage live partial lane replies.
3. If v281-v300 is 600/600 and global v2 is complete, wake Aletheon in this thread and ask to begin v301-v320 from the prepared gate and reactivation packet.
4. Before any commit or push, verify branch drift and stage only curated non-raw artifacts. Never stage .raw.txt files, stdout/stderr logs, live .log files, or active partial lane files.
5. Preserve the truth boundary: the local wake signal is a durable prompt, not proof that the app can resume itself without this automation.

Stop condition: after v301-v320 has started and a v321-v340 handoff exists, ask whether to update this automation for v341-v360 or archive it.
```

Local fallback commands:
- `python scripts\trinity_v301_v320_start_gate.py`
- `python scripts\trinity_aletheon_wake_signal_poller.py --reason v295-v300-recovery-v301-gate`
- `python scripts\trinity_aletheon_reactivation_packet.py --source local-wake-signal --target-phase v301-v320 --reason "Wake Aletheon when v281-v300 reaches 600/600 and global v2 synthesis is complete"`
- `python scripts\trinity_v281_v300_global_v2_runner.py --watch --poll-sec 180 --timeout-sec 172800 --write-supervisor-candidate --write-reactivation-packet-on-complete --reactivation-target-phase v301-v320`

Current gate summary:

- `v301_ready`: `False`
- `valid_responses`: `450`
- `expected_responses`: `600`
- `complete_phases`: `15`
- `expected_phases`: `20`
- `first_incomplete_phase`: `296`
- `wake_status`: `waiting`
- `reactivation_target_phase`: `v301-v320`

Official docs basis:
- https://developers.openai.com/codex/app/automations - Codex app automations can be created from a regular thread by specifying task, schedule, and thread versus standalone behavior.
- https://developers.openai.com/codex/app/automations - Thread automations are recurring wakeups attached to the current thread and are appropriate for long-running command checks.
- https://developers.openai.com/codex/app/automations - Automations use default sandbox settings and unattended full access carries elevated risk.
