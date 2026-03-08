---
name: filesystem-scope-governor-integration
description: Operate the Filesystem Scope Governor Integration pack with explicit cache-backed promotion boundaries.
---

# Filesystem Scope Governor Integration

Use when Codex needs to work with the `filesystem_scope_governor` pack.

## Workflow
1. Read `docs/filesystem-scope-governor-contract-v1.json` and `docs/filesystem-scope-governor-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/filesystem-scope-governor-latest.json`.
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative, comparison, or orchestration docs.
