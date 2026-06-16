# v540-gmut-thos-v76-v3-x1 Curated Source Ledger

Generated UTC: `2026-06-16T01:44:53Z`

Status: `PASS_CURATED_SOURCE_LEDGER`

## Sources

### source-01: OpenAI Codex changelog

- URL: `https://developers.openai.com/codex/changelog`
- Takeaway: the 2026-06-11 Codex app 26.609 entry adds Browser Developer Mode for Chrome and the Codex in-app browser, with controlled CDP access for performance, network, console, runtime, and page-state debugging; it also says Browser use is up to 2x faster through CDP and DOM snapshot optimizations.
- Phase use: use Browser Developer Mode as a bounded diagnostic surface for the Lumen route while keeping signed-in ChatGPT panel delivery status-only.

### source-02: OpenAI Codex 0.140.0 GitHub release

- URL: `https://github.com/openai/codex/releases/tag/rust-v0.140.0`
- Takeaway: Codex 0.140.0 adds usage views, larger goal preservation, session deletion with safeguards, selective import flows, unified mentions, MCP reliability fixes, and large-repository responsiveness improvements.
- Phase use: use the 0.140.0 line to improve goal-continuity, current-state beacons, MCP warning handling, and large-repo lookup discipline.

## Local Status Signals

- Codex CLI version observed: `codex-cli 0.140.0`
- Node version observed: `v24.15.0`
- npm version was not recorded because the combined version probe timed out after returning Node output.
