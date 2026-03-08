---
name: journey-continuity-integration
description: Operate the Journey Continuity Integration pack with explicit cache-backed promotion boundaries.
---

# Journey Continuity Integration

Use when Codex needs to work with the `journey_continuity` pack.

## Workflow
1. Read `docs/journey-continuity-contract-v1.json` and `docs/journey-continuity-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/journey-continuity-latest.json`.
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative, comparison, or orchestration docs.
