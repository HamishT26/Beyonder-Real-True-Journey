> Current release: see [GHC Nexus Hub 2.2](RELEASE-2.2.md) for selected snapshot/restore, Sentinel offline planning, four local plugins, and corrected CMD/chat guidance. Earlier release details below are retained as history.

# GHC Nexus Hub 2

Keyboard terminal menu, ordinary commands and JSON for the current Windows or Linux executor. The core uses Node 20+ and its standard library. The optional read-only MCP bridge has pinned official SDK dependencies.

Menu 7 combines local Codex App/CLI records, managed-cloud routes, legacy cloud tasks and ChatGPT links. Menu 10 opens the Laboratory; later entries open Freed ID profiles, selected memory, Sentinel specifications and remote plans. Existing chats keep their selected provider and settings.

```text
ghc-nexus --help
ghc-nexus doctor --json
ghc-nexus chats list --json
ghc-nexus chats list --refresh --json
ghc-nexus chats plan --id EXACT-ID --json
ghc-nexus chats open --id EXACT-ID --execute
ghc-nexus lab run --id diffusion --size 1000 --execute --json
ghc-nexus identity verify --id merrin-tide --json
ghc-nexus sentinel plan --id sentinel-1 --json
ghc-nexus remote plan --json
```

The installed Windows command is a small wrapper in the D-drive tool directory; a new terminal may be needed to pick up its PATH entry. Before installation, use `node hub.mjs` followed by the same arguments. On Linux use `sh start-ghc-hub.sh` from this directory, or an explicitly installed wrapper. The Windows Administrator hub shortcut requests normal UAC. The ordinary App action uses registered package activation; the separate Administrator App action directly starts the signed current executable with normal Windows elevation.

A saved chat listing is not live admission to a session. Local resume requires a fresh provider summary and refuses held, busy, conflicting or unverified states. Managed-cloud and ChatGPT entries retain their original provider route. A failed metadata read never turns into a duplicate conversation.

Private profiles, memory and signing keys are stored separately from source. Human contact details stay in the private D-only file. MCP exposes fixed read-only aliases and summaries; it has no arbitrary shell, credential, raw-history or personal-contact tool.

PowerShell remains the local foundation. Existing managed cloud Linux handles larger work; WSL is optional and is not started by opening the menu. A phone connection controls its connected computer. The VPN supports authorized outbound private-service access and does not create an incoming cloud SSH endpoint or a permanent VM.

See [NEXUS-V2-GUIDE.md](NEXUS-V2-GUIDE.md) for the complete operator guide and evidence boundaries, [OPERATOR-GUIDE.md](OPERATOR-GUIDE.md) for the retained first-release history, and the release receipt for exact verification results.

## Configuration

`GHC_HUB_WORKSPACE` chooses an existing working directory; `GHC_HUB_HOME` is the event-state directory; `GHC_NEXUS_HOME` chooses the private Nexus state root; `GHC_NEXUS_HOST_ID` labels the current executor. `GHC_HUB_CODEX` and `GHC_HUB_PWSH` may name verified absolute executables. Local operator values are never imported from web documents. Windows overrides must be .exe files.

Read and plan commands return JSON without starting a model or shell. Writes and launches require `--execute`; interactive actions require a real terminal. Exit zero means that command's reported result, not global system certification. Missing dependencies, rejected arguments, invalid signatures and held execution use nonzero exits.

## Verification

```text
node --test --test-isolation=none --test-concurrency=1 hub.test.mjs privacy-regression.test.mjs nexus.test.mjs mcp-bindings.test.mjs
```

Set `GHC_HUB_TEST_TMP` to an owned D-drive directory on Windows. Test receipts distinguish Windows/Linux, supplied checks, independent review, live observations, retained first failures and isolated corrections. Historical suite counts do not become a new aggregate. Research run (3) x2 remains a separate, unstarted stage.
