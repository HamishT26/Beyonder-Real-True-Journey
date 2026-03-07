---
name: github-devflow-operations
description: Operate the GitHub Devflow pack with cache-backed gating and explicit connector boundaries.
---

# GitHub Devflow Operations

Use when Codex needs to work with the `github_devflow` pack.

## Workflow
1. Read `docs/github-devflow-contract-v1.json` and `docs/github-devflow-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/github-devflow-latest.json.`
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative or comparison docs.
