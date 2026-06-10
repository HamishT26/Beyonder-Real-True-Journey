# V101 Web Research Snapshot

- generated_utc: `2026-05-04T02:22:00+00:00`
- phase: `v101`
- mode: `official_docs_and_primary_sources_only`

## Sources

1. OpenAI Help Center, `Using Codex with your ChatGPT plan`: https://help.openai.com/en/articles/11369540-codex-in-chatgpt
2. OpenAI Developers, `Docs MCP`: https://developers.openai.com/learn/docs-mcp
3. Model Context Protocol, `Architecture overview`: https://modelcontextprotocol.io/docs/learn/architecture
4. Model Context Protocol, `Official MCP Registry`: https://registry.modelcontextprotocol.io/

## Decisions

- Use MCP sources as context and capability discovery, not as authority to mutate provider accounts.
- Keep OpenAI docs MCP as a candidate read-only documentation lane before any OpenAI product/API implementation changes.
- Classify remote MCP servers and registry entries as untrusted third-party surfaces until inspected and pinned.
- Preserve `v101` provider probing as local command availability/version checks with no secret reads and no provider writes.
