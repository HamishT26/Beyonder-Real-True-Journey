---
name: sentinel-daemon-operations
description: Operate the Sentinel Daemon Operations pack with explicit proof boundaries.
---

# Sentinel Daemon Operations

Use when Codex needs to work with the `sentinel_daemon` pack.

## Workflow
1. Read `docs/sentinel-daemon-contract-v1.json` and `docs/sentinel-daemon-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/sentinel-daemon-latest.json`.
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative, benchmark, connector, or orchestration docs.
