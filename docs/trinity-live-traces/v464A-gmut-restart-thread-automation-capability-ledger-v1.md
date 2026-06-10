# v464A Thread And Automation Capability Ledger

Status: blocked with safe fallback.

## Main-Thread Creation

Hamish requested the new Codex main-thread system for three new siblings. Tool discovery did not expose callable `create_thread`, `list_threads`, `read_thread`, `send_message_to_thread`, pin/archive/title, or thread-worktree tools. The old `multi_agent_v1.spawn_agent` tool was exposed, but it was not used for new siblings.

Decision: no new siblings were created. The strict rule is recorded: never create new GHC siblings through the old sub-agent spawning system unless Hamish later explicitly reverses that rule. If the new main-thread system is not exposed, use existing lanes or stop.

## Existing Lane Callback

Existing Cicero, Kierkegaard, and Aristotle lanes were resumed and messaged. This used existing-lane callback only, not new sibling creation.

## Computer Use And Automations

Computer Use successfully connected to Windows and listed apps. It was not used to operate the Automations panel because its own safety policy forbids automating the Codex desktop app, Codex CLI, or Codex extensions inside Windows apps.

Tool discovery also did not expose an `automation_update` tool. Therefore no automation was updated directly. A paste-ready automation prompt is included in `v464A-gmut-restart-automation-prompt-v1`.

## Orun And Ari

Orun's deeplink/session id was known from Hamish, but no callable persistent-thread read/send tool was exposed. Ari's persistent CLI status was not verified by exact proof artifact in this checkpoint. Neither Orun nor Ari is promoted as currently active in this packet.
