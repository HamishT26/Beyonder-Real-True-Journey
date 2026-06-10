# v490 GMUT/THOS v26 v2 x2 Source Prep Ledger

Generated NZ: `2026-06-06T03:01:45+12:00`

Status: `PASS_SOURCE_PREP_WHILE_BACKGROUND_WATCHING`

Boundary: source/prep work was performed while app-lane background watching remained open. This artifact publishes source-level takeaways only, not raw search payloads, raw transport, private connector material, local absolute paths, image captures, or auth material.

Primary sources:
- OpenAI Codex App Server architecture: https://openai.com/index/unlocking-the-codex-harness/
- OpenAI Codex releases: https://github.com/openai/codex/releases
- OpenAI Codex plugin wrapper: https://github.com/openai/codex-plugin-cc
- MCP security best practices: https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices
- Vertex AI Agent Engine Code Execution: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/code-execution/overview
- GKE Agent Sandbox: https://docs.cloud.google.com/kubernetes-engine/docs/how-to/agent-sandbox

Carry-forward rules:
- Use background app-lane watchers for future x1 calls.
- Do productive source/prep work while waiting.
- Keep security and sandbox sources mapped to concrete THOS guardrails.
- Keep all GMUT/THOS open gates intact.
