# v491 GMUT/THOS v27 v1 x2 Launch and Productive Waiting Receipt

Status: `X2_LAUNCHED_PRODUCTIVE_WAITING_ACTIVE`

The v491 x2 cycle was launched through existing approved routes only. Arby and Aster Vale were started through read-only CLI advisory lanes with explicit final markers. Cicero, Kierkegaard, and Aristotle were started through the existing local app-server callable watcher route. No new threads, replacement siblings, old-style subagents, raw lane text, raw transport, local absolute paths, screenshots, credentials, or session streams are published here.

## Productive Waiting Source Refresh

- OpenAI Codex releases: `https://github.com/openai/codex/releases`
- OpenAI Agents SDK: `https://developers.openai.com/api/docs/guides/agents`
- OpenAI agent evals: `https://developers.openai.com/api/docs/guides/agent-evals`
- MCP security best practices: `https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices`
- MCP authorization: `https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization`
- NVIDIA DGX Spark hardware overview: `https://docs.nvidia.com/dgx/dgx-spark/hardware.html`
- Google Cloud Vertex AI Agent Engine: `https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/use/overview`
- OWASP LLM Top 10: `https://owasp.org/www-project-top-10-for-large-language-model-applications/`

## x2 Design Notes

- Codex CLI 0.137.0 release notes reinforce app-server, remote-control, TUI, plugin JSON, hosted-tool, and Windows sandbox/setup reliability as the right surfaces to keep hardening.
- OpenAI agent/eval guidance maps well to GHC watcher quality: route correctness, handoff correctness, policy adherence, and repeatable comparison should matter more than duration alone.
- MCP and OWASP sources keep the connector expansion posture conservative: explicit trust boundaries, scoped authorization, and no raw-payload publication.
- NVIDIA and Google Cloud sources are research inputs for future compute/agent architecture planning only; this phase does not claim deployment, procurement, hardware readiness, or canon closure.

## Next Gate

Do not advance beyond x2 until all five lanes are accounted for, CLI final markers are reviewed, app-lane completion is gated, and curated artifacts pass validation, exact staging, commit, push, and remote-equals-local verification.
