---
name: postgres-materialization-integration
description: Operate the Postgres Materialization pack with disposable schema tracers and explicit DSN gates.
---

# Postgres Materialization Integration

Use when Codex needs to work with the `postgres_materialization` pack.

## Workflow
1. Read `docs/postgres-materialization-contract-v1.json` and `docs/postgres-materialization-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/postgres-materialization-latest.json`.
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative, comparison, or orchestration docs.
