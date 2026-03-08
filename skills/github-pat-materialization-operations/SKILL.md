---
name: github-pat-materialization-operations
description: Operate the GitHub PAT Materialization Operations pack with explicit cache-backed promotion boundaries.
---

# GitHub PAT Materialization Operations

Use when Codex needs to work with the `github_pat_materialization` pack.

## Workflow
1. Read `docs/github-pat-materialization-contract-v1.json` and `docs/github-pat-materialization-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/github-pat-materialization-latest.json`.
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative, comparison, or orchestration docs.
