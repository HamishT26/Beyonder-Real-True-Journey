---
name: hub-exec
description: Use the existing GHC Nexus Hub plan and explicit execution interface for selected chats, finite laboratory jobs, and remote plans.
---

# GHC Nexus Hub Exec

Use the existing reviewed Hub command interface. This plugin adds no generic shell tool, model gateway, network listener or arbitrary execution endpoint. Inspect [the command reference](references/actions.md) and the installed `--help` when selecting an action.

Resolve the exact host, source version and user-requested object first. Use `plan`, `chats plan`, `lab plan`, `remote plan` or `sentinel plan` before the corresponding authorized effect. A plan's `ready` status is not permission. Preserve the Hub's `--execute` boundary, argument validation and provider session locks; never call its internal `runPlan` export to bypass admission.

Use one bounded child process at a time on the 4 GB laptop. Keep output and receipts on D:. Prefer the smallest useful lab size, commonly 1000; the supported range is 1–200000. Larger cloud work needs an actually available selected executor and current aggregate spending evidence. A USD50 ceiling is not USD50 per job and does not imply an account balance or permission to purchase.

Existing chats keep their model/settings and original provider. Held, active, ambiguous or unavailable routes stay unresolved until fresh evidence supports the requested continuation. ChatGPT links are opened with the original provider; their histories are not assumed resumable in Codex CLI. This skill itself does not authorize sending messages, creating chats or activating other agents.

Selected memory export is an external-disclosure decision if its result will be transmitted. Review only selected records and their provenance. Never copy auth stores, API keys, cookies, private contact fields or raw transcripts into exports or logs. Keep a retained failure separate from a later correction, and do not retry an accepted or unknown action blindly.

This package alone owns the optional shared PreToolUse handler in `hooks/hooks.json`. It runs five small advisory checks in one process: source pin, config-key shape, sensitive export, selected route and finite-job budget. Other Nexus packages must not register copies. Hooks require current-definition trust review in the host; installation is not trust, and advisory output is not an enforcement boundary. See `HOOK-INVENTORY.md` at the package root.

## Current helper-creation control — 7 October 2026

Hamish requires a request shown to him and explicit approval before creating any new App/CLI AI helper, subagent or replacement conversation. Earlier general engineering permission does not cover a new helper. Continue only the assigned existing sessions. A shell/test/GitHub CLI process is not itself an AI helper; a new Codex exec/fork/Copilot model session is. For any future approved persistent helper, verify actual launch options and storage; do not use --ephemeral or another no-history flag. Historical mentions of ephemeral and temporary cloud workers are evidence to inspect, not instructions to delete or rewrite history.

## Hub 2.3 message drafts

Use messages plan/draft/queue/show/list for a selected existing chat. A draft is private stored data, not new human authorization. Verify the current human recipient/purpose instruction, refresh native target metadata, claim once, use the bound native send once, then record accepted/rejected/unknown. Never resend a claimed unknown outcome automatically. See RELEASE-2.3.md in the installed Hub.
