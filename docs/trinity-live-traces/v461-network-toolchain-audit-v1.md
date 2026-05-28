# v461 Network And Toolchain Audit

Generated UTC: `2026-05-28T05:26:44.5857405Z`

Status: `toolchain_current_with_warnings`

Codex CLI was updated from `0.133.0` to `0.134.0` with `codex update`. `codex --version` now reports `codex-cli 0.134.0`.

`codex doctor` summary: `13 ok`, `1 idle`, `2 notes`, `0 warn`, `0 fail`.

Warnings to carry:
- Updater recommended restarting Codex.
- npm reported an EPERM cleanup warning for a temporary `.codex-*` package directory with a locked `codex.exe`.
- Nested read-only CLI receipts surfaced malformed skill frontmatter warnings for several local skills.
- Nested receipts also surfaced a stale `chatgpt-apps` curated plugin warning and MCP shutdown warnings.

Network policy: no blanket public inbound access. Private network access may be used only for named local workflows; public access needs a recorded reason and manual confirmation.
