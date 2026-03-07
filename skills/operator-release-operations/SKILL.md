---
name: operator-release-operations
description: Operate the Operator Release pack with cache-backed gating and explicit connector boundaries.
---

# Operator Release Operations

Use when Codex needs to work with the `operator_release` pack.

## Workflow
1. Read `docs/operator-release-contract-v1.json` and `docs/operator-release-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/operator-release-latest.json.`
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative or comparison docs.
