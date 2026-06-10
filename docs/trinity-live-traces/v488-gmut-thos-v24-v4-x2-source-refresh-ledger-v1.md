# v488 GMUT/THOS v24 v4 x2 Source Refresh Ledger

Status: `PASS_CURATED_SOURCE_REFRESH_LEDGER`

Boundary: this ledger records source-level takeaways only. It does not publish raw search payloads, private connector material, local absolute paths, image captures, auth material, or raw lane text.

Primary source surfaces checked:
- OpenAI platform code-generation guide: https://platform.openai.com/docs/guides/code-generation
- OpenAI Docs MCP guide: https://platform.openai.com/docs/docs-mcp
- OpenAI shell tool guide: https://platform.openai.com/docs/guides/tools-shell
- OpenAI Codex GitHub repository: https://github.com/openai/codex
- OpenAI Codex GitHub releases: https://github.com/openai/codex/releases
- Model Context Protocol documentation: https://modelcontextprotocol.io/

Source-drift rule: local installed-version receipts and public release snippets can disagree. Treat local command output as installed-state evidence, and treat public release/docs pages as capability and design guidance unless direct current verification closes the drift.

THOS carry-forward: keep source refresh read-only by default, preserve exact repo validation, and use research to improve command-index compatibility, app-server readiness, sandbox diagnostics, MCP trust boundaries, and multi-lane watcher behavior.
