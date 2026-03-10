---
name: postgres-local-runtime-operations
description: Operate the Postgres Local Runtime Operations pack with explicit cache-backed promotion boundaries.
---

# Postgres Local Runtime Operations

Use when Codex needs to work with the `postgres_local_runtime` pack.

## Workflow
1. Read `docs/postgres-local-runtime-contract-v1.json` and `docs/postgres-local-runtime-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/postgres-local-runtime-latest.json`.
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative, comparison, or orchestration docs.
