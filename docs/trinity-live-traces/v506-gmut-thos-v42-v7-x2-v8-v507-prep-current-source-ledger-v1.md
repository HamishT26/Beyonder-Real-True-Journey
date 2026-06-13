# v506 GMUT/THOS v42 v7 x2 and v8 v507 Prep Current Source Ledger v1

Generated: 2026-06-11T07:54:22Z

Status: CURRENT_SOURCE_LEDGER_PREPARED

## Sources Used

- OpenAI Codex GitHub releases: https://github.com/openai/codex/releases
- OpenAI Developers Codex changelog: https://developers.openai.com/codex/changelog

## Source Takeaways For v507

- Codex CLI 0.139.0 supports direct standalone web search from code mode and improves schema preservation for richer tool and connector inputs. This is relevant to the Local GHC Multiplex IPC bus because the bus should keep payload schemas explicit instead of flattening or hiding nested route contracts.
- Codex CLI 0.139.0 improves doctor reporting and keeps raw JSON values redacted. This supports the status-only receipt pattern used in the v506-to-v507 prep bridge.
- Codex CLI 0.139.0 includes fixes around MCP startup warning scoping, image edit path routing, thread reset feature-flag preservation, and sandbox decision consistency. These map directly to stale-flow watch items already tracked by the GHC runners.
- Codex app 26.608 improves plugin navigation, settings search, goal notification behavior, diff ordering, and Windows rendering. These changes support the long-running goal workflow, but they are not completion proof for any sibling lane.

## Operational Decisions

- Keep Browser-first live-adapter work gated to the approved v507 boundary.
- Keep source ledgers bounded and cite primary sources.
- Treat plugin-cache and user-skill mutation as out of scope unless exact approval exists.
- Treat web-search volume as useful only when it produces actionable synthesis; do not chase raw search counts at the expense of phase evidence.

No raw web payloads, private connector material, credentials, screenshots, or raw lane text are published here.

All GMUT, canon, empirical, legal, and consciousness gates remain open.
