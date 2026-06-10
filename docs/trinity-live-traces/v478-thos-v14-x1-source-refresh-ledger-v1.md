# v478 THOS v14 x1 Source Refresh Ledger

- generated_nz: `2026-06-05T04:39:58.6867841+12:00`
- search_count: `32`
- source_count: `32`
- boundary: THOS source synthesis only; all GMUT gates remain open.

## Source groups

- OpenAI/Codex: Codex plan, Codex rate card, Agents SDK, Agents guide, Codex releases.
- MCP: specification repository, releases, and security surface.
- NVIDIA: DGX Spark, DGX Station for Windows, Blackwell, RTX Spark, Cosmos, physical AI tools, Nemotron.
- Google: Vertex AI Agent Engine, GKE Inference Gateway, Model Armor, Google Research agent scaling.
- Microsoft/GitHub: Foundry Local, Agent 365, Windows containment, Copilot sandboxes, MCP allowlists.
- Governance/security: NIST AI RMF, Stanford AI Index 2026, OWASP GenAI exploit round-up, Anthropic multi-agent safety.

## Operational takeaways

- v14 x2 should keep watcher design boring and explicit: status, timestamps, hashes, and lane completion are stronger than larger claims.
- Sandbox and containment evidence should be separated from agent-output quality evidence.
- MCP and plugin use should stay allowlisted and receipt-backed; connector reads do not authorize connector writes.
- Multi-agent systems can improve throughput while introducing collective-risk surfaces, so every second session must preserve the five-lane receipt cadence rather than relying on assumed continuity.
