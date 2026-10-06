---
name: hub-admin
description: Plan and operate the existing GHC Nexus Hub Windows administrator and registered-app routes, with host-specific privilege observations.
---

# GHC Nexus Hub Admin

Use the installed Hub at `D:/GHC-Archives/global-tools/ghc-nexus-hub/hub.mjs`. This package supplies an operating workflow, not a privilege provider. On another host, locate its separately reviewed Hub installation; D: is not an implied cloud mount.

Read [the supported routes](references/routes.md) for the chosen action. Inspect `actions --json` and `plan ACTION --json` before an authorized `run ACTION --execute`. Use the available terminal execution tool, not terminal UI automation. An existing user authorization remains valid within its scope; the plan does not confer new authority.

Separate four observations: requested Hub route, current executor token, child-app token, and provider/cloud rights. `doctor --json` observes this executor and writes one small Hub event; it does not attest every process. A plugin called Admin, a Full access setting, or a successful process-start request grants no Windows membership or cloud role. Use normal Windows consent when the existing signed launcher requests it; never automate the consent dialog or change security settings to avoid it.

The direct administrator App route and registered App route serve different purposes. Preserve the direct route for the user's chosen elevated work. Use the registered route for package identity and update checks when the user is ready to close and reopen the App. Do not repair the already-working launcher, switch routes mid-task, force-close an App, or repeat a start after an unknown outcome.

Before a mutation, retain the source hash, plan, selected host, expected effects and rollback reference. Afterward, report the actual exit/status and the scope of token evidence. A timeout can mean unknown effect; reconcile the existing process rather than starting a duplicate. Keep credential stores and private configuration backups outside shareable receipts.

## Current helper-creation control — 7 October 2026

Hamish requires a request shown to him and explicit approval before creating any new App/CLI AI helper, subagent or replacement conversation. Earlier general engineering permission does not cover a new helper. Continue only the assigned existing sessions. A shell/test/GitHub CLI process is not itself an AI helper; a new Codex exec/fork/Copilot model session is. For any future approved persistent helper, verify actual launch options and storage; do not use --ephemeral or another no-history flag. Historical mentions of ephemeral and temporary cloud workers are evidence to inspect, not instructions to delete or rewrite history.
