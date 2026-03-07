---
name: filesystem-materialization-integration
description: Operate the Filesystem Materialization pack with explicit connector/tool-surface proof boundaries.
---

# Filesystem Materialization Integration

Use when Codex needs to work with the `filesystem_materialization` pack.

## Workflow
1. Read `docs/filesystem-materialization-contract-v1.json` and `docs/filesystem-materialization-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/filesystem-materialization-latest.json`.
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative, comparison, or orchestration docs.
