---
name: connector-materialization-integration
description: Operate the Connector Materialization Integration pack with explicit proof boundaries.
---

# Connector Materialization Integration

Use when Codex needs to work with the `connector_materialization` pack.

## Workflow
1. Read `docs/connector-materialization-contract-v1.json` and `docs/connector-materialization-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/connector-materialization-latest.json`.
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative, benchmark, connector, or orchestration docs.
