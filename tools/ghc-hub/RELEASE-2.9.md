# GHC Nexus Hub 2.9

Hub 2.9 fixes message records and makes recovery after interruption more reliable. It retains the existing private 25-tool connector and its command approvals.

## Changes

- Reject duplicate aliases for one target before creating a draft.
- Canonicalize receipt UUIDs before persistence and idempotency comparisons.
- Normalize ChatGPT host metadata to null before route binding.
- Report ineligible status, missing hosts and ambiguous UUIDs accurately in route listings. Route listings use one consistent catalogue snapshot; claims still refresh their own state.
- Refuse a new tunnel launch when process state is missing or nonboolean.
- Report Stop as pending while the process still runs. Status and Stop remain available when a server deployment input is missing.
- Refresh the existing Exec plugin to 0.1.8 with 15 source fingerprints. No lifecycle hook is added.

## Validation

The final focused message run passed 34/34 tests; launcher-state fixtures passed 14/14. Seven separate direct-module readiness checks passed. These are distinct evidence groups and are not summed into an invented full-suite count. An earlier 33/34 run failed in selector-fixture setup with Windows EPERM. That receipt is retained; the fixture was changed to create its intended initial configuration directly, and the complete focused run then passed. An earlier selected-test invocation stalled without output and was interrupted.

The prior 26 SDK interoperability checks belong to Hub 2.8. The modern admin rerun was capacity-held and is not claimed as a new 2.9 success. Installation hashes and the real private connection have separate deployment receipts.

## Operating scope

Hamish selected native chat tools for current communication. The MCP relay remains exposed but is not part of this operating path; it has no autonomous sender. Preserve original App/CLI histories, reconcile unknown delivery, and distinguish acceptance from recipient completion.

The compatible mcp-hub28-server.mjs entrypoint and ghc.hub28.config.v1 schema remain in use; runtime metadata reports 2.9.0. Administrator commands still require exact local approval. GUI input remains unexposed. Windows Native/CMD remain selected, and WSL is on-demand only.

The verified 87-file 2.8 rollback is in the owner midday recovery bank. No App cache or conversation history is deleted by this release.
