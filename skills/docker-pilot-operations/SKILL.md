---
name: docker-pilot-operations
description: Operate the Docker Pilot Operations pack with explicit proof boundaries.
---

# Docker Pilot Operations

Use when Codex needs to work with the `docker_pilot` pack.

## Workflow
1. Read `docs/docker-pilot-contract-v1.json` and `docs/docker-pilot-workflow-v1.md`.
2. Refresh or inspect `docs/trinity-mcp-cache/docker-pilot-latest.json`.
3. Keep the pack offline-safe unless its explicit live gate is enabled.
4. Promote only PASS-backed outputs into narrative, benchmark, connector, or orchestration docs.
