# v497 GMUT/THOS v33 v6 x2 Source/Reflection/Build Crosswalk

- overall_status: `PASS_SOURCE_REFLECTION_BUILD_CROSSWALK_READY`
- generated_utc: `2026-06-06T21:25:50Z`

## Crosswalk Rows

- Codex release volatility: use [OpenAI Codex releases](https://github.com/openai/codex/releases) as a planning anchor. Launcher and version receipts must stay explicit because CLI behavior changes quickly. x2 build: carry version and launcher state into readiness packets without treating version freshness as proof of lane quality.
- MCP least privilege: use [MCP security best practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). App lanes, CLI lanes, connector reads, and repair helpers are separate authority classes. x2 build: keep existing lane routing only and convert any authority gap into a stale-flow blocker receipt.
- GenAI observability: use [OpenTelemetry GenAI conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/). The runner needs consistent fields for phase, lane, boundary, quality, repair state, and blocker state. x2 build: promote `repair_state` and `watcher_policy` fields into v6 x2 boards.
- Agent callback structure: use [Google ADK callbacks](https://google.github.io/adk-docs/callbacks/). Prelaunch, cadence, completion, quality, repair, and publication are distinct hooks. x2 build: keep cadence gates separate from completion gates so Aletheon can work while watchers supervise.
- Guardrail separation: use [NVIDIA NeMo Guardrails](https://docs.nvidia.com/nemo-guardrails/index.html). No-overclaim and raw-boundary checks are core runtime guardrails. x2 build: publish a no-overclaim guard and make it a prerequisite for v7 x1 launch.

## Claim Boundary

Sources are planning inputs only. No empirical closure, final physics proof, consciousness proof, or canon promotion is claimed.
