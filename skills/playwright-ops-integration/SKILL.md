---
name: playwright-ops-integration
description: Operate the Playwright Operations pack with cache-backed gating and explicit connector boundaries.
---

# Playwright Operations Integration

Use when Codex needs to work with the `playwright_ops` pack.

## Workflow
1. Read `docs/playwright-ops-contract-v1.json` and `docs/playwright-ops-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/playwright-ops-latest.json.`
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative or comparison docs.
