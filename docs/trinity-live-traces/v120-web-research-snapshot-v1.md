# v120-web-research-snapshot-v1

```json
{
  "generated_utc": "2026-05-05T12:31:30+00:00",
  "phase": "v120",
  "mode": "official_docs_and_primary_sources_only",
  "sources": [
    {
      "title": "Using Codex with your ChatGPT plan",
      "url": "https://help.openai.com/en/articles/11369540-codex-in-chatgpt",
      "relevance": "Codex plan usage, plugin controls, model/version variability, and data-control surfaces."
    },
    {
      "title": "OpenAI Docs MCP",
      "url": "https://developers.openai.com/learn/docs-mcp",
      "relevance": "OpenAI's docs MCP is read-only documentation access and can be configured through Codex."
    },
    {
      "title": "Model Context Protocol architecture overview",
      "url": "https://modelcontextprotocol.io/docs/learn/architecture",
      "relevance": "MCP host/client/server separation, JSON-RPC data layer, and stdio versus streamable HTTP transports."
    },
    {
      "title": "Official MCP Registry",
      "url": "https://registry.modelcontextprotocol.io/",
      "relevance": "Public MCP server discovery surface that requires trust and quality gates before activation."
    }
  ],
  "decisions": [
    "Use MCP sources as context and capability discovery, not as authority to mutate provider accounts.",
    "Keep OpenAI docs MCP as a candidate read-only documentation lane before OpenAI product/API implementation changes.",
    "Classify remote MCP servers and registry entries as untrusted third-party surfaces until inspected and pinned.",
    "Preserve v120 provider probing as local command availability/version checks with no secret reads and no provider writes."
  ]
}
```
