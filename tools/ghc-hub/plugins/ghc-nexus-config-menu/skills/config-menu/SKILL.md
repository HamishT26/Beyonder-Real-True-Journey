---
name: config-menu
description: Inspect selected Codex configuration layers and prepare allowlisted display-setting proposals with source hashes, precedence conflicts and private rollback requirements.
---

# GHC Nexus Config Menu

Offer three operations: inspect selected layers, propose a supported display-setting change, or review a proposal for integration. The helper `scripts/config_menu.py` at the plugin root is read/propose only; it has no apply command. The existing Hub does not expose a config command at the recorded baseline.

Read [the input and review contract](references/config-contract.md). Supply explicit layer files, low to high precedence, plus whether each is declared active. Do not scan credential stores or raw histories. The helper parses TOML, emits only allowlisted values and source hashes, and reports overrides among selected active layers. That is selected-file evidence, not a claim to know the live host's effective settings.

The current proposal allowlist is `tui.alternate_screen`, `tui.animations`, and `hide_agent_reasoning`. Other keys, including models, context/compaction, privileges, authentication and hook-trust controls, require a separately scoped implementation and are refused by this helper. Do not work around a refusal with direct editing under this skill.

Before integration, resolve requirements/managed policy, invocation overrides, profiles and project trust through the actual host's supported controls. A Codex config file does not automatically govern the ChatGPT App, another computer, a managed cloud worker or the provider's account limits.

A proposal binds the exact target hash and records whether a higher selected layer overrides it. Conflicts and stale hashes prevent a ready proposal. Before any separately authorized write, save the exact original file to a private D-drive backup outside release artifacts, recheck its digest, apply only the reviewed keys while preserving unrelated TOML, parse and review the diff, then verify in that client. On rollback, compare the post-change digest first and preserve later edits. Never export a full config merely to demonstrate the three permitted fields.

## Retired Guardian flag audit and repair

The separate scripts/config_guard.py helper audits exactly features.guardianv2.thread_context in a selected TOML file, including profiles. Use audit --file ABSOLUTE-TOML first. A repair preview requires --expected-sha256; applying also requires --execute and --backup-dir pointing at an existing private backup directory. This narrow removal is separate from the display-setting proposal allowlist.

The helper removes supported standalone or dotted assignments, compares all other parsed settings, preserves comments/newline format outside removed lines, and verifies a private exact backup before replacement. Unsupported inline or multiline syntax is refused without rewriting. It is not a watcher: if another writer reintroduces the flag, audit that writer before another repair. Never rewrite a clean file or claim the running App warning cleared without observing it.
