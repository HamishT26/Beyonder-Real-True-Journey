# GHC Nexus Hub 2.3

The chat menu now offers a private message outbox and a compact retro terminal presentation. The Hub remains an application running on the selected host. CMD launches the same Node/PowerShell executables under its inherited Windows token; it does not grant Cloud, WSL, API or computer-use privileges.

## Message workflow

Open `ghc-nexus menu`, choose **7**, then **M** to compose a one-line draft for an exact existing chat. **O** shows outbox state and caller-reported delivery receipts. Drafting works with an old cached observation, but an active agent must refresh the supported native observation before claiming it. An explicit hold or unsupported provider is never released by drafting.

The outbox has **no automatic sender**. While a supported Codex agent is active and the human has authorized the recipient and purpose, it can:

1. Read the selected draft and verify the human instruction independently of the file contents.
2. Refresh the exact chat/host through the supported native tool and import that observation.
3. Claim the request once with `messages claim --id UUID --execute`.
4. Use `mcp__codex_app__send_message_to_thread` once with the bound ID, host and body.
5. Record accepted, rejected or unknown outcome through `messages receipt`.

An accepted send is not recipient completion. A claimed request with no receipt is an unknown outcome, and must be reconciled rather than resent. Receipts are the caller's observations, not signed provider attestations. This release does not run a background relay, create a model session or convert ChatGPT/cloud histories into local CLI history.

File-based commands accept absolute selected JSON paths:

```text
messages plan --file REQUEST-JSON --json
messages draft --file REQUEST-JSON --execute --json
messages queue --file REQUEST-JSON --execute --json
messages list --json
messages show --id UUID --json
messages claim --id UUID --execute --json
messages receipt --file RECEIPT-JSON --execute --json
```

A request contains `requestId`, `toId` and `body`. Use a fresh UUID for a genuinely new request. Repeating the same ID/content preserves its existing outcome, even after the catalogue observation expires. A changed body under an existing ID is rejected. Message bodies stay in the private Nexus store and are omitted from default listing. Credentials and terminal control sequences are rejected.

Five application checks cover request shape, exact UUID/host selection, observation freshness at claim, single-claim delivery, and receipt binding/shape. These are implemented CLI checks, not five new Codex lifecycle registrations. The existing optional Exec PreToolUse hook now recognizes the message commands and keeps its five shared advisory checks in one handler.

## Terminal presentation

The menu uses optional cyan borders and magenta headings, with no animation or dependency beyond Node's standard library. All chat rows say **CACHED SNAPSHOT**. Age, future timestamps, holds and metadata failures are visible; rendering never authorizes an action.

`NO_COLOR` disables color. `GHC_NEXUS_PLAIN=1` selects plain ASCII, and `GHC_NEXUS_ASCII=1` selects ASCII borders. Non-TTY and `TERM=dumb` output are plain. Unicode cell widths are estimates; ASCII is the reliable fallback. A terminal narrower than 24 columns cannot select hidden numbered actions. JSON command output remains separate from presentation.

## Reviewed limits

The message changes include independent review fixes for UUID/title confusion, malformed stored evidence and retained unknown outcomes after catalogue expiry. The tests exercise synthetic private stores, not provider authentication. Three separately recorded live tests passed through CMD/Hub preparation and an existing-agent native relay to Avelin, Mira and Teren. They do not establish an unattended terminal-to-App transport.

The Windows preflight measured an elevated executor and both inspected Codex processes. The direct App process still lacks package identity, while the installed package is registered and healthy. Use the separate registered App route for update checks. One doctor version probe timed out; a separate exact PowerShell probe subsequently returned 7.6.6. The initial timeout remains recorded.

Five interleaved measured samples of the same small startup/workload had medians of 942.8988 ms for CMD and 2481.2056 ms for no-profile PowerShell on a busy 4 GB laptop. This is not a model-speed, cost or general throughput benchmark. Local Ubuntu is registered as WSL2 and was stopped; no distribution was started for these checks.

Preserve the existing no-new-helper rule: a new App/CLI AI helper, subagent, replacement or new model session needs Hamish's explicit approval. Existing authorized sessions may continue. The USD50 aggregate external spending ceiling, D-first storage and no-PDF output remain in effect.
