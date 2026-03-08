---
name: wetware-device-readiness-v5-operations
description: Operate the Wetware Device Readiness v5 Operations pack with explicit cache-backed promotion boundaries.
---

# Wetware Device Readiness v5 Operations

Use when Codex needs to work with the `wetware_device_readiness_v5` pack.

## Workflow
1. Read `docs/wetware-device-readiness-v5-contract-v1.json` and `docs/wetware-device-readiness-v5-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/wetware-device-readiness-v5-latest.json`.
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative, comparison, or orchestration docs.
