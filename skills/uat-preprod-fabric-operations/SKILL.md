---
name: uat-preprod-fabric-operations
description: Operate the UAT Pre-Prod Fabric pack with explicit v7 command-system and ladder boundaries.
---

# UAT Pre-Prod Fabric Operations

Use when Codex needs to work with the `uat_preprod_fabric` pack.

## Workflow
1. Read `docs/uat-preprod-fabric-contract-v1.json` and `docs/uat-preprod-fabric-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/uat-preprod-fabric-latest.json`.
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative, benchmark, connector, or control-tower docs.
