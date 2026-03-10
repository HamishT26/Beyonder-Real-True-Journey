---
name: ha-production-fabric-integration
description: Operate the HA Production Fabric pack with explicit v7 command-system and ladder boundaries.
---

# HA Production Fabric Integration

Use when Codex needs to work with the `ha_production_fabric` pack.

## Workflow
1. Read `docs/ha-production-fabric-contract-v1.json` and `docs/ha-production-fabric-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/ha-production-fabric-latest.json`.
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative, benchmark, connector, or control-tower docs.
